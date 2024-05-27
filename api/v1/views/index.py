#!/usr/bin/python3
"""this script to define app_views"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


classes = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }


@app_views.route('/status')
def view():
    """return json"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def state():
    """retrieves the number of each objects by type"""
    states = {}
    for key, value in classes.items():
        states[key] = storage.count(value)
    
    return jsonify(states)
