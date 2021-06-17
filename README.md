# somafm

Short Python script that grabs the SomaFM channels information from https://somafm.com/channels.json, and prints out a list of the highest quality aac format playlists. Useful for creating a playlist for your favorite stream-capable music player.

The script will print out (standard out) a list of the URLs for all of the SomaFM radio stations.


### Usage:

HTTPS playlist (default)
    `python somafm.py > soma_channels.pl`

HTTP playlist
    `python3 somafm.py | sed 's/https/http/' > soma_channels_http.pl`


### Example HTTP playlist:

```
http://api.somafm.com/7soul130.pls
http://api.somafm.com/bagel130.pls
http://api.somafm.com/beatblender130.pls
http://api.somafm.com/bootliquor130.pls
http://api.somafm.com/brfm130.pls
http://api.somafm.com/cliqhop130.pls
http://api.somafm.com/covers130.pls
...
http://api.somafm.com/u80s130.pls
http://api.somafm.com/metal130.pls
http://api.somafm.com/reggae130.pls
http://api.somafm.com/scanner130.pls
http://api.somafm.com/vaporwaves130.pls
http://api.somafm.com/specials130.pls
http://api.somafm.com/n5md130.pls
http://api.somafm.com/synphaera130.pls
```