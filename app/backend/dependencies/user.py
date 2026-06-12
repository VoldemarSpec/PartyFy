from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session.session import get_session
from app.backend.service.UserService import UserService
from app.backend.repository.UserRepo import UserRepository
from app.backend.repository.PartyRepo import PartyRepository
from app.backend.repository.ItemRepo import ItemRepository



def insert_session(session: AsyncSession = Depends(get_session)) -> UserService:


    return UserService(ItemRepository(session), UserRepository(session), PartyRepository(session))


