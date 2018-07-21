from datetime import datetime
from app import db


class Menu(db.Document):
    date_modified = db.DateTimeField(default=datetime.now)

    breakfast = db.ListField(db.ListField(db.StringField(required=True)))
    lunch = db.ListField(db.ListField(db.StringField(required=True)))
    dinner = db.ListField(db.ListField(db.StringField(required=True)))
