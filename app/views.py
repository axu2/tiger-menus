import urllib2
from bs4 import BeautifulSoup
from flask import render_template
import datetime
from app import app

#database (lol)
lunchList = [[] for x in range(6)]
dinnerList = [[] for x in range(6)]
lastDate = datetime.datetime.today().weekday()

future = []
for i in range(6):
	future.append(datetime.datetime.now() + datetime.timedelta(days=i+1))

lunchFuture  = [[ [] for y in range(6) ] for x in range(6)]
dinnerFuture = [[ [] for y in range(6) ] for x in range(6)]

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

	#update future
	global lunchFuture
	global dinnerFuture
	lunchFuture  = [[ [] for y in range(6) ] for x in range(6)]
	dinnerFuture = [[ [] for y in range(6) ] for x in range(6)]

	for i in range(6):
		prefixFuture = 'myaction=read&dtdate={}%2F{}%2F{}'.format(future[i].month, future[i].day, future[i].year)

		roma    = prefix + prefixFuture + '&locationNum=01'
		wucox   = prefix + prefixFuture + '&locationNum=02'
		forbes  = prefix + prefixFuture + '&locationNum=03'
		grad    = prefix + prefixFuture + '&locationNum=04'
		cjl     = prefix + prefixFuture + '&locationNum=05'
		whitman = prefix + prefixFuture + '&locationNum=08'
		
		halls = [wucox, cjl, whitman, roma, forbes, grad]
		scrape(halls, lunchFuture[i], dinnerFuture[i])

#check if menus have changed
def checkForUpdate():
	global lastDate
	global future
	currentDay = datetime.datetime.today().weekday()
	if currentDay != lastDate:
		lastDate = currentDay
		for i in range(6):
			future[i] = datetime.datetime.now() + datetime.timedelta(days=i+1)
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
							day = days[future[0].isoweekday()-1],
							wucox = lunchFuture[0][0],
							cjl = lunchFuture[0][1],
							whitman = lunchFuture[0][2],
							roma = lunchFuture[0][3],
							forbes = lunchFuture[0][4],
							grad = lunchFuture[0][5])


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
							day = days[future[0].isoweekday()-1],
							wucox = dinnerFuture[0][0],
							cjl = dinnerFuture[0][1],
							whitman = dinnerFuture[0][2],
							roma = dinnerFuture[0][3],
							forbes = dinnerFuture[0][4],
							grad = dinnerFuture[0][5])

#homepage will default
@app.route('/')
def index():
	now = datetime.datetime.now()
	if now.hour < 14:
		return lunch()
	#else:
	elif now.hour < 20:
		return dinner()
	else: 
		return lunch2()


