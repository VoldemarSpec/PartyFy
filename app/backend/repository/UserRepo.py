from typing import Any, Sequence

from app.db.models import Party
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def exists_by_email(self, email: str) -> bool:
        result = await self.session.execute(
            select(User.id).where(User.email == email)
        )
        return result.first() is not None




    async def create(
        self,
        *,
        email: str,
        username: str,
        hashed_password: str,
    ) -> User:
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
        )
        self.session.add(user)
        await self.session.flush()   # получаем id
        return user
