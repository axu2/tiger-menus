import os
from app import app
from datetime import datetime, timedelta
from flask import render_template
from app.scrape import scrapeWeek, hallToId
from app.test_menus import b, l, d

minidays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

breakfastLists = b
lunchLists = l
dinnerLists = d

day = datetime.now()
nextWeek = []

title = "Tiger Menus"
message = ""


@app.before_first_request
def update():
    """Update global variables and database."""
    global breakfastLists
    global lunchLists
    global dinnerLists
    global nextWeek

    i = day.weekday()
    nextWeek = minidays[i:] + minidays[:i]

    # if os.getenv('HEROKU'):
    breakfastLists, lunchLists, dinnerLists = scrapeWeek(day)


@app.before_request
def checkForUpdate():
    """Check if day has changed."""
    global title
    global message
    title = os.getenv('TITLE') or "Tiger Menus"
    message = os.getenv('MESSAGE') or ""

    global day
    currentDay = datetime.now()
    if currentDay.weekday() != day.weekday():
        day = currentDay
        update()


@app.route('/<meal>/<int:i>')
def meal(meal, i):
    """Return meal HTML."""
    if meal == 'breakfast':
        l = breakfastLists[i]
    if meal == 'lunch':
        l = lunchLists[i]
    if meal == 'dinner':
        l = dinnerLists[i]

    return render_template("meal.html", meal=meal, i=i, nextWeek=nextWeek,
        title=title, message=message, cols=zip(hallToId.keys(), l))


@app.route('/')
def index():
    """Return homepage HTML. The displayed meal depends on time of day."""
    now = datetime.now()
    if now.hour < 14:
        return meal('lunch', 0)
    elif now.hour < 20:
        return meal('dinner', 0)
    else:
        return meal('lunch', 1)


@app.route('/breakfast')
def breakfast0():
    """Return breakfast/0 HTML for convenience."""
    return meal('breakfast', 0)


@app.route('/lunch')
def lunch0():
    """Return lunch/0 HTML for convenience."""
    return meal('lunch', 0)


@app.route('/dinner')
def dinner0():
    """Return dinner/0 HTML for convenience."""
    return meal('dinner', 0)


@app.route('/install')
def install():
    return render_template("install.html", message="Install Instructions")


@app.route('/about')
def about():
    return render_template("about.html", message="About")
