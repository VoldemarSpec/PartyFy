from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.models.party import Party
from app.db.models.item import Item
from app.db.models.user import User


class PartyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session



    async def get_by_id(self, party_id: int) -> Party | None:
        result = await self.session.execute(
            select(Party)
            .where(Party.id == party_id)
        )
        return result.scalar_one_or_none()

    async def get_by_uuid(self, party_uuid: str):
        result = await self.session.execute(
            select(Party)
            .options(selectinload(Party.items))  # 👈 ВАЖНО
            .where(Party.uuid == party_uuid)
        )
        return result.scalar_one_or_none()

    async def get_by_id_with_owner(self, party_id: int) -> Party | None:
        result = await self.session.execute(
            select(Party)
            .options(joinedload(Party.owner))
            .where(Party.id == party_id)
        )
        return result.scalar_one_or_none()


    async def get_parties_by_id(self, user_id: int):

        result = await self.session.execute(
            select(Party).where(Party.owner_id == user_id)
        )
        return result.scalars().all()

    async def get_by_uuid_with_verification(self, party_uuid: str, user_id: int):
        result = await self.session.execute(
            select(Party)
            .options(selectinload(Party.items))  # 👈 ВАЖНО
            .where(
                Party.uuid == party_uuid,
                Party.owner_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def get_full(self, party_id: int) -> Party | None:
        """Party + owner + items"""
        result = await self.session.execute(
            select(Party)
            .options(
                joinedload(Party.owner),
                selectinload(Party.items),
            )
            .where(Party.id == party_id)
        )
        return result.scalar_one_or_none()



    async def create(
        self,
        *,
        party_name: str,
        owner: User,
    ) -> Party:
        party = Party(owner=owner,party_name=party_name)
        self.session.add(party)
        await self.session.flush()  # получаем party.id
        return party

    # --------------------
    # ITEMS
    # --------------------

    async def add_item(
        self,
        *,
        party: Party,
        item: Item,
    ) -> Item:
        item.party = party
        self.session.add(item)
        await self.session.flush()
        return item

    async def remove_item(
        self,
        *,
        item: Item,
    ) -> None:
        await self.session.delete(item)

    # --------------------
    # DELETE
    # --------------------

    async def delete(self, party: Party) -> None:
        await self.session.delete(party)
