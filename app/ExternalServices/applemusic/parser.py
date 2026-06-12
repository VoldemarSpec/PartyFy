import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio





async def apple_music_get(session, url):
    async with session.get(url) as response:
        html = await response.text(encoding="utf-8")

    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(strip=True)

    try:
        parts = [p.strip() for p in title.split("–")]
        search_param = f"{parts[0]}+{parts[1].replace('Song by ', '')}"
        return {
            "name": parts[0],
            "artists": parts[1].replace('Song by ', ''),
            "search_param": search_param
        }
    except IndexError:
        parts = [p.strip() for p in title.split("-")]
        search_param = f"{parts[0]}+{parts[1].replace('Song by ', '')}"
        return {
            "name": parts[0],
            "artists": parts[1].replace('Song by ', ''),
            "search_param": search_param
        }





