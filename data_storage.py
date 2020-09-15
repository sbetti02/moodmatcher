import csv
import os

from category_parser import get_all_categories

DATA_FOLDER = './data'
CATEGORIES_FILE = 'all_categories.csv'
CATEGORY_HEADER = 'Category ID'


def write_new_data(f):
    """
    Decorator for saving new data inside of the data folder,
    to make sure the folder exists first. Only really needs
    to work the first time you try to save the file,
    afterwards, a bit unnecessary
    """
    def wrapper(*args, **kwargs):
        if not os.path.isdir(DATA_FOLDER):
            os.mkdir(DATA_FOLDER)
        return f(*args, **kwargs)
    return wrapper


@write_new_data
def write_categories(overwrite=False):
    """
    Save the spotify categories to a file
    """
    categories = get_all_categories()
    file_path = f'{DATA_FOLDER}/{CATEGORIES_FILE}'
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
    file_path = f'{DATA_FOLDER}/{CATEGORIES_FILE}'
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    categories = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            categories.append(row[CATEGORY_HEADER])
    return categories
