#!/usr/bin/python3
"""define States"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Return list of State"""
    my_states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(my_states)


@app.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Return a specific State object by its state_id."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


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



@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """create a state"""
    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    if data.get("name") is None:
        abort(400, "Missing name")

    new = State(**data)
    new.save()

    return jsonify(new.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """update a state"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)

    d = request.get_json()

    if d is None:
        abort(400, "Not a JSON")

    for k, v in d.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    state.save()

    return jsonify(state.to_dict()), 200
