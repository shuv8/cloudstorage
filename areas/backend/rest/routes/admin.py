"""The Endpoints to manage the ADMIN_REQUESTS"""
from flask import jsonify, Blueprint, request

from controller.data_store_controller import *
from controller.user_controller import UserController
from core.department import Department
from decorators.token_required import admin_access
from exceptions.exceptions import AlreadyExistsError
from core.department_manager import DepartmentNotFoundError
from core.user_manager import UserNotFoundError
import app_state

ADMIN_REQUEST_API = Blueprint('request_admin_api', __name__)

dataStoreController = DataStoreController(app_state.state)
userController = UserController(app_state.state)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return ADMIN_REQUEST_API


"""
    ===================
    Block with Department
    ===================
"""


@ADMIN_REQUEST_API.route('/department', methods=['GET'])
@admin_access
def get_department_list():
    """
    Query:
        - query: page
        - query: limit
    Result:
        {
            departments: [{
              department_name: string
            }]
        }
    """
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    departments = userController.get_all_departments(page, limit)
    items = [{"department_name": department.department_name} for department in departments]
    return jsonify(
        {
            "departments": items
        }
    ), 200


@ADMIN_REQUEST_API.route('/department', methods=['POST'])
@admin_access
def add_new_department():
    """
    Request Body:
        {
          department_name: string
        }
    Result:
        {}
    """
    request_data = request.get_json()
    try:
        new_department = Department(department_name=request_data['department_name'], users=None)
    except KeyError:
        return jsonify({'error': 'Invalid request body'}), 400

    try:
        userController.add_new_department(new_department)
    except AlreadyExistsError:
        return jsonify({'error': 'Already exists department with such name'}), 400

    return jsonify({}), 200


@ADMIN_REQUEST_API.route('/department', methods=['DELETE'])
@admin_access
def delete_department():
    """
    Request Body:
        {
          department_name: string
        }
    Result:
        {}
    """
    request_data = request.get_json()
    try:
        new_department = Department(department_name=request_data['department_name'], users=None)
    except KeyError:
        return jsonify({'error': 'Invalid request body'}), 400

    try:
        userController.delete_department_by_name(new_department.department_name)
    except DepartmentNotFoundError:
        return jsonify({'error': 'Department with such name doesnt exist'}), 404

    return jsonify({}), 200


@ADMIN_REQUEST_API.route('/department/users', methods=['GET'])
@admin_access
def get_department_with_users():
    """
    Query:
        - query: name
    Result:
        {
            users: [{
              id: string
            }],
            department_name: string
        }
    """
    name = request.args.get('name', default=None, type=str)
    try:
        department = userController.get_department_by_name(name)
    except DepartmentNotFoundError:
        return jsonify({'error': 'Department with such name doesnt exist'}), 404
    users = [{"id": user.get_id()} for user in department.users]
    return jsonify(
        {
            "department_name": department.department_name,
            "users": users
        }
    ), 200


@ADMIN_REQUEST_API.route('/department/users', methods=['POST'])
@admin_access
def add_users_to_department():
    """
    Query:
        - query: name
    Request Body:
    {
      users: [{
            id: string
            }]
    }
    Result:
        {
            users: [{
              id: string
            }],
            department_name: string
        }
    """
    name = request.args.get('name', default=None, type=str)
    request_data = request.get_json()
    try:
        users = request_data['users']
    except KeyError:
        return jsonify({'error': 'invalid request body'}), 400
    try:
        department = userController.add_users_to_department(name, users)
    except DepartmentNotFoundError:
        return jsonify({'error': 'Department with such name doesnt exist'}), 404
    except UserNotFoundError:
        return jsonify({'error': 'Such user not found'}), 404
    users = [{"id": user.get_id()} for user in department.users]
    return jsonify(
        {
            "department_name": department.department_name,
            "users": users
        }
    ), 200


@ADMIN_REQUEST_API.route('/department/users', methods=['DELETE'])
@admin_access
def delete_user_from_department():
    """
    Query:
        - query: name
    Request Body:
    {
      users: [{
            id: string
            }]
    }
    Result:
        {
            users: [{
              id: string
            }],
            department_name: string
        }
    """
    name = request.args.get('name', default=None, type=str)
    request_data = request.get_json()
    try:
        users = request_data['users']
    except KeyError:
        return jsonify({'error': 'invalid request body'}), 400
    try:
        department = userController.delete_users_from_department(name, users)
    except DepartmentNotFoundError:
        return jsonify({'error': 'Department with such name doesnt exist'}), 404
    except UserNotFoundError:
        return jsonify({'error': 'Such user not found'}), 404
    users = [{"id": user.get_id()} for user in department.users]
    return jsonify(
        {
            "department_name": department.department_name,
            "users": users
        }
    ), 200

