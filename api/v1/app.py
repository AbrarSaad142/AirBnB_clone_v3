#!/usr/bin/python3
"""This script defines a Flask application"""
from flask import Flask
from models import storage
from flask import jsonify
import os
from flask_cors import CORS
from api.v1.views import app_views

port = os.getenv("HBNB_API_PORT", "5000")
host = os.getenv("HBNB_API_HOST", "0.0.0.0")


app = Flask(__name__)

app.register_blueprint(app_views)
CORS(app, resources ={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """Calls storage close method"""
    storage.close()


@app.errorhandler(404)
def error_404(exception):
    """Handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, host=host, port=port, threaded=True)
