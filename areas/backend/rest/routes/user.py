"""The Endpoints to manage the TEST_REQUESTS"""
from flask import jsonify, Blueprint, request

from controller.data_store_controller import *

USER_REQUEST_API = Blueprint('request_user_api', __name__)

dataStoreController = DataStoreController()


def get_blueprint():
    """Return the blueprint for the main app module"""
    return USER_REQUEST_API


REQUEST = {
    'id': 6
}


@USER_REQUEST_API.route('/user')
def default():
    return jsonify({"msg": "Hello, stranger"}), 200


@USER_REQUEST_API.route('/user/hello')
def hello():
    return jsonify({"msg": "Hello, world"}), 200


@USER_REQUEST_API.route('/search', methods=['GET'])
def get_request():
    user_mail = "test_mail@mail.com"  # TODO NEED REAL USER MAIL FORM AUTH
    query = request.args.get('query', default=".", type=str)
    items: list[tuple[BaseStorageItem, str]] = dataStoreController.search_in_cloud(user_mail, query)
    items_name = [file.name for (file, path) in items]
    return jsonify({"items": items_name}), 200
