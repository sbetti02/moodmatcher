from flask import jsonify, current_app

from MoodMatcher import app
from spotify_scraping.category_parser import get_track
from spotify_scraping.category_parser import get_playlists
from spotify_scraping.data_storage import read_audio_features_for_category

@app.route('/')
def index():
    return "Hello, World!"


@app.route('/<category>/get_playlists')
def category_playlists(category):
    return jsonify(get_playlists(category))


@app.route('/<category>/category_track_feats')
def cat_track_features(category):
    return read_audio_features_for_category(category).to_html(header=True)


@app.route('/<track>/info')
def get_track_info(track):
    track_info = get_track(track)
    if track_info.get('error'):
        return track_info['error']

    artists = [artist['name'] for artist in track_info['artists']]
    return jsonify({
        'artists': artists,
        'title': track_info['name']
    })
