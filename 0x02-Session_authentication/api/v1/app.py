#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
type_auth = os.getenv('AUTH_TYPE', None)
if type_auth is not None:
    if type_auth == 'auth':
        from api.v1.auth.auth import Auth
        auth = Auth()
    elif type_auth == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    elif type_auth == 'session_auth':
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()


@app.before_request
def before_request() -> None:
    """ decorator excuted before request action to save user data"""
    if auth is None:
        return
    paths_excluded = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/', '/api/v1/auth_session/login/']

    path_ok = auth.require_auth(request.path, paths_excluded)
    if not path_ok:
        return
    valid_session = auth.session_cookie(request) is None
    if auth.authorization_header(request) is None and valid_session:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)
    # save authenticated user in new attribute
    setattr(request, 'current_user', auth.current_user(request))


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_access(error) -> str:
    """ ressource protected , need authentication
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_access(error) -> str:
    """ ressource protected , need authorization
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
