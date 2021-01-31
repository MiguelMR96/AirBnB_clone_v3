#!/usr/bin/python3
""" RESTful Api - use methods HTTP in users
"""
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/users', strict_slashes=False, methods=['GET'])
@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def all_users(user_id=None):
    """ method to list all users
    """
    new_list = []
    if user_id:
        for item in storage.all(User).values():
            if user_id == item.id:
                return (jsonify(item.to_dict()))
        abort(404)

    for item in storage.all(User).values():
        new_list.append(item.to_dict())
    return(jsonify(new_list))


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id=None):
    """ method to delete an users
    """
    for item in storage.all(User).values():
        if user_id == item.id:
            item.delete()
            storage.save()
            return (jsonify({}))
    abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """ method to create an users
    """
    is_json = request.get_json()
    if is_json is None:
        abort(400, description="Not a Json")

    if is_json.get('email') is None:
        abort(400, description="Missing email")

    if is_json.get('password') is None:
        abort(400, description="Missing password")

    New_user = User(**is_json)
    New_user.save()
    return(jsonify(New_user.to_dict())), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id=None):
    """ method to update an users
    """
    if user_id:
        for item in storage.all(User).values():
            if user_id == item.id:
                is_json = request.get_json()
                if is_json is None:
                    abort(400, description="Not a Json")

                item.password = is_json.get('password')
                storage.save()
                return (jsonify(item.to_dict()))
        abort(404)
