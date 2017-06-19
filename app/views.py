import requests
from bs4 import BeautifulSoup
from flask import render_template, redirect
import datetime
from app import app, db
import re
#from mongoengine import *
from flask_mongoengine.wtf import model_form

#connect("menus", host="mongodb://Arable:Arable@ds127982.mlab.com:27982/heroku_pbbvt44m")

class Item(db.EmbeddedDocument):
	item = db.StringField(required=True)
	legend = db.StringField()

class Menu(db.Document):
	date_modified = db.DateTimeField(default=datetime.datetime.now)
	lunch  = db.ListField(db.ListField(db.EmbeddedDocumentField(Item)))
	dinner = db.ListField(db.ListField(db.EmbeddedDocumentField(Item)))

@app.route('/form', methods=['GET', 'POST'])
def add_post():
    form = model_form(Menu)
    if form.validate():
        # add to DB
        redirect('done')
    return render_template('add_menu.html', form=form)

#database (lol)
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
minidays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

#today's menus
lunchList = [[] for x in range(6)]
dinnerList = [[] for x in range(6)]

#the last date checked
lastDate = datetime.datetime.today().weekday()

#the next 7 days
nextWeek = []
for i in range(7):
	nextWeek.append(minidays[lastDate+i])

#datetimes for this week
future = []
now = datetime.datetime.now()
for i in range(6):
	future.append(now + datetime.timedelta(days=i+1))

#scrape future days differently in case campus dining changes their format slightly so
#only part of the scraper will break
lunchFuture  = [[ [] for y in range(6) ] for x in range(6)]
dinnerFuture = [[ [] for y in range(6) ] for x in range(6)]

#######################################################################################

#find main entrees
def findMainEntrees(foodArray):
	if len(foodArray) > 1:
		foodBefore = []
		foodMain = []
		foodAfter = []

		before = True
		main = False
		after = False

		for item in foodArray:
			if main and item["item"][0] == '-' and not item["item"] == '-- Vegetarian & Vegan Entree --':
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

#scrape campus dining
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
				lunch  = True
			if string == 'Dinner':
				lunch  = False
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

		lunchArray[i] = findMainEntrees(lunchArray[i])
		dinnerArray[i] = findMainEntrees(dinnerArray[i])

#update database
def update():
	prefix = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?'

	roma    = prefix + 'locationNum=01'
	wucox   = prefix + 'locationNum=02'
	forbes  = prefix + 'locationNum=03'
	grad    = prefix + 'locationNum=04'
	cjl     = prefix + 'locationNum=05'
	whitman = prefix + 'locationNum=08'

	halls = [wucox, cjl, whitman, roma, forbes, grad]

	#update today
	global lunchList
	global dinnerList
	lunchList = [[] for x in range(6)]
	dinnerList = [[] for x in range(6)]
	scrape(halls, lunchList, dinnerList)

	#update future
	global lunchFuture
	global dinnerFuture
	lunchFuture  = [[ [] for y in range(6) ] for x in range(6)]
	dinnerFuture = [[ [] for y in range(6) ] for x in range(6)]

	#update nextWeek
	global nextWeek
	nextWeek = []
	for i in range(7):
		nextWeek.append(minidays[lastDate+i])

	for i in range(6):
		prefixFuture = prefix + 'myaction=read&dtdate={}%2F{}%2F{}'.format(future[i].month, future[i].day, future[i].year)

		roma    = prefixFuture + '&locationNum=01'
		wucox   = prefixFuture + '&locationNum=02'
		forbes  = prefixFuture + '&locationNum=03'
		grad    = prefixFuture + '&locationNum=04'
		cjl     = prefixFuture + '&locationNum=05'
		whitman = prefixFuture + '&locationNum=08'

		halls = [wucox, cjl, whitman, roma, forbes, grad]
		scrape(halls, lunchFuture[i], dinnerFuture[i])

	#mongoDB stuff
	count = Menu.objects.count()
	if count == 0:
		Menu(lunch=lunchList, dinner=dinnerList).save() #commit to MongoDB
	else:
		last = Menu.objects[count-1]
		#datetime.date objects are year, month, day only.
		oldDate = last.date_modified.date()
		newDate = datetime.datetime.now().date()
		if oldDate != newDate:
			Menu(lunch=lunchList, dinner=dinnerList).save()

#check if menus have changed
def checkForUpdate():
	global lastDate
	global future
	currentDay = datetime.datetime.today().weekday()
	if currentDay != lastDate:
		lastDate = currentDay
		now = datetime.datetime.now()
		for i in range(6):
			future[i] =  now + datetime.timedelta(days=i+1)
		update()

###########################################################################
#populate database when server starts
update()
###########################################################################

@app.route('/lunch0')
def lunch0():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[lastDate],
							nextWeek = nextWeek[1:],
							wucox   = lunchList[0],
							cjl     = lunchList[1],
							whitman = lunchList[2],
							roma    = lunchList[3],
							forbes  = lunchList[4],
							grad    = lunchList[5])

@app.route('/lunch1')
def lunch1():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[0].isoweekday()-1],
							nextWeek = nextWeek[1:],
							wucox   = lunchFuture[0][0],
							cjl     = lunchFuture[0][1],
							whitman = lunchFuture[0][2],
							roma    = lunchFuture[0][3],
							forbes  = lunchFuture[0][4],
							grad    = lunchFuture[0][5])

@app.route('/lunch2')
def lunch2():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[1].isoweekday()-1],
							nextWeek = nextWeek[1:],
							wucox   = lunchFuture[1][0],
							cjl     = lunchFuture[1][1],
							whitman = lunchFuture[1][2],
							roma    = lunchFuture[1][3],
							forbes  = lunchFuture[1][4],
							grad    = lunchFuture[1][5])

@app.route('/lunch3')
def lunch3():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[2].isoweekday()-1],
							nextWeek = nextWeek[1:],
							wucox   = lunchFuture[2][0],
							cjl     = lunchFuture[2][1],
							whitman = lunchFuture[2][2],
							roma    = lunchFuture[2][3],
							forbes  = lunchFuture[2][4],
							grad    = lunchFuture[2][5])

@app.route('/lunch4')
def lunch4():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[3].isoweekday()-1],
							nextWeek = nextWeek[1:],
							wucox   = lunchFuture[3][0],
							cjl     = lunchFuture[3][1],
							whitman = lunchFuture[3][2],
							roma    = lunchFuture[3][3],
							forbes  = lunchFuture[3][4],
							grad    = lunchFuture[3][5])

@app.route('/lunch5')
def lunch5():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[4].isoweekday()-1],
							nextWeek = nextWeek[1:],
							wucox   = lunchFuture[4][0],
							cjl     = lunchFuture[4][1],
							whitman = lunchFuture[4][2],
							roma    = lunchFuture[4][3],
							forbes  = lunchFuture[4][4],
							grad    = lunchFuture[4][5])

@app.route('/lunch6')
def lunch6():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[5].isoweekday()-1],
							nextWeek = nextWeek[1:],
							wucox   = lunchFuture[5][0],
							cjl     = lunchFuture[5][1],
							whitman = lunchFuture[5][2],
							roma    = lunchFuture[5][3],
							forbes  = lunchFuture[5][4],
							grad    = lunchFuture[5][5])

@app.route('/dinner0')
def dinner0():
	checkForUpdate()

	return render_template(	"meal.html",
							day     = days[lastDate],
							nextWeek = nextWeek[1:],
							wucox   = dinnerList[0],
							cjl     = dinnerList[1],
							whitman = dinnerList[2],
							roma    = dinnerList[3],
							forbes  = dinnerList[4],
							grad    = dinnerList[5])

@app.route('/dinner1')
def dinner1():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[0].isoweekday()-1],
							nextWeek = nextWeek[1:],
							wucox   = dinnerFuture[0][0],
							cjl     = dinnerFuture[0][1],
							whitman = dinnerFuture[0][2],
							roma    = dinnerFuture[0][3],
							forbes  = dinnerFuture[0][4],
							grad    = dinnerFuture[0][5])

@app.route('/dinner2')
def dinner2():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[1].isoweekday()-1],
							nextWeek = nextWeek[1:],
							wucox   = dinnerFuture[1][0],
							cjl     = dinnerFuture[1][1],
							whitman = dinnerFuture[1][2],
							roma    = dinnerFuture[1][3],
							forbes  = dinnerFuture[1][4],
							grad    = dinnerFuture[1][5])

@app.route('/dinner3')
def dinner3():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[2].isoweekday()-1],
							nextWeek = nextWeek[1:],
							wucox   = dinnerFuture[2][0],
							cjl     = dinnerFuture[2][1],
							whitman = dinnerFuture[2][2],
							roma    = dinnerFuture[2][3],
							forbes  = dinnerFuture[2][4],
							grad    = dinnerFuture[2][5])

@app.route('/dinner4')
def dinner4():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[3].isoweekday()-1],
							nextWeek = nextWeek[1:],
							wucox   = dinnerFuture[3][0],
							cjl     = dinnerFuture[3][1],
							whitman = dinnerFuture[3][2],
							roma    = dinnerFuture[3][3],
							forbes  = dinnerFuture[3][4],
							grad    = dinnerFuture[3][5])

@app.route('/dinner5')
def dinner5():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[4].isoweekday()-1],
							nextWeek = nextWeek[1:],
							wucox   = dinnerFuture[4][0],
							cjl     = dinnerFuture[4][1],
							whitman = dinnerFuture[4][2],
							roma    = dinnerFuture[4][3],
							forbes  = dinnerFuture[4][4],
							grad    = dinnerFuture[4][5])

@app.route('/dinner6')
def dinner6():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[5].isoweekday()-1],
							nextWeek = nextWeek[1:],
							wucox   = dinnerFuture[5][0],
							cjl     = dinnerFuture[5][1],
							whitman = dinnerFuture[5][2],
							roma    = dinnerFuture[5][3],
							forbes  = dinnerFuture[5][4],
							grad    = dinnerFuture[5][5])

#homepage will default
@app.route('/')
def index():
	now = datetime.datetime.now()
	if now.hour < 14:
		return lunch0()
	elif now.hour < 20:
		return dinner0()
	else:
		return lunch1()

@app.route('/lunch')
def lunch():
	return lunch0()

@app.route('/dinner')
def dinner():
	return dinner0()

@app.route('/about')
def about():
	return render_template(
	"index.html",
	day = days[lastDate],
	nextWeek = nextWeek[1:])

@app.route('/dinner/<int:month>/<int:day>/<int:year>')
def dinnerOld(month, day, year):
	query = datetime.date(year, month, day)
	for menu in Menu.objects:
		if menu.date_modified.date() == query:
			return render_template(
			"meal.html",
			day      = days[lastDate],
			nextWeek = nextWeek[1:],
			wucox    = menu.dinner[0],
			cjl      = menu.dinner[1],
			whitman  = menu.dinner[2],
			roma     = menu.dinner[3],
			forbes   = menu.dinner[4],
			grad     = menu.dinner[5]
			)
	return "Not found!"

@app.route('/lunch/<int:month>/<int:day>/<int:year>')
def lunchOld(month, day, year):
	query = datetime.date(year, month, day)
	for menu in Menu.objects:
		if menu.date_modified.date() == query:
			return render_template(
			"meal.html",
			day      = days[lastDate],
			nextWeek = nextWeek[1:],
			wucox    = menu.lunch[0],
			cjl      = menu.lunch[1],
			whitman  = menu.lunch[2],
			roma     = menu.lunch[3],
			forbes   = menu.lunch[4],
			grad     = menu.lunch[5]
			)
	return "Not found!"
