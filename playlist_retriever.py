import requests

from spotify_lib import connect, get_header
from utils import get_paginated_results


def get_song():
    connect()
    response = requests.get(
        'https://api.spotify.com/v1/tracks/2TpxZ7JUBn3uw46aR7qd6V',
        headers=get_header())
    return response

def get_playlists(category):
    """
    Get the playlists for a particular category

    NOTE: Current limitation: Only returns playlists owned by the official
          Spotify account
    """
    connect()
    results = get_paginated_results(
        f'https://api.spotify.com/v1/browse/categories/{category}/playlists',
        'playlists')
    return results

def get_all_categories():
    """
    Get all of the spotify category IDs.
    """
    connect()
    categories = get_paginated_results(
        'https://api.spotify.com/v1/browse/categories', 'categories')
    category_ids = [cat['id'] for cat in categories]
    return category_ids

