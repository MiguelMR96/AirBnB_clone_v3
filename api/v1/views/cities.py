#!/usr/bin/python3
""" RESTful Api - use methods HTTP in cities
"""
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.city import City
from models.state import State
from flask import jsonify, abort, Response, request


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def all_cities(state_id=None):
    new_list = []
    if state_id:
        for item in storage.all(State).values():
            if state_id == item.id:
                for city in item.cities:
                    new_list.append(city.to_dict())
                return(jsonify(new_list))
        abort(404)


@app_views.route('cities/<city_id>', strict_slashes=False, methods=['GET'])
def one_city(city_id=None):
    if city_id:
        for item in storage.all(City).values():
            if city_id == item.id:
                return (jsonify(item.to_dict()))
        abort(404)


@app_views.route('cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id=None):
    for item in storage.all(City).values():
            if city_id == item.id:
                item.delete()
                storage.save()
                return (jsonify({}))
    abort(404)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def post_city(state_id=None):
    if state_id:
        is_json = request.get_json()
        if is_json is None:
            abort(400, description="Not a Json")

        if is_json.get('name') is None:
            abort(400, description="Missing name")

        for state in storage.all(State).values():
            if state.id == state_id:
                city = City()
                city.name = is_json.get('name')
                city.state_id = state.id
                city.save()
                return(jsonify(city.to_dict())), 201
        abort(404)

    else:
        abort(404)


@app_views.route('cities/<city_id>', strict_slashes=False, methods=['PUT'])
def put_cities(city_id=None):
    if city_id:
        for item in storage.all(City).values():
            if city_id == item.id:
                is_json = request.get_json()
                if is_json is None:
                    abort(400, description="Not a Json")

                item.name = is_json.get('name')
                storage.save()
                return (jsonify(item.to_dict()))
        abort(404)
