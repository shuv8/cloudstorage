"""The Endpoints to manage the USER_REQUESTS"""
import uuid

from controller.user_controller import UserController
from flask import jsonify, Blueprint, make_response, request, send_file

from controller.data_store_controller import *
from core.accesses import BaseAccess, UrlAccess, UserAccess, DepartmentAccess
from core.department import Department
from core.directory import Directory
from core.files import File
from core.role import Role
from core.user_cloud_space import SpaceType
from decorators.token_required import token_required, get_user_by_token
from exceptions.exceptions import AlreadyExistsError, InvalidCredentialsError, ItemNotFoundError, UserNotFoundError, \
    DepartmentNotFoundError, SpaceNotFoundError, AccessError

USER_REQUEST_API = Blueprint('request_user_api', __name__)

dataStoreController = DataStoreController()
userController = UserController()


def get_blueprint():
    """Return the blueprint for the main app module"""
    return USER_REQUEST_API


@USER_REQUEST_API.route('/registration', methods=['POST'])
def registration():
    request_data = request.get_json()
    try:
        email = request_data['email']
        password = request_data['password']
        role = Role.get_enum_from_value(request_data['role'])
        username = request_data['username']
    except KeyError:
        return jsonify({'error': 'Invalid request body'}), 400
    try:
        userController.registration(email, password, role, username)
    except AlreadyExistsError:
        return jsonify({'error': 'Email already exists'}), 403
    return jsonify({}), 200


@USER_REQUEST_API.route('/login', methods=['PUT'])
def login():
    request_data = request.get_json()
    try:
        email = request_data['email']
        password = request_data['password']
    except KeyError:
        return jsonify({'error': 'Invalid request body'}), 400
    try:
        token = userController.login(email, password)
        response = make_response()
        response.set_cookie('token', token)
        return response
    except InvalidCredentialsError:
        return jsonify({'error': 'Invalid email or password'}), 403


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
    user = get_user_by_token()
    query = request.args.get('query', default=".", type=str)

    items: list[tuple[BaseStorageItem, str]] = dataStoreController.search_in_cloud(user.email, query)
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
    user = get_user_by_token()

    items: list[UserCloudSpace] = dataStoreController.get_spaces(user.email)

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
    user = get_user_by_token()

    try:
        items: list[BaseStorageItem] = dataStoreController.get_space_content(user.email, UUID(space_id))

        items_content = []
        for item in items:
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
    except SpaceNotFoundError:
        return jsonify("Can't find space with ID"), 404


@USER_REQUEST_API.route('/directory', methods=['POST'])
@token_required
def add_new_directory():
    request_data = request.get_json()
    try:
        space_id = request_data['space_id']
        parent_id = request_data['parent_id']
        new_directory_name = request_data['new_directory_name']
    except KeyError:
        return jsonify({'error': 'Invalid request body'}), 400
    try:
        user = get_user_by_token()
        directory_id = dataStoreController.add_new_directory(
            user_email=user.get_email(),
            space_id=UUID(space_id),
            parent_id=UUID(parent_id),
            new_directory_name=new_directory_name
        )
    except AlreadyExistsError:
        return jsonify({'error': 'directory name already exist'}), 403
    return jsonify({'id': directory_id}), 200


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
    user = get_user_by_token()

    try:
        items: list[BaseStorageItem] = dataStoreController.get_dir_content(user.email, UUID(space_id), UUID(dir_id))

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
        return jsonify("Can't find directory with ID"), 404
    except SpaceNotFoundError:
        return jsonify("Can't find space with ID"), 404


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
        return jsonify({'error': 'Invalid request body'}), 400
    try:
        user = get_user_by_token()
        new_file_id = dataStoreController.add_new_file(user.email, UUID(space_id), UUID(dir_id), new_file_name,
                                                       new_file_type, new_file_data)
    except ItemNotFoundError:
        return jsonify({'error': 'Incorrect directory'}), 404
    except AlreadyExistsError:
        # TODO: ответ должен содержать предложение о замене существующего файла
        return jsonify({'error': 'File name already exists'}), 409
    return jsonify({'id': new_file_id}), 200


@USER_REQUEST_API.route('/file/<space_id>/<file_id>/view', methods=['GET'])
@token_required
def view_file_by_id(space_id, file_id):
    """
    Path:
        - file_id: id of file to view
    Result:
        file to view
    """
    user = get_user_by_token()
    file: Optional[File] = dataStoreController.get_item_by_id(user.email, UUID(hex=space_id), UUID(hex=file_id))
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
    if file.type not in allowed_file_type_to_view:
        return jsonify({'error': 'Cannot view such type of file'}), 403
    try:
        binary_file = dataStoreController.get_binary_file_from_cloud_by_id(file.id, file.type)
        return send_file(binary_file, mimetype_dict[file.type])
    except FileNotFoundError:
        return jsonify({'error': 'File is damaged'}), 404


"""
    ===================
    Block with Accesses
    ===================
"""


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
                    "class": access.__class__.__name__,
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

    view_only = request.args.get('view_only', default="true")
    if view_only == "true":
        view_only_bool: bool = True
    else:
        view_only_bool: bool = False

    try:
        result = dataStoreController.edit_access(
            item_id, AccessEditTypeEnum.Add, AccessClassEnum.Url, view_only_bool)
        return jsonify({"status": result}), 200

    except NotAllowedError:
        return jsonify({'error': 'Not allowed to do this action'}), 401


@USER_REQUEST_API.route('/reset_access/<item_id>', methods=['DELETE'])
@token_required
def reset_access_by_url(item_id):
    """
    Path:
        - item_id: id of item to change access
    Result:
        url
    """

    try:
        result = dataStoreController.edit_access(
            item_id, AccessEditTypeEnum.Remove, AccessClassEnum.Url)
        return jsonify({"status": result}), 200

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

    view_only = request.args.get('view_only', default="true")
    if view_only == "true":
        view_only_bool: bool = True
    else:
        view_only_bool: bool = False

    try:
        result = dataStoreController.edit_access(
            item_id,
            AccessEditTypeEnum.Add,
            AccessClassEnum.UserEmail,
            view_only_bool,
            email
        )
        return jsonify({"status": result}), 200

    except NotAllowedError:
        return jsonify({'error': 'Not allowed to do this action'}), 401
    except UserNotFoundError:
        return jsonify({'error': 'User not found'}), 404


@USER_REQUEST_API.route('/remove_access/<item_id>/email/<email>', methods=['DELETE'])
@token_required
def remove_access_by_user(item_id, email):
    """
    Path:
        - item_id: id of item to change access
    Result:
        url
    """

    try:
        result = dataStoreController.edit_access(item_id, AccessEditTypeEnum.Remove, AccessClassEnum.UserEmail,
                                                 name=email)
        return jsonify({"status": result}), 200

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

    view_only = request.args.get('view_only', default="true")
    if view_only == "true":
        view_only_bool: bool = True
    else:
        view_only_bool: bool = False

    try:
        result = dataStoreController.edit_access(
            item_id,
            AccessEditTypeEnum.Add,
            AccessClassEnum.Department,
            view_only_bool,
            department
        )
        return jsonify({"status": result}), 200

    except NotAllowedError:
        return jsonify({'error': 'Not allowed to do this action'}), 401
    except DepartmentNotFoundError:
        return jsonify({'error': 'Department not found'}), 404


@USER_REQUEST_API.route('/remove_access/<item_id>/department/<department>', methods=['DELETE'])
@token_required
def remove_access_by_department(item_id, department):
    """
    Path:
        - item_id: id of item to change access
    Result:
        url
    """

    try:
        result = dataStoreController.edit_access(
            item_id,
            AccessEditTypeEnum.Remove,
            AccessClassEnum.Department,
            name=department
        )
        return jsonify({"status": result}), 200

    except NotAllowedError:
        return jsonify({'error': 'Not allowed to do this action'}), 401


@USER_REQUEST_API.route('/rename/<space_id>/<item_id>', methods=['PUT'])
@token_required
def rename_item(space_id, item_id):
    """
    Path:
        - space_id: id of space with item
        - item_id: id of item to rename
    """

    new_name = request.args.get('new_name', type=str)

    try:
        if new_name is not None:
            user = get_user_by_token()
            result = dataStoreController.rename_item(user.email, space_id, item_id, new_name)
            if result is not None:
                return jsonify({'new_name': result}), 200
            else:
                return jsonify({'error': 'Can\'t find item'}), 404
        else:
            return jsonify({'error': 'No new name presented. Use query parameter \'new_name\''}), 400
    except AccessError:
        return jsonify({'error': 'Not allowed to do this action'}), 401


@USER_REQUEST_API.route('/move/<space_id>/<item_id>', methods=['PUT'])
@token_required
def move_item(space_id, item_id):
    """
    Path:
        - item_id: id of item to move
        - target_directory: new target directory of item
    """

    user = get_user_by_token()
    target_space = request.args.get('target_space', type=str)
    target_directory = request.args.get('target_directory', type=str)
    try:
        if target_directory is not None and target_space is not None:
            result = dataStoreController.move_item(user.email, space_id, item_id,
                                                   uuid.UUID(hex=target_space), uuid.UUID(hex=target_directory))
            if result is not None:
                return jsonify({'new_directory': result}), 200
            else:
                return jsonify({'error': 'Can\'t find one of items'}), 404
        else:
            return jsonify({'error': 'No target directory presented. Use query parameter \'target_directory\''}), 400
    except AccessError:
        return jsonify({'error': 'Not allowed to do this action'}), 401
    except ItemNotFoundError:
        return jsonify({'error': 'Item not found'}), 404


@USER_REQUEST_API.route('/download/<space_id>/<item_id>', methods=['GET'])
@token_required
def download_by_item_id(space_id, item_id):
    """
    Path:
        - space_id: id of space with item
        - item_id: id of item to download
    Result:
        file
    """
    user = get_user_by_token()
    result = dataStoreController.download_item(user.email, space_id, item_id)
    if result[0] is not None:
        if isinstance(result[1], File):
            file_name = result[1].name + result[1].type
            return send_file(result[0], download_name=file_name, as_attachment=True), 200
        elif isinstance(result[1], Directory):
            file_name = result[1].name
            return send_file(result[0], download_name=file_name, as_attachment=True), 200
    else:
        return jsonify({'error': 'No such file or directory'}), 404


@USER_REQUEST_API.route('/delete/<space_id>/<item_id>', methods=['DELETE'])
@token_required
def delete_by_item_id(space_id, item_id):
    """
    Path:
        - item_id: id of item to delete
    Result:
        bool status of deleting
    """

    user = get_user_by_token()
    try:
        result = dataStoreController.delete_item(user.email, uuid.UUID(hex=space_id), uuid.UUID(hex=item_id))
        if result:
            return jsonify({'delete': 'success'}), 200
    except AccessError:
        return jsonify({'error': 'Not allowed to do this action'}), 401
    except ItemNotFoundError:
        return jsonify({'error': 'Item not found'}), 404


@USER_REQUEST_API.route('/copy/<space_id>/<item_id>', methods=['POST'])
@token_required
def copy_item(space_id, item_id):
    """
    Path:
        - item_id: id of item to move
        - target_directory: new target directory of item
    """

    user = get_user_by_token()
    target_space = request.args.get('target_space', type=str)
    target_directory = request.args.get('target_directory', type=str)
    try:
        if target_directory is not None and target_space is not None:
            result = dataStoreController.copy_item(
                user.email,
                uuid.UUID(hex=space_id),
                uuid.UUID(hex=item_id),
                uuid.UUID(hex=target_space),
                uuid.UUID(hex=target_directory)
            )
            return jsonify({'new_directory': result}), 200
        else:
            return jsonify({'error': 'No target directory presented. Use query parameter \'target_directory\''}), 400
    except AccessError:
        return jsonify({'error': 'Not allowed to do this action'}), 401
    except ItemNotFoundError:
        return jsonify({'error': 'Item not found'}), 404


@USER_REQUEST_API.route('/whoiam', methods=['GET'])
@token_required
def get_user_list():
    """
    Result:
        {
            id: string
            email: string
            departments: string
            space_id: string
            root_dir_id: string
        }
    """

    user = get_user_by_token()
    user_info: tuple[list[str], UUID, UUID] = userController.get_user_info(user)

    return jsonify(
        {
            "id": user.get_id(),
            "email": user.email,
            "departments": ' '.join(user_info[0]),
            "root_space_id": str(user_info[1]),
            "root_dir_id": str(user_info[2]),
        }
    ), 200
