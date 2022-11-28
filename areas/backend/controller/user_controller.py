from typing import List

from flask import jsonify, request
from jwt import InvalidTokenError

from core.department import Department
from core.user import User
from service.user_service import UserService


class UserController:
    def __init__(self):
        self.user_service = UserService()

    def registration(self, new_user: User) -> None:
        self.user_service.registration(new_user)

    def login(self, email: str, password: str) -> str:
        return self.user_service.login(email, password)

    def authentication(self) -> None:
        try:
            token = request.headers.get('token')
            if token is None:
                return jsonify({'error': 'unauthorised'}), 401
            id = self.user_service.authentication(token)
            request.headers.set('id', id)
        except InvalidTokenError:
            return jsonify({'error': 'invalid token'}), 403

    def get_all_departments(self, page: int, limit: int) -> List[Department]:
        return self.user_service.get_all_departments(page, limit)

    def add_new_department(self, new_department: Department) -> None:
        self.user_service.add_new_department(new_department)

    def delete_department_by_name(self, department_name: str) -> None:
        self.user_service.delete_department_by_name(department_name)
