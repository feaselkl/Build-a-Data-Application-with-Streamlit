import streamlit as st
import pandas as pd
import numpy as np
 
st.title('Chicago Parking Tickets Analysis')
 
st.write("""
        This application provides a simple interface for analyzing parking tickets in Chicago. The data originally came from the City of Chicago's data portal. The great and wonderful Daniel Hutmacher [converted this data into a SQL Server database](https://sqlsunday.com/2022/12/05/new-demo-database/) and that is what we are querying in this application.
        """)
 
# Sidebar widgets
st.sidebar.header('Filters')
st.sidebar.write("Use these options to filter the data.")
st.sidebar.subheader('Violation Code')
# TODO: add code to filter by violation code
st.sidebar.subheader('Ticket Status')
# TODO: add code to filter by ticket status
st.sidebar.subheader('Notice Level')
# TODO: add code to filter by notice level