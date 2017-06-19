from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['MONGODB_SETTINGS'] = {
    'db': 'menus',
    'host': 'mongodb://Arable:Arable@ds127982.mlab.com:27982/heroku_pbbvt44m'
}

db = MongoEngine(app)

from app import views
