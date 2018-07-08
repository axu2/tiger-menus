from datetime import datetime
from app import db


class Item(db.EmbeddedDocument):
    item = db.StringField(required=True)
    legend = db.StringField()


class Menu(db.Document):
    date_modified = db.DateTimeField(default=datetime.now)

    breakfast = db.ListField(db.ListField(db.EmbeddedDocumentField(Item)))
    lunch = db.ListField(db.ListField(db.EmbeddedDocumentField(Item)))
    dinner = db.ListField(db.ListField(db.EmbeddedDocumentField(Item)))
