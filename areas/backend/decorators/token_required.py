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
            token = request.headers.get('token')
            if token is None:
                return jsonify({'error': 'unauthorised'}), 401
            user = userController.authentication(token)
            return f(user, *args, **kwargs)
        except InvalidTokenError:
            return jsonify({'error': 'invalid token'}), 403

    return decorated
