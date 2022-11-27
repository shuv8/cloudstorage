"""The Endpoints to manage the USER_REQUESTS"""
from flask import jsonify, Blueprint, request

from controller.data_store_controller import *
from core.accesses import BaseAccess, UrlAccess, UserAccess, DepartmentAccess

USER_REQUEST_API = Blueprint('request_user_api', __name__)

dataStoreController = DataStoreController()


def get_blueprint():
    """Return the blueprint for the main app module"""
    return USER_REQUEST_API


@USER_REQUEST_API.route('/search', methods=['GET'])
def search_for():
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
                "path": path,
                "type": str(type(item)),
            }
        )

    return jsonify(
        {
            "items": items_content
        }
    ), 200


"""
    ===================
    Block with Accesses
    ===================
"""


# TODO Add validation after auth


@USER_REQUEST_API.route('/accesses/<item_id>', methods=['GET'])
def get_accesses(item_id):
    """
    Path:
        - item_id: id of item to change access
    Result:
        url
    """

    try:
        accesses: Optional[list[BaseAccess]] = dataStoreController.get_accesses(item_id) or list()

        accesses_content = []
        for access in accesses:

            content = "undefined"

            if type(access) == UrlAccess:
                content = access.get_url()
            elif type(access) == UserAccess:
                content = access.get_email()
            elif type(access) == DepartmentAccess:
                content = access.get_department_name()

            accesses_content.append(
                {
                    "level": access.access_type.name,
                    "class": str(type(access)),
                    "type": access.access_type.name,
                    "content": content
                }
            )

        return jsonify(
            {
                "accesses": accesses_content
            }
        ), 200

    except NotAllowedError:
        return jsonify({'error': 'Not allowed to do this action'}), 401


@USER_REQUEST_API.route('/set_access/<item_id>', methods=['PUT'])
def add_access_by_url(item_id):
    """
    Path:
        - item_id: id of item to change access
    Result:
        url
    """

    view_only = request.args.get('view_only', default=".", type=bool)

    try:
        dataStoreController.edit_access(item_id, AccessEditTypeEnum.Add, AccessClassEnum.Url, view_only)
        return jsonify({}), 200

    except NotAllowedError:
        return jsonify({'error': 'Not allowed to do this action'}), 401


@USER_REQUEST_API.route('/reset_access/<item_id>', methods=['PUT'])
def remove_access_by_url(item_id):
    """
    Path:
        - item_id: id of item to change access
    Result:
        url
    """

    try:
        dataStoreController.edit_access(item_id, AccessEditTypeEnum.Remove, AccessClassEnum.Url)
        return jsonify({}), 200

    except NotAllowedError:
        return jsonify({'error': 'Not allowed to do this action'}), 401


@USER_REQUEST_API.route('/add_access/<item_id>/email/<email>', methods=['PUT'])
def add_access_by_user(item_id, email):
    """
    Path:
        - item_id: id of item to change access
    Result:
        url
    """
    view_only = request.args.get('view_only', default=".", type=bool)

    try:
        dataStoreController.edit_access(
            item_id,
            AccessEditTypeEnum.Add,
            AccessClassEnum.UserEmail,
            view_only,
            email
        )
        return jsonify({}), 200

    except NotAllowedError:
        return jsonify({'error': 'Not allowed to do this action'}), 401


@USER_REQUEST_API.route('/remove_access/<item_id>/email/<email>', methods=['PUT'])
def remove_access_by_user(item_id, email):
    """
    Path:
        - item_id: id of item to change access
    Result:
        url
    """

    try:
        dataStoreController.edit_access(item_id, AccessEditTypeEnum.Remove, AccessClassEnum.UserEmail, name=email)
        return jsonify({}), 200

    except NotAllowedError:
        return jsonify({'error': 'Not allowed to do this action'}), 401


@USER_REQUEST_API.route('/add_access/<item_id>/department/<department>', methods=['PUT'])
def add_access_by_department(item_id, department):
    """
    Path:
        - item_id: id of item to change access
    Result:
        url
    """
    view_only = request.args.get('view_only', default=".", type=bool)

    try:
        dataStoreController.edit_access(
            item_id,
            AccessEditTypeEnum.Add,
            AccessClassEnum.Department,
            view_only,
            department
        )
        return jsonify({}), 200

    except NotAllowedError:
        return jsonify({'error': 'Not allowed to do this action'}), 401


@USER_REQUEST_API.route('/remove_access/<item_id>/department/<department>', methods=['PUT'])
def remove_access_by_department(item_id, department):
    """
    Path:
        - item_id: id of item to change access
    Result:
        url
    """

    try:
        dataStoreController.edit_access(
            item_id,
            AccessEditTypeEnum.Remove,
            AccessClassEnum.Department,
            name=department
        )
        return jsonify({}), 200

    except NotAllowedError:
        return jsonify({'error': 'Not allowed to do this action'}), 401
