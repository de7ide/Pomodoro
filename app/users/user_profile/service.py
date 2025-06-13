from dataclasses import dataclass

from app.users.user_profile.repository import UserRepo
from app.users.auth.service import AuthServices
from app.users.auth.schema import UserLoginSchema


@dataclass
class UserService:
    user_repo: UserRepo
    auth_service: AuthServices

    async def create_user(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repo.create_user(username=username, password=password)
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
