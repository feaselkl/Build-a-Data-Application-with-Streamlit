-- Query adapted from Thomas Williams: https://thomasswilliams.github.io/sqlserver/2021/10/13/database-markdown-documentation.html
-- Added info on indexes and foreign key constraints

--database documentation queries for current database, outputs markdown format
--outputs:
-- * for each database table, a table with column name, type, description
-- * for each view, the first 3,000 characters of the view definition
-- * for functions and stored procedures, the name and the description
--tested with SQL Server 2019
--run this query with "Results to Text"
--can be copy/pasted to app that supports markdown e.g. static site/blog, GitHub, Confluence etc.
--adapted from https://gist.github.com/mwinckler/2577364, https://www.red-gate.com/hub/product-learning/flyway/managing-database-documentation-during-flyway-based-development, https://gist.github.com/aplocher/fa86d16d3dd94ab4e42cc22b6b2fafa0

SET NOCOUNT, XACT_ABORT ON
SET CONCAT_NULL_YIELDS_NULL OFF

--temp table for lines to output, returned at end of process
DECLARE @temp_lines TABLE (
   --internal identifier used for ordering
   [id] INT IDENTITY (1, 1) PRIMARY KEY,
   --line of SQL code
   [line] NVARCHAR(4000)
)
--temp table for list of tables from INFORMATION_SCHEMA.TABLES
DECLARE @temp_all_tables TABLE (
   [id] INT IDENTITY (1, 1) PRIMARY KEY,
   [TABLE_SCHEMA] SYSNAME NOT NULL,
   [TABLE_NAME] SYSNAME NOT NULL
)
--temp table for just primary keys
DECLARE @temp_primary_keys TABLE (
   [TABLE_SCHEMA] SYSNAME NOT NULL,
   [TABLE_NAME] SYSNAME NOT NULL,
   [COLUMN_NAME] SYSNAME NOT NULL
)

--insert disclaimer into output in italics
--date in unambiguous month format d/MMM/YYYY (because, Aussie here)
INSERT INTO @temp_lines ([line])
SELECT  N'*This page was generated from a script at ' + FORMAT(GETDATE(), 'yyyy-MM-dd hh:mmtt') + N'*'

--get tables into temp table (will not include system tables)
INSERT INTO @temp_all_tables
SELECT  [TABLE_SCHEMA], [TABLE_NAME]
FROM    INFORMATION_SCHEMA.TABLES
WHERE   TABLE_TYPE = 'BASE TABLE'
ORDER BY 1, 2

--get just primary keys into temp table for easier retrieval & comparison later
--need table schema, table name, primary key column(s)
INSERT INTO @temp_primary_keys
SELECT  [TABLE_SCHEMA] = CONVERT(SYSNAME, SCHEMA_NAME(o.[schema_id])),
       [TABLE_NAME] = o.[name],
       --column name
       [COLUMN_NAME] = c.[name]
FROM    sys.objects o INNER JOIN
           --only objects with indexes
           sys.indexes i ON
               o.object_id = i.object_id INNER JOIN
           sys.index_columns ic ON
               i.object_id = ic.object_id AND
               i.index_id = ic.index_id INNER JOIN
           sys.columns c ON
               ic.object_id = c.object_id AND
               ic.column_id = c.column_id
WHERE   --user (not system) tables only
       o.[type] = 'U' AND
       --ignore system tables
       o.[is_ms_shipped] = 0 AND
       --ignore heaps
       i.[index_id] > 0 AND
       --ignore indexes that "...cannot be used directly as a data access path. Hypothetical indexes hold column-level statistics..."
       i.[is_hypothetical] = 0 AND
       --primary keys only
       i.[is_primary_key] = 1

--current table loop index (start at 1, unless there's no tables)
DECLARE @current_loop_table_index INT = (SELECT MIN([id]) FROM @temp_all_tables)

--output section heading for tables
INSERT INTO @temp_lines ([line])
SELECT  N'## Tables
';

--loop through each table
WHILE @current_loop_table_index IS NOT NULL BEGIN
   --current loop schema and table name
   DECLARE @current_loop_table_schema SYSNAME = (SELECT MIN([TABLE_SCHEMA]) FROM @temp_all_tables WHERE [id] = @current_loop_table_index)
   DECLARE @current_loop_table_name SYSNAME = (SELECT MIN([TABLE_NAME]) FROM @temp_all_tables WHERE [id] = @current_loop_table_index)

   --output schema & table name as heading 3, make into an anchor
   INSERT INTO @temp_lines ([line])
   SELECT  N'### [' + @current_loop_table_schema + N'.' + @current_loop_table_name + N'](#' + @current_loop_table_schema + N'.' + @current_loop_table_name + N')'

   --output extended property for table, allow up to 2,000 characters
   --adapted from https://gist.github.com/mwinckler/2577364
   INSERT INTO @temp_lines ([line])
   SELECT  --if there's no trailing full stop, add one
           LTRIM(RTRIM(CONVERT(NVARCHAR(2000), [value]))) +
           CASE
               WHEN RIGHT(LTRIM(RTRIM(CONVERT(NVARCHAR(2000), [value]))), 1) != N'.' THEN N'.'
               ELSE N''
           END
   FROM    sys.extended_properties
   WHERE   --MS_Description metadata only
           [name] = N'MS_Description' AND
           --should be zero for table and column metadata
           [minor_id] = 0 AND
           --match object ID of current loop table
           [major_id] = OBJECT_ID(QUOTENAME(@current_loop_table_schema) + N'.' + QUOTENAME(@current_loop_table_name))

   --output markdown table header for columns
   INSERT INTO @temp_lines ([line])
   SELECT N''
   UNION ALL
   SELECT  N'| Column name | Description | Data type | Allow NULLs |'
   UNION ALL
   SELECT  N'| ------- | ------- | ------- | ------- |'
   

   --output columns from INFORMATION_SCHEMA.COLUMNS
   --as markdown table rows
   --roughly match SSMS designers
   --data types in uppercase, because that's the way I like 'em
   INSERT INTO @temp_lines ([line])
   SELECT  --column name as bold text
           N'| **' + COLUMNS.[COLUMN_NAME] + N'**' +
           --if this column is a primary key, add star symbol (ideally could use "key" emoji)
           CASE
               WHEN EXISTS (
                     SELECT  1
                     FROM    @temp_primary_keys p
                     WHERE   COLUMNS.[TABLE_SCHEMA] = p.[TABLE_SCHEMA] AND
                             COLUMNS.[TABLE_NAME] = p.[TABLE_NAME] AND
                             COLUMNS.[COLUMN_NAME] = p.[COLUMN_NAME]
                    ) THEN N' ★'
               ELSE N''
           END +
           --get description for extended properties
           --if there's no trailing full stop, add one
           N' | ' + LTRIM(RTRIM(CONVERT(NVARCHAR(2000), ep.[value]))) +
           CASE
               WHEN RIGHT(LTRIM(RTRIM(CONVERT(NVARCHAR(2000), ep.[value]))), 1) != N'.' THEN N'.'
               ELSE N''
           END +
           --put together data type
           N' | ' + UPPER(COLUMNS.[DATA_TYPE]) +
           --append precision in brackets, for certain data types only
           CASE
               --add precision for datetime offset
               WHEN UPPER(COLUMNS.[DATA_TYPE]) IN (N'DATETIMEOFFSET') THEN N'(' + CONVERT(NVARCHAR(25), COLUMNS.[DATETIME_PRECISION]) + N')'
               --for numeric columns, add precision
               WHEN UPPER(COLUMNS.[DATA_TYPE]) IN (N'NUMERIC') THEN N'(' + CONVERT(NVARCHAR(25), COLUMNS.[NUMERIC_PRECISION]) + N',' + CONVERT(NVARCHAR(25), COLUMNS.[NUMERIC_SCALE]) + N')'
               --for character columns, add length (replace length of -1 with MAX)
               WHEN UPPER(COLUMNS.[DATA_TYPE]) IN (N'CHAR', N'NCHAR', N'VARCHAR', N'NVARCHAR') THEN
                   REPLACE(N'(' + CONVERT(NVARCHAR(25), COLUMNS.CHARACTER_MAXIMUM_LENGTH) + N')', N'(-1)', N'(MAX)')
               ELSE N''
           END +
           --special case - if an IDENTITY column, append word "identity"
           CASE
               WHEN c.[is_identity] = 1 THEN N' IDENTITY'
               ELSE N''
           END +
           --custom NULL column, ticked check box if is nullable
           N' | ' + CASE
               WHEN COLUMNS.[IS_NULLABLE] = N'YES' THEN N'☑'
               --empty check box if not nullable
               ELSE N'☐'
           END +
           --close table row
           N' |'
   FROM    INFORMATION_SCHEMA.COLUMNS LEFT OUTER JOIN
               sys.extended_properties ep ON
                   ep.[name] = N'MS_Description' AND
                   --table is "major_id"
                   ep.[major_id] = OBJECT_ID(QUOTENAME(@current_loop_table_schema) + N'.' + QUOTENAME(@current_loop_table_name)) AND
                   --column number is "minor_id"
                   ep.[minor_id] = COLUMNS.[ORDINAL_POSITION] LEFT OUTER JOIN
               --sys.columns, needed for identity columns
               sys.columns C ON
                   C.[object_id] = OBJECT_ID(QUOTENAME(@current_loop_table_schema) + N'.' + QUOTENAME(@current_loop_table_name)) AND
                   C.[name] = COLUMNS.[COLUMN_NAME]
   WHERE   COLUMNS.[TABLE_SCHEMA] = @current_loop_table_schema AND
           COLUMNS.[TABLE_NAME] = @current_loop_table_name
   ORDER BY
           --order the same as SSMS designers
           COLUMNS.[ORDINAL_POSITION]

    -- Add a newline
    INSERT INTO @temp_lines([line])
    VALUES(N''), (N'#### Indexes'), (N'| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |'), (N'| ----- | ----- | ----- | ----- | ----- | ---- |');

    -- Add in indexes
    WITH records AS 
    (
        SELECT
            -- NOTE: change the collation to your own database's collation!
            CAST(i.name AS NVARCHAR(128)) COLLATE Latin1_General_100_CI_AS_SC AS index_name,
            i.type_desc AS index_desc,
            i.is_unique,
            i.is_primary_key,
            i.is_unique_constraint,
            STRING_AGG(c.name, ', ') WITHIN GROUP (ORDER BY ic.key_ordinal) AS columns
        FROM sys.indexes i
            INNER JOIN sys.objects o
                ON i.object_id = o.object_id
            INNER JOIN sys.schemas s
                ON o.schema_id = s.schema_id
            INNER JOIN sys.index_columns ic
                ON ic.index_id = i.index_id
                AND ic.object_id = i.object_id
            INNER JOIN sys.columns c
                ON ic.column_id = c.column_id
                AND ic.object_id = c.object_id
        WHERE
            s.name = @current_loop_table_schema
            AND o.name = @current_loop_table_name
        GROUP BY
            i.name,
            i.type_desc,
            i.is_unique,
            i.is_primary_key,
            i.is_unique_constraint
    )
    INSERT INTO @temp_lines([line])
    SELECT
        CONCAT(N'| **', r.index_name, N'** | ', r.index_desc, N' | ', r.columns, N' | ',
            CASE WHEN r.is_unique = 1 THEN N'☑' ELSE N'☐' END, N' | ',
            CASE WHEN r.is_primary_key = 1 THEN N'☑' ELSE N'☐' END, N' | ',
            CASE WHEN r.is_unique_constraint = 1 THEN N'☑' ELSE N'☐' END, N' |')
    FROM records r;
    
    -- Add a newline
    INSERT INTO @temp_lines([line])
    VALUES(N''), (N'#### Foreign Key Constraints'), (N'| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |'), (N'| ----- | ----- | ----- | ----- | ----- |');

    WITH records AS
    (
        SELECT
            fk.name,
            CONCAT(QUOTENAME(OBJECT_SCHEMA_NAME(fk.parent_object_id)), N'.', QUOTENAME(OBJECT_NAME(fk.parent_object_id))) AS parent_table,
            STRING_AGG(pc.name, ', ') WITHIN GROUP (ORDER BY fkc.constraint_column_id) AS parent_table_columns,
            CONCAT(QUOTENAME(OBJECT_SCHEMA_NAME(fk.referenced_object_id)), N'.', QUOTENAME(OBJECT_NAME(fk.referenced_object_id))) AS referenced_table,
            STRING_AGG(rc.name, ', ') WITHIN GROUP (ORDER BY fkc.constraint_column_id) AS referenced_table_columns
        FROM sys.foreign_keys fk
            INNER JOIN sys.foreign_key_columns fkc
                ON fk.object_id = fkc.constraint_object_id
            INNER JOIN sys.columns pc
                ON pc.object_id = fkc.parent_object_id
                AND pc.column_id = fkc.parent_column_id
            INNER JOIN sys.columns rc
                ON rc.object_id = fkc.referenced_object_id
                AND rc.column_id = fkc.referenced_column_id
        WHERE
            OBJECT_SCHEMA_NAME(fk.parent_object_id) = @current_loop_table_schema
            AND OBJECT_NAME(fk.parent_object_id) = @current_loop_table_name
        GROUP BY
            fk.name,
            CONCAT(QUOTENAME(OBJECT_SCHEMA_NAME(fk.parent_object_id)), N'.', QUOTENAME(OBJECT_NAME(fk.parent_object_id))),
            CONCAT(QUOTENAME(OBJECT_SCHEMA_NAME(fk.referenced_object_id)), N'.', QUOTENAME(OBJECT_NAME(fk.referenced_object_id)))
    )
    INSERT INTO @temp_lines([line])
    SELECT
        CONCAT(N'| **', r.name, N'** | ', r.parent_table, N' | ', r.parent_table_columns, N' | ', r.referenced_table, N' | ', r.referenced_table_columns, N' |')
    FROM records r;

    -- Add a newline
    INSERT INTO @temp_lines([line])
    VALUES(N'');

   --increment table loop index
   SET @current_loop_table_index = (SELECT MIN([id]) FROM @temp_all_tables WHERE [id] > @current_loop_table_index)
END

--are there any views?
IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.VIEWS) BEGIN
   --output section heading for views
   INSERT INTO @temp_lines ([line])
   SELECT  N'## Views'

   --for views, output name as heading, and definition as code block
   INSERT INTO @temp_lines ([line])
   SELECT  N'### ' + [TABLE_SCHEMA] + N'.' + [TABLE_NAME] + CHAR(13) +
           --if definition is longer than 4,000 characters, will be NULL
           CASE
               WHEN [VIEW_DEFINITION] IS NULL THEN N'*Text too large to display*'
               ELSE
                   --start code block
                   N'````' + CHAR(13) +
                   --first 3,000 characters of definition
                   --need to remove leading and trailing linebreaks
                   TRIM(CONVERT(NVARCHAR(3000), TRIM(CHAR(13) FROM TRIM(CHAR(10) FROM TRIM(CHAR(13) FROM [VIEW_DEFINITION]))))) +
                   --if definition is longer than 3,000 characters, add ellipses
                   (CASE WHEN LEN([VIEW_DEFINITION]) > 3000 THEN N'...' ELSE N'' END) + CHAR(13) +
                   --end of code block
                   N'````' + CHAR(13)
           END
   FROM    INFORMATION_SCHEMA.VIEWS
   ORDER BY [TABLE_SCHEMA], [TABLE_NAME]
END

--are there any (non-system) stored procedures?
IF EXISTS(SELECT * FROM sys.procedures WHERE [is_ms_shipped] = 0) BEGIN
   --output section heading for stored procedures
   INSERT INTO @temp_lines ([line])
   SELECT  N'## Stored procedures'

   --stored procedures, output name and description separated by line break
   INSERT INTO @temp_lines ([line])
   SELECT  N'**' + procs.[name] + N'**' + CHAR(13) + LTRIM(RTRIM(CONVERT(NVARCHAR(2000), ep.[value])))
   FROM    sys.procedures procs LEFT OUTER JOIN
               sys.extended_properties ep ON
                       ep.[name] = N'MS_Description' AND
                       ep.[major_id] = procs.[object_id] AND
                       --stored procedure comments (not parameters)
                       ep.[minor_id] = 0
   WHERE   --not system stored procs
           procs.[is_ms_shipped] = 0
   ORDER BY procs.[name]
END

--are there any functions?
IF EXISTS(SELECT * FROM sys.objects WHERE [type] = 'FN' AND [is_ms_shipped] = 0) BEGIN
   --output section heading for functions
   INSERT INTO @temp_lines ([line])
   SELECT  N'## Functions'

   --functions, output name and metadata separated by line break
   INSERT INTO @temp_lines ([line])
   SELECT  N'**' + o.[name] + N'**' + CHAR(13) + LTRIM(RTRIM(CONVERT(NVARCHAR(2000), ep.[value])))
   FROM    sys.objects o LEFT OUTER JOIN
               sys.extended_properties ep ON
                       ep.[name] = N'MS_Description' AND
                       ep.[major_id] = o.[object_id] AND
                       ep.[minor_id] = 0
   WHERE   --functions
           o.[type] = 'FN' AND
           --not system functions
           o.[is_ms_shipped] = 0
   ORDER BY o.[name]
END

SET NOCOUNT OFF

--return output in order of line number, but without line number in output
SELECT  [line]
FROM    @temp_lines