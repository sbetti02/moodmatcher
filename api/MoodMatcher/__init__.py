import os

from flask import Flask

app = Flask(__name__)
app.config['SPOT_CLIENT_ID'] = os.environ['SPOT_CLIENT_ID']
app.config['SPOT_CLIENT_SECRET'] = os.environ['SPOT_CLIENT_SECRET']

# class HerokuConfig:
#     SPOT_CLIENT_ID = os.environ['SPOT_CLIENT_ID']
#     SPOT_CLIENT_SECRET = os.environ['SPOT_CLIENT_SECRET']

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(HerokuConfig)

#     from MoodMatcher import routes

#     return app


