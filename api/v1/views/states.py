#!/usr/bin/python3
"""define States"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """return list of states"""
    all_states = []
    for state in storage.all(State).values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """retrieves a State"""
    state = storage.get(State, state_id)
    return abort(404) if state is None else jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """deletes a state"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200



@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Create a state"""
    if request.content_type != 'application/json':
        abort(400, description="Not a JSON")

    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    if not data:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name")

    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Update a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.content_type != 'application/json':
        abort(400, description="Not a JSON")

    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    if not data:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    
    return jsonify(state.to_dict()), 200
