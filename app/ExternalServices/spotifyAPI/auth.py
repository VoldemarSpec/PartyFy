import aiohttp
import requests
from dotenv import load_dotenv
import os
import base64
import asyncio
load_dotenv(".env.auth")


async def get_token(session):
    spotify_client_id = os.getenv("SPOTIFY_CLIENT")
    spotify_secret = os.getenv("SPOTIFY_SECRET")
    auth_data = base64.b64encode((spotify_client_id + ":" + spotify_secret).encode()).decode()
    async with session.post("https://accounts.spotify.com/api/token",
                         headers={'Authorization': f'Basic {auth_data}',
                                  "Content-Type": "application/x-www-form-urlencoded"},

                         data={"grant_type":"client_credentials"}) as response:
        token = await response.json()

    return token["access_token"]

