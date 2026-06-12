from app.backend.repository.ItemRepo import ItemRepository
from app.backend.repository.PartyRepo import PartyRepository
from app.db.models import User
from fastapi import Depends, Cookie, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_access_token, verify_refresh_token, create_access_token
from app.db.session.session import get_session
from app.backend.repository.UserRepo import UserRepository
from app.backend.service.AuthService import AuthService
from app.backend.service.UserService import UserService
from starlette.requests import Request


def get_auth_service(
        session: AsyncSession = Depends(get_session),
) -> AuthService:

    user_repo = UserRepository(session)
    return AuthService(user_repo)


async def get_current_user(
    request: Request,
    ):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = verify_access_token(access_token)
    if payload["sub"] == "guest":
        raise HTTPException(status_code=403, detail="Forbidden")
    user_id = int(payload["sub"])
    return user_id


async def get_current_user_for_guest(
    request: Request,
    ):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = verify_access_token(access_token)
    return payload

async def refresh_access_token(requset: Request) -> str:
    refresh_token = requset.cookies.get("refresh_token")
    payload = verify_refresh_token(refresh_token)
    user_id = int(payload["sub"])

    return create_access_token(user_id)

