import os
from flask import Flask
from bson import ObjectId
from flask_cors import CORS
from datetime import datetime
from flask.json import JSONEncoder
from mongoengine import connect, Document, QuerySet, EmbeddedDocument


class FlaskJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, QuerySet):
            return [doc for doc in o]
        elif isinstance(o, Document):
            return o.to_mongo()
        elif isinstance(o, EmbeddedDocument):
                return o.to_mongo()
        elif isinstance(o, ObjectId):
            return str(o)
        else:
            return JSONEncoder.default(self, o)

app = Flask(__name__)
CORS(app)
app.json_encoder = FlaskJSONEncoder
from app import views   # noqa

if os.getenv('MONGODB_URI'):
    connect("menus", host=os.getenv('MONGODB_URI'))
