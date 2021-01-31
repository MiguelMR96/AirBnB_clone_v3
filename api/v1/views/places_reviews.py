#!/usr/bin/python3
""" RESTful Api - use methods HTTP in places_review
"""
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify, abort, Response, request


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def all_reviews(place_id=None):
    """ to list all reviews of a place
    """
    new_list = []
    if place_id:
        for item in storage.all(Place).values():
            if place_id == item.id:
                for review in item.reviews:
                    new_list.append(review.to_dict())
                return(jsonify(new_list))
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def one_review(review_id=None):
    """ to list one review
    """
    if review_id:
        for item in storage.all(Review).values():
            if review_id == item.id:
                return (jsonify(item.to_dict()))
        abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_review(review_id=None):
    """ to delete one reviews
    """
    if review_id:
        for item in storage.all(Review).values():
                if review_id == item.id:
                    item.delete()
                    storage.save()
                    return (jsonify({}))
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def post_review(place_id=None):
    """ to create a new review
    """
    if place_id:
        if storage.get(Place, place_id) is None:
            abort(404)

        is_json = request.get_json()
        if is_json is None:
            abort(400, description="Not a Json")

        if is_json.get('user_id') is None:
            abort(400, description="Missing user_id")

        if storage.get(User, is_json.get('user_id')) is None:
            abort(404)

        if is_json.get('text') is None:
            abort(400, description="Missing text")

        new_review = Review(**is_json)
        new_review.place_id = place_id
        new_review.save()
        return(jsonify(new_review.to_dict())), 201

    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def put_review(review_id=None):
    """ to update a place
    """
    if review_id:
        for item in storage.all(Review).values():
            if place_id == item.id:
                is_json = request.get_json()
                if is_json is None:
                    abort(400, description="Not a Json")

                item.text = is_json.get("text")
                storage.save()
                return (jsonify(item.to_dict()))
        abort(404)
    abort(404)
