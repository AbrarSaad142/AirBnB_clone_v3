#!/usr/bin/python3
"""This script defines State"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def all_states():
    """get State objects"""
    my_states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(my_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """get State object"""
    my_state = storage.get(State, state_id)
    if my_state is None:
        abort(404)
    return jsonify(my_state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State"""
    my_state = storage.get(State, state_id)
    if my_state is None:
        abort(404)
    storage.delete(my_state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates state"""
"""Creates state"""
    j = request.get_json()
    if j is None:
        abort(400, "Not a JSON")
    if 'name' not in j:
        abort(400, "Missing name")
    new = State(**j)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a State"""
    my_state = storage.get(State, state_id)
    if my_state is None:
        abort(404)
    j = request.get_json()
    if j is None:
         abort(400, "Not a JSON")
    for key, value in j.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(my_state, key, value)
    my_state.save()
    return jsonify(my_state.to_dict()), 200
