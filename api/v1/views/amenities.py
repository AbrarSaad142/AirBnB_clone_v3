#!/usr/bin/python3
"""This script defines State"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def all_amenity():
    """get State objects"""
    amen = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amen)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """get amenity object"""
    amen = storage.get(Amenity, amenity_id)
    if amen is None:
        abort(404)
    return jsonify(amen.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete amenity"""
    amen = storage.get(Amenity, amenity_id)
    if amen is None:
        abort(404)
    storage.delete(amen)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates amenity"""
    a = request.get_json()
    if a is None:
        abort(400, "Not a JSON")
    if 'name' not in a:
        abort(400, "Missing name")
    new = Amenity(**j)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Update amenity"""
    amen = storage.get(Amenity, amenity_id)
    if amen is None:
        abort(404)
    a = request.get_json()
    if a is None:
        abort(400, "Not a JSON")
    for key, value in j.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amen, key, value)
    amen.save()
    return jsonify(amen.to_dict()), 200
