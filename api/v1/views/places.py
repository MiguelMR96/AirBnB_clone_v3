#!/usr/bin/python3
""" RESTful Api - use methods HTTP in places
"""
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def all_places(city_id=None):
    """ to list all place of a city
    """
    new_list = []
    if city_id:
        for item in storage.all(City).values():
            if city_id == item.id:
                for place in item.places:
                    new_list.append(place.to_dict())
                return(jsonify(new_list))
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def one_place(place_id=None):
    """ to list one plane
    """
    if place_id:
        for item in storage.all(Place).values():
            if place_id == item.id:
                return (jsonify(item.to_dict()))
        abort(404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place(place_id=None):
    """ to delete one place
    """
    for item in storage.all(Place).values():
            if place_id == item.id:
                item.delete()
                storage.save()
                return (jsonify({}))
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def post_place(city_id=None):
    """ to create a new place
    """
    if city_id:
        if storage.get(City, city_id) is None:
            abort(404)

        is_json = request.get_json()
        if is_json is None:
            abort(400, description="Not a Json")

        if is_json.get('user_id') is None:
            abort(400, description="Missing user_id")

        if storage.get(User, is_json.get('user_id')) is None:
            abort(404)

        if is_json.get('name') is None:
            abort(400, description="Missing name")

        new_place = Place(**is_json)
        new_place.save()
        return(jsonify(new_place.to_dict())), 201

    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def put_place(place_id=None):
    """ to update a place
    """
    if place_id:
        for item in storage.all(Place).values():
            if place_id == item.id:
                is_json = request.get_json()
                if is_json is None:
                    abort(400, description="Not a Json")

                value_update = Place(**is_json)
                storage.save()
                return (jsonify(item.to_dict()))
        abort(404)
    abort(404)
