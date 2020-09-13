import requests

from spotify_lib import get_header


def get_paginated_results(url, obj_type):
    """
    For spotify results that require pagination to get the full
    list, just provide the url and this function will deal with any
    required next calls and return the items in the results in a
    flat list.

    The obj_type parameter is used for the outer encasing of
    the response objects, as seems common in the responses
    I've seen so far from the Spotify API
    """
    results = []
    headers = get_header()
    while url:
        response = requests.get(url, headers=headers)
        resp_json = response.json()
        resp_items = resp_json[obj_type]['items']
        if resp_items:
            results.extend(resp_items)
        url = resp_json[obj_type]['next']
    return results
