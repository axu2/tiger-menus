import os
from flask import Flask
from flask_cas import CAS
from flask_cors import CORS
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'you-will-never-guess'
app.config['CAS_SERVER'] = 'https://fed.princeton.edu/cas'
app.config['CAS_AFTER_LOGIN'] = '/'

cas = CAS(app)
CORS(app)
Bootstrap(app)

dummy = "mongodb://heroku_t6g31fxj:8u1g6iotm21eg7r11u6ai38j20@ds013495.mlab.com:13495/heroku_t6g31fxj"
app.config['MONGODB_SETTINGS'] = {
    'db': 'menus',
    'host': os.getenv('MONGODB_URI') or dummy
}
db = MongoEngine(app)

from app import views   # noqa
