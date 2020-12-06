from flask import Flask

class heroku_config(Object):
    SPOT_CLIENT_ID = os.environ['SPOT_CLIENT_ID']
    SPOT_CLIENT_SECRET = os.environ['SPOT_CLIENT_SECRET']

def create_app():
    app = Flask(__name__)
    app.config.from_object(heroku_config)

    from MoodMatcher import routes

    return app


