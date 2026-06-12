from app.backend.service.AuthService import AuthService
from fastapi import FastAPI, routing, APIRouter,Response, Depends, HTTPException
from app.backend.schemas.user import UserCreate, UserLogin, UserResponse
from app.backend.service.UserService import UserService
from app.backend.service.PartyService import PartyService
from app.backend.dependencies.user import insert_session
from app.backend.dependencies.party import insert_party_session
from app.backend.dependencies.auth import get_auth_service, get_current_user, refresh_access_token
from app.backend.exceptions.UserExceptions import UserExists
from app.backend.exceptions.AuthExceptions import InvalidCredentials


router = APIRouter()




@router.post("/register", response_model=UserResponse)
async def root(data: UserCreate,
               service: UserService = Depends(insert_session)
                ):
    try:
        response = await service.create_user(email=data.email,username=data.username,password=data.password)
        return response
    except UserExists as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/login")
async def login(data: UserLogin,
                response: Response,
                service: AuthService = Depends(get_auth_service),
                ):
    try:
        access_token, refresh_token =await service.login(email=data.email,password=data.password)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=False,
            samesite="lax",
            secure=False,
            max_age=60 * 15,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=60 * 60 * 24 * 7,
        )
        return {"login": "success"}
    except InvalidCredentials as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/get_user")
async def get_user(user: int = Depends(get_current_user)
        ):
    return user

@router.post("/refresh")
async def refresh(
        response: Response,
        new_access_token = Depends(refresh_access_token)
        ):
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=False,
        secure=False,
        samesite="lax",
        max_age=60 * 15,
    )
    return {"message": "Access token refreshed"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token", httponly=True)
    response.delete_cookie(key="refresh_token", httponly=True)
    return {"message": "Successfully logged out"}


@router.get("/invitation/{uuid}")
async def invitation(
    uuid: str,
    response: Response,
    service: PartyService = Depends(insert_party_session),
    auth_service: AuthService = Depends(get_auth_service)
):

    verify = await service.check_party_by_uuid(party_uuid=uuid)

    if not verify:
        raise HTTPException(status_code=404, detail="Party not found")

    access_token = await auth_service.create_guest_access(uuid)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 120
    )

    return {"message": "joined"}