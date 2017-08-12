from flask import Flask
from mongoengine import connect
import os

app = Flask(__name__)
from app import views   # noqa

connect("menus", host=os.getenv('MONGODB_URI'))
