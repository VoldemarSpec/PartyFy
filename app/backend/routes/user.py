from app.backend.service.AuthService import AuthService
from fastapi import FastAPI, routing, APIRouter,Response, Depends, HTTPException
from app.backend.schemas.user import UserCreate, UserLogin, UserResponse
from app.backend.service.UserService import UserService
from app.backend.dependencies.user import insert_session
from app.backend.dependencies.auth import get_auth_service, get_current_user, refresh_access_token
from app.backend.exceptions.UserExceptions import UserExists
from app.backend.exceptions.AuthExceptions import InvalidCredentials


router = APIRouter()




@router.get("/get_user")
async def get_user(user: int = Depends(get_current_user)
        ):
    return user

