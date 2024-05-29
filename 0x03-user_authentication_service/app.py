#!/usr/bin/env python3
"""Flask application
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    return message Bienvenue when web server invoking router '/'
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
