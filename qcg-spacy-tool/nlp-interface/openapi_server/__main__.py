#!/usr/bin/env python3
from openapi_server.start_app import start_app

if __name__ == '__main__':
    import logging.config
    import yaml

    with open('openapi_server/config.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    start_app(base_path='/', port=8080)
