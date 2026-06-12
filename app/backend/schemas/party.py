from pydantic import BaseModel,Field, ConfigDict
from app.backend.schemas.items import ItemInPartyResponse
from typing import Optional
class  PartyCreate(BaseModel):
    party_name: str =Field(min_length=1,max_length=50)

class PartyGet(BaseModel):
    id: Optional[str] = None


class PartyResponse(BaseModel):
    uuid: str
    party_name: str

class PartyResponseWithItems(BaseModel):
    uuid: str
    party_name: str
    items: list[ItemInPartyResponse]

    model_config = ConfigDict(from_attributes=True)
