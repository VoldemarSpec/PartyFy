from app.backend.repository.UserRepo import UserRepository
from app.backend.repository.PartyRepo import PartyRepository
from app.backend.repository.ItemRepo import ItemRepository
from fastapi import HTTPException
from app.backend.schemas.items import MusicLink, ItemDelete
from app.backend.FactoryService.factory import get_music_service
from app.ExternalServices.s3 import get_url, delete_file_from_s3
import asyncio

class ItemService:
    def __init__(
        self,
        item_repo: ItemRepository,
        party_repo: PartyRepository,
        user_repo: UserRepository,
    ):
        self.item_repo = item_repo
        self.party_repo = party_repo
        self.user_repo = user_repo

    async def get_presigned_url(self, s3_name: str):
        url = await asyncio.to_thread(get_url, s3_name)
        return {"presigned_url": url}



    async def add_item(
        self,
        data: MusicLink,
        payload
    ):
        party_uuid = None
        user = None
        username = "Guest"
        if payload["sub"] == "guest":
            party_uuid = payload["party_uuid"]
            party = await self.party_repo.get_by_uuid(party_uuid)
        else:
            party = await self.party_repo.get_by_uuid_with_verification(data.party_uuid, int(payload["sub"]))
            user = await self.user_repo.get_by_id(int(payload["sub"]))
            username = user.username
        if not party:
            raise HTTPException(status_code=404, detail="Party not found")
        try:
            handler = get_music_service(data.service)
            result = await handler.process_track(str(data.url))
        except ValueError as e:
            raise HTTPException(status_code=501, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing link: {e}")

        return await self.item_repo.create(
            item_name=result["title"],
            artists= result["artist"],
            provided_link=result["provided_link"],
            source= result["source"],
            s3_name=result["s3_name"],
            party=party,
            added_by_user=user,
            added_by_name=username,
        )

    async def remove_item(self, data: ItemDelete, payload=None):


        item = await self.item_repo.get_by_id_full(data.id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")


        if not payload:
            raise HTTPException(status_code=401, detail="Not authenticated")


        if payload.get("sub") == "guest":
            party_uuid = payload.get("party_uuid")

            if not party_uuid or not item.party or str(item.party.uuid) != str(party_uuid):
                raise HTTPException(status_code=403, detail="Forbidden")
            if item.added_by_user is not None:
                raise HTTPException(status_code=403, detail="Guests can delete only guest-added items")

        else:

            user_id = int(payload.get("sub"))

            is_owner = await self.party_repo.get_by_uuid_with_verification(party_uuid=str(item.party.uuid), user_id=user_id)
            is_adder = item.added_by_user is not None and item.added_by_user.id == user_id
            if not (is_owner or is_adder):
                raise HTTPException(status_code=403, detail="Forbidden")


        await self.item_repo.delete(item)

        try:
            result = await asyncio.to_thread(delete_file_from_s3, item.s3_name)
        except Exception:

            raise HTTPException(status_code=500, detail="Failed to delete file from storage")

        return {"status": "deleted", "id": item.id, "party_uuid": str(item.party.uuid)}
