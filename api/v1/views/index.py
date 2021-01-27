#!/usr/bin/python3
"""Our first template with blueprint
"""


from api.v1.views import app_views
from flask import jsonify, request


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    """ Route status check first reponse json
    """
    return jsonify({"status": "OK"})
