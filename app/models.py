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


# many-to-many SQL implementation 

# prefs = db.Table('prefs',
#     db.Column('food_id', db.Integer, db.ForeignKey('food.id'), primary_key=True),
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
# )


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     foods = db.relationship('Food', secondary=prefs, lazy='subquery',
#         backref=db.backref('users', lazy=True))

#     def __repr__(self):
#         return '<User {}>'.format(self.email)


# class Food(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), index=True, unique=True)

#     def __repr__(self):
#         return '<Food {}>'.format(self.name)
