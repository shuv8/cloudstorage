"""The Endpoints to manage the ADMIN_REQUESTS"""
from flask import Blueprint

from controller.data_store_controller import *

ADMIN_REQUEST_API = Blueprint('request_admin_api', __name__)

dataStoreController = DataStoreController()


def get_blueprint():
    """Return the blueprint for the main app module"""
    return ADMIN_REQUEST_API
