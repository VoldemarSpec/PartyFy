from app.backend.service.AuthService import AuthService
from typing import Optional
from fastapi import FastAPI, routing, APIRouter,Response, Depends, HTTPException
from app.backend.schemas.party import PartyCreate, PartyGet, PartyResponse, PartyResponseWithItems
from app.backend.service.PartyService import PartyService
from app.backend.service.UserService import UserService
from app.backend.dependencies.party import insert_party_session
from app.backend.dependencies.auth import get_auth_service, get_current_user, refresh_access_token, \
    get_current_user_for_guest
from app.backend.exceptions.UserExceptions import UserExists
from app.backend.exceptions.AuthExceptions import InvalidCredentials
from sqlalchemy.util import await_only
from starlette.requests import Request

router = APIRouter()

@router.post("/create_party")
async def create_party(party: PartyCreate,
                 service: PartyService = Depends(insert_party_session),
                 user: int = Depends(get_current_user)):

    party = await service.create_party(owner_id=user, party_name=party.party_name)
    return party

@router.get("/get_parties", response_model=list[PartyResponse])
async def get_parties(
                    service: PartyService = Depends(insert_party_session),
                    user: int = Depends(get_current_user)):
    parties = await service.get_parties(user_id=user)
    return parties



@router.get("/get_full_party", response_model=PartyResponseWithItems)
async def get_full_party(
                    party_uuid: Optional[str] = None,
                    service: PartyService = Depends(insert_party_session),
                    user: dict = Depends(get_current_user_for_guest)):
    party = await service.get_party_by_id(payload=user, party_uuid=party_uuid)
    return party




