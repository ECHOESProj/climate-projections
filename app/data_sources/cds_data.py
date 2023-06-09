from app.init import get_env, get_path
import cdsapi
from zipfile import ZipFile
import xarray as xr
from app.utils.fs import ensure_folder, clear_folder
from os import path
import logging

cds_client = cdsapi.Client()

temp_path = path.join(get_env('Temp_Dir'), 'climate_projections', 'cds')
temp_zip_file = path.join(temp_path, 'download.zip')

def get_cds_data(name, attributes):
    ensure_folder(temp_path)
    logging.info('Downloading data from the CDS')
    cds_client.retrieve(name, attributes, temp_zip_file)

    zf = ZipFile(temp_zip_file, 'r')
    zf.extractall(temp_path)
    list_of_files = zf.namelist()
    zf.close()

    return [path.join(temp_path, file) for file in list_of_files]
