import os
from pathlib import Path

import yaml

from utils.logger import logger

config: dict = {}

def init_config():
    logger.info('Loading config.yaml file ...')
    project_path = Path(__file__).parent.parent
    config_file = os.getenv('COMM-TEAM-AI-PROJECT', str(project_path) + '/config.yaml')
    if config_file:
        _load_config(config_file)

def _load_config(config_file: str):
    global config

    logger.info(f'Initializing comm team ai project with config file {config_file}')
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
            config = replace_env_variables(config)
    except Exception as e:
        logger.exception(f'Failed to load config file: {config_file}')
        raise Exception(f'Failed to load config file: {config_file}. Error: {e}')

def replace_env_variables(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = replace_env_variables(value)
    elif isinstance(data, list):
        for i in range(len(data)):
            data[i] = replace_env_variables(data[i])
    elif isinstance(data, str) and data.startswith('os.environ/'):
        env_variable = data.split('/')[1]
        data = os.environ.get(env_variable, None)
        if not data:
            raise Exception(f'Environment variable: {env_variable} not found!!!')
    return data

def get_config():
    if not config:
        init_config()

    return config

if __name__ == "__main__":
    config = get_config()
    logger.info(config)
    logger.info(config['genai']['api_key'])
