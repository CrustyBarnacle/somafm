"""Tests for somafm module."""

from somafm import (
    get_playlists,
    get_channels,
    print_playlists
)
from models import Channel, Playlist
from unittest.mock import patch, Mock
import requests


def test_get_playlists_returns_list() -> None:
    """Test that get_playlists extracts URLs correctly."""
    channels = [
        Channel(
            id="drone",
            title="Drone Zone",
            description="Droning",
            genre="ambient",
            playlists=[
                Playlist(url="https://example.com/drone.pls", format="aac", quality="highest"),         
                Playlist(url="https://example.com/drone-low.pls", format="mp3", quality="low"),
            ],
        ),
    ]

    result = get_playlists(channels)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == "https://example.com/drone.pls"


def test_get_playlists_empty_channels() -> None:
    """Test with empty channels list."""
    result = get_playlists([])
    assert result == []


def test_get_playlists_filters_correctly() -> None:
    """Test that only highest quality AAC playlists are returned."""
    channels = [
        Channel(
            id="nosuch-channel",
            title="No Such Channel",
            description="Test No Such",
            genre="test",
            playlists=[
                Playlist(url="https://keep.pls", format="aac", quality="highest"),                      
                Playlist(url="https://skip.pls", format="mp3", quality="highest"),                      
                Playlist(url="https://also-skip.pls", format="aac", quality="low"),
            ],
        ),
    ]

    result = get_playlists(channels)

    assert result == ["https://keep.pls"]


def test_get_channels_success() -> None:
    """Test successful API response."""
    with patch("somafm.requests.get") as mock_get:
        # Create a fake Response object
        mock_response = Mock()
        mock_response.raise_for_status = Mock()  # Does nothing (no exception)

        # Make requests.get() return our fake response
        mock_get.return_value = mock_response

        # Call the real function
        result = get_channels("https://example.com/api")

        # Verify it returns our mock response
        assert result is mock_response
        # Verify requests.get was called correctly
        mock_get.assert_called_once_with("https://example.com/api")


def test_get_channels_http_error() -> None:                                                             
    """Test that HTTP errors return None."""                                                            
    with patch("somafm.requests.get") as mock_get:                                                      
        # Make requests.get() raise an exception                                                        
        mock_get.side_effect = requests.exceptions.HTTPError("404 Not Found")                           
                                                                                                        
        result = get_channels("https://example.com/api")                                                
                                                                                                        
        assert result is None


def test_print_playlists_output(capsys) -> None:                                                        
    """Test that playlists are printed correctly."""                                                    
    playlists = ["https://example.com/1.pls", "https://example.com/2.pls"]                              
                                                                                                        
    print_playlists(playlists)                                                                          
                                                                                                        
    captured = capsys.readouterr()                                                                      
    assert "https://example.com/1.pls" in captured.out                                                  
    assert "https://example.com/2.pls" in captured.out