import os
from app import app, cas
from .models import Menu, getUser
from datetime import datetime, timedelta
from flask import render_template
from app.scrape import scrapeWeek
from app.test_menus import b, l, d

minidays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

breakfastLists = b
lunchLists = l
dinnerLists = d

day = datetime.now()
nextWeek = [minidays[(day.weekday() + i) % 7] for i in range(7)]

title = "Tiger Menus"
message = ""


@app.before_first_request
def update():
    """Update global variables and database."""
    global breakfastLists
    global lunchLists
    global dinnerLists
    global nextWeek

    nextWeek = [minidays[(day.weekday()+i) % 7] for i in range(7)]

    if os.getenv('HEROKU'):
        breakfastLists, lunchLists, dinnerLists = scrapeWeek(day)

        start = datetime(day.year, day.month, day.day)
        end = start + timedelta(days=1)
        if not Menu.objects(date_modified__gte=start, date_modified__lt=end):
            Menu(breakfast=breakfastLists[0],
                lunch=lunchLists[0],
                dinner=dinnerLists[0]).save()


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

    l2 = ['Wu / Wilcox', 'CJL', 'Whitman', 'Ro / Ma', 'Forbes', 'Grad']

    l3 = [(l2[j], l[j]) for j in range(6)]

    return render_template("meal.html", meal=meal, i=i, nextWeek=nextWeek,
        title=title, message=message, l=l3)


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

@app.route('/landing')
def landing():
    """Return homepage HTML."""
    return render_template("landing.html",
        title=title, message=message,
        i=0, nextWeek=nextWeek)

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


@app.route('/about')
def about():
    """Return about page HTML."""
    return render_template(
        "index.html",
        title=title, message=message,
        i=0, nextWeek=nextWeek)

@app.route('/install')
def install():
    """Return install page HTML."""
    return render_template(
        "install.html",
        title=title, message=message,
        i=0, nextWeek=nextWeek)
