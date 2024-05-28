#!/usr/bin/python3
"""This module handle states"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Returns list of states"""
    my_states = storage.all(State)
    return jsonify([state.to_dict() for state in my_states.values()])


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """get state."""
    my_state = storage.get(State, state_id)
    if my_state is None:
        abort(404)
    return jsonify(my_state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete state"""
    my_state = storage.get(State, state_id)
    if my_state is None:
        abort(404)
    storage.delete(my_state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new state with data sent in the request"""
    data = request.get_json(silent=True)
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    new = State(**data)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update state"""
    my_state = storage.get(State, state_id)
    if my_state is None:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ("id", "created_at", "updated_at"):
            setattr(my_state, key, value)
    my_state.save()
    return jsonify(my_state.to_dict()), 200
