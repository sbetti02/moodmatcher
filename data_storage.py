import csv
import os

import pandas as pd

from category_parser import (get_all_categories,
                             get_tracks_audio_features_from_category,
                             get_all_songs_in_category)

DATA_DIR = './data'
AUDIO_FEATURES_DIR = f'{DATA_DIR}/Audio_Features'
CATEGORIES_FILE = 'all_categories.csv'
CATEGORY_HEADER = 'Category ID'
UNAVAILABLE_CATEGORIES = [
    'regional_mexican',
    'music_of_mexico',
    'kpop',
    'j_tracks',
    'thirdparty',
    'soul',
    'blackhistorymonth',
    'roots',
    'anime',
    'popculture',
    'sessions',
    'colombian',
    'brazilian',
    'french_variety',
    'student'
]


def write_new_data(base_dir):
    """
    Decorator for saving new data inside of a data folder,
    to make sure the folder exists first. Only necessary
    to work the first time you try to save the file, after that,
    the folder should exist
    """
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            if not os.path.isdir(base_dir):
                os.mkdir(base_dir)
            return f(*args, **kwargs)
        return wrapped_f
    return wrap


@write_new_data(DATA_DIR)
def write_categories(overwrite=False):
    """
    Save the spotify categories to a file
    """
    categories = get_all_categories()
    file_path = f'{DATA_DIR}/{CATEGORIES_FILE}'
    if os.path.isfile(file_path) and not overwrite:
        print(f'{file_path} already exists, not overwriting')
        return

    with open(file_path, 'w') as f:
        print(f'Writing to {file_path}')
        writer = csv.DictWriter(f, fieldnames=[CATEGORY_HEADER])
        writer.writeheader()
        for cat in categories:
            writer.writerow({CATEGORY_HEADER: cat})


def read_categories():
    """
    Pull all the spotify categories out from a local file
    """
    file_path = f'{DATA_DIR}/{CATEGORIES_FILE}'
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    categories = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            categories.append(row[CATEGORY_HEADER])
    return categories


def get_category_audio_tracks_df(category):
    tracks_audio_features = get_tracks_audio_features_from_category(category)
    unneeded_fields = ['type', 'uri', 'track_href', 'analysis_url']
    for track_audio_features in tracks_audio_features:
        for field in unneeded_fields:
            track_audio_features.pop(field)
    return pd.DataFrame(tracks_audio_features)


@write_new_data(AUDIO_FEATURES_DIR)
def write_category_tracks_audio_features(category, overwrite=False):
    file_path = f'{AUDIO_FEATURES_DIR}/{category}.csv'
    if os.path.isfile(file_path) and not overwrite:
        print(f'{file_path} already exists, not overwriting')
        return

    df = get_category_audio_tracks_df(category)
    print(f'Writing to {file_path}')
    df.to_csv(file_path)


def get_category_general_track_info(category):
    print(f'Getting general track info for {category}')
    tracks = get_all_songs_in_category(category)
    tracks_info = [track['track'] for track in tracks]
    useful_fields = ['popularity', 'explicit', 'id']
    parsed_tracks = []
    for track_info in tracks_info:
        if not track_info:
            print('No track info found')
            continue
        parsed_track = {}
        for field in useful_fields:
            parsed_track[field] = track_info[field]
        parsed_tracks.append(parsed_track)
    df = pd.DataFrame(parsed_tracks)
    return df


def add_data_to_stored_csv(path, df):
    """
    Given the path to a stored csv, update the data in it to
    include additional data provided by the given dataframe.

    This function assumes that there is a simple way for the pandas merge
    function to merge the data
    """
    pass


def write_track_info_additional_info(category, drop_columns=None):
    file_path = f'{AUDIO_FEATURES_DIR}/{category}.csv'
    # Check if file exists or not, and if yet, if the additional values exist
    # new_fields = ['popularity', 'explicit']
    audio_feats_df = read_audio_features_for_category(category)
    gen_info_df = get_category_general_track_info(category)
    audio_feats_df = audio_feats_df.drop_duplicates(subset=['id'])
    gen_info_df = gen_info_df.drop_duplicates(subset=['id'])
    combined_df = audio_feats_df.merge(gen_info_df, how='inner')
    if drop_columns:
        combined_df = combined_df.loc[:, ~combined_df.columns.str.contains(drop_columns)]
    print(f'Updating {file_path} with general info')
    combined_df.to_csv(file_path)


def write_all_categories_addl_general_info(drop_columns=None):
    categories = read_categories()
    for category in categories:
        if category in UNAVAILABLE_CATEGORIES:
            print(f'Skipping {category}')
            continue
        write_track_info_additional_info(category, drop_columns=drop_columns)


def write_all_category_audio_features(overwrite=False):
    categories = read_categories()
    for category in categories:
        if category in UNAVAILABLE_CATEGORIES:
            print(f'Skipping {category}')
            continue
        write_category_tracks_audio_features(category, overwrite)


def read_audio_features_for_category(category):
    file_path = f'{AUDIO_FEATURES_DIR}/{category}.csv'
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    df = pd.read_csv(file_path)
    return df

def get_all_audio_feats_in_all_categories():
    categories = read_categories()
    categories = list(set(categories) - set(UNAVAILABLE_CATEGORIES))
    dfs = [read_audio_features_for_category(cat) for cat in categories]
    return dfs

def read_all_category_audio_features():
    categories = read_categories()
    all_category_audio_feats = {}
    for category in categories:
        if category in UNAVAILABLE_CATEGORIES:
            print(f'Skipping {category}')
            continue
        audio_feats = read_audio_features_for_category(category)
        print(audio_feats)
        all_category_audio_feats[category] = audio_feats
    return all_category_audio_feats

