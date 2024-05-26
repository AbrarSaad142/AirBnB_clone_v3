#!/usr/bin/python3
"""This script defines State"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'])
def get_states():
    """define states"""
    my_states = []
    for state in storage.all(State).values():
        my_states.append(state.to_dict())
    return jsonify(my_states)

@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """define state by id"""
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

@app_views.route('/states', methods=['POST'])
def do_state():
    """Create state"""
    j = request.get_json()
    if j is None:
        return jsonify({"Not a JSON"}), 400
    if 'name' not in j:
        return jsonify({"Missing name"}), 400
    new_state = State(**j)
    new_state.save()
    return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update state"""
    my_state = storage.get(State, state_id)
    if my_state is None:
        abort(404)
    j = request.get_json()
    if j is None:
        return jsonify({"Not a JSON"}), 400
    for key, value in j.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(my_state, key, value)
    my_state.save()
    return jsonify(my_state.to_dict()), 200
