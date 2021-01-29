#!/usr/bin/python3
""" RESTful Api - use methods HTTP in amenities
"""
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity
from flask import jsonify, abort, Response, request


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def amenities(amenity_id=None):
    new_list = []
    if amenity_id:
        for key in storage.all(Amenity).values():
            if amenity_id == key.id:
                return (jsonify(key.to_dict()))
        abort(404)

    for item in storage.all(Amenity).values():
        new_list.append(item.to_dict())
    return(jsonify(new_list))


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id=None):
    if amenity_id:
        for key in storage.all(Amenity).values():
            if amenity_id == key.id:
                key.delete()
                storage.save()
                return (jsonify({}))
        abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    is_json = request.get_json()
    if is_json is None:
        abort(400, description="Not a Json")

    if is_json.get('name') is None:
        abort(400, description="Missing name")

    new_state = Amenity()
    new_state.name = is_json.get('name')
    new_state.save()
    return(jsonify(new_state.to_dict())), 201


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id=None):
    if amenity_id:
        for key in storage.all(Amenity).values():
            if amenity_id == key.id:
                is_json = request.get_json()
                if is_json is None:
                    abort(400, description="Not a Json")

                key.name = is_json.get('name')
                storage.save()
                return (jsonify(key.to_dict()))
        abort(404)
