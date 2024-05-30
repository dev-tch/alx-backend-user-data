#!/usr/bin/env python3
"""Flask application
"""
from flask import Flask, jsonify, request, abort, redirect
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


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ logout user"""
    cookie = request.headers.get('Cookie')
    session_id = cookie[len('session_id='):]
    user_obj = AUTH.get_user_from_session_id(session_id)
    if user_obj is not None:
        AUTH.destroy_session(user_obj.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ get user profile"""
    cookie = request.headers.get('Cookie')
    session_id = cookie[len('session_id='):]
    user_obj = AUTH.get_user_from_session_id(session_id)
    if user_obj is not None:
        return jsonify({"email": user_obj.email})
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ gen token for registred user"""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    except ValueError:
        abort(403)


@app.route('/update_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """ endapi to update password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
