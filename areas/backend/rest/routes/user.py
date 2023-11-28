"""The Endpoints to manage the USER_REQUESTS"""
import uuid
from typing import Optional

from flask import jsonify, Blueprint, make_response, request, send_file

from areas.backend.controller.data_store_controller import DataStoreController, AccessEditTypeEnum, AccessClassEnum
from areas.backend.controller.user_controller import UserController
from areas.backend.core.accesses import BaseAccess, UrlAccess, UserAccess, DepartmentAccess
from areas.backend.core.document import Document
from areas.backend.core.role import Role
from areas.backend.core.workspace import WorkSpace
from areas.backend.decorators.token_required import token_required, get_user_by_token
from areas.backend.exceptions.exceptions import AlreadyExistsError, InvalidCredentialsError, ItemNotFoundError, \
    NotAllowedError, UserNotFoundError, DepartmentNotFoundError, AccessError, SpaceNotFoundError

USER_REQUEST_API = Blueprint('request_user_api', __name__)

dataStoreController = DataStoreController()
userController = UserController()


def get_blueprint():
    """Return the blueprint for the main app module"""
    return USER_REQUEST_API


# TODO REFACTOR OLD
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


# TODO REFACTOR OLD
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


# TODO REFACTOR OLD
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

    items: list[tuple[Document, str]] = dataStoreController.search_in_cloud(user.email, query)
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


"""
    ===================
    Block with Workspaces
    ===================
"""


@USER_REQUEST_API.route('/get_workspaces', methods=['GET'])
@token_required
def get_workspaces():
    """
    Query:
        - query: get all workspaces
    Result:
        {
            spaces: [{
              space
            }]
        }
    """

    # query date
    user = get_user_by_token()

    items: list[WorkSpace] = dataStoreController.get_workspaces(user.email)

    workspaces_content = []
    for item in items:
        workspaces_content.append(
            {
                "branches_num": len(item.branches),
                "title": item.title,
                "description": item.description,
                "status": item.status.value,
                "id": str(item.get_id()),
            }
        )

    return jsonify(
        {
            "workspaces": workspaces_content
        }
    ), 200


@USER_REQUEST_API.route('/get_workspace/<space_id>', methods=['GET'])
@token_required
def get_workspace_content(space_id):
    """
    Query:
        - space_id: id of space to view
    Result:
        {
            workspace: [{
              files and dirs in space
            }]
        }
    """

    # query date
    user = get_user_by_token()

    try:
        item: WorkSpace = dataStoreController.get_workspace_by_id(user.email, uuid.UUID(space_id))

        requests = []
        for request in item.requests:
            requests.append(
                {
                    "title": request.title,
                    "description": request.description,
                    "status": request.status.value,
                    "id": request.get_id(),
                }
            )

        branches = []
        for branch in item.branches:
            branches.append(
                {
                    "name": len(branch.name),
                    "id": branch.get_id(),
                }
            )

        return jsonify(
            {
                "branches_num": len(item.branches),
                "title": item.title,
                "description": item.description,
                "status": item.status.value,
                "main_branch": item.main_branch,
                "branches": branches,
                "requests": requests,
                "id": str(item.get_id()),
            }
        ), 200
    except SpaceNotFoundError:
        return jsonify("Can't find space with ID"), 404


"""
    ===================
    Block with Branches
    ===================
"""

# Delete branch

# View branch

# Create new branch from current

"""
    ===================
    Block with Request
    ===================
"""

# Add Request

# Delete Request

# View Request

# Change Request status

"""
    ===================
    Block with Files
    ===================
"""


# TODO REFACTOR OLD
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
        new_file_id = dataStoreController.add_new_file(user.email, uuid.UUID(space_id), uuid.UUID(dir_id),
                                                       new_file_name,
                                                       new_file_type, new_file_data)
    except ItemNotFoundError:
        return jsonify({'error': 'Incorrect directory'}), 404
    except AlreadyExistsError:
        # TODO: ответ должен содержать предложение о замене существующего файла
        return jsonify({'error': 'File name already exists'}), 409
    return jsonify({'id': new_file_id}), 200


# TODO REFACTOR OLD
@USER_REQUEST_API.route('/file/<file_id>/view', methods=['GET'])
@token_required
def view_file_by_id(file_id):
    """
    Path:
        - file_id: id of file to view
    Result:
        file to view
    """
    user = get_user_by_token()
    try:
        file: Optional[Document] = dataStoreController.get_file_by_id(user.email, uuid.UUID(hex=file_id))
    except FileNotFoundError:
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


# TODO !!!!!!!!!!!!!!!!!!! Вот тут всё переписать на доступы к Wortkspace !!!!!!!!!!!!!!!!!!!
# TODO ! На самый низкий слой запилить проверку доступа к чужому воркспейсу и прокидывать наверх эксепшн


# TODO REFACTOR OLD
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


# TODO REFACTOR OLD
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


# TODO REFACTOR OLD
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


# TODO REFACTOR OLD
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


# TODO REFACTOR OLD
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


# TODO REFACTOR OLD
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


# TODO REFACTOR OLD
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


# FILE CONTROL

# TODO REFACTOR OLD
# TODO space_id -> branch_id
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


# TODO REFACTOR OLD
@USER_REQUEST_API.route('/download/<item_id>', methods=['GET'])
@token_required
def download_by_item_id(item_id):
    """
    Path:
        - space_id: id of space with item
        - item_id: id of item to download
    Result:
        file
    """
    user = get_user_by_token()
    try:
        result: Document = dataStoreController.download_item(user.email, item_id)
        return send_file(result[0], download_name=result.name, as_attachment=True), 200
    except ItemNotFoundError:
        return jsonify({'error': 'Item not found'}), 404


# ????????

# TODO REFACTOR OLD
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
    user_info: tuple[list[str], uuid.UUID, uuid.UUID] = userController.get_user_info(user)

    return jsonify(
        {
            "id": user.get_id(),
            "email": user.email,
            "departments": ' '.join(user_info[0]),
            "root_space_id": str(user_info[1]),
            "root_dir_id": str(user_info[2]),
        }
    ), 200
