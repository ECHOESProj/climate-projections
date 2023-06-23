# Climate Projections

## Getting started
This project pulls climate projection data from [CDS](https://cds.climate.copernicus.eu/#!/home) and [CEDA](https://www.ceda.ac.uk/), automatically creates time-series layers in GeoServer and inserts raw climate projection data into the PostgresSQL database for consumption by the web platform.

Accounts need to be created on both CDS and CEDA to access the data. To access data on CDS, the Python library [cdsapi](https://cds.climate.copernicus.eu/api-how-to) is used. This needs a url and api key, which is stored in a file called `.cdsapirc`. See the [cdsapi How to](https://cds.climate.copernicus.eu/api-how-to) on how to set this up. The configured `.cdsapirc` file needs to be copied to the root directory of this project so that it can be used by Docker (see `Dockerfile` where `.cdsapirc` is copied).

CEDA uses FTP, the username and password for which can be found on the CEDA website https://services.ceda.ac.uk/cedasite/myceda/user/

GeoServer, PostGresSQL and CEDA endpoints and credentials need to be set in the relevant environment file under `app/config` before the application is built/run. 

<br>

## Project structure
A package structure is used so that top level scripts (e.g. app.py) and second level scripts (e.g. utils/fs.py) can be run individually and can import each other easily.
`init.py` contains a `get_env` function that will retrieve the value of an environment variable (defined in the `config` folder using `dotenv`). It also has a `get_path` function which will resolve paths relative to the project root.

The config folder contains `.env` files which contain settings for each environment, along with a `base.env` to store common settings. All settings defined in the `.env` files can be overridden with container / system environment variables.
A file called `overrides.env` can be added to the config folder and can contain settings for local development. This file can contain usernames and passwords and is ignored by source control so never gets checked in.

<br>

## Update config
Before running the application, ensure that relevant credentials and endpoints are set in `base.env` or `dev/qa/production.env` in the `app/config` folder.
Values can also be set in `overrides.env` for local testing.

## Run
This project uses Docker to allow easy installation of GDAL on a Windows based system. The project can be run on both Windows (with WSL) or native Linux

https://www.docker.com/products/docker-desktop/

### Build

```bash
docker build . -t echoes-climate-projections --network host
```

### Run

```bash
docker run echoes-climate-projections --network host
```

### Run with environment flag

```bash
docker run echoes-climate-projections --network host --env=qa
```

<br>


### Run / debug with Visual Studio Code
Install the following extensions:
* [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
* [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)

`F5` to start debugging

