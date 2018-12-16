from datetime import datetime
from app import db


class Menu(db.Document):
    date_modified = db.DateTimeField(default=datetime.now)

    breakfast = db.ListField(db.ListField(db.StringField(required=True)))
    lunch = db.ListField(db.ListField(db.StringField(required=True)))
    dinner = db.ListField(db.ListField(db.StringField(required=True)))


class User(db.Document):
    email = db.StringField(max_length=40)
    prefs = db.ListField(db.StringField(max_length=40))

    def __unicode__(self):
        netid, domain = self.email.split('@')
        if domain == "princeton.edu":
            return netid
        else:
            return self.email


def getUser(netid):
    email = netid + '@princeton.edu'
    users = User.objects(email=email)
    user = None
    if users:
        user = User.objects(email=email).first()
    else:
        user = User(email=email)
        user.prefs.append('chicken parm')
        user.prefs.append('dim sum')
        user.prefs.append('egg roll')
        user.save()
    return user
