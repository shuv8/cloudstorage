"""The Endpoints to manage the TEST_REQUESTS"""
from flask import jsonify, Blueprint

from controller.DataStoreController import *

REQUEST_API = Blueprint('request_api', __name__)

dataStoreController = DataStoreController()


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


REQUEST = {
    'id': 6
}


@REQUEST_API.route('/hello')
def hello():
    return 'Hello, World 2!'


@REQUEST_API.route('/request', methods=['GET'])
def get_request():
    return jsonify({"id": dataStoreController.get_test_id()}), 200
