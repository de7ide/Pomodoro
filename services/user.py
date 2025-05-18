from dataclasses import dataclass

from repository.user import UserRepo
from services.auth import AuthServices
from schemas import UserLoginSchema


@dataclass
class UserService:
    user_repo: UserRepo
    auth_service: AuthServices

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repo.create_user(username=username, password=password)
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
