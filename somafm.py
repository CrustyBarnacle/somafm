import requests # https://requests.readthedocs.io
from requests.exceptions import HTTPError
from typing import Any
from models import (
    Channel,
    Playlist,
    parse_channels
)

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
    response = get_channels(url)
    if response is None:
        exit(1)
    channels = parse_channels(response.json())
    somafm_playlist = get_playlists(channels)
    print_playlists(somafm_playlist)
