from app.backend.service.ItemService import ItemService
from app.backend.repository.ItemRepo import ItemRepository
from app.backend.repository.UserRepo import UserRepository
from app.backend.repository.PartyRepo import PartyRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import  Depends
from app.db.session.session import get_session

def get_item_service(
        session: AsyncSession = Depends(get_session),
) -> ItemService:

    item_repo = ItemRepository(session)
    user_repo = UserRepository(session)
    party_repo = PartyRepository(session)

    return ItemService(item_repo=item_repo, party_repo=party_repo, user_repo= user_repo)