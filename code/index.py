import streamlit as st
import pandas as pd
import numpy as np
import pyodbc
import plotly.express as px
import plotly.graph_objects as go
import json
 
connection_string = st.secrets['db']['connection_string']
 
@st.cache_data
def get_tickets_by_month():
    conn = pyodbc.connect(connection_string)
    # NOTE: this query works with SQL Server 2022
    # With prior versions, you will need to replace DATETRUNC()
    # with DATEPART() (for year and then for month)
    # or some other function
    sql = """
        SELECT
            DATETRUNC(MONTH, pv.Issued_date) AS IssuedMonth,
            v.Violation_Code AS ViolationCode,
            ts.Ticket_Status AS TicketStatus,
            nl.Notice_Level AS NoticeLevel,
            COUNT(*) AS NumberOfTickets,
            SUM(pv.Fine_amount) AS TotalFineAmount,
            SUM(pv.Late_fee) AS TotalLateFee,
            SUM(pv.Collection_fee) AS TotalCollectionFee,
            SUM(pv.Amount_paid) AS TotalAmountPaid,
            SUM(pv.Amount_due) AS TotalAmountDue
        FROM Tickets.Parking_Violations pv
            INNER JOIN Tickets.Violation v
                ON pv.Violation_ID = v.Violation_ID
            INNER JOIN Tickets.Ticket_Status ts
                ON pv.Ticket_Status_ID = ts.Ticket_Status_ID
            INNER JOIN Tickets.Notice_Level nl
                ON pv.Notice_Level_ID = nl.Notice_Level_ID
        GROUP BY
            DATETRUNC(MONTH, pv.Issued_date),
            v.Violation_Code,
            ts.Ticket_Status,
            nl.Notice_Level;
    """
    return pd.read_sql(sql, conn)
 
@st.cache_data
def get_violation_codes():
    conn = pyodbc.connect(connection_string)
    sql = """
        SELECT
            Violation_Code AS ViolationCode,
            Violation_Description AS ViolationDescription
        FROM Tickets.Violation;
    """
    return pd.read_sql(sql, conn)
 
@st.cache_data
def get_ticket_status_codes():
    conn = pyodbc.connect(connection_string)
    sql = """
        SELECT
            Ticket_Status AS TicketStatus,
            Ticket_Status_Description AS TicketStatusDescription
        FROM Tickets.Ticket_Status;
    """
    return pd.read_sql(sql, conn)
 
@st.cache_data
def get_notice_level_codes():
    conn = pyodbc.connect(connection_string)
    sql = """
        SELECT
            Notice_Level AS NoticeLevel,
            Notice_Level_Description AS NoticeLevelDescription
        FROM Tickets.Notice_Level;
    """
    return pd.read_sql(sql, conn)
 
st.title('Chicago Parking Tickets Analysis')
 
st.write("""
        This application provides a simple interface for analyzing parking tickets in Chicago. The data originally came from the City of Chicago's data portal. The great and wonderful Daniel Hutmacher [converted this data into a SQL Server database](https://sqlsunday.com/2022/12/05/new-demo-database/) and that is what we are querying in this application.
        """)
 
# Sidebar widgets
st.sidebar.header('Filters')
st.sidebar.write("Use these options to filter the data.")
st.sidebar.subheader('Violation Code')
violation_codes = get_violation_codes()
# format_func is a setting to control how the options are displayed in the dropdown
violation_code = st.sidebar.selectbox(label='Select a violation code:', index=None, options=violation_codes['ViolationCode'].unique(),
                format_func=lambda x: f'{x} - {violation_codes[violation_codes["ViolationCode"] == x]["ViolationDescription"].values[0]}')
 
st.sidebar.subheader('Ticket Status')
ticket_status_codes = get_ticket_status_codes()
ticket_status = st.sidebar.selectbox(label='Select a ticket status:', index=None, options=ticket_status_codes['TicketStatus'].unique())
 
st.sidebar.subheader('Notice Level')
notice_level_codes = get_notice_level_codes()
notice_level = st.sidebar.selectbox(label='Select a notice level:', index=None, options=notice_level_codes['NoticeLevel'].unique(),
                format_func=lambda x: f'{x} - {notice_level_codes[notice_level_codes["NoticeLevel"] == x]["NoticeLevelDescription"].values[0]}')
 
st.header('Tickets by Month')
 
tickets_by_month = get_tickets_by_month()
# Perform filtering if filters are set
if violation_code:
    tickets_by_month = tickets_by_month[tickets_by_month['ViolationCode'] == violation_code]
if ticket_status:
    tickets_by_month = tickets_by_month[tickets_by_month['TicketStatus'] == ticket_status]
if notice_level:
    tickets_by_month = tickets_by_month[tickets_by_month['NoticeLevel'] == notice_level]
 
# Aggregate filtered data
agg_tickets_by_month = tickets_by_month.groupby('IssuedMonth').agg({'NumberOfTickets': 'sum', 'TotalFineAmount': 'sum', 'TotalLateFee': 'sum', 'TotalCollectionFee': 'sum', 'TotalAmountPaid': 'sum', 'TotalAmountDue': 'sum'}).reset_index().sort_values(by='IssuedMonth', ascending=False)
 
tab1, tab2, tab3 = st.tabs(['Tickets per Month', 'Fine Breakdown', 'Raw Data'])
 
with tab1:
    st.header("Number of Tickets per Month")
    g = px.line(agg_tickets_by_month, x='IssuedMonth', y='NumberOfTickets', title='Number of Tickets by Month',
                hover_data=['TotalFineAmount', 'TotalLateFee', 'TotalCollectionFee', 'TotalAmountPaid', 'TotalAmountDue'])
    st.plotly_chart(g, use_container_width=True)
 
with tab2:
    st.header("Breakdown of Fines per Month")
    g2 = px.bar(agg_tickets_by_month, x='IssuedMonth', y=['TotalFineAmount', 'TotalLateFee', 'TotalCollectionFee'], title='Breakdown of Fines by Month')
    st.plotly_chart(g2, use_container_width=True)
 
with tab3:
    st.header("Table of Monthly Ticket Data")
    agg_tickets_by_month = agg_tickets_by_month.style.format(
        {
            'IssuedMonth': lambda x: x.strftime('%Y-%m'),
            'NumberOfTickets': '{:,.0f}',
            'TotalFineAmount': lambda x: '${:,.0f}'.format(x),
            'TotalLateFee': lambda x: '${:,.0f}'.format(x),
            'TotalCollectionFee': lambda x: '${:,.0f}'.format(x),
            'TotalAmountPaid': lambda x: '${:,.0f}'.format(x),
            'TotalAmountDue': lambda x: '${:,.0f}'.format(x),
        }
    )
    st.dataframe(data=agg_tickets_by_month)