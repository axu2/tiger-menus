import os
from flask import Flask
from flask_cors import CORS
from datetime import datetime
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

CORS(app)
Bootstrap(app)

from app import views  # noqa
