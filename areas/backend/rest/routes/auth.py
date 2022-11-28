from flask import Blueprint, jsonify, request

from controller.data_store_controller import DataStoreController
from controller.user_controller import UserController
from core.user import User
from exceptions.exceptions import AlreadyExistsError, InvalidCredentialsError
import app_state

dataStoreController = DataStoreController(app_state.state)
userController = UserController(app_state.state)

AUTH_REQUEST_API = Blueprint('request_auth_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return AUTH_REQUEST_API


@AUTH_REQUEST_API.route('/registration', methods=['POST'])
def registration():
    request_data = request.get_json()
    try:
        new_user = User(
            email=request_data['email'],
            password=request_data['password'],
            role=request_data['role'],
            username=request_data['username']
        )
    except KeyError:
        return jsonify({'error': 'invalid request body'}), 400

    try:
        userController.registration(new_user)
    except AlreadyExistsError:
        return jsonify({'error': 'email already exist'}), 403
    return jsonify({}), 200


@AUTH_REQUEST_API.route('/login', methods=['PUT'])
def login():
    request_data = request.get_json()
    try:
        email = request_data['email']
        password = request_data['password']
    except KeyError:
        return jsonify({'error': 'invalid request body'}), 400
    try:
        token = userController.login(email, password)
    except InvalidCredentialsError:
        return jsonify({'error': 'invalid email or password'}), 403
    return jsonify({'data': token}), 200
