from datetime import datetime
from app import db


class Menu(db.Document):
    date_modified = db.DateTimeField(default=datetime.now)

    breakfast = db.ListField(db.ListField(db.StringField(required=True)))
    lunch = db.ListField(db.ListField(db.StringField(required=True)))
    dinner = db.ListField(db.ListField(db.StringField(required=True)))


class User(db.Document):
    email = db.StringField(unique=True, max_length=40)
    prefs = db.ListField(db.StringField(max_length=40), default=lambda:["chicken parm", "dim sum", "spring roll"])

    def __unicode__(self):
        netid, domain = self.email.split('@')
        if domain == "princeton.edu":
            return netid
        else:
            return self.email


def getUser(netid):
    email = netid + '@princeton.edu'
    # lol race conditions
    # probably a better way to do this
    try:
        return User.objects(email=email).get()
    except:
        try:
            return User(email=email).save()
        except:
            return User.objects(email=email).get()
