#!/usr/bin/python3
"""This script defines a Flask application"""
from flask import Flask
from flask import make_response
from models import storage
import os
from api.v1.views import app_views

port = os.getenv("HBNB_API_PORT", "5000")
host = os.getenv("HBNB_API_HOST", "0.0.0.0")


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Calls storage close method"""
    storage.close()
@app.error_handler(404)
def handler(error):
    return make_response(jsonify({"error": "Not found"}, 404)


if __name__ == "__main__":
    app.run(debug=True, host=host, port=port, threaded=True)
