import os
import tempfile
from yt_dlp import YoutubeDL

def youtube_download(url):
    tmp_dir = tempfile.mkdtemp()
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(tmp_dir, "%(id)s.%(ext)s"),

        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],


        "downloader": "ffmpeg",
        "concurrent_fragment_downloads": 1,
        "http_chunk_size": 5 * 1024 * 1024,
        "force_ipv4": True,

        "extractor_args": {
            "youtube": {
                "player_client": ["android"]
            }
        },

        "noplaylist": True,
        "retries": 10,
        "socket_timeout": 20,
        "quiet": False,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return filename, tmp_dir


def get_song_data(url):

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "name": info.get("title"),
        "artists": info.get("artist") or info.get("uploader")
    }
