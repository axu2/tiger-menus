import os
import emails
import requests
from mongoengine import connect
from app.models import User
from app.compose import compose_email, getMatches
from app import dummy

connect("users", host=os.getenv('MONGODB_URI') or dummy)

for user in User.objects():
    matches = getMatches(user)
    if matches != [[] for i in range(7)]:
        text = compose_email(matches)

        message = emails.html(text=text,
                              subject='Meals Mail',
                              mail_from='tigermenu@gmail.com')

        smtp = {'host':'smtp.googlemail.com',
                'port': 465,
                'ssl': True,
                'user': 'tigermenu',
                'password': os.getenv('MAIL_PASSWORD')}
        r = message.send(to=user.email, smtp=smtp)

        assert r.status_code == 250