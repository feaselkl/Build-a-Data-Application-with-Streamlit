FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
	build-essential \
	curl \
	software-properties-common \
	git \
	&& rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 msodbcsql17
RUN git clone https://github.com/feaselkl/Build-a-Data-Application-with-Streamlit.git .
WORKDIR /app/code
RUN pip3 install -r requirements.txt
# You must have a secrets.toml file in .streamlit.
# This file should contain the following sections and keys:
    # db: connection_string
        # Note that we are not running SQL Server in the container, so the connection string
        # should point to a SQL Server instance that is accessible from the container.
    # aoai: endpoint, key, deployment_name
    # search: endpoint, key, index_name
    # speech: key, region
COPY ./.streamlit/ ./.streamlit/
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["streamlit", "run", "index.py", "--server.port=8501", "--server.address=0.0.0.0"]