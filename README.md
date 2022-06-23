[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[![Docker](https://badgen.net/badge/icon/docker?icon=docker&label)](https://hub.docker.com/r/mert019/open-etl)

# Open ETL

<div style="margin-bottom: 16px;">
    <img
    src="https://user-images.githubusercontent.com/67417415/168584766-a148a778-8dae-4a83-9a1e-88f5e833ca21.png"
    alt="etl-image"
    width="100"
    />
</div>

Open ETL is a simplified tool to extract data from data sources, process data and to load the extracted & processed data to data targets. 

## Why Open ETL?
Easy to install and configure. \
Simplified web based interface to create ETL operations. \
Detailed monitoring of the ETL operations.

## Screenshots
\
**Dashboard**
\
<img src="app/static/imgs/dashboard.png"/>
<br>
\
**Operation Logs**
\
<img src="app/static/imgs/logs.png"/>
<br>
\
**System Status**
\
<img src="app/static/imgs/system_status.png"/>
<br>
\
**Operation Configuration**
\
<img src="app/static/imgs/operation_config.png"/>
<br>
\
**Data Source Configuration**
\
<img src="app/static/imgs/db_extract_config.png"/>
<br>
\
**Data Target Configuration**
\
<img src="app/static/imgs/db_load_config.png"/>
<br>
\
**Database Connection**
\
<img src="app/static/imgs/db_connection.png"/>
<br>

## Supported Data Sources
Open ETL can extract data from databases (MS SQL Server, Postgresql) and XLSX & CSV files from FTP/SFTP servers. If you want additional data sources please create an issue.

<img
  style="background-color:white;border-radius:0px;"
  src="https://user-images.githubusercontent.com/67417415/168590045-8d77a7c3-b5fd-4fe6-9eec-de6182aa5fc5.png"
  alt="database-image"
  height="75"
/>
<img
  style="background-color:white;border-radius:0px;"
  src="https://user-images.githubusercontent.com/67417415/168590248-34447287-48e0-4b70-a67f-142fef08fbad.png"
  alt="mssqlserver-image"
  height="75"
/>
<img
  style="background-color:white;border-radius:0px;"
  src="https://user-images.githubusercontent.com/67417415/168590471-975001bd-5602-4f85-bdf9-3e6275cf94c9.png"
  alt="postgresql-image"
  height="75"
/>
<img
  style="background-color:white;border-radius:0px;"
  src="https://user-images.githubusercontent.com/67417415/168589665-075a1fc9-b130-44a5-ba9b-e47149af8bb8.png"
  alt="ftp-image"
  width="75"
/>
<img
  style=""
  src="https://user-images.githubusercontent.com/67417415/168588939-8787c81b-fe7c-485d-a48e-706a658db2be.png"
  alt="xlsx-image"
  width="75"
/>
<img
  style=""
  src="https://user-images.githubusercontent.com/67417415/168589359-4a98c126-6dbc-4769-9dba-97aa45d31cac.png"
  alt="csv-image"
  width="75"
/>



## Supported Data Targets
Open ETL can load the extracted data to databases (MS SQL Server, Postgresql). If you want additional data targets please create an issue.

<img
  style="background-color:white;border-radius:0px;"
  src="https://user-images.githubusercontent.com/67417415/168590045-8d77a7c3-b5fd-4fe6-9eec-de6182aa5fc5.png"
  alt="database-image"
  height="75"
/>
<img
  style="background-color:white;border-radius:0px;"
  src="https://user-images.githubusercontent.com/67417415/168590248-34447287-48e0-4b70-a67f-142fef08fbad.png"
  alt="mssqlserver-image"
  height="75"
/>
<img
  style="background-color:white;border-radius:0px;"
  src="https://user-images.githubusercontent.com/67417415/168590471-975001bd-5602-4f85-bdf9-3e6275cf94c9.png"
  alt="postgresql-image"
  height="75"
/>

## Transform Operations
Transform operations handled by utilizing staging database.

## Installation and Configuration
### Using Docker
```console
git clone https://github.com/mert019/open-ETL
cd open-ETL
docker-compose up -d
```
Go to http://localhost:8080/ \
Default admin user:
  - username: admin
  - password: password

### Configuration
For more information visit https://hub.docker.com/r/mert019/open-etl

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
