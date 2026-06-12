from app.backend.repository.UserRepo import UserRepository
from app.backend.repository.PartyRepo import PartyRepository
from app.backend.repository.ItemRepo import ItemRepository
from app.backend.exceptions.UserExceptions import UserExists
from app.core.security import hash_password
from app.db.models import User


class UserService:
    def __init__(
        self,
        item_repo: ItemRepository,
        user_repo: UserRepository,
        party_repo: PartyRepository,
    ):
        self.item_repo = item_repo
        self.user_repo = user_repo
        self.party_repo = party_repo

    async def create_user(self,
                          *,
                          email: str,
                          username: str,
                          password: str,
                          ):

        if await self.user_repo.exists_by_email(email):
            raise UserExists

        else:
            user = await self.user_repo.create(email=email, username=username, hashed_password=hash_password(password))
            return user



    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.user_repo.get_by_id(user_id)
        return user