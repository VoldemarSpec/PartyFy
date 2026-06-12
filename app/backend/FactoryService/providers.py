import asyncio

from app.backend.FactoryService.base import BaseMusicService
from app.ExternalServices.spotifyAPI import get_spotify_track, get_token
from app.ExternalServices.applemusic import apple_music_get
from app.ExternalServices.s3 import upload_file_to_s3
from app.ExternalServices.youtube import youtube_download, youtube_link_search, get_song_data
import aiohttp
import os
import shutil





class SpotifyService(BaseMusicService):
    async def _fetch_track_data(self, session, url: str):
        token = await get_token(session=session)
        track_data = await get_spotify_track(url=url, token=token, session=session)
        return track_data

    def get_source_name(self) -> str:
        return "Spotify"



class YouTubeService(BaseMusicService):
    async def _fetch_track_data(self, session, url: str):
        track_data = await asyncio.to_thread(get_song_data, url)
        return track_data

    def get_source_name(self) -> str:
        return "YouTube"

class AppleMusicService(BaseMusicService):
    async def _fetch_track_data(self, session, url: str):
        track_data = await apple_music_get(url=url, session=session)
        print(track_data)
        return track_data

    def get_source_name(self) -> str:
        return "AppleMusic"


class SoundCloudService(BaseMusicService):
    async def _fetch_track_data(self, session, url: str):
        track_data = await asyncio.to_thread(get_song_data, url)
        return track_data

    def get_source_name(self) -> str:
        return "Soundcloud"