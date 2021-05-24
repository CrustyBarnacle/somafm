# somafm

Short Python script that grabs the SomaFM channels information from https://somafm.com/channels.json, and prints out a list of the highest quality aac format playlists. Useful for creating a playlist for your favorite stream-capable music player.

The script will print out (standard out) a list of the URLs for all of the SomaFM radio stations.


Usage:

HTTPS playlist (default)
    `python somafm.py > myplaylist.pl`

HTTP playlist
    `python3 somafm.py | sed 's/https/http/' > soma_channels_http.pl`