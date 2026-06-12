from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.item import Item
from app.db.models.party import Party
from app.db.models.user import User


class ItemRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_s3_name(self, s3_name: str) -> Item | None:
        result = await self.session.execute(
            select(Item)
            .where(Item.s3_name == s3_name)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, item_id: int) -> Item | None:
        result = await self.session.execute(
            select(Item)
            .where(Item.id == item_id)
        )
        return result.scalar_one_or_none()

    async def get_by_id_full(self, item_id: int) -> Item | None:
        """Item + added_by_user + party"""
        result = await self.session.execute(
            select(Item)
            .options(
                joinedload(Item.added_by_user),
                joinedload(Item.party),
            )
            .where(Item.id == item_id)
        )
        return result.scalar_one_or_none()

    async def get_by_party_id(self, party_id: int) -> list[Item]:
        result = await self.session.execute(
            select(Item)
            .where(Item.party_id == party_id)
        )
        return result.scalars().all()

    async def get_by_party_id_full(self, party_id: int) -> list[Item]:
        result = await self.session.execute(
            select(Item)
            .options(joinedload(Item.added_by_user))
            .where(Item.party_id == party_id)
        )
        return result.scalars().all()


    async def create(
        self,
        *,
        item_name: str,
        artists: str,
        provided_link: str,
        source: str,
        s3_name:str,
        party: Party,
        added_by_user: User | None,
        added_by_name: str,
    ) -> Item:
        item = Item(
            item_name = item_name,
            artist_name = artists,
            provided_link=provided_link,
            source= source,
            s3_name = s3_name,
            party=party,
            added_by_user=added_by_user,
            added_by_name=added_by_name,
        )
        self.session.add(item)
        await self.session.flush()
        return item



    async def delete(self, item: Item) -> None:
        await self.session.delete(item)
