from app.backend.repository.UserRepo import UserRepository
from app.backend.repository.PartyRepo import PartyRepository
from app.backend.repository.ItemRepo import ItemRepository
from app.db.models import User
from fastapi import HTTPException


class PartyService:
    def __init__(
        self,
        item_repo: ItemRepository,
        user_repo: UserRepository,
        party_repo: PartyRepository,
    ):
        self.item_repo = item_repo
        self.user_repo = user_repo
        self.party_repo = party_repo

    async def create_party(self,
                          *,
                          owner_id: int,
                          party_name: str,
                          ):
        user = await self.user_repo.get_by_id(user_id=owner_id)
        return await self.party_repo.create(owner = user, party_name = party_name)

    async def get_parties(self,
                           user_id: int
                            ):
        parties = await self.party_repo.get_parties_by_id(user_id)
        return parties

    async def get_party_by_id(self, payload, party_uuid):

        if payload["sub"] == "guest":
            party = await self.party_repo.get_by_uuid(payload["party_uuid"])
        else:
            party = await self.party_repo.get_by_uuid_with_verification(party_uuid=party_uuid, user_id=int(payload["sub"]))
        if not party:
            raise HTTPException(status_code=404, detail="Party not found")
        return party



    async def check_party_by_uuid(self, party_uuid:str):
        party = await self.party_repo.get_by_uuid(party_uuid)
        if not party:
            raise HTTPException(status_code=404, detail="Party not found")
        return True