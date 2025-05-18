from dataclasses import dataclass
import datetime
from datetime import timedelta, timezone

from jose import JWTError, jwt

from exception import *
from schemas import UserLoginSchema
from models import UserProfile
from repository import UserRepo
from settings import Settings


@dataclass
class AuthServices:
    user_repo: UserRepo
    settings: Settings

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repo.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotFoundPasswordException


    def generate_access_token(self, user_id: int) -> str:
        expire_date_unix = (datetime.datetime.now(timezone.utc) + timedelta(days=7)).timestamp()
        token = jwt.encode(
            {'user_id': user_id, 'expire': expire_date_unix},
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ENCODE_ALGO)
        return token


    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(access_token, self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ENCODE_ALGO])
        except JWTError:
            raise TokenInvalide
        if payload['expire'] < datetime.datetime.now(timezone.utc).timestamp():
            raise TokenExpire
        return payload['user_id']