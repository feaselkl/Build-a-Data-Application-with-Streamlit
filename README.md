# Build a Data Application with Streamlit

This repository provides the supporting code for my presentation entitled [Build a Data Application with Streamlit](https://www.catallaxyservices.com/presentations/build-a-data-application-with-streamlit/).

## Running the Code

If you are running things locally, follow the relevant cheat sheet in the Cheat Sheets folder.

## Requirements per Project

Each of the three Streamlit web applications with have its own set of requirements.

### Parking Tickets Analysis

To run the parking ticket analysis application, you will need SQL Server and a copy of [the Chicago Parking Tickets database](https://sqlsunday.com/2022/12/05/new-demo-database/). You may also need to update the SQL Server connection string in `code\01_parking_tickets_analysis\src\config.json` if you are not running SQL Server using Windows authentication on localhost.

### Anomaly Detection

There are no specific external requirements for the anomaly detection example, although you will host a REST API using Uvicorn as part of the process.

### Azure OpenAI Integration

In order to try out the Azure OpenAI integration, you will need the following resources:

1. An Azure OpenAI endpoint. You will want to copy the URL endpoint for Azure OpenAI, as well as one of your access keys.
2. Create a GPT-4 deployment named something like "gpt-4"
3. Azure AI Search
4. Azure AI Speech

For full instructions on how to set everything up, [follow the Microsoft TechExcel training](https://github.com/microsoft/TechExcel-Implementing-automation-practices-using-Azure-OpenAI) to see what you need to replicate this scenario.
