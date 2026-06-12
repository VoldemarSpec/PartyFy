from app.backend.dependencies.items import get_item_service
from fastapi import APIRouter, Depends
from app.backend.schemas.items import MusicLink, ItemResponse, ItemS3Response, ItemDelete
from app.backend.service.ItemService import ItemService
from app.backend.dependencies.auth import get_current_user_for_guest
from app.backend.ws.ws_manager import ws_manager


router = APIRouter()


@router.post("/add_item", response_model=ItemResponse)
async def add_item(
    data: MusicLink,
    payload=Depends(get_current_user_for_guest),
    service: ItemService = Depends(get_item_service),
):
    item = await service.add_item(data, payload)

    await ws_manager.broadcast_to_party(
        party_uuid=str(item.party.uuid),
        message={
            "type": "item_added",
            "data": ItemResponse.model_validate(item, from_attributes=True).model_dump(),
        },
    )

    return item


@router.get("/get_url/{s3_name}", response_model=ItemS3Response)
async def get_item(s3_name: str,
                   user = Depends(get_current_user_for_guest),
                   service: ItemService = Depends(get_item_service)):
    presigned_url = await service.get_presigned_url(s3_name)
    return presigned_url


@router.delete("/remove_item")
async def remove_item(
    data: ItemDelete,
    payload = Depends(get_current_user_for_guest),
    service: ItemService = Depends(get_item_service),
):
    result = await service.remove_item(data, payload)

    # если удаление прошло успешно — рассылаем сообщение в WS
    try:
        await ws_manager.broadcast_to_party(
            party_uuid=result.get("party_uuid"),
            message={
                "type": "item_removed",
                "data": {"id": result.get("id")},
            },
        )
    except Exception:

        pass

    return result