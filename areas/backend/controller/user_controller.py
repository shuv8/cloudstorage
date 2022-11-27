from typing import Optional

from core.user import User
from service.user_service import UserService


class UserController:
    user_service = UserService()

    def registration(self, new_user: User) -> Optional[str]:
        return self.user_service.registration(new_user)

    def login(self, email: str, password: str):
        return self.user_service.login(email, password)
