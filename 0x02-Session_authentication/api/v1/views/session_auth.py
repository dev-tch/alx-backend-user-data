#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import jsonify, request,  make_response, abort
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
      - 400 if can't create the new User
    """
    # retrieve email and password parameters
    email = request.form.get('email')
    if not email:
        return jsonify({'error': 'email missing'}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({'error': 'password missing'}), 400
    try:
        list_usr_instance = []
        list_usr_instance = User.search({'email': email})
        if len(list_usr_instance) == 0:
            return jsonify({"error": "no user found for this email"}), 404
        else:
            for obj_user in list_usr_instance:
                if obj_user.is_valid_password(password):
                    from api.v1.app import auth
                    from os import getenv
                    session_id = auth.create_session(obj_user.id)
                    user_json = jsonify(obj_user.to_json())
                    resp = make_response(user_json)
                    cookie_name = getenv('SESSION_NAME')
                    if cookie_name:
                        resp.set_cookie(cookie_name, session_id)
                    return resp
            return jsonify({"error": "wrong password"}), 401
    except KeyError:
        return jsonify({"error": "no user found for this email"}), 404


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """  logout delete session_id from storage  """
    from api.v1.app import auth
    is_logged_out = auth.destroy_session(request)
    if not is_logged_out:
        abort(404)
    return jsonify({}), 200
