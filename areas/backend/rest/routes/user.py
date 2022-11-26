"""The Endpoints to manage the USER_REQUESTS"""
from flask import jsonify, Blueprint, request

from controller.data_store_controller import *

USER_REQUEST_API = Blueprint('request_user_api', __name__)

dataStoreController = DataStoreController()


def get_blueprint():
    """Return the blueprint for the main app module"""
    return USER_REQUEST_API


@USER_REQUEST_API.route('/search', methods=['GET'])
def get_request():
    """
    Query:
        - query: file/dir name tosearch for
        - user_mail
    Result:
        {
            items: [{
              name: string,
              path: string,
              type: string
            }]
        }
    """

    # query date
    user_mail = "test_mail@mail.com"  # TODO NEED REAL USER MAIL FORM AUTH
    query = request.args.get('query', default=".", type=str)

    items: list[tuple[BaseStorageItem, str]] = dataStoreController.search_in_cloud(user_mail, query)
    items_content = []
    for (item, path) in items:
        items_content.append(
            {
                "name": item.name,
                "path": path
            }
        )

    return jsonify(
        {
            "items": items_content
        }
    ), 200
