#!/usr/bin/python3
"""reviews view"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_places(place_id):
    """Retrieves the list of all Review objects of a State"""
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        return abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete review"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    if not request.get_json():
        return abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        return abort(400, 'Missing user_id')
    data = request.get_json()
    user = storage.get(User, data['user_id'])
    if not user:
        return abort(404)
    if 'text' not in data:
        return abort(400, 'Missing text')
    data['place-id'] = place_id

    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_reviews(review_id):
    """Update a review"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    review = storage.get(Review, review_id)
    if review:
        if not request.get_json():
            return abort(400, 'Not a JSON')
        data = request.get_json()
        Ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in Ignore_keys:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    else:
        return abort(404)
