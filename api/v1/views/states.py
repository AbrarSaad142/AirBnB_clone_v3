#!/usr/bin/python3
"""This script defines State"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def all_states():
    """get State objects"""
    list_states = []
    for state in storage.all(State).values():
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """get State object"""
    state = storage.get(State, state_id)
    return abort(404) if state is None else jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates state"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if data.get("name") is None:
        abort(400, "Missing name")
    new_state = State(**data)
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a State"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)

    data = request.get_json()

    if data is None:
         abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    
    return jsonify(state.to_dict()), 200
