from app.init import get_env, get_path
from ftplib import FTP
import logging
from app.utils.fs import ensure_folder, clear_folder
from os import path

ftp_url = get_env('CEDA_FTP')
username = get_env('CEDA_Username')
password = get_env('CEDA_Password')
temp_path = path.join(get_env('Temp_Dir'), 'climate_projections', 'ceda')

def download_files(ftp_path: str, local_path: str):
    ftp = FTP(ftp_url)
    ftp.login(user=username, passwd=password)
    ftp.cwd(ftp_path)

    files = ftp.nlst()
    for f in files:
        ftp.retrbinary("RETR " + f, open(f'{local_path}/{f}', 'wb').write)

    ftp.quit()

    return files

def get_ceda_data(ftp_path: str):
    local_path = ensure_folder(path.join(temp_path, ftp_path))
    logging.info(f'Downloading data in {ftp_path} from the CEDA')
    clear_folder(local_path)
    files = download_files(ftp_path, local_path)
    return [path.join(local_path, file) for file in files]
