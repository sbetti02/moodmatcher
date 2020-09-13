import base64
import requests

from exceptions import AuthError
from secrets import SPOT_CLIENT_ID, SPOT_CLIENT_SECRET


class SpotifyAuth:
    def __init__(self):
        self.access_token = self.connect()

    @staticmethod
    def connect():
        """
        Connect to spotify client credentials API and return access token
        """
        auth_str = f'{SPOT_CLIENT_ID}:{SPOT_CLIENT_SECRET}'
        b64_auth_str = base64.b64encode(auth_str.encode()).decode()
        response = requests.post(
            'https://accounts.spotify.com/api/token',
            data={'grant_type': 'client_credentials'},
            headers={'Authorization': f'Basic {b64_auth_str}'})
        if response.status_code == 200:
            return response.json()['access_token']
        raise AuthError(response.status_code)

    def get_header():
        """
        Get the auth header needed to make API requests
        """
        return {'Authorization': self.access_token}

