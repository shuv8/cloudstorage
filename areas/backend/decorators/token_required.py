from functools import wraps
from flask import jsonify, request
from jwt import InvalidTokenError
from controller.user_controller import UserController
import app_state


userController = UserController(app_state.state)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.cookies.get('token')
            if token is None:
                return jsonify({'error': 'unauthorised'}), 401
            userController.authentication(token)
            return f(*args, **kwargs)
        except InvalidTokenError:
            return jsonify({'error': 'invalid token'}), 403

    return decorated


def get_user_by_token():
    token = request.cookies.get('token')
    return userController.authentication(token)
