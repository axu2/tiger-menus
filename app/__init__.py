import os
from flask import Flask
from flask_cas import CAS
from flask_cors import CORS
from flask_admin import Admin
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask.ext.compress import Compress
from flask_mongoengine import MongoEngine
from flask_admin.contrib.mongoengine import ModelView

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'you-will-never-guess'
app.config['CAS_SERVER'] = 'https://fed.princeton.edu/cas'
app.config['CAS_AFTER_LOGIN'] = 'index'

cas = CAS(app)
CORS(app)
Bootstrap(app)
Compress(app)

dummy = "mongodb://heroku_t6g31fxj:8u1g6iotm21eg7r11u6ai38j20@ds013495.mlab.com:13495/heroku_t6g31fxj"
app.config['MONGODB_SETTINGS'] = {
    'db': 'menus',
    'host': os.getenv('MONGODB_URI') or dummy
}
db = MongoEngine(app)

from app.models import User
admin = Admin(app, 'TigerMenus')

class UserView(ModelView):
    def is_accessible(self):
        return cas.username in {"ax2"}

admin.add_view(UserView(User))

from app import views, api, finder   # noqa
