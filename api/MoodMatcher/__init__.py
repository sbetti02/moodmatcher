import os

from flask import Flask

app = Flask(__name__)
app.config['SPOT_CLIENT_ID'] = os.environ['SPOT_CLIENT_ID']
app.config['SPOT_CLIENT_SECRET'] = os.environ['SPOT_CLIENT_SECRET']
app.config['PYTHONUNBUFFERED'] = True

from MoodMatcher import routes
