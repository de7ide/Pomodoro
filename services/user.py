import string
from random import choice
from dataclasses import dataclass

from repository.user import UserRepo
from schemas import UserLoginSchema


@dataclass
class UserService:
    user_repo: UserRepo

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        access_token = self._generate_access_token()
        user = self.user_repo.create_user(username=username, password=password, access_token=access_token)
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)

    @staticmethod
    def _generate_access_token() -> str:
        return ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(10))