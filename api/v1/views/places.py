#!/usr/bin/python3
"""This script defines API routes for Place objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def all_places(city_id):
    """Retrieve places"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """get Place"""
    my_place = storage.get(Place, place_id)
    if not my_place:
        abort(404)
    return jsonify(my_place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes Place"""
    p = storage.get(Place, place_id)
    if not p:
        abort(404)
    storage.delete(p)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates new Place"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    c = storage.get(City, city_id)
    if c is None:
        abort(404)
    pl = request.get_json()
    if pl is None:
        abort(400, "Not a JSON")
    if 'user_id' not in pl:
        abort(400, "Missing user_id")
    u = storage.get(User, pl['user_id'])
    if u is None:
        abort(404)
    if 'name' not in pl:
        abort(400, "Missing name")
    pl['city_id'] = city_id
    n_place = Place(**pl)
    n_place.save()
    return jsonify(n_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates Place"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    pl = request.get_json()
    if pl is None:
        abort(400, "Not a JSON")
    for key, value in pl.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(my_place, key, value)
    my_place.save()
    return jsonify(my_place.to_dict()), 200
