import os

from flask import Flask

class HerokuConfig:
    SPOT_CLIENT_ID = os.environ['SPOT_CLIENT_ID']
    SPOT_CLIENT_SECRET = os.environ['SPOT_CLIENT_SECRET']

def create_app():
    app = Flask(__name__)
    app.config.from_object(HerokuConfig)

    from MoodMatcher import routes

    return app


