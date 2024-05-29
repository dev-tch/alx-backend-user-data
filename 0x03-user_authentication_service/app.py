#!/usr/bin/env python3
"""Flask application
"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    return message Bienvenue when web server invoking router '/'
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """ api to register new user"""
    email = request.form['email']
    password = request.form['password']
    try:
        auth.register_user(email=email, password=password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
