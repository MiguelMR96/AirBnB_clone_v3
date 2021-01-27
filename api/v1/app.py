#!/usr/bin/python3
"""Get start working RESTful API
"""


from flask import Flask, make_response, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown_app(exception):
    """ close sesion db
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 custom page
    """
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    if getenv('HBNB_API_HOST') is None:
        HBNB_API_HOST = '0.0.0.0'
    else:
        HBNB_API_HOST = getenv('HBNB_API_HOST')

    if getenv('HBNB_API_PORT') is None:
        HBNB_API_PORT = '5000'
    else:
        HBNB_API_PORT = getenv('HBNB_API_PORT')

    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, debug=True, threaded=True)
