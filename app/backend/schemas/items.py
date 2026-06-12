from typing import Optional
from pydantic import BaseModel, HttpUrl, model_validator, ConfigDict
from app.core.constants import SERVICE_DOMAINS

class ItemDelete(BaseModel):
    id: int

class ItemResponse(BaseModel):
    id: int
    item_name: str
    artist_name: str
    source: str
    s3_name: str
    provided_link: str
    added_by_name: str

class ItemS3Response(BaseModel):
    presigned_url: HttpUrl

class ItemInPartyResponse(BaseModel):
    id:int
    item_name: str
    artist_name: str
    source: str
    s3_name: str
    provided_link: str
    added_by_name: str

    model_config = ConfigDict(from_attributes=True)

class MusicLink(BaseModel):
    url: HttpUrl
    party_uuid: Optional[str]
    service: Optional[str] = None

    @model_validator(mode="after")
    def detect_service(self):
        domain_host = self.url.host

        if not domain_host:
            raise ValueError("Invalid URL host")

        clean_host = domain_host.replace("www.", "").lower()

        found_service = None
        for service_name, domains in SERVICE_DOMAINS.items():

            if any(clean_host == d or clean_host.endswith(f".{d}") for d in domains):
                found_service = service_name
                break

        if not found_service:
            raise ValueError(f"Сервис не поддерживается: {clean_host}")

        # Записываем результат в поле модели
        self.service = found_service

        return self