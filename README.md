# Build a Data Application with Streamlit

This repository provides the supporting code for my presentation entitled [Build a Data Application with Streamlit](https://www.catallaxyservices.com/presentations/build-a-data-application-with-streamlit/).

I have also made [a YouTube playlist of videos](https://www.youtube.com/playlist?list=PLeWL8zChJ2uuM9ekUgR6pLjxXVfv_IVZb) in case you would prefer the content in approximately 20-minute chunks.

## Branching

This repository includes a series of branches, starting with `01-intro` and ending with `master`. The idea is to traverse each branch in order. This will allow you to see the Chicago Parking Tickets application as we build it. Each branch represents the **completed** code for that section.

## Running the Code

If you are running things locally, follow the relevant cheat sheet in the Cheat Sheets folder.

## Requirements

This 

### Secrets

The code in this repository relies on a file that you'll have to create in `code\.streamlit\secrets.toml`. Note that you will need to create the `.streamlit` directory as well as the file. This file will contain all of the secrets that you'll need to follow along. Here is a sample of how it should look:

```toml
[db]
connection_string="DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=ChicagoParkingTickets;Trusted_Connection=yes"
# Replace this connection string with whatever is appropriate for your environment.

[aoai]
endpoint = "YOUR ENDPOINT"
key = "YOUR KEY"
deployment_name = "YOUR DEPLOYMENT NAME"

[search]
endpoint = "YOUR ENDPOINT"
key = "YOUR KEY"
index_name = "YOUR INDEX NAME"

[speech]
key = "YOUR KEY"
region = "YOUR REGION"
```

### Parking Tickets Analysis

To run the parking ticket analysis application, you will need SQL Server and a copy of [the Chicago Parking Tickets database](https://sqlsunday.com/2022/12/05/new-demo-database/). You may also need to update the SQL Server connection string in `code\.streamlit\secrets.toml` if you are not running SQL Server using Windows authentication on localhost.

### Azure OpenAI Integration

In order to try out the Azure OpenAI integration, you will need the following resources:

1. An Azure OpenAI endpoint. You will want to copy the URL endpoint for Azure OpenAI, as well as one of your access keys.
2. Create a GPT-4 deployment named something like "gpt-4"
3. Azure AI Search
4. Azure AI Speech

Note that [Azure OpenAI no longer requires explicit approval](https://learn.microsoft.com/en-us/legal/cognitive-services/openai/limited-access) for using the service in the scenarios we cover. You should not need explicit approval in order to use Azure OpenAI on your Azure subscription.
