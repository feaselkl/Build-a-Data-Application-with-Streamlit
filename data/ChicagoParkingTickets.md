*This page was generated from a script at 2024-07-19 08:50AM*
## Tables 
### [Chicago.Buildings](#Chicago.Buildings)
City of Chicago list of buildings.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Building_ID** ★ |  | INT | ☐ |
| **Building_Status** | Status of building, PROPOSED or ACTIVE. | VARCHAR(10) | ☑ |
| **From_Address** ★ | Lower-bound address number. | SMALLINT | ☐ |
| **To_Address** | Upper-bound address number. | SMALLINT | ☐ |
| **Street** | Full street name. | VARCHAR(50) | ☐ |
| **Side** | Street side, odd (1) or even (0). | INT | ☑ |
| **Structure** | Structure ordinal, where a building can have multiple structures. | TINYINT | ☐ |
| **Build_year** | Construction year. | DATE | ☑ |
| **Above_ground_stories** | Number of floors above ground. | TINYINT | ☑ |
| **Below_ground_stories** | Number of floors below ground. | SMALLINT | ☑ |
| **Number_of_units** | Number of residential units. | SMALLINT | ☑ |
| **WKT** | Well-known text for the building boundary. | VARCHAR(MAX) | ☐ |
| **Boundary** | Boundary geo type. | GEOMETRY | ☑ |
| **Middle_Point** | Geographical middle point. | GEOMETRY | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **IX_Middle_Point** | SPATIAL | Middle_Point | ☐ | ☐ | ☐ |
| **IX_Street** | NONCLUSTERED | To_Address, Middle_Point, Number_of_units, Street, Side, From_Address, Structure | ☑ | ☐ | ☐ |
| **PK_Buildings** | CLUSTERED | Building_ID, From_Address | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [Chicago.Census_Tracts](#Chicago.Census_Tracts)
Census tracts in the City of Chicago.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **WKT** | The boundary of the area formatted as well-known text (WKT). | VARCHAR(MAX) | ☐ |
| **State_FP10** ★ | State. Always 17 for Illinois. | TINYINT | ☐ |
| **County_FP10** ★ | County code. Always 031 for Cook County. | CHAR(3) | ☐ |
| **Tract_CE10** ★ | 6-digit local tract number. | CHAR(6) | ☐ |
| **Census_Block** | The 11-character full census tract number (state + county + tract). | VARCHAR(11) | ☑ |
| **Census_Tract_Name** | Plaintext name of the census tract. | VARCHAR(50) | ☐ |
| **Community** |  | TINYINT | ☐ |
| **Notes** | Community number to which the census tract belongs. | VARCHAR(MAX) | ☑ |
| **Boundary** |  | GEOMETRY | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_CensusTracts** | CLUSTERED | State_FP10, County_FP10, Tract_CE10 | ☑ | ☑ | ☐ |
| **Tract** | NONCLUSTERED | Tract_CE10 | ☑ | ☐ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |
| **FK_Census_Community** | [Chicago].[Census_Tracts] | Community | [Chicago].[Community_Areas] | Community |

### [Chicago.Community_Areas](#Chicago.Community_Areas)
City of Chicago community areas.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **WKT** | The boundary of the area formatted as well-known text (WKT). | VARCHAR(MAX) | ☐ |
| **Community** ★ | Community number, 1-77. | TINYINT | ☐ |
| **Community_Name** | Name of the community area. | VARCHAR(150) | ☐ |
| **Sector** | Plaintext sector name. | VARCHAR(50) | ☑ |
| **Side** | Plaintext side. | VARCHAR(50) | ☑ |
| **Boundary** | The boundary of the census tract, ask a geo datatype. | GEOMETRY | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **Community_Name** | NONCLUSTERED | Community_Name | ☑ | ☐ | ☐ |
| **IX_Spatial** | SPATIAL | Boundary | ☐ | ☐ | ☐ |
| **PK_Community_AreaS** | CLUSTERED | Community | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [Chicago.Intersections](#Chicago.Intersections)
Computed coordinates of intersections.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **NS_Street** ★ | North-South street name. | VARCHAR(50) | ☐ |
| **EW_Street** ★ | East-West street name. | VARCHAR(50) | ☐ |
| **Intersection** |  | GEOMETRY | ☐ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_Intersections** | CLUSTERED | NS_Street, EW_Street | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [Chicago.Neighborhoods](#Chicago.Neighborhoods)
City of Chicago neighborhoods.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Neighborhood** ★ | Neighborhood code (generated, local to this database). | VARCHAR(3) | ☐ |
| **Neighborhood_Name** | Neighborhood name. | VARCHAR(50) | ☐ |
| **Greater_Neighborhood** | Group of neighborhoods. | VARCHAR(50) | ☐ |
| **WKT** | The boundary of the area formatted as well-known text (WKT). | VARCHAR(MAX) | ☐ |
| **Boundary** | The boundary of the census tract, ask a geo datatype. | GEOMETRY | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_Neighborhood** | CLUSTERED | Neighborhood | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [Chicago.Police_Districts](#Chicago.Police_Districts)
Contains the boundaries of each police district.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **District** ★ | Police district number. | TINYINT | ☐ |
| **District_Name** | Police district number. | VARCHAR(100) | ☐ |
| **WKT** | WKT (well-known text) format boundary of the district. | VARCHAR(MAX) | ☐ |
| **Boundary** |  | GEOMETRY | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_Police_Districts** | CLUSTERED | District | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |
| **FK_Police_Districts_Station** | [Chicago].[Police_Districts] | District | [Chicago].[Police_Stations] | District |

### [Chicago.Police_Stations](#Chicago.Police_Stations)
One row for each police station.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **District** ★ | Police district (or location). | TINYINT | ☐ |
| **Station_name** | Police district (or location). | VARCHAR(20) | ☐ |
| **Building_ID** | corresponding Building_ID in Chicago.Buildings. Some addresses could not be matched to buildings, probably because all of the data was not sourced at the same point in time. | INT | ☑ |
| **Street** | Street name. | VARCHAR(50) | ☐ |
| **Street_number** | House number on this street. | SMALLINT | ☐ |
| **WKT** | WKT (well-known text) format location of the station. | VARCHAR(MAX) | ☐ |
| **Location** |  | GEOMETRY | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_Police_Stations** | CLUSTERED | District | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [Chicago.Population_by_Census_Block](#Chicago.Population_by_Census_Block)
Population statistics per census block.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Census_Block** ★ | 11-character census tract number. | CHAR(15) | ☐ |
| **Population** | Population. | INT | ☐ |
| **Year** ★ | Census year. | INT | ☐ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_Population_by_Census_Block** | CLUSTERED | Year, Census_Block | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [Chicago.Population_by_Zip_Code](#Chicago.Population_by_Zip_Code)
Population statistics per ZIP code.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **ZIP** ★ | ZIP code. | NUMERIC(5,0) | ☐ |
| **Year** ★ | Population, census year. | INT | ☐ |
| **Population_Total** | Population. | INT | ☑ |
| **Population_Age_0_4** | Population, ages 0-4. | INT | ☑ |
| **Population_Age_5** | Population, age 5+. | INT | ☑ |
| **Population_Age_5_11** | Population, ages 5-11. | INT | ☑ |
| **Population_Age_12_17** | Population, ages 12-17. | INT | ☑ |
| **Population_Age_0_17** | Population, ages 0-17. | INT | ☑ |
| **Population_Age_18** | Population, age 18+. | INT | ☑ |
| **Population_Age_18_29** | Population, ages 18-29. | INT | ☑ |
| **Population_Age_30_39** | Population, ages 30-39. | INT | ☑ |
| **Population_Age_40_49** | Population, ages 40-49. | INT | ☑ |
| **Population_Age_50_59** | Population, ages 50-59. | INT | ☑ |
| **Population_Age_60_69** | Population, ages 60-69. | INT | ☑ |
| **Population_Age_65** | Population, age 65+. | INT | ☑ |
| **Population_Age_70_79** | Population, ages 70-79. | INT | ☑ |
| **Population_Age_80** | Population, age 80+. | INT | ☑ |
| **Population_Female** | Population, female. | INT | ☑ |
| **Population_Male** | Population, male. | INT | ☑ |
| **Population_Latinx** | Population, Latinx. | INT | ☑ |
| **Population_Asian_Non_Latinx** | Population, Asian. | INT | ☑ |
| **Population_Black_Non_Latinx** | Population, Black. | INT | ☑ |
| **Population_White_Non_Latinx** | Population, White. | INT | ☑ |
| **Population_Other_Race_Non_Latinx** | Population, Other (except Latinx). | INT | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_Population_by_Zip_Code** | CLUSTERED | Year, ZIP | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [Chicago.Socioeconomic_Indicators_per_Community_Area](#Chicago.Socioeconomic_Indicators_per_Community_Area)
Socioeconomic indicators per Community Area.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Year** ★ |  | SMALLINT | ☐ |
| **Community** ★ | Community Area. | TINYINT | ☐ |
| **Percent of housing crowded** | Percent of population in crowded housing. | NUMERIC(5,2) | ☑ |
| **Percent households below poverty** | Percent of households below the poverty line. | NUMERIC(5,2) | ☑ |
| **Percent aged 16+ unemployed** | Percent of population aged 16+ years unemployed. | NUMERIC(5,2) | ☑ |
| **Percent aged 25+ without high school diploma** | Percent of population 25+ years old, without high school diploma. | NUMERIC(5,2) | ☑ |
| **Percent aged under 18 or over 64** | Percent of population under 18 years or over 64 years old. | NUMERIC(5,2) | ☑ |
| **Per capita income** | Average per-capita income. | NUMERIC(10,2) | ☑ |
| **Hardship index** | Hardship index. | NUMERIC(5,2) | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_Socioeconomic_indicators** | CLUSTERED | Year, Community | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |
| **FK_Socioeconomic_Community** | [Chicago].[Socioeconomic_Indicators_per_Community_Area] | Community | [Chicago].[Community_Areas] | Community |

### [Chicago.StreetNames](#Chicago.StreetNames)
City of Chicago streets.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Full_Street_Name** ★ | Fully qualified street name. | VARCHAR(50) | ☐ |
| **Direction** | Street direction as a single character (N, S, W, E). | VARCHAR(50) | ☑ |
| **Street** | Plain street name. | VARCHAR(50) | ☐ |
| **Suffix** | Street name suffix ("St", "Ave", "Pl", "Blvd", etc). | VARCHAR(50) | ☑ |
| **Suffix_Direction** | Suffix direction, for certain types of streets. Example: IB (inbound), OB (outbound), etc. | VARCHAR(50) | ☑ |
| **Min_Address** | Maximum used street number for this street. | SMALLINT | ☑ |
| **Max_Address** | Minimum used street number for this street. | SMALLINT | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_StreetNames** | CLUSTERED | Full_Street_Name | ☑ | ☑ | ☐ |
| **Street** | NONCLUSTERED | Full_Street_Name, Min_Address, Max_Address, Street, Direction, Suffix | ☐ | ☐ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [Chicago.Wards](#Chicago.Wards)
City of Chicago wards.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Ward** ★ | Ward number, 1-50. | TINYINT | ☐ |
| **WKT** | The boundary of the area formatted as well-known text (WKT). | NVARCHAR(MAX) | ☐ |
| **Boundary** |  | GEOMETRY | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_Ward** | CLUSTERED | Ward | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [Chicago.ZipCodes](#Chicago.ZipCodes)
ZIP code in the City of Chicago.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **ZIP** ★ | ZIP code. | NUMERIC(5,0) | ☐ |
| **WKT** | The boundary of the area formatted as well-known text (WKT). | VARCHAR(MAX) | ☐ |
| **Boundary** | The boundary of the census tract, ask a geo datatype. | GEOMETRY | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **IX_Spatial** | SPATIAL | Boundary | ☐ | ☐ | ☐ |
| **PK_ZipCodes** | CLUSTERED | ZIP | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [ReferenceData.License_Plate_Types](#ReferenceData.License_Plate_Types)
Type of license plate.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Plate_Type** ★ | License plate type code. | VARCHAR(5) | ☐ |
| **Plate_Type_Name** | Description of license plate type code. | VARCHAR(50) | ☐ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_License_Plate_Type** | CLUSTERED | Plate_Type | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [ReferenceData.Months](#ReferenceData.Months)
Contains a list of calendar months.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Month** ★ | Month. | DATE | ☐ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_Months** | CLUSTERED | Month | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [ReferenceData.Population_by_State](#ReferenceData.Population_by_State)
Population by state and year.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **State_abbr** ★ | . | CHAR(2) | ☐ |
| **Year** ★ | . | DATE | ☐ |
| **Population** | . | INT | ☐ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_Population_by_State** | CLUSTERED | State_abbr, Year | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |
| **FK_Population_by_State_State** | [ReferenceData].[Population_by_State] | State_abbr | [ReferenceData].[States] | State_abbr |

### [ReferenceData.Population_by_Zip_Code](#ReferenceData.Population_by_Zip_Code)
Population by ZIP code and year.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **ZIP** ★ | . | NUMERIC(5,0) | ☐ |
| **Year** ★ | . | DATE | ☐ |
| **Population** | . | INT | ☐ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_Population_by_Zip_Code** | CLUSTERED | ZIP, Year | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |
| **FK_Population_by_Zip_Code_ZIP** | [ReferenceData].[Population_by_Zip_Code] | ZIP | [ReferenceData].[ZipCodes] | ZIP |

### [ReferenceData.States](#ReferenceData.States)
List of US states.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **State_abbr** ★ | Two-character abbreviation of the state. | CHAR(2) | ☐ |
| **State** | Name of the state. | VARCHAR(50) | ☐ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_States** | CLUSTERED | State_abbr | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [ReferenceData.Vehicle_Makes](#ReferenceData.Vehicle_Makes)
Standardized NCIC vehicle make codes.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Vehicle_Make** ★ | Vehicle make code. | VARCHAR(10) | ☐ |
| **Vehicle_Make_Name** | Name of the vehicle maker. | VARCHAR(250) | ☐ |
| **Automobile** |  | BIT | ☐ |
| **Motorcycle** | 1/0 if this make code applies to automobiles or trucks. | BIT | ☐ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_Vehicle_Makes** | CLUSTERED | Vehicle_Make | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [ReferenceData.ZipCodes](#ReferenceData.ZipCodes)
ZIP codes in the United States.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **State_abbr** |  | CHAR(2) | ☐ |
| **ZIP** ★ | Two-character state code. | NUMERIC(5,0) | ☐ |
| **County** | ZIP code. | VARCHAR(50) | ☑ |
| **City** | County code that contains the ZIP code. | VARCHAR(50) | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_ZipCodes** | CLUSTERED | ZIP | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |
| **FK_ZipCodes_State** | [ReferenceData].[ZipCodes] | State_abbr | [ReferenceData].[States] | State_abbr |

### [Tickets.Accounting](#Tickets.Accounting)
Contains accounting transactions related to parking tickets.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Date** | Accounting date. | DATE | ☐ |
| **Ticket_number** | Ticket number. | BIGINT | ☐ |
| **Notice_Level_ID** | Notice level. | TINYINT | ☐ |
| **Plate_ID** | License plate. | INT | ☐ |
| **Location_ID** | Location. | INT | ☐ |
| **Violation_ID** | Type of parking violation. | INT | ☐ |
| **Amount_issued** | Initial issued. | NUMERIC(10,2) | ☐ |
| **Amount_written_off** | Amount written off. | NUMERIC(12,2) | ☐ |
| **Amount_paid** | Amount paid. | NUMERIC(10,2) | ☐ |
| **Amount_due** | Amount due. | NUMERIC(12,2) | ☐ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **CIX** | CLUSTERED | Date | ☐ | ☐ | ☐ |
| **Violation_Plate** | NONCLUSTERED | Amount_issued, Amount_due, Violation_ID, Plate_ID, Date | ☐ | ☐ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [Tickets.Fine_amounts](#Tickets.Fine_amounts)
Fine amounts per violation code.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Violation_ID** ★ |  | INT | ☐ |
| **From_Date** ★ | Valid as of date. | DATE | ☐ |
| **To_Date** | Valid until date. | DATE | ☑ |
| **Fine_amount** | The initial fine amount. | NUMERIC(10,2) | ☑ |
| **Fine_including_fees** | Fine after notice of final determination, i.e. the total fine after additional charges and late fees. | NUMERIC(10,2) | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_Fine_amounts** | CLUSTERED | Violation_ID, From_Date | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |
| **FK_Violation** | [Tickets].[Fine_amounts] | Violation_ID | [Tickets].[Violation] | Violation_ID |

### [Tickets.License_Plates](#Tickets.License_Plates)
Information about license plates (vehicles).

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Plate_ID** ★ |  | INT | ☐ |
| **License_Plate_Hash** | Hashed license plate number. | BINARY | ☐ |
| **From_Date** | Start of date range. | DATETIME2 | ☐ |
| **To_Date** | End of date range (or NULL if there's no end date). | DATETIME2 | ☑ |
| **ZIP** | ZIP code where the license plate is registered. | NUMERIC(5,0) | ☑ |
| **License_Plate_State** | State that issued the license plate. | CHAR(2) | ☑ |
| **Plate_Type** | License plate type, indicating the type of vehicle. | VARCHAR(5) | ☑ |
| **Vehicle_Make** | NCIC vehicle make code. | VARCHAR(10) | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **IX_License_Plate** | NONCLUSTERED | License_Plate_Hash, From_Date | ☑ | ☐ | ☐ |
| **IX_Vehicle_Make** | NONCLUSTERED | License_Plate_Hash, Vehicle_Make | ☐ | ☐ | ☐ |
| **PK_License_Plates** | CLUSTERED | Plate_ID | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |
| **FK_License_Plates_Vehicle_Make** | [Tickets].[License_Plates] | Vehicle_Make | [ReferenceData].[Vehicle_Makes] | Vehicle_Make |

### [Tickets.Location_Text](#Tickets.Location_Text)
The text of the location, as written on the ticket. Not corrected for spelling and other errors.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Location_Text_ID** ★ |  | INT | ☐ |
| **Location_Text** | Plaintext. | VARCHAR(50) | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_Location_Text** | CLUSTERED | Location_Text_ID | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [Tickets.Locations](#Tickets.Locations)
Parking violation locations.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Location_ID** ★ |  | INT | ☐ |
| **geocoded_lat** |  | NUMERIC(12,7) | ☑ |
| **geocoded_lng** |  | NUMERIC(12,7) | ☑ |
| **Street** |  | VARCHAR(200) | ☑ |
| **Street_number** |  | INT | ☑ |
| **ZIP** |  | NUMERIC(5,0) | ☑ |
| **Ward** |  | TINYINT | ☑ |
| **Tract** |  | CHAR(6) | ☑ |
| **Community** | Latitude. | TINYINT | ☑ |
| **Neighborhood** | Longitude. | VARCHAR(3) | ☑ |
| **Police_District** | Fully qualified street name. | TINYINT | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **IX_Street** | NONCLUSTERED | ZIP, Street, Street_number | ☑ | ☐ | ☐ |
| **PK_Locations** | CLUSTERED | Location_ID | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |
| **FK_Location_Community** | [Tickets].[Locations] | Community | [Chicago].[Community_Areas] | Community |
| **FK_Location_Neighborhood** | [Tickets].[Locations] | Neighborhood | [Chicago].[Neighborhoods] | Neighborhood |
| **FK_Location_PoliceDistrict** | [Tickets].[Locations] | Police_District | [Chicago].[Police_Districts] | District |
| **FK_Location_Tract** | [Tickets].[Locations] | Tract | [Chicago].[Census_Tracts] | Tract_CE10 |
| **FK_Location_Ward** | [Tickets].[Locations] | Ward | [Chicago].[Wards] | Ward |
| **FK_Location_ZIP** | [Tickets].[Locations] | ZIP | [ReferenceData].[ZipCodes] | ZIP |

### [Tickets.Notice_Level](#Tickets.Notice_Level)
Types of notices issued for a ticket.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Notice_Level_ID** ★ |  | TINYINT | ☐ |
| **Notice_Level** | Notice level code. | VARCHAR(4) | ☑ |
| **Notice_Level_Description** | Description of notice level. | VARCHAR(200) | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **IX_Notice_Level** | NONCLUSTERED | Notice_Level | ☑ | ☐ | ☐ |
| **PK_Notice_Level** | CLUSTERED | Notice_Level_ID | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [Tickets.Officer_assignments](#Tickets.Officer_assignments)

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Officer_ID** ★ |  | INT | ☐ |
| **Unit_ID** |  | INT | ☐ |
| **From_date** ★ |  | DATE | ☐ |
| **To_date** |  | DATE | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_Officer_assignments** | CLUSTERED | Officer_ID, From_date | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |
| **FK_Officer_assignments_Officer** | [Tickets].[Officer_assignments] | Officer_ID | [Tickets].[Officers] | Officer_ID |
| **FK_Officer_assignments_Unit** | [Tickets].[Officer_assignments] | Unit_ID | [Tickets].[Units] | Unit_ID |

### [Tickets.Officers](#Tickets.Officers)
Officer or parking enforcement aide.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Officer_ID** ★ |  | INT | ☐ |
| **Officer** | Unique ID. | VARCHAR(15) | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **IX_Officers** | NONCLUSTERED | Officer | ☑ | ☐ | ☐ |
| **PK_Officer** | CLUSTERED | Officer_ID | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [Tickets.Parking_Violations](#Tickets.Parking_Violations)
Parking violation tickets.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Ticket_number** ★ | Unique ticket number. | BIGINT | ☐ |
| **Issued_date** ★ | Date and time when the ticket was issued. | DATETIME2 | ☐ |
| **Location_ID** | Parking violation location. | INT | ☐ |
| **Plate_ID** | License plate. | INT | ☐ |
| **Unit_ID** | Issuing agency. | INT | ☐ |
| **Location_Text_ID** | Original text for the location. | INT | ☐ |
| **Violation_ID** | Type of parking violation. | INT | ☐ |
| **Officer_ID** | Issuing officer or parking enforcement aide. | INT | ☐ |
| **Ticket_Status_ID** | Status (queue) of the ticket. | TINYINT | ☐ |
| **Ticket_Status_date** | Date as of which the ticket status applies. | DATE | ☐ |
| **Notice_Level_ID** | Type of notice (if any) sent to the owner of the vehicle. | TINYINT | ☐ |
| **Notice_Number** | Unique identification number for the notice. | BIGINT | ☑ |
| **Hearing_Outcome_is_Liable** | Outcome of a hearing: if found liable (1) or not liable (0). NULL if the ticket was not contested. | BIT | ☑ |
| **Fine_amount** | Original fine amount. | NUMERIC(10,2) | ☐ |
| **Late_fee** |  | NUMERIC(10,2) | ☐ |
| **Collection_fee** |  | NUMERIC(10,2) | ☐ |
| **Amount_paid** |  | NUMERIC(10,2) | ☐ |
| **Amount_due** | Total amount paid for this ticket. | NUMERIC(10,2) | ☐ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_Parking_Violations** | CLUSTERED | Issued_date, Ticket_number | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |
| **FK_Parking_Violation_Location** | [Tickets].[Parking_Violations] | Location_ID | [Tickets].[Locations] | Location_ID |
| **FK_Parking_Violation_Notice_Level** | [Tickets].[Parking_Violations] | Notice_Level_ID | [Tickets].[Notice_Level] | Notice_Level_ID |
| **FK_Parking_Violation_Officer** | [Tickets].[Parking_Violations] | Officer_ID | [Tickets].[Officers] | Officer_ID |
| **FK_Parking_Violation_Plate** | [Tickets].[Parking_Violations] | Plate_ID | [Tickets].[License_Plates] | Plate_ID |
| **FK_Parking_Violation_Status** | [Tickets].[Parking_Violations] | Ticket_Status_ID | [Tickets].[Ticket_Status] | Ticket_Status_ID |
| **FK_Parking_Violation_Text** | [Tickets].[Parking_Violations] | Location_Text_ID | [Tickets].[Location_Text] | Location_Text_ID |
| **FK_Parking_Violation_Unit** | [Tickets].[Parking_Violations] | Unit_ID | [Tickets].[Units] | Unit_ID |
| **FK_Parking_Violation_Violation** | [Tickets].[Parking_Violations] | Violation_ID | [Tickets].[Violation] | Violation_ID |

### [Tickets.Ticket_Status](#Tickets.Ticket_Status)
The status (queue) of the ticket.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Ticket_Status_ID** ★ |  | TINYINT | ☐ |
| **Ticket_Status** | Status code. | VARCHAR(20) | ☑ |
| **Ticket_Status_Description** | Description of the status. | VARCHAR(200) | ☑ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **IX_Ticket_Status** | NONCLUSTERED | Ticket_Status | ☑ | ☐ | ☐ |
| **PK_Ticket_Status** | CLUSTERED | Ticket_Status_ID | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [Tickets.Units](#Tickets.Units)
Issuing agency.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Unit_ID** ★ |  | INT | ☐ |
| **Reporting_Unit** | Reporting district (unit). | VARCHAR(4) | ☐ |
| **Police_District** |  | TINYINT | ☑ |
| **Department_Description** | Description. | VARCHAR(100) | ☐ |
| **Department_Category** | Type of department. | VARCHAR(21) | ☐ |
| **Department_Subcategory** | Department. | VARCHAR(13) | ☐ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **IX_Units** | NONCLUSTERED | Reporting_Unit | ☑ | ☐ | ☐ |
| **PK_Units** | CLUSTERED | Unit_ID | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |
| **FK_Units_Police_District** | [Tickets].[Units] | Police_District | [Chicago].[Police_Districts] | District |

### [Tickets.Violation](#Tickets.Violation)
Types of parking violation.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Violation_ID** ★ |  | INT | ☐ |
| **Violation_Code** | Parking violation code. | VARCHAR(15) | ☐ |
| **Violation_Description** | Description of violation code. | VARCHAR(150) | ☐ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **IX_Violation** | NONCLUSTERED | Violation_Code | ☑ | ☐ | ☐ |
| **PK_Violation** | CLUSTERED | Violation_ID | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [Weather.Precipitation](#Weather.Precipitation)
Precipitation statistics per month for Chicago.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Month** ★ | Calendar month. | DATE | ☐ |
| **Total_precipitation_in** | Total precipitation for the month, in inches. | NUMERIC(4,2) | ☐ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_Precipitation** | CLUSTERED | Month | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

### [Weather.Temperature](#Weather.Temperature)
Temperature statistics per month for Chicago.

| Column name | Description | Data type | Allow NULLs |
| ------- | ------- | ------- | ------- |
| **Month** ★ | Calendar month. | DATE | ☐ |
| **Min_Temperature_F** | Lowest temperature of the month, degrees Fahrenheit. | NUMERIC(5,2) | ☐ |
| **Avg_temperature_F** | Average temperature of the month, degrees Fahrenheit. | NUMERIC(5,2) | ☐ |
| **Max_Temperature_F** | Highest temperature of the month, degrees Fahrenheit. | NUMERIC(5,2) | ☐ |

#### Indexes
| Index name | Description | Columns | Is Unique | Is Primary Key | Is Unique Constraint |
| ----- | ----- | ----- | ----- | ----- | ---- |
| **PK_Temperature** | CLUSTERED | Month | ☑ | ☑ | ☐ |

#### Foreign Key Constraints
| Foreign key constraint name | Parent table | Parent columns | Referenced table | Referenced columns |
| ----- | ----- | ----- | ----- | ----- |

## Views
### Chicago.Socioeconomic_Indicators_per_ZIP ```` ------------------------------------------------------------------------------- --- --- Recomputes average income from community area to ZIP code ---  -------------------------------------------------------------------------------  CREATE   VIEW Chicago.Socioeconomic_Indicators_per_ZIP AS  --- Compute the overlap (intersection) of community areas and ZIP codes WITH geo AS (     SELECT zip.ZIP,             ca.Community,             ca.Boundary.STArea() AS Community_area,             ROUND(ca.Boundary.STIntersection(zip.Boundary).STArea()/zip.Boundary.STArea(), 4) AS Area_overlap_percent     FROM Chicago.ZipCodes AS zip     INNER JOIN Chicago.Community_Areas AS ca ON ca.Boundary.STIntersects(zip.Boundary)=1)   --- Calculate the weighted average (by geographical area) for each measure: SELECT geo.ZIP,         CAST(SUM(soc.[Percent of housing crowded]*geo.Area_overlap_percent)/             NULLIF(SUM(geo.Area_overlap_percent), 0) AS numeric(5, 2)) [Percent of housing crowded],         CAST(SUM(soc.[Percent households below poverty]*geo.Area_overlap_percent)/             NULLIF(SUM(geo.Area_overlap_percent), 0) AS numeric(5, 2)) [Percent households below poverty],         CAST(SUM(soc.[Percent aged 16+ unemployed]*geo.Area_overlap_percent)/             NULLIF(SUM(geo.Area_overlap_percent), 0) AS numeric(5, 2)) [Percent aged 16+ unemployed],         CAST(SUM(soc.[Percent aged 25+ without high school diploma]*geo.Area_overlap_percent)/             NULLIF(SUM(geo.Area_overlap_percent), 0) AS numeric(5, 2)) [Percent aged 25+ without high school diploma],         CAST(SUM(soc.[Percent aged under 18 or over 64]*geo.Area_overlap_percent)/             NULLIF(SUM(geo.Area_overlap_percent), 0) AS numeric(5, 2)) [Percent aged under 18 or over 64],         CAST(SUM(soc.[Per capita income]*geo.Area_overlap_percent)/             NULLIF(SUM(geo.Area_overlap_percent), 0) AS numeric(10, 2)) [Per capita income],         CAST(SUM(soc.[Hardship index]*geo.Area_overlap_percent)/             NULLIF(SUM(geo.Area_overlap_percent), 0) AS numeric(5, 2)) [Hardship index] FROM geo INNER JOIN Chicago.Population_by_Zip_Code AS pop ON geo.ZIP=pop.ZIP AND pop.[Year]=2019 INNER JOIN Chicago.Socioeconomic_Indicators_per_Community_Area AS soc ON geo.Community=soc.Community AND soc.[Year]=2012 GROUP BY geo.ZIP  ```` 
### Tickets.Monthly_Balances ```` CREATE   VIEW Tickets.Monthly_Balances WITH SCHEMABINDING AS  SELECT Ticket_Status_ID,        DATEFROMPARTS(             DATEPART(year, Issued_date),             DATEPART(month, Issued_date),             1) AS Issued_month,         SUM(Amount_paid) AS Amount_paid,         SUM(Amount_due) AS Amount_due,         COUNT_BIG(*) AS Ticket_count FROM Tickets.Parking_Violations GROUP BY Ticket_Status_ID,          DATEFROMPARTS(               DATEPART(year, Issued_date),               DATEPART(month, Issued_date),               1)  ```` 
## Stored procedures
**Apply_Location_Geocoding** 
**Compute_Intersections** 
**Compute_Officer_assignments** 
**Populate_Accounting** 
**Set_Table_Description** 
**Vehicle_make_ticket_count** 
## Functions
**Celsius_to_Fahrenheit** 
**Fahrenheit_to_Celsius** 
**JSON_to_WKT** 
**Title_Case** 