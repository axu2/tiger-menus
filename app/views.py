import os
from app import app
from .models import Menu, Item
from datetime import datetime, timedelta
from flask import render_template, jsonify
from mongoengine import MultipleObjectsReturned, DoesNotExist

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
        'Saturday', 'Sunday']
minidays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

breakfastLists = [[[] for y in range(6)] for x in range(7)]
lunchLists = [[[] for y in range(6)] for x in range(7)]
dinnerLists = [[[] for y in range(6)] for x in range(7)]

now = datetime.now()
lastDate = now.weekday()
nextWeek = [minidays[(lastDate + i) % 7] for i in range(7)]
future = [now + timedelta(days=i) for i in range(7)]

title = "Tiger Menus"
message = ""


def floatMainEntrees(foodList):
    """Return foodList with main entrees at the top."""
    if len(foodList) > 1:
        foodBefore = []
        foodMain = []
        foodAfter = []

        before = True
        main = False
        after = False

        for item in foodList:
            more = ['-- Vegetarian & Vegan Entree --', '-- Euro Special --']
            if main and item["item"][0] == '-' and not item["item"] in more:
                main = False
                after = True
            if item["item"] == '-- Main Entree --':
                main = True
                before = False
            if before:
                foodBefore.append(item)
            if main:
                foodMain.append(item)
            if after:
                foodAfter.append(item)

        foodList = [foodBefore[0]] + foodMain + foodBefore[1:] + foodAfter

    return foodList


def scrape(halls, breakfastList, lunchList, dinnerList):
    """Scrape one day of campus dining."""
    import requests
    from bs4 import BeautifulSoup

    for i, url in enumerate(halls):
        breakfast = False
        lunch = False
        dinner = False

        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')

        for tag in soup.table.findAll('div'):
            string = tag.get_text().strip()
            tag = unicode(tag)
            toAppend = []

            if string == 'Breakfast':
                breakfast = True
            if string == 'Lunch':
                breakfast = False
                lunch = True
            if string == 'Dinner':
                breakfast = False
                lunch = False
                dinner = True

            if breakfast:
                toAppend = breakfastList[i]
            if lunch:
                toAppend = lunchList[i]
            if dinner:
                toAppend = dinnerList[i]

            if string:
                if "#0000FF" in tag:
                    toAppend.append(Item(string, "vegan"))
                elif "#00FF00" in tag:
                    toAppend.append(Item(string, "vegetarian"))
                elif "#8000FF" in tag:
                    toAppend.append(Item(string, "pork"))
                elif "#FF0000" in tag:
                    toAppend.append(Item(string, "halal"))
                else:
                    if string[0] == '-':
                        toAppend.append(Item(string, "label"))
                    else:
                        toAppend.append(Item(string, ""))

        breakfastList[i] = floatMainEntrees(breakfastList[i])
        lunchList[i] = floatMainEntrees(lunchList[i])
        dinnerList[i] = floatMainEntrees(dinnerList[i])


@app.before_first_request
def update():
    """Update global variables and database."""
    global breakfastLists
    global lunchLists
    global dinnerLists
    global nextWeek

    breakfastLists = [[[] for y in range(6)] for x in range(7)]
    lunchLists = [[[] for y in range(6)] for x in range(7)]
    dinnerLists = [[[] for y in range(6)] for x in range(7)]
    nextWeek = [minidays[(lastDate+i) % 7] for i in range(7)]

    if os.getenv('TZ'):
        for i in range(7):
            p = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?'
            m = future[i].month
            d = future[i].day
            y = future[i].year
            prefix = p + 'myaction=read&dtdate={}%2F{}%2F{}'.format(m, d, y)

            roma = prefix + '&locationNum=01'
            wucox = prefix + '&locationNum=02'
            forbes = prefix + '&locationNum=03'
            grad = prefix + '&locationNum=04'
            cjl = prefix + '&locationNum=05'
            whitman = prefix + '&locationNum=08'

            halls = [wucox, cjl, whitman, roma, forbes, grad]
            scrape(halls, breakfastLists[i], lunchLists[i], dinnerLists[i])

    now = datetime.now()
    start = datetime(now.year, now.month, now.day)
    end = start + timedelta(days=1)
    if not Menu.objects(date_modified__gte=start, date_modified__lt=end):
        Menu(breakfast=breakfastLists[0], lunch=lunchLists[0], dinner=dinnerLists[0]).save()


@app.before_request
def checkForUpdate():
    """Check if day has changed."""
    global title
    global message
    title = os.getenv('TITLE') or "Tiger Menus"
    message = os.getenv('MESSAGE') or ""

    global lastDate
    global future
    now = datetime.now()
    currentDay = now.weekday()
    if currentDay != lastDate:
        lastDate = currentDay
        future = [now + timedelta(days=i) for i in range(7)]
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

@app.route('/api2')
def api3():
    """Return week's menus in JSON."""
    return jsonify([breakfastLists, lunchLists, dinnerLists])


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


@app.route('/about')
def about():
    """Return about page HTML."""
    return render_template(
        "index.html", meal='dinner',
        title=title, message=message,
        i=0, day=days[lastDate], nextWeek=nextWeek)


@app.route('/api/<int:month>/<int:day>/<int:year>')
def api(month, day, year):
    """Return past menu JSON from database."""
    start = datetime(year, month, day)
    end = start + timedelta(days=1)
    menu = Menu.objects.get(date_modified__gte=start, date_modified__lt=end)
    return jsonify(menu)


@app.route('/api/<int:m0>/<int:d0>/<int:y0>/<int:m1>/<int:d1>/<int:y1>')
def api2(m0, d0, y0, m1, d1, y1):
    """Return past menu JSON from database."""
    start = datetime(y0, m0, d0)
    end = datetime(y1, m1, d1)
    menus = Menu.objects(date_modified__gte=start, date_modified__lte=end)
    return jsonify(menus)


@app.errorhandler(DoesNotExist)
def handle_does_not_exist(e):
    """MongoEngine `DoesNotExist` error handler."""
    payload = {
        'reason': type(e).__name__,
        'description': e.message
    }
    return jsonify(payload), 404


@app.errorhandler(MultipleObjectsReturned)
def handle_multiple_objects_returned(e):
    """MongoEngine `MultipleObjectsReturned` error handler."""
    payload = {
        'reason': 'Database problem please use contact form on homepage',
        'description': e.message
    }
    return jsonify(payload), 500
