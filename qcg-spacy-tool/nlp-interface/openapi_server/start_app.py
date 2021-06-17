import connexion
from flask import Flask,redirect

from openapi_server import encoder

import logging
logger = logging.getLogger(__name__)

app = connexion.App(__name__, specification_dir='./openapi/')

def start_app(base_path='/', port=8080):

    options = {
        'swagger_url': '/api-docs'
    }

    logger.debug("Starting app on port "+str(port))
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                base_path=base_path,
                arguments={'title': 'Analysis API'},
                pythonic_params=True,
                options=options) #openapi_console_ui_path
    app.run(port=port, debug=False)

@app.route('/<base_path>/')
def redirect_to_docs(base_path):
    print("redirecting...")
    return redirect('/'+base_path+'/api-docs', code=302)