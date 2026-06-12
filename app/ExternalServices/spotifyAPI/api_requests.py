import aiohttp


async def get_spotify_track(url, token, session):
    song_id = url.split("/")[-1].split("?")[0]
    url = f"https://api.spotify.com/v1/tracks/{song_id}"

    async with session.get(url, headers={"Authorization": f"Bearer {token}"}) as response:
        if response.status != 200:
            raise ValueError(f"Spotify API Error: {await response.text()}")

        track_info = await response.json()
    artist_names = [artist["name"] for artist in track_info.get("artists", [])]

    artists_str = ", ".join(artist_names)

    track_name = track_info.get("name", "Unknown Track")
    primary_artist = artist_names[0] if artist_names else ""
    search_param = f"{primary_artist} - {track_name}"

    return {
        "name": track_name,
        "artists": artists_str,  # Это теперь СТРОКА
        "search_param": search_param  # Готовый запрос для YouTube
    }