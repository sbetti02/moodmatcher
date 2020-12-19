import os

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SPOT_CLIENT_ID'] = os.environ['SPOT_CLIENT_ID']
app.config['SPOT_CLIENT_SECRET'] = os.environ['SPOT_CLIENT_SECRET']
app.config['PYTHONUNBUFFERED'] = True

from MoodMatcher import routes
