import requests
from bs4 import BeautifulSoup
from flask import render_template
import datetime
from app import app
import re
import os
from .models import Menu, Item

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
        'Saturday', 'Sunday']
minidays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# today's menus
lunchList = [[] for x in range(6)]
dinnerList = [[] for x in range(6)]

# the last date checked
lastDate = datetime.datetime.today().weekday()

# the next 7 days
nextWeek = []
for i in range(7):
    nextWeek.append(minidays[(lastDate+i) % 7])

# datetimes for this week
future = []
now = datetime.datetime.now()
for i in range(6):
    future.append(now + datetime.timedelta(days=i+1))

# scrape future days differently in case campus dining changes their format
# slightly so only part of the scraper will break
lunchFuture = [[[] for y in range(6)] for x in range(6)]
dinnerFuture = [[[] for y in range(6)] for x in range(6)]


# find main entrees
def floatMainEntrees(foodArray):
    if len(foodArray) > 1:
        foodBefore = []
        foodMain = []
        foodAfter = []

        before = True
        main = False
        after = False

        for item in foodArray:
            v = '-- Vegetarian & Vegan Entree --'
            if main and item["item"][0] == '-' and not item["item"] == v:
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

        foodArray = [foodBefore[0]] + foodMain + foodBefore[1:] + foodAfter
        return foodArray
    else:
        return foodArray


# scrape campus dining
def scrape(halls, lunchArray, dinnerArray):
    lunch = False
    dinner = False

    for i in range(len(halls)):
        r = requests.get(halls[i])
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        tag_strings = soup.table.findAll('div')

        for tag in tag_strings:
            string = tag.get_text().strip()
            tag = unicode(tag)
            toAppend = []

            if string == 'Lunch':
                lunch = True
            if string == 'Dinner':
                lunch = False
                dinner = True

            if lunch:
                toAppend = lunchArray[i]
            if dinner:
                toAppend = dinnerArray[i]

            if len(string) > 0:
                if re.search("#0000FF", tag):
                    toAppend.append(Item(string, "vegan"))
                elif re.search("#00FF00", tag):
                    toAppend.append(Item(string, "vegetarian"))
                elif re.search("#8000FF", tag):
                    toAppend.append(Item(string, "pork"))
                else:
                    if string[0] == '-':
                        toAppend.append(Item(string, "label"))
                    else:
                        toAppend.append(Item(string, ""))

        lunch = False
        dinner = False

        lunchArray[i] = floatMainEntrees(lunchArray[i])
        dinnerArray[i] = floatMainEntrees(dinnerArray[i])


# update database
@app.before_first_request
def update():
    prefix = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?'

    roma = prefix + 'locationNum=01'
    wucox = prefix + 'locationNum=02'
    forbes = prefix + 'locationNum=03'
    grad = prefix + 'locationNum=04'
    cjl = prefix + 'locationNum=05'
    whitman = prefix + 'locationNum=08'

    halls = [wucox, cjl, whitman, roma, forbes, grad]

    # update today
    global lunchList
    global dinnerList
    lunchList = [[] for x in range(6)]
    dinnerList = [[] for x in range(6)]
    scrape(halls, lunchList, dinnerList)

    # update future
    global lunchFuture
    global dinnerFuture
    lunchFuture = [[[] for y in range(6)] for x in range(6)]
    dinnerFuture = [[[] for y in range(6)] for x in range(6)]

    # update nextWeek
    global nextWeek
    nextWeek = []
    for i in range(7):
        nextWeek.append(minidays[(lastDate+i) % 7])

    for i in range(6):
        p = prefix
        m = future[i].month
        d = future[i].day
        y = future[i].year
        prefixFuture = p + 'myaction=read&dtdate={}%2F{}%2F{}'.format(m, d, y)

        roma = prefixFuture + '&locationNum=01'
        wucox = prefixFuture + '&locationNum=02'
        forbes = prefixFuture + '&locationNum=03'
        grad = prefixFuture + '&locationNum=04'
        cjl = prefixFuture + '&locationNum=05'
        whitman = prefixFuture + '&locationNum=08'

        halls = [wucox, cjl, whitman, roma, forbes, grad]
        scrape(halls, lunchFuture[i], dinnerFuture[i])

    # mongoDB stuff
    count = Menu.objects.count()
    if count == 0:
        Menu(lunch=lunchList, dinner=dinnerList).save()
    else:
        last = Menu.objects[count-1]
        # datetime.date objects are year, month, day only.
        oldDate = last.date_modified.date()
        newDate = datetime.datetime.now().date()
        if oldDate != newDate:
            Menu(lunch=lunchList, dinner=dinnerList).save()


# check if menus have changed
@app.before_request
def checkForUpdate():
    global lastDate
    global future
    currentDay = datetime.datetime.today().weekday()
    if currentDay != lastDate:
        lastDate = currentDay
        now = datetime.datetime.now()
        for i in range(6):
            future[i] = now + datetime.timedelta(days=i+1)
        update()


@app.route('/lunch/0')
def lunch0():
    return render_template(
        "meal.html",
        day=days[lastDate],
        nextWeek=nextWeek[1:],
        wucox=lunchList[0],
        cjl=lunchList[1],
        whitman=lunchList[2],
        roma=lunchList[3],
        forbes=lunchList[4],
        grad=lunchList[5])


@app.route('/lunch/<int:i>')
def lunchF(i):
    if 0 < i and i < 7:
        return render_template(
            "meal.html",
            day=days[future[i-1].isoweekday()-1],
            nextWeek=nextWeek[1:],
            wucox=lunchFuture[i-1][0],
            cjl=lunchFuture[i-1][1],
            whitman=lunchFuture[i-1][2],
            roma=lunchFuture[i-1][3],
            forbes=lunchFuture[i-1][4],
            grad=lunchFuture[i-1][5])
    else:
        return "error"


@app.route('/dinner/0')
def dinner0():
    return render_template(
        "meal.html",
        day=days[lastDate],
        nextWeek=nextWeek[1:],
        wucox=dinnerList[0],
        cjl=dinnerList[1],
        whitman=dinnerList[2],
        roma=dinnerList[3],
        forbes=dinnerList[4],
        grad=dinnerList[5])


@app.route('/dinner/<int:i>')
def dinnerF(i):
    if 0 < i and i < 7:
        return render_template(
            "meal.html",
            day=days[future[0].isoweekday()-1],
            nextWeek=nextWeek[1:],
            wucox=dinnerFuture[i-1][0],
            cjl=dinnerFuture[i-1][1],
            whitman=dinnerFuture[i-1][2],
            roma=dinnerFuture[i-1][3],
            forbes=dinnerFuture[i-1][4],
            grad=dinnerFuture[i-1][5])
    else:
        return "error"


# homepage will default
@app.route('/')
def index():
    now = datetime.datetime.now()
    if now.hour < 14:
        return lunch0()
    elif now.hour < 20:
        return dinner0()
    else:
        return lunchF(1)


@app.route('/lunch')
def lunch():
    return lunch0()


@app.route('/dinner')
def dinner():
    return dinner0()


@app.route('/about')
def about():
    return render_template(
        "index.html", day=days[lastDate], nextWeek=nextWeek[1:])


@app.route('/dinner/<int:month>/<int:day>/<int:year>')
def dinnerOld(month, day, year):
    query = datetime.date(year, month, day)
    for menu in Menu.objects:
        if menu.date_modified.date() == query:
            return render_template(
                "meal.html",
                day=days[lastDate],
                nextWeek=nextWeek[1:],
                wucox=menu.dinner[0],
                cjl=menu.dinner[1],
                whitman=menu.dinner[2],
                roma=menu.dinner[3],
                forbes=menu.dinner[4],
                grad=menu.dinner[5])
    return "Not found!"


@app.route('/lunch/<int:month>/<int:day>/<int:year>')
def lunchOld(month, day, year):
    query = datetime.date(year, month, day)
    for menu in Menu.objects:
        if menu.date_modified.date() == query:
            return render_template(
                "meal.html",
                day=days[lastDate],
                nextWeek=nextWeek[1:],
                wucox=menu.lunch[0],
                cjl=menu.lunch[1],
                whitman=menu.lunch[2],
                roma=menu.lunch[3],
                forbes=menu.lunch[4],
                grad=menu.lunch[5])
    return "Not found!"
