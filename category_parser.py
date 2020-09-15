import requests

from spotify_lib import connect, get_header
from utils import get_paginated_results, make_chunks


def get_tracks_in_playlist(playlist_id):
    """
    Get all the track dicts for a particular playlist, return
    in flat list
    """
    connect()
    results = get_paginated_results(
        f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks')
    return results


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


def get_all_songs_in_category(category):
    """
    Given a particular category, grab all of the songs in playlists
    for that category
    """
    connect()
    playlists = get_playlists(category)
    playlist_ids = [playlist['id'] for playlist in playlists]
    category_tracks = []
    for play_id in playlist_ids:
        category_tracks.extend(get_tracks_in_playlist(play_id))
    return category_tracks


def parse_track_ids_from_metadata(tracks):
    """
    Take the track metadata and pull out the actual ids
    into a list
    """

    track_ids = []
    for track in tracks:
        if not track.get('track'):
            continue
        track_id = track['track']['id']
        track_ids.append(track_id)
    if not track_ids:
        raise ValueError
    return track_ids


def get_tracks_audio_features(track_ids):
    """
    Given the track ids, return a flat list with all of
    their audio features
    """
    connect()
    url = 'https://api.spotify.com/v1/audio-features/'
    track_groups = make_chunks(track_ids, 100)
    audio_features = []
    for group in track_groups:
        query_params = {'ids': ','.join(group)}
        response = requests.get(
            url, params=query_params, headers=get_header()
        )
        resp_json = response.json()
        if resp_json.get('audio_features'):
            audio_features.extend(resp_json['audio_features'])
    return audio_features


def get_tracks_audio_features_from_category(category):
    """
    For a particular category, get a list of track features
    for songs in that category
    """
    tracks_meta = get_all_songs_in_category(category)
    track_ids = parse_track_ids_from_metadata(tracks_meta)
    return get_tracks_audio_features(track_ids)


def get_all_categories():
    """
    Get all of the spotify category IDs.
    """
    connect()
    categories = get_paginated_results(
        'https://api.spotify.com/v1/browse/categories', 'categories')
    category_ids = [cat['id'] for cat in categories]
    return category_ids
