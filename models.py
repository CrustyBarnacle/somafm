"""Data models - somaFM API responses"""

from dataclasses import dataclass
from typing import Any


@dataclass
class Playlist:
    url: str
    format: str
    quality: str


@dataclass
class Channel:
    id: str
    title: str
    description: str
    genre: str
    playlists: list[Playlist]


def parse_channels(data: dict[str, Any]) -> list[Channel]:                                              
    """Parse API response into Channel objects."""                                                      
    channels: list[Channel] = []                                                                        
                                                                                                        
    for ch in data.get("channels", []):                                                                 
        playlists = [                                                                                   
            Playlist(                                                                                   
                url=p["url"],                                                                           
                format=p["format"],                                                                     
                quality=p["quality"],                                                                   
            )                                                                                           
            for p in ch.get("playlists", [])                                                            
        ]                                                                                               
                                                                                                        
        channel = Channel(                                                                              
            id=ch["id"],                                                                                
            title=ch["title"],                                                                          
            description=ch["description"],                                                              
            genre=ch["genre"],                                                                          
            playlists=playlists,                                                                        
        )                                                                                               
        channels.append(channel)                                                                        
                                                                                                        
    return channels