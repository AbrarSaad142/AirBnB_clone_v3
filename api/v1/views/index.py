#!/usr/bin/python3
"""this script to define app_views"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def view():
    """return json"""
    return jsonify({"status": "OK"})
