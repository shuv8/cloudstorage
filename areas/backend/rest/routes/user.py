"""The Endpoints to manage the USER_REQUESTS"""
import uuid

from controller.user_controller import UserController
from flask import jsonify, Blueprint, make_response, request, send_file
from io import BytesIO

from controller.data_store_controller import *
from core.accesses import BaseAccess, UrlAccess, UserAccess, DepartmentAccess
from core.directory import Directory
from core.files import File
from core.role import Role
from core.user import User
from core.user_cloud_space import SpaceType
from decorators.token_required import token_required, get_user_by_token
from exceptions.exceptions import AlreadyExistsError, InvalidCredentialsError
import app_state

USER_REQUEST_API = Blueprint('request_user_api', __name__)

dataStoreController = DataStoreController(app_state.state)
userController = UserController(app_state.state)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return USER_REQUEST_API


@USER_REQUEST_API.route('/registration', methods=['POST'])
def registration():
    request_data = request.get_json()
    try:
        new_user = User(
            email=request_data['email'],
            password=request_data['password'],
            role=Role.get_enum_from_value(request_data['role']),
            username=request_data['username']
        )
    except KeyError:
        return jsonify({'error': 'invalid request body'}), 400

    try:
        userController.registration(new_user)
    except AlreadyExistsError:
        return jsonify({'error': 'email already exist'}), 403
    return jsonify({}), 200


@USER_REQUEST_API.route('/login', methods=['PUT'])
def login():
    request_data = request.get_json()
    try:
        email = request_data['email']
        password = request_data['password']
    except KeyError:
        return jsonify({'error': 'invalid request body'}), 400
    try:
        token = userController.login(email, password)
        response = make_response()
        response.set_cookie('token', token)
        return response
    except InvalidCredentialsError:
        return jsonify({'error': 'invalid email or password'}), 403


"""
    ===================
    Block with Files
    ===================
"""


@USER_REQUEST_API.route('/search', methods=['GET'])
@token_required
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

    scope = request.args.get('scope', default="prod", type=str)
    dataStoreController.set_scope(ScopeTypeEnum.get_class_by_str(scope))

    items: list[tuple[BaseStorageItem, str]] = dataStoreController.search_in_cloud(user_mail, query)
    items_content = []
    for (item, path) in items:
        items_content.append(
            {
                "name": item.name,
                "path": path,
                "type": item.__class__.__name__,
                "id": str(item.id)
            }
        )

    return jsonify(
        {
            "items": items_content
        }
    ), 200


@USER_REQUEST_API.route('/get_spaces', methods=['GET'])
@token_required
def get_spaces():
    """
    Query:
        - query: get all spaces
    Result:
        {
            spaces: [{
              space
            }]
        }
    """

    # query date
    user_mail = "test_mail@mail.com"  # TODO NEED REAL USER MAIL FORM AUTH

    scope = request.args.get('scope', default="prod", type=str)
    dataStoreController.set_scope(ScopeTypeEnum.get_class_by_str(scope))

    items: list[UserCloudSpace] = dataStoreController.get_spaces(user_mail)

    spaces_content = []
    for item in items:

        space_name = "Main"
        if item.get_space_type() == SpaceType.Shared:
            space_name = item.get_directory_manager().items[0].name  # We have only 1 root folder in shared space

        spaces_content.append(
            {
                "type": str(item.get_space_type().name),
                "name": space_name,
                "id": str(item.get_id()),
            }
        )

    return jsonify(
        {
            "spaces": spaces_content
        }
    ), 200


@USER_REQUEST_API.route('/get_space/<space_id>', methods=['GET'])
@token_required
def get_space_content(space_id):
    """
    Query:
        - space_id: id of space to view
    Result:
        {
            items: [{
              files and dirs in space
            }]
        }
    """

    # query date
    user_mail = "test_mail@mail.com"  # TODO NEED REAL USER MAIL FORM AUTH

    scope = request.args.get('scope', default="prod", type=str)
    dataStoreController.set_scope(ScopeTypeEnum.get_class_by_str(scope))

    try:
        items: list[BaseStorageItem] = dataStoreController.get_space_content(user_mail, UUID(space_id))

        items_content = []
        for item in items:
            if type(item) == File:
                items_content.append(
                    {
                        "id": str(item.get_id()),
                        "name": item.name,
                        "type": item.type,
                        "entity": item.__class__.__name__,
                    }
                )
            if type(item) == Directory:
                items_content.append(
                    {
                        "id": str(item.get_id()),
                        "name": item.name,
                        "type": "",
                        "entity": item.__class__.__name__,
                    }
                )

        return jsonify(
            {
                "items": items_content
            }
        ), 200
    except ItemNotFoundError:
        return jsonify("Can't find space with that ID"), 404


@USER_REQUEST_API.route('/get_dir/<space_id>/<dir_id>', methods=['GET'])
@token_required
def get_dir_in_space_content(space_id, dir_id):
    """
    Query:
        - space_id: id of space to search in
        - dir_id: id of dir to view
    Result:
        {
            items: [{
              files and dirs in dir
            }]
        }
    """

    # query date
    user_mail = "test_mail@mail.com"  # TODO NEED REAL USER MAIL FORM AUTH

    scope = request.args.get('scope', default="prod", type=str)
    dataStoreController.set_scope(ScopeTypeEnum.get_class_by_str(scope))

    try:
        items: list[BaseStorageItem] = dataStoreController.get_dir_content(user_mail, UUID(space_id), UUID(dir_id))

        items_content = []
        for item in items:
            if type(item) == File:
                items_content.append(
                    {
                        "id": str(item.get_id()),
                        "name": item.name,
                        "type": item.type,
                        "entity": item.__class__.__name__,
                    }
                )
            if type(item) == Directory:
                items_content.append(
                    {
                        "id": str(item.get_id()),
                        "name": item.name,
                        "entity": item.__class__.__name__,
                    }
                )

        return jsonify(
            {
                "items": items_content
            }
        ), 200
    except ItemNotFoundError:
        return jsonify("Can't find space with that ID"), 404


@USER_REQUEST_API.route('/file', methods=['POST'])
def add_new_file():
    request_data = request.get_json()
    try:
        space_id = request_data['space_id']
        dir_id = request_data['dir_id']
        new_file_name = request_data['new_file_name']
        new_file_type = request_data['new_file_type']
        new_file_data = request_data['new_file_data']
    except KeyError:
        return jsonify({'error': 'invalid request body'}), 400
    try:
        user_email = "test_mail@mail.com"
        new_file_id = dataStoreController.add_new_file(user_email, UUID(space_id), UUID(dir_id), new_file_name, new_file_type, new_file_data)
    except ItemNotFoundError:
        return jsonify({'error': 'incorrect directory'}), 404
    except AlreadyExistsError:
        # TODO: ответ должен содержать предложение о замене существующего файла
        return jsonify({'error': 'file name alreay exists'}), 409
    return jsonify({'id': new_file_id}), 200
    

@USER_REQUEST_API.route('/file/<file_id>/view', methods=['GET'])
@token_required
def view_file_by_id(file_id):
    """
    Path:
        - file_id: id of file to view
    Result:
        file to view
    """
    scope = request.args.get('scope', default="prod", type=str)
    dataStoreController.set_scope(ScopeTypeEnum.get_class_by_str(scope))
    user = get_user_by_token()
    user_mail = "test_mail@mail.com"  # TODO NEED REAL USER MAIL FORM AUTH
    file: Optional[File] = dataStoreController.get_item_by_id(
        user_mail, UUID(hex=file_id))
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
        if file.name + file.type == 'test2.txt':
            buf = BytesIO(b"TestText")
            return send_file(buf, mimetype_dict[file.type])
        with open(f'./database/{file.name}{file.type}', 'rb') as file_buffer:
            buf = BytesIO(file_buffer.read())
            return send_file(buf, mimetype_dict[file.type])
    except FileNotFoundError as ex:
        return jsonify({'error': 'File is damaged'}), 404


"""
    ===================
    Block with Accesses
    ===================
"""


# TODO Add validation after auth


@USER_REQUEST_API.route('/accesses/<item_id>', methods=['GET'])
@token_required
def get_accesses(item_id):
    """
    Path:
        - item_id: id of item to change access
    Result:
        url
    """
    try:
        scope = request.args.get('scope', default="prod", type=str)
        dataStoreController.set_scope(ScopeTypeEnum.get_class_by_str(scope))

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
@token_required
def set_access_by_url(item_id):
    """
    Path:
        - item_id: id of item to change access
    Result:
        url
    """

    scope = request.args.get('scope', default="prod", type=str)
    dataStoreController.set_scope(ScopeTypeEnum.get_class_by_str(scope))

    view_only = request.args.get('view_only', default="true")
    if view_only == "true":
        view_only_bool: bool = True
    else:
        view_only_bool: bool = False

    try:
        dataStoreController.edit_access(
            item_id, AccessEditTypeEnum.Add, AccessClassEnum.Url, view_only_bool)
        return jsonify({}), 200

    except NotAllowedError:
        return jsonify({'error': 'Not allowed to do this action'}), 401
    except AlreadyExistsError:
        return jsonify({'error': 'email already exist'}), 403


@USER_REQUEST_API.route('/reset_access/<item_id>', methods=['DELETE'])
@token_required
def reset_access_by_url(item_id):
    """
    Path:
        - item_id: id of item to change access
    Result:
        url
    """

    scope = request.args.get('scope', default="prod", type=str)
    dataStoreController.set_scope(ScopeTypeEnum.get_class_by_str(scope))

    try:
        dataStoreController.edit_access(
            item_id, AccessEditTypeEnum.Remove, AccessClassEnum.Url)
        return jsonify({}), 200

    except NotAllowedError:
        return jsonify({'error': 'Not allowed to do this action'}), 401


@USER_REQUEST_API.route('/add_access/<item_id>/email/<email>', methods=['PUT'])
@token_required
def add_access_by_user(item_id, email):
    """
    Path:
        - item_id: id of item to change access
    Result:
        url
    """

    scope = request.args.get('scope', default="prod", type=str)
    dataStoreController.set_scope(ScopeTypeEnum.get_class_by_str(scope))

    view_only = request.args.get('view_only', default="true")
    if view_only == "true":
        view_only_bool: bool = True
    else:
        view_only_bool: bool = False

    try:
        dataStoreController.edit_access(
            item_id,
            AccessEditTypeEnum.Add,
            AccessClassEnum.UserEmail,
            view_only_bool,
            email
        )
        return jsonify({}), 200

    except NotAllowedError:
        return jsonify({'error': 'Not allowed to do this action'}), 401


@USER_REQUEST_API.route('/remove_access/<item_id>/email/<email>', methods=['DELETE'])
@token_required
def remove_access_by_user(item_id, email):
    """
    Path:
        - item_id: id of item to change access
    Result:
        url
    """

    scope = request.args.get('scope', default="prod", type=str)
    dataStoreController.set_scope(ScopeTypeEnum.get_class_by_str(scope))

    try:
        dataStoreController.edit_access(item_id, AccessEditTypeEnum.Remove, AccessClassEnum.UserEmail, name=email)
        return jsonify({}), 200

    except NotAllowedError:
        return jsonify({'error': 'Not allowed to do this action'}), 401


@USER_REQUEST_API.route('/add_access/<item_id>/department/<department>', methods=['PUT'])
@token_required
def add_access_by_department(item_id, department):
    """
    Path:
        - item_id: id of item to change access
    Result:
        url
    """

    scope = request.args.get('scope', default="prod", type=str)
    dataStoreController.set_scope(ScopeTypeEnum.get_class_by_str(scope))

    view_only = request.args.get('view_only', default="true")
    if view_only == "true":
        view_only_bool: bool = True
    else:
        view_only_bool: bool = False

    try:
        dataStoreController.edit_access(
            item_id,
            AccessEditTypeEnum.Add,
            AccessClassEnum.Department,
            view_only_bool,
            department
        )
        return jsonify({}), 200

    except NotAllowedError:
        return jsonify({'error': 'Not allowed to do this action'}), 401


@USER_REQUEST_API.route('/remove_access/<item_id>/department/<department>', methods=['DELETE'])
@token_required
def remove_access_by_department(item_id, department):
    """
    Path:
        - item_id: id of item to change access
    Result:
        url
    """

    scope = request.args.get('scope', default="prod", type=str)
    dataStoreController.set_scope(ScopeTypeEnum.get_class_by_str(scope))

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


@USER_REQUEST_API.route('/rename/<item_id>', methods=['PUT'])
@token_required
def rename_item(item_id):
    """
    Path:
        - item_id: id of item to rename
    """

    scope = request.args.get('scope', default="prod", type=str)
    dataStoreController.set_scope(ScopeTypeEnum.get_class_by_str(scope))

    new_name = request.args.get('new_name', type=str)
    if new_name is not None:
        user = get_user_by_token()
        result = dataStoreController.rename_item(user.email, item_id, new_name)
        if result is not None:
            return jsonify({'new_name': result}), 200
        else:
            return jsonify({'error': 'Can\'t find item'}), 404
    else:
        return jsonify({'error': 'No new name presented. Use query parameter \'new_name\''}), 400


@USER_REQUEST_API.route('/move/<item_id>', methods=['PUT'])
@token_required
def move_item(item_id):
    """
    Path:
        - item_id: id of item to move
        - target_directory: new target directory of item
    """

    scope = request.args.get('scope', default="prod", type=str)
    dataStoreController.set_scope(ScopeTypeEnum.get_class_by_str(scope))
    target_directory = request.args.get('target_directory', type=str)
    if target_directory is not None:
        result = dataStoreController.move_item('test@mail.ru', item_id, uuid.UUID(hex=target_directory))
        if result is not None:
            return jsonify({'new_directory': result}), 200
        else:
            return jsonify({'error': 'Can\'t find one of items'}), 404
    else:
        return jsonify({'error': 'No target directory presented. Use query parameter \'target_directory\''}), 400


@USER_REQUEST_API.route('/download/<item_id>', methods=['GET'])
@token_required
def download_by_item_id(item_id):
    """
    Path:
        - item_id: id of item to download
    Result:
        file
    """
    result, file = dataStoreController.download_item(item_id)
    if result is not None:
        if isinstance(file, File):
            file_name = file.name + file.type
            return send_file(result, download_name=file_name, as_attachment=True), 200
        elif isinstance(file, Directory):
            file_name = file.name
            return send_file(result, download_name=file_name, as_attachment=True), 200
    else:
        return jsonify({'error': 'No such file or directory'}), 404


@USER_REQUEST_API.route('/delete/<item_id>', methods=['DELETE'])
@token_required
def delete_by_item_id(item_id):
    """
    Path:
        - item_id: id of item to delete
    Result:
        bool status of deleting
    """

    scope = request.args.get('scope', default="prod", type=str)
    dataStoreController.set_scope(ScopeTypeEnum.get_class_by_str(scope))

    result = dataStoreController.delete_item(item_id)
    if result:
        return jsonify({'delete': 'success'}), 200
    else:
        return jsonify({'error': 'No such file or directory'}), 404


@USER_REQUEST_API.route('/copy/<item_id>', methods=['POST'])
@token_required
def copy_item(item_id):
    """
    Path:
        - item_id: id of item to move
        - target_directory: new target directory of item
    """

    target_directory = request.args.get('target_directory', type=str)
    if target_directory is not None:
        result = dataStoreController.copy_item('test@mail.ru', item_id, uuid.UUID(hex=target_directory))
        if result is not None:
            return jsonify({'new_directory': result}), 200
        else:
            return jsonify({'error': 'Can\'t find one of items'}), 404
    else:
        return jsonify({'error': 'No target directory presented. Use query parameter \'target_directory\''}), 400
