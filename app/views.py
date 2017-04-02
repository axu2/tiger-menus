import urllib2
from bs4 import BeautifulSoup
from flask import render_template
import datetime
from app import app

#database (lol)
lunchList = [[] for x in range(6)]
dinnerList = [[] for x in range(6)]
lastDate = datetime.datetime.today().weekday()

tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
lunchTomorrow  = [[] for x in range(6)]
dinnerTomorrow = [[] for x in range(6)]

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

#######################################################################################

#scrape campus dining
def scrape(halls, lunchList, dinnerList):
	lunch = False
	dinner = False

	for i in range(len(halls)):
		response = urllib2.urlopen(halls[i])
		html = response.read()
		soup = BeautifulSoup(html, 'html.parser')

		for string in soup.stripped_strings:
			if string == 'Lunch':
				lunch  = True
			if string == 'Dinner':
				lunch  = False
				dinner = True
			if string == 'Powered by FoodPro':
				dinner = False
			if lunch:
				lunchList[i].append(string)
			if dinner:
				dinnerList[i].append(string)

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

	#update tomorrow
	prefixTomorrow = 'myaction=read&dtdate={}%2F{}%2F{}'.format(tomorrow.month, tomorrow.day, tomorrow.year)

	roma    = prefix + prefixTomorrow + '&locationNum=01'
	wucox   = prefix + prefixTomorrow + '&locationNum=02'
	forbes  = prefix + prefixTomorrow + '&locationNum=03'
	grad    = prefix + prefixTomorrow + '&locationNum=04'
	cjl     = prefix + prefixTomorrow + '&locationNum=05'
	whitman = prefix + prefixTomorrow + '&locationNum=08'
	
	halls = [wucox, cjl, whitman, roma, forbes, grad]

	global lunchTomorrow
	global dinnerTomorrow
	lunchTomorrow = [[] for x in range(6)]
	dinnerTomorrow = [[] for x in range(6)]
	scrape(halls, lunchTomorrow, dinnerTomorrow)

#check if menus have changed
def checkForUpdate():
	global lastDate
	global tomorrow
	currentDay = datetime.datetime.today().weekday()
	if currentDay != lastDate:
		lastDate = currentDay
		tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
		update()

###########################################################################
#scrape when server starts
update()
###########################################################################

@app.route('/lunch')
def lunch():
	checkForUpdate()

	return render_template( "meal.html",
							day = days[lastDate],
							wucox = lunchList[0],
							cjl = lunchList[1],
							whitman = lunchList[2],
							roma = lunchList[3],
							forbes = lunchList[4],
							grad = lunchList[5])

@app.route('/lunch2')
def lunch2():
	checkForUpdate()

	return render_template( "meal.html",
							day = days[tomorrow.isoweekday()-1],
							wucox = lunchTomorrow[0],
							cjl = lunchTomorrow[1],
							whitman = lunchTomorrow[2],
							roma = lunchTomorrow[3],
							forbes = lunchTomorrow[4],
							grad = lunchTomorrow[5])


@app.route('/dinner')
def dinner():
	checkForUpdate()

	return render_template(	"meal.html",
							day = days[lastDate],
							wucox = dinnerList[0],
							cjl = dinnerList[1],
							whitman = dinnerList[2],
							roma = dinnerList[3],
							forbes = dinnerList[4],
							grad = dinnerList[5])

@app.route('/dinner2')
def dinner2():
	checkForUpdate()

	return render_template( "meal.html",
							day = days[tomorrow.isoweekday()-1],
							wucox = dinnerTomorrow[0],
							cjl = dinnerTomorrow[1],
							whitman = dinnerTomorrow[2],
							roma = dinnerTomorrow[3],
							forbes = dinnerTomorrow[4],
							grad = dinnerTomorrow[5])

#homepage will default
@app.route('/')
def index():
	now = datetime.datetime.now()
	if now.hour < 14:
		return lunch()
	else:
	#elif now.hour < 20:
		return dinner()
	#else: 
	#	return lunch2()


