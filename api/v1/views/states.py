#!/usr/bin/python3
"""[summary]
"""
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.state import State
from flask import jsonify, abort, Response, request


@app_views.route('/states', strict_slashes=False, methods=['GET'])
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def states(state_id=None):
    new_list = []
    if state_id:
        for key in storage.all(State).values():
            if state_id == key.id:
                return (jsonify(key.to_dict()))
        abort(404)

    for item in storage.all(State).values():
        new_list.append(item.to_dict())
    return(jsonify(new_list))


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_state(state_id=None):
    if state_id:
        for key in storage.all(State).values():
            if state_id == key.id:
                key.delete()
                storage.save()
                return (jsonify({}))
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_state():
    is_json = request.get_json()
    if is_json is None:
        abort(400, description="Not a Json")

    if is_json.get('name') is None:
        abort(400, description="Missing name")

    new_state = State()
    new_state.name = is_json.get('name')
    new_state.save()
    return(jsonify(new_state.to_dict())), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def put_state(state_id=None):
    if state_id:
        for key in storage.all(State).values():
            if state_id == key.id:
                is_json = request.get_json()
                if is_json is None:
                    abort(400, description="Not a Json")

                key.name = is_json.get('name')
                storage.save()
                return (jsonify(key.to_dict()))
        abort(404)
