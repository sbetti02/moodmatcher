import csv
import os

import pandas as pd

from category_parser import get_all_categories, get_tracks_audio_features_from_category

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


@write_new_data(AUDIO_FEATURES_DIR)
def write_category_tracks_audio_features(category, overwrite=False):
    file_path = f'{AUDIO_FEATURES_DIR}/{category}.csv'
    if os.path.isfile(file_path) and not overwrite:
        print(f'{file_path} already exists, not overwriting')
        return

    tracks_audio_features = get_tracks_audio_features_from_category(category)
    unneeded_fields = ['type', 'uri', 'track_href', 'analysis_url']
    for track_audio_features in tracks_audio_features:
        for field in unneeded_fields:
            track_audio_features.pop(field)
    df = pd.DataFrame(tracks_audio_features)
    print(f'Writing to {file_path}')
    df.to_csv(file_path)


def write_all_category_audio_features(overwrite=False):
    categories = read_categories()
    for category in categories:
        if category in UNAVAILABLE_CATEGORIES:
            print(f'Skipping {category}')
            continue
        write_category_tracks_audio_features(category, overwrite)
