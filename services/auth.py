from dataclasses import dataclass

from exception import UserNotFoundException, UserNotFoundPasswordException
from schemas import UserLoginSchema
from models import UserProfile
from repository import UserRepo


@dataclass
class AuthServices:
    user_repo: UserRepo

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repo.get_user_by_username(username)
        self._validate_auth_user(user, password)
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotFoundPasswordException
