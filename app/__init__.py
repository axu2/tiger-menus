import os
from flask import Flask
from bson import ObjectId
from flask_cors import CORS
from datetime import datetime
from flask.json import JSONEncoder
from mongoengine import connect, Document, QuerySet

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from wtforms_sqlalchemy.orm import model_form


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

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ynhhvyxupixyii:7052707d2f2fdbfb11274af178a04674913051243eaff26885a7e6c6ace0ae3c@ec2-184-72-248-8.compute-1.amazonaws.com:5432/dua854a3rg0o'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140))
    author = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime(), default=datetime.now, index=True)

CommentForm = model_form(Comment)

from app import views   # noqa

dummy = 'mongodb://heroku_t6g31fxj:8u1g6iotm21eg7r11u6ai38j20@ds013495.mlab.com:13495/heroku_t6g31fxj'
host = os.getenv('MONGODB_URI', default=dummy)
connect("menus", host=host)
