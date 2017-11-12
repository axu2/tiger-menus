from app import app, Comment, CommentForm, db
from .models import Menu, Item
from datetime import datetime, timedelta
from flask import render_template, jsonify, request
from mongoengine import MultipleObjectsReturned, DoesNotExist

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
        'Saturday', 'Sunday']
minidays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

lunchLists = [[[] for y in range(6)] for x in range(7)]
dinnerLists = [[[] for y in range(6)] for x in range(7)]

now = datetime.now()
lastDate = now.weekday()
nextWeek = [minidays[(lastDate + i) % 7] for i in range(7)]
future = [now + timedelta(days=i) for i in range(7)]


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


def scrape(halls, lunchList, dinnerList):
    """Scrape one day of campus dining."""
    import requests
    from bs4 import BeautifulSoup

    lunch = False
    dinner = False

    for i, url in enumerate(halls):
        html = requests.get(url).text
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
                toAppend = lunchList[i]
            if dinner:
                toAppend = dinnerList[i]

            if len(string) > 0:
                if "#0000FF" in tag:
                    toAppend.append(Item(string, "vegan"))
                elif "#00FF00" in tag:
                    toAppend.append(Item(string, "vegetarian"))
                elif "#8000FF" in tag:
                    toAppend.append(Item(string, "pork"))
                else:
                    if string[0] == '-':
                        toAppend.append(Item(string, "label"))
                    else:
                        toAppend.append(Item(string, ""))

        lunch = False
        dinner = False

        lunchList[i] = floatMainEntrees(lunchList[i])
        dinnerList[i] = floatMainEntrees(dinnerList[i])


#@app.before_first_request
def update():
    """Update global variables and database."""
    global lunchLists
    global dinnerLists
    global nextWeek

    lunchLists = [[[] for y in range(6)] for x in range(7)]
    dinnerLists = [[[] for y in range(6)] for x in range(7)]
    nextWeek = [minidays[(lastDate+i) % 7] for i in range(7)]

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
        scrape(halls, lunchLists[i], dinnerLists[i])

    now = datetime.now()
    start = datetime(now.year, now.month, now.day)
    end = start + timedelta(days=1)
    if not Menu.objects(date_modified__gte=start, date_modified__lt=end):
        Menu(lunch=lunchLists[0], dinner=dinnerLists[0]).save()


#@app.before_request
def checkForUpdate():
    """Check if day has changed."""
    global lastDate
    global future
    now = datetime.now()
    currentDay = now.weekday()
    if currentDay != lastDate:
        lastDate = currentDay
        future = [now + timedelta(days=i) for i in range(7)]
        update()


def getComment(request):
    comment = Comment()
    success = False

    if request.method == 'POST':
        form = CommentForm(request.form, obj=comment)
        if form.validate():
            form.populate_obj(comment)
            db.session.add(comment)
            db.session.commit()
            success = True
    else:
        form = CommentForm(obj=comment)

    return comment, success, form

@app.route('/lunch/<int:i>', methods=['GET', 'POST'])
def lunch(i):
    """Return lunch HTML."""
    comment, success, form = getComment(request)

    return render_template(
        "meal.html",
        form=form,
        success=success,
        comments=Comment.query.order_by(Comment.timestamp.asc()),
        day=days[future[i].weekday()],
        nextWeek=nextWeek[1:],
        wucox=lunchLists[i][0],
        cjl=lunchLists[i][1],
        whitman=lunchLists[i][2],
        roma=lunchLists[i][3],
        forbes=lunchLists[i][4],
        grad=lunchLists[i][5])



@app.route('/dinner/<int:i>', methods=['GET', 'POST'])
def dinner(i):
    """Return dinner HTML."""
    comment, success, form = getComment(request)

    return render_template(
        "meal.html",
        form=form,
        success=success,
        comments=Comment.query.order_by(Comment.timestamp.asc()),
        day=days[future[i].weekday()],
        nextWeek=nextWeek[1:],
        wucox=dinnerLists[i][0],
        cjl=dinnerLists[i][1],
        whitman=dinnerLists[i][2],
        roma=dinnerLists[i][3],
        forbes=dinnerLists[i][4],
        grad=dinnerLists[i][5])



@app.route('/')
def index():
    """Return homepage HTML. The displayed meal depends on time of day."""
    now = datetime.now()
    if now.hour < 14:
        return lunch(0)
    elif now.hour < 20:
        return dinner(0)
    else:
        return lunch(1)


@app.route('/lunch')
def lunch0():
    """Return lunch/0 HTML for convenience."""
    return lunch(0)


@app.route('/dinner')
def dinner0():
    """Return dinner/0 HTML for convenience."""
    return dinner(0)


@app.route('/about')
def about():
    """Return about page HTML."""
    return render_template(
        "index.html", day=days[lastDate], nextWeek=nextWeek[1:])


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
