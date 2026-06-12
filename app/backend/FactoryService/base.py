import asyncio
from abc import ABC, abstractmethod
import os
import shutil
import aiohttp
from app.ExternalServices.s3 import upload_file_to_s3
from app.ExternalServices.youtube import youtube_download, youtube_link_search


class BaseMusicService(ABC):
    async def process_track(self, url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            track_data = await self._fetch_track_data(url=url, session=session)
            search_param = track_data.get("search_param")
            if search_param:
                link = await youtube_link_search(session=session, search_param=search_param)
                filename, tmp_dir = await asyncio.to_thread(youtube_download, link)
            else:
                filename, tmp_dir = await asyncio.to_thread(youtube_download, url)

            try:

                mp3_filename = os.path.splitext(filename)[0] + ".mp3"
                await asyncio.to_thread(upload_file_to_s3, mp3_filename)
                s3_name = os.path.basename(mp3_filename)

            finally:
                shutil.rmtree(tmp_dir, ignore_errors=True)


        return {
            "title": track_data["name"],
            "artist": track_data["artists"],
            "provided_link": url,
            "source": self.get_source_name(),
            "s3_name": s3_name
        }

    @abstractmethod
    async def _fetch_track_data(self,session, url: str):

        pass

    @abstractmethod
    def get_source_name(self) -> str:
        pass
