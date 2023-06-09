import sys
import pathlib
import os
from dotenv import load_dotenv
import logging
from logging.handlers import TimedRotatingFileHandler

#file_handler = TimedRotatingFileHandler('logs/log.txt', when='midnight', interval=1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        #file_handler,
        logging.StreamHandler()
    ]
)

args = ''.join(sys.argv)
config_folder = os.path.join(os.path.dirname(__file__), 'config') # f'{base_dir}/config'

os.environ['Temp_Dir'] = os.path.join(os.path.dirname(__file__), '.temp')

is_dev = '--env=dev' in args
is_qa = '--env=qa' in args
is_production = '--env=production' in args

# Local overrides
load_dotenv(f'{config_folder}/overrides.env')
load_dotenv(f'{config_folder}/local.env')

if is_production:
  logging.info('env: Production')
  load_dotenv(f'{config_folder}/production.env')
elif is_qa:
  logging.info('env: QA')
  load_dotenv(f'{config_folder}/qa.env')
elif is_dev:
  logging.info('env: DEV')
  load_dotenv(f'{config_folder}/dev.env')
else:
  logging.info('env: NONE')

load_dotenv(f'{config_folder}/base.env')

def get_env(key):
    return os.getenv(key)

def get_path(path):
    return os.path.join(os.path.dirname(__file__), path)
