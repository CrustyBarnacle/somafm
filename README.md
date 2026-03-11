## somafm.py - somaFM channel playlist generator for MPD
# SomaFM MPD Playlist Generator

Fetches SomaFM channel data and generates a PLS playlist for use with MPD.
If you like this script, or it helps you with your own ideas, please support https://somafm.com/!

## Requirements

- Python 3.10+
- `requests` library

## Installation
```bash
pip install requests
```

## Usage
```bash
./somafm.py
```

Generates a PLS playlist at `~/Music/Playlists/somaFM.pls`, creating the directory if it doesn't exist.

## Configuration

Edit the constants at the top of `somafm.py`:
```python
URL = "https://somafm.com/channels.json"
PLAYLIST_PATH = Path.home() / "Music" / "Playlists" / "somaFM.pls"
```

## Notes

- Selects the highest quality AAC stream per channel
- Resolves SomaFM API playlist URLs to direct stream URLs
- Compatible with MPD and any client that supports PLS format (e.g. rmpc)
