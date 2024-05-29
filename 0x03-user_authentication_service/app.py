#!/usr/bin/env python3
"""Flask application
"""
from flask import Flask, jsonify, request, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    return message Bienvenue when web server invoking router '/'
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """ api to register new user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email=email, password=password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """create session cookie for registered user"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    else:
        token_session = AUTH.create_session(email)
        json_response = {"email": email, "message": "logged in"}
        response = jsonify(json_response)
        response.set_cookie('session_id', token_session)
        return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
