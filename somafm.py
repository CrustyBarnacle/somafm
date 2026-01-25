import requests # https://requests.readthedocs.io
from requests.exceptions import HTTPError
from typing import Any, cast
from models import (
    Channel,
    Playlist,
    parse_channels
)
from pathlib import Path
from datetime import datetime, timedelta
import json


CACHE_DIR = Path.home() / ".cache" / "somafm"
CACHE_FILE = CACHE_DIR / "channels.json"
CACHE_MAX_AGE = timedelta(hours=24)
url = "https://somafm.com/channels.json"


def get_channels(url: str) -> requests.Response | None:
# Return list of SomaFM channels (json object)
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response

    except HTTPError as http_err:
        print(f'HTTP error occured:\n {http_err}')
        return None

    except Exception as err:
        print(f'Other error occured: {err}')
        return None

def get_cached_channels() -> dict[str, Any] | None:
    """Load from cache (unless expired), or return None"""
    if not CACHE_FILE.exists():
        return None
    
    # Check cache age
    mtime = datetime.fromtimestamp(CACHE_FILE.stat().st_mtime)
    if datetime.now() - mtime > CACHE_MAX_AGE:
        return None # Stale cache
    
    try:
        with CACHE_FILE.open() as f:
            return cast(dict[str, Any], json.load(f))
    except json.JSONDecodeError:
        return None # Empty or corrupt cache

def save_to_cache(data: dict[str, Any]) -> None:
    """Save response to cache file"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with CACHE_FILE.open("w") as f:
        json.dump(data, f)


def get_playlists(channels: list[Channel]) -> list[Playlist]:
    """Select AAC (highest quality) playlist URLs from channels"""
    playlists: list[Playlist] = [] # Store channel playlists
    for channel in channels:
        for playlist in channel.playlists:
            if playlist.quality == "highest" and playlist.format == 'aac':
                playlists.append(playlist)
    return playlists


def print_playlists(playlists: list[Playlist]) -> None:
    for playlist in playlists:
        print(playlist.url)


if __name__ == "__main__":
    channels_data = get_cached_channels()

    if channels_data is None:
        response = get_channels(url)
        if response is None:
            exit(1)
        channels_data = response.json()
        save_to_cache(channels_data)
    
    channels = parse_channels(channels_data)
    somafm_playlist = get_playlists(channels)
    print_playlists(somafm_playlist)
