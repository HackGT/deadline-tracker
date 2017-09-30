from configparser import ConfigParser
import os

ENV_CONFIG_KEY = 'BUS_MONITOR_CONFIG'
ENV_SECRETS_KEY = 'BUS_MONITOR_SECRETS'

class Config:
    def __init__(self, config, secrets):
        self.mongo = config['MONGO']
        self.auth = secrets['AUTH']
        self.auth_enabled = secrets.getboolean('AUTH', 'ENABLED')

def _loadConfig():
    config_file = 'config.ini'
    if ENV_CONFIG_KEY in os.environ and len(os.environ[ENV_CONFIG_KEY].strip()) > 0:
        config_file = os.environ[ENV_CONFIG_KEY]
    config = ConfigParser()
    config.read(config_file)

    secrets_file = 'secrets.ini'
    if ENV_SECRETS_KEY in os.environ and len(os.environ[ENV_SECRETS_KEY].strip()) > 0:
        secrets_file = os.environ[ENV_SECRETS_KEY]
    secrets = ConfigParser()
    secrets.read(secrets_file)

    return Config(config, secrets)

CONFIG = _loadConfig()
