import os
from flask import Flask
from bson import ObjectId
from flask_cors import CORS
from datetime import datetime
from flask.json import JSONEncoder
from mongoengine import connect, Document, QuerySet


class FlaskJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, QuerySet):
            return [doc for doc in o]
        if isinstance(o, Document):
            return o.to_mongo()
        elif isinstance(o, ObjectId):
            return str(o)
        else:
            return JSONEncoder.default(self, o)

app = Flask(__name__)
CORS(app)
app.json_encoder = FlaskJSONEncoder
from app import views   # noqa

if 'MONGODB_URI' in os.environ:
    host = os.getenv('MONGODB_URI')
else:
    # dummy mongodb server so developers dont have to install MongoDB
    host = 'mongodb://heroku_t6g31fxj:8u1g6iotm21eg7r11u6ai38j20@ds013495.mlab.com:13495/heroku_t6g31fxj'

connect("menus", host=host)
