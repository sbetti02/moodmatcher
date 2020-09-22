import matplotlib.pyplot as plt
import numpy as np

from spotify_scraping.category_parser import get_tracks_audio_features_from_category


def get_feature_info(category):
    key_features = {
        'acousticness': 1,
        'danceability': 1,
        'energy': 1,
        'instrumentalness': 1,
        'liveness': 1,
        'loudness': -60,
        'speechiness': 1,
        'valence': 1
    }
    tracks_audio_features = get_tracks_audio_features_from_category(category)
    for feature in key_features:
        feat_vals = [t[feature] for t in tracks_audio_features]
        normed_feat_vals = [feat_val/key_features[feature] for feat_val in feat_vals]
        feat_variance = np.var(normed_feat_vals)
        print(f'Mean of {feature}: {np.average(feat_vals)}')
        print(f'variance of {feature}: {feat_variance}')
