import bcrypt
import jwt

from core.user import User
from repository.user_storage_repository import UserRepository


class UserService:
    user_repo = UserRepository()

    def registration(self, new_user: User):
        if self.user_repo.get_user_by_email(new_user.email):
            return "email already exist"

        salt = bcrypt.gensalt()
        new_user.password = bcrypt.hashpw(
            new_user.password.encode(), salt).decode()

        return self.user_repo.create_user(new_user)

    def login(self, email: str, password: str):
        user = self.user_repo.get_user_by_email(email)

        if not user:
            return None, "incorrect email or password"

        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            return None, "incorrect email or password"

        token = jwt.encode({"email": user.email, "hash": user.password},
                           "SUPER-SECRET-KEY", algorithm="HS256")  # TODO: get secret from env

        return token, None
