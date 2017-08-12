from datetime import datetime
from mongoengine import (EmbeddedDocument, Document,
                         ListField, StringField, DateTimeField,
                         EmbeddedDocumentField)


class Item(EmbeddedDocument):
    item = StringField(required=True)
    legend = StringField()


class Menu(Document):
    date_modified = DateTimeField(default=datetime.now)
    lunch = ListField(ListField(EmbeddedDocumentField(Item)))
    dinner = ListField(ListField(EmbeddedDocumentField(Item)))
