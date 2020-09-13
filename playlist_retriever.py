import requests

from spotify_lib import connect, get_header



def get_song():
    connect()
    response = requests.get(
        'https://api.spotify.com/v1/tracks/2TpxZ7JUBn3uw46aR7qd6V',
        headers=get_header())
    return response

def get_playlists():
    connect()
    category_id = 'party'
    response = requests.get(
        f'https://api.spotify.com/v1/browse/categories/{category_id}/playlists',
        headers=get_header())
    import pdb
    pdb.set_trace()
    return response

def get_categories():
    connect()
    response = requests.get(
        'https://api.spotify.com/v1/browse/categories',
        headers=get_header())
    import pdb
    pdb.set_trace()
    return response
