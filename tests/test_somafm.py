"""Tests for somafm module."""

from somafm import get_playlists


def test_get_playlists_returns_list() -> None:
    """Test that get_playlists extracts URLs correctly."""
    sample_data = {
        "channels": [
            {
                "title": "Drone Zone",
                "playlists": [
                    {"quality": "highest", "format": "aac", "url": "https://example.com/drone.pls"},
                    {"quality": "low", "format": "mp3", "url": "https://example.com/drone-low.pls"},
                ],
            },
        ]
    }

    result = get_playlists(sample_data)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == "https://example.com/drone.pls"


def test_get_playlists_empty_channels() -> None:
    """Test with empty channels list."""
    result = get_playlists({"channels": []})
    assert result == []


def test_get_playlists_filters_correctly() -> None:
    """Test that only highest quality AAC playlists are returned."""
    sample_data = {
        "channels": [
            {
                "title": "Test",
                "playlists": [
                    {"quality": "highest", "format": "aac", "url": "https://keep.pls"},
                    {"quality": "highest", "format": "mp3", "url": "https://skip.pls"},
                    {"quality": "low", "format": "aac", "url": "https://also-skip.pls"},
                ],
            }
        ]
    }

    result = get_playlists(sample_data)

    assert result == ["https://keep.pls"]