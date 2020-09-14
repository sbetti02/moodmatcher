import requests

from spotify_lib import get_header


def get_paginated_results(url, obj_type=None):
    """
    For spotify results that require pagination to get the full
    list, just provide the url and this function will deal with any
    required next calls and return the items in the results in a
    flat list.

    The obj_type parameter is used for the outer encasing of
    the response objects, as seems common in the responses
    I've seen so far from the Spotify API.
    This doesn't appear to always be necessary, so I've set the default
    case to None to account for that.
    """
    results = []
    headers = get_header()
    while url:
        response = requests.get(url, headers=headers)
        resp_json = response.json()
        if obj_type:
            resp_info = resp_json[obj_type]
        else:
            resp_info = resp_json
        resp_items = resp_info['items']
        if resp_items:
            results.extend(resp_items)
        url = resp_info['next']
    return results


def make_chunks(lst, n):
    """
    For query param searches where the number of items
    you can search for at once is limited
    """
    for i in range(0, len(lst), n):
        yield lst[i:i+n]
