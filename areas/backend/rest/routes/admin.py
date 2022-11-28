"""The Endpoints to manage the ADMIN_REQUESTS"""
from flask import jsonify, Blueprint, request

from controller.data_store_controller import *
from controller.user_controller import UserController
from core.department import Department
from exceptions.exceptions import AlreadyExistsError
from core.department_manager import DepartmentNotFoundError
import app_state

ADMIN_REQUEST_API = Blueprint('request_admin_api', __name__)

dataStoreController = DataStoreController(app_state.state)
userController = UserController(app_state.state)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return ADMIN_REQUEST_API


@ADMIN_REQUEST_API.before_request
def authentication(): 
    return userController.authentication() 


@ADMIN_REQUEST_API.route('/admin_reset', methods=['GET'])
def reset_core():
    global dataStoreController
    global userController
    dataStoreController = DataStoreController(app_state.state)
    userController = UserController(app_state.state)
    print('CORE ADMIN RESET')
    return 'Core reset OK', 200


"""
    ===================
    Block with Department
    ===================
"""


@ADMIN_REQUEST_API.route('/department', methods=['GET'])
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
