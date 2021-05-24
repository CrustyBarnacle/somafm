import requests # https://requests.readthedocs.io
from requests.exceptions import HTTPError


url = "https://somafm.com/channels.json"


def get_channels(url): # Get list of SomaFM channels (json object)
    try:
        response = requests.get(url)
        response.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occured:\n {http_err}')
    except Exception as err:
        print(f'Other error occured: {err}')
    
    return response

def get_playlists(response):
    channels = [] # Store channel playlists
    for channel in response['channels']:
        #print(f"{channel['title']} : {channel['description']}")
        for playlist in channel['playlists']:
            if playlist['quality'] == 'highest' and playlist['format'] == 'aac':
                channels.append(f"{playlist['url']}")

    return (channels)

def print_playlists(playlist):
    for url in playlist:
        print(url)


print('--- SomaFM Channels ---')
response = get_channels(url)
somafm_playlist = get_playlists(response.json())
print_playlists(somafm_playlist)
