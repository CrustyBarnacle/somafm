import configparser
import urllib.request
import requests # https://requests.readthedocs.io
from requests.exceptions import HTTPError
from models import (
    Channel,
    Playlist,
    parse_channels
)
from pathlib import Path

URL = "https://somafm.com/channels.json"
PLAYLIST_PATH = Path.home() / "Music" / "Playlists" / "somaFM.pls"

def get_channels(url: str) -> requests.Response | None:
    """Return list of SomaFM channels (json object)"""
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


def resolve_stream_url(playlist_url: str) -> tuple[str | None, str | None]:
    """Fetch a .pls URL and extract the actual stream URL and title"""
    with urllib.request.urlopen(playlist_url) as response:
        content = response.read().decode('utf-8')
    config = configparser.ConfigParser()
    config.read_string(content)
    return (
        config.get('playlist', 'file1', fallback=None),
        config.get('playlist', 'title1', fallback=None)
    )


def write_pls(playlists: list[Playlist], output_path: Path) -> None:
    """Resolve stream URLs and write a proper PLS file for MPD"""
    entries: list[tuple[str, str]] = []

    for playlist in playlists:
        stream_url, title = resolve_stream_url(playlist.url)
        if stream_url and title:
            entries.append((stream_url, title))

    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('[playlist]\n')
        for i, (url, title) in enumerate(entries, start=1):
            f.write(f'File{i}={url}\n')
            f.write(f'Title{i}={title}\n')
            f.write(f'Length{i}=-1\n')
        f.write(f'numberofentries={len(entries)}\n')
        f.write('Version=2\n')


def print_playlists(playlists: list[Playlist]) -> None:
    for playlist in playlists:
        print(playlist.url)


if __name__ == "__main__":
    response = get_channels(URL)
    if response is None:
        exit(1)
    channels = parse_channels(response.json())
    somafm_playlists = get_playlists(channels)
    write_pls(somafm_playlists, PLAYLIST_PATH)
