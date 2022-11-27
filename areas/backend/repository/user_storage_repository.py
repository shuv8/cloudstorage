from typing import Optional

from core.user import User
from database.directories_mock import DataBaseTemporaryMock


class UserRepository:
    db = DataBaseTemporaryMock()

    def create_user(self, new_user: User) -> Optional[str]:
        self.db.create_user(new_user)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.get_user_by_email(email)
