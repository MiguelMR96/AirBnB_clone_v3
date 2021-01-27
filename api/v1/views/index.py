#!/usr/bin/python3
"""Our first template with blueprint
"""


from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    """ Route status check first reponse json
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    """ Retrieves the number of each objects by type
    """
    cls_dic = {'amenities': storage.count(Amenity),
               'cities': storage.count(City),
               'places': storage.count(Place),
               'reviews': storage.count(Review),
               'states': storage.count(State),
               'users': storage.count(User)}

    return jsonify(cls_dic)
