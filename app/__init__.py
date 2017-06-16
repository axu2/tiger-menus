from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'menus',
    'host': 'mongodb://Arable:Arable@ds127982.mlab.com:27982/heroku_pbbvt44m'
}

db = MongoEngine(app)

from app import views
