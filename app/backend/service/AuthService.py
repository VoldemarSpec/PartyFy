from os import access
from fastapi import HTTPException
from app.backend.repository.UserRepo import UserRepository
from app.backend.exceptions.AuthExceptions import InvalidCredentials
from app.core.security import create_access_token, create_refresh_token, verify_password, create_guest_access_token


class AuthService:
    def __init__(self,
                 user_repo: UserRepository,
                 ):
        self.user_repo = user_repo


    async def login(self, email: str, password: str):
        user = await self.user_repo.get_by_email(email)

        if not user:
            raise InvalidCredentials()

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentials()

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        return access_token, refresh_token

    async def create_guest_access(self, party_uuid: str):
        access_token = create_guest_access_token(party_uuid=party_uuid)
        return access_token




