import aiohttp
import asyncio
from dotenv import load_dotenv
import os



async def youtube_link_search(search_param, session) -> str:
    load_dotenv("../.env.auth")
    API_KEY = os.getenv("YT_API_KEY")
    print(API_KEY)
    async with session.get(f'https://www.googleapis.com/youtube/v3/search?part='
                           f'snippet&q={search_param}+officialaudio&type=video&maxResults=1&key={API_KEY}') as response:
        html = await response.json()
        print(html)
        return html["items"][0]["id"]["videoId"]


