from app.backend.FactoryService.providers import SpotifyService, YouTubeService, AppleMusicService, SoundCloudService
from app.backend.FactoryService.base import BaseMusicService

from typing import Type

SERVICES_REGISTRY: dict[str, Type[BaseMusicService]] = {
    "spotify": SpotifyService,
    "youtube": YouTubeService,
    "apple_music": AppleMusicService,
    "soundcloud": SoundCloudService
}

def get_music_service(service_name: str) -> BaseMusicService:
    service_cls = SERVICES_REGISTRY.get(service_name)
    if not service_cls:
        raise ValueError(f"Service handler for '{service_name}' is not implemented")
    return service_cls()
