import logging.config
import yaml
import os

with open(os.path.join('tool','log_config.yaml'), 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)