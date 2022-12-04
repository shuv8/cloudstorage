import sys
from typing import List
from uuid import UUID

from accessify import private

from app_state import ServerDatabase
from app_states_for_test import ScopeTypeEnum
from core.user import User
from core.department import Department

import pytest

from core.user_manager import UserNotFoundError


class UserRepository:
    def __init__(self, server_state: ServerDatabase):
        self.server_state = server_state.prod
        self.test_server_state = server_state.test
        self.scope = ScopeTypeEnum.Prod

    """
        New methods
    """

    def get_user_from_db_by_id(self, _id: UUID):
        from database.users.user_model import UserModel
        user: UserModel = UserModel.query.filter_by(id=str(_id)).first()
        return user

    def get_user_from_db_by_email(self, email: str) -> User:
        from database.users.user_model import UserModel
        user: UserModel = UserModel.query.filter_by(email=email).first()
        if user is None:
            raise UserNotFoundError
        return User(
            _id=UUID(hex=user.id),
            email=user.email,
            username=user.username,
            password=user.passwordHash,
            role=user.role
        )

    def add_new_user_to_db(self, new_user: User) -> None:
        from app_db import get_current_db
        db = get_current_db()
        from database.users.user_model import UserModel
        user: UserModel = UserModel(
            id=str(new_user.get_id()),
            email=new_user.email,
            username=new_user.username,
            passwordHash=new_user.password,
            role=new_user.role
        )

        db.session.add(user)
        db.session.commit()

    """
        Old methods
    """

    @private
    def get_db(self):
        if "pytest" in sys.modules:
            return ScopeTypeEnum.return_state_by_scope(self.scope, self.server_state, self.test_server_state)
        else:
            return self.server_state

    def set_scope(self, scope: ScopeTypeEnum):
        self.scope = scope

    def get_user(self, id: UUID) -> User:
        return self.get_db().get_user(id)

    def get_user_by_email(self, email: str) -> User:
        return self.get_db().get_user_by_email(email)

    def add_new_user(self, new_user: User) -> None:
        self.get_db().add_new_user(new_user)

    def get_departments(self) -> List[Department]:
        return self.get_db().get_department_list()

    def get_department_by_name(self, department_name) -> Department:
        return self.get_db().get_department_by_name(department_name)

    def add_new_department(self, new_department: Department) -> None:
        self.get_db().add_new_department(new_department)

    def delete_department_by_name(self, department_name: str) -> None:
        self.get_db().delete_department_by_name(department_name)
