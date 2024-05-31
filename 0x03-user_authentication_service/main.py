#!/usr/bin/env python3
"""
module integration of user
- register
- login
- logout
- reset password
- update password
- user profile
"""
import requests
import json

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ test register api"""
    payload = {'email': email, 'password': password}
    response = requests.post('http://localhost:5000/users', data=payload)
    expected_json = {"email": email, "message": "user created"}
    msg = json.dumps(expected_json, separators=(",", ":"))
    assert response.status_code == 200
    assert response.text.strip() == msg
    return None


def log_in_wrong_password(email: str, password: str) -> None:
    """ test login with wrong credentials"""
    payload = {'email': email, 'password': password}
    response = requests.post('http://localhost:5000/sessions', data=payload)
    assert response.status_code == 401
    return None


def log_in(email: str, password: str) -> str:
    """ test login with valid credentials """
    payload = {'email': email, 'password': password}
    response = requests.post('http://localhost:5000/sessions', data=payload)
    expected_json = {"email": email, "message": "logged in"}
    msg = json.dumps(expected_json, separators=(",", ":"))
    assert response.status_code == 200
    assert response.text.strip() == msg
    return response.headers.get('Set-Cookie'
                                ).split(';', 1)[0][len('session_id='):]


def profile_unlogged() -> None:
    """ test profile unlogged user"""
    headers = {'Cookie': f'session_id=zzzz'}
    response = requests.get('http://localhost:5000/profile', headers=headers)
    assert response.status_code == 403
    return None


def profile_logged(session_id: str) -> None:
    """ user logged whe have token session """
    headers = {'Cookie': f'session_id={session_id}'}
    response = requests.get('http://localhost:5000/profile', headers=headers)
    assert response.status_code == 200
    expected_json = {"email": EMAIL}
    msg = json.dumps(expected_json, separators=(",", ":"))
    assert response.text.strip() == msg
    return None


def log_out(session_id: str) -> None:
    """ test logout """
    headers = {'Cookie': f'session_id={session_id}'}
    response = requests.delete('http://localhost:5000/sessions',
                               headers=headers)
    assert response.status_code == 200
    expected_json = {"message": "Bienvenue"}
    msg = json.dumps(expected_json, separators=(",", ":"))
    assert response.text.strip() == msg
    return None


def reset_password_token(email: str) -> str:
    """test reset password api """
    payload = {'email': email}
    response = requests.post('http://localhost:5000/reset_password',
                             data=payload)
    assert response.status_code == 200
    _dict = json.loads(response.text.strip())
    assert _dict.get('email') == email and _dict.get('reset_token') is not None
    return _dict.get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ test update method"""
    payload = {'email': email, 'reset_token': reset_token,
               'new_password': new_password}
    response = requests.put('http://localhost:5000/reset_password',
                            data=payload)
    assert response.status_code == 200
    expected_json = {"email": email, "message": "Password updated"}
    msg = json.dumps(expected_json, separators=(",", ":"))
    assert response.status_code == 200
    assert response.text.strip() == msg
    return None


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
