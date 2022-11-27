"""The Endpoints to manage the USER_REQUESTS"""
from controller.user_controller import UserController
from core.user import User
from flask import jsonify, Blueprint, request, send_file
from io import BytesIO

from controller.data_store_controller import *
from core.accesses import BaseAccess, UrlAccess, UserAccess, DepartmentAccess
from core.files import File

USER_REQUEST_API = Blueprint('request_user_api', __name__)

dataStoreController = DataStoreController()
userController = UserController()


def get_blueprint():
    """Return the blueprint for the main app module"""
    return USER_REQUEST_API


@USER_REQUEST_API.route('/registration', methods=['POST'])
def registration():
    request_data = request.get_json()

    new_user: Optional[User] = None

    try:
        new_user = User(
            email=request_data['email'],
            password=request_data['password'],
            role=request_data['role'],
            username=request_data['username']
        )
    except:
        return jsonify({'error': 'invalid request body'}), 400

    err = userController.registration(new_user)
    if err:
        return jsonify({'error': err}), 400

    return jsonify({'error': None}), 200


@USER_REQUEST_API.route('/login', methods=['PUT'])
def login():
    request_data = request.get_json()

    email: Optional[str] = None
    password: Optional[str] = None

    try:
        email = request_data['email']
        password = request_data['password']
    except:
        return jsonify({'data': None, 'error': 'invalid request body'}), 400

    token, err = userController.login(email, password)
    if err:
        return jsonify({'data': None, 'error': err}), 400

    return jsonify({'data': token, 'error': None}), 200


"""
    ===================
    Block with Files
    ===================
"""


@USER_REQUEST_API.route('/search', methods=['GET'])
def search_for():
    """
    Query:
        - query: file/dir name to search for
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

    items: list[tuple[BaseStorageItem, str]
    ] = dataStoreController.search_in_cloud(user_mail, query)
    items_content = []
    for (item, path) in items:
        items_content.append(
            {
                "name": item.name,
                "path": path,
                "type": str(type(item)),
                "id": str(item.id)
            }
        )

    return jsonify(
        {
            "items": items_content
        }
    ), 200


@USER_REQUEST_API.route('/file/<file_id>/view', methods=['GET'])
def view_file_by_id(file_id):
    """
    Path:
        - file_id: id of file to view
    Result:
        file to view
    """

    user_mail = "test_mail@mail.com"  # TODO NEED REAL USER MAIL FORM AUTH
    file: Optional[File] = dataStoreController.get_item_by_id(
        user_mail, file_id)
    if file is None:
        return jsonify({'error': 'File not found'}), 404

    allowed_file_type_to_view = ['.png', '.pdf',
                                 '.jpeg', 'jpg', '.svg', '.mp4', '.txt']
    mimetype_dict = {
        '.png': 'image/png',
        '.pdf': 'application/pdf',
        '.jpeg': 'image/jpeg',
        '.jpg': 'image/jpeg',
        '.svg': 'image/svg+xml',
        '.mp4': 'video/mp4',
        '.txt': 'text/plain'
    }
    # TODO GET FILE FROM DATABASE
    if file.type not in allowed_file_type_to_view:
        return jsonify({'error': 'Cannot view such type of file'}), 403
    try:
        with open(f'./database/{file.name}{file.type}', 'rb') as file_buffer:
            buf = BytesIO(file_buffer.read())
            return send_file(buf, mimetype_dict[file.type])
    except FileNotFoundError:
        return jsonify({'error': 'File is damaged'}), 404


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
        accesses: Optional[list[BaseAccess]] = dataStoreController.get_accesses(
            item_id) or list()

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
    except ItemNotFoundError:
        return jsonify({'error': 'No item found to modify'}), 404


@USER_REQUEST_API.route('/set_access/<item_id>', methods=['PUT'])
def set_access_by_url(item_id):
    """
    Path:
        - item_id: id of item to change access
    Result:
        url
    """

    view_only = request.args.get('view_only', default=".", type=bool)

    try:
        dataStoreController.edit_access(
            item_id, AccessEditTypeEnum.Add, AccessClassEnum.Url, view_only)
        return jsonify({}), 200

    except NotAllowedError:
        return jsonify({'error': 'Not allowed to do this action'}), 401
    except ItemNotFoundError:
        return jsonify({'error': 'No item found to modify'}), 404


@USER_REQUEST_API.route('/reset_access/<item_id>', methods=['DELETE'])
def reset_access_by_url(item_id):
    """
    Path:
        - item_id: id of item to change access
    Result:
        url
    """

    try:
        dataStoreController.edit_access(
            item_id, AccessEditTypeEnum.Remove, AccessClassEnum.Url)
        return jsonify({}), 200

    except NotAllowedError:
        return jsonify({'error': 'Not allowed to do this action'}), 401
    except ItemNotFoundError:
        return jsonify({'error': 'No item found to modify'}), 404


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
    except ItemNotFoundError:
        return jsonify({'error': 'No item found to modify'}), 404


@USER_REQUEST_API.route('/remove_access/<item_id>/email/<email>', methods=['DELETE'])
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
    except ItemNotFoundError:
        return jsonify({'error': 'No item found to modify'}), 404


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
    except ItemNotFoundError:
        return jsonify({'error': 'No item found to modify'}), 404


@USER_REQUEST_API.route('/remove_access/<item_id>/department/<department>', methods=['DELETE'])
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
    except ItemNotFoundError:
        return jsonify({'error': 'No item found to modify'}), 404


@USER_REQUEST_API.route('/rename/<item_id>', methods=['PUT'])
def rename_item(item_id):
    """
    Path:
        - item_id: id of item to rename
    """

    new_name = request.args.get('new_name', type=str)
    if new_name is not None:
        result = dataStoreController.rename_item('test@mail.ru', item_id, new_name)
        if result is not None:
            return jsonify({'new_name': result}), 200
        else:
            return jsonify({'error': 'Can\'t find item'}), 404
    else:
        return jsonify({'error': 'No new name presented. Use query parameter \'new_name\''}), 400


@USER_REQUEST_API.route('/move/<item_id>', methods=['PUT'])
def move_item(item_id):
    """
    Path:
        - item_id: id of item to move
    Body:
        - new_path: new path to item
    """

    target_directory = request.args.get('target_directory', type=str)
    if target_directory is not None:
        result = dataStoreController.move_item('test@mail.ru', item_id, target_directory)
        if result is not None:
            return jsonify({'new_directory': result}), 200
        else:
            return jsonify({'error': 'Can\'t find one of items'}), 404
    else:
        return jsonify({'error': 'No target directory presented. Use query parameter \'target_directory\''}), 400


@USER_REQUEST_API.route('/download/<item_id>', methods=['GET'])
def download_by_item_id(item_id):
    """
    Path:
        - item_id: id of item to download
    Result:
        file
    """
    result, file = dataStoreController.download_item(item_id)
    if result is not None:
        file_name = file.name + file.type
        return send_file(result, download_name=file_name, as_attachment=True), 200
    else:
        return jsonify({'error': 'No such fail or directory'}), 400


@USER_REQUEST_API.route('/delete/<item_id>', methods=['DELETE'])
def delete_by_item_id(item_id):
    """
    Path:
        - item_id: id of item to download
    Result:
        file
    """
    result = dataStoreController.delete_item(item_id)
    if result:
        return jsonify({'delete': 'success'}), 200
    else:
        return jsonify({'error': 'Wrong try to delete'}), 400


@USER_REQUEST_API.route('/copy/<item_id>', methods=['POST'])
def copy_item(item_id):
    """
    Path:
        - item_id: id of item to move
    Body:
        - new_path: new path to item
    """

    target_directory = request.args.get('target_directory', type=str)
    if target_directory is not None:
        result = dataStoreController.copy_item('test@mail.ru', item_id, target_directory)
        if result is not None:
            return jsonify({'new_directory': result}), 200
        else:
            return jsonify({'error': 'Can\'t find one of items'}), 404
    else:
        return jsonify({'error': 'No target directory presented. Use query parameter \'target_directory\''}), 400
