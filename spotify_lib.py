import base64
import requests

from exceptions import AuthError
from secrets import SPOT_CLIENT_ID, SPOT_CLIENT_SECRET


ACCESS_TOKEN = None


def connect():
    """
    Connect to spotify client credentials API and return access token

    Note: In practice, would need to confirm access token is still valid,
          and if not, refresh it. Not necessary for now.
    """
    global ACCESS_TOKEN

    if ACCESS_TOKEN is not None:
        return

    auth_str = f'{SPOT_CLIENT_ID}:{SPOT_CLIENT_SECRET}'
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    response = requests.post(
        'https://accounts.spotify.com/api/token',
        data={'grant_type': 'client_credentials'},
        headers={'Authorization': f'Basic {b64_auth_str}'})

    if response.status_code == 200:
        ACCESS_TOKEN = response.json()['access_token']
        return

    raise AuthError(response.status_code)


def get_header():
    """
    Get the auth header needed to make API requests
    """
    global ACCESS_TOKEN
    if ACCESS_TOKEN is None:
        raise AuthError('Access token is None!')
    return {'Authorization': f'Bearer {ACCESS_TOKEN}'}
