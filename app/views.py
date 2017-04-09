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
minidays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] 

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
#populate database when server starts
update()
###########################################################################

@app.route('/lunch')
def lunch():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[lastDate],
							zero    = minidays[lastDate+0],
							one     = minidays[lastDate+1],
							two     = minidays[lastDate+2],
							three   = minidays[lastDate+3],
							four    = minidays[lastDate+4],
							five    = minidays[lastDate+5],
							six     = minidays[lastDate+6], 
							wucox   = lunchList[0],
							cjl     = lunchList[1],
							whitman = lunchList[2],
							roma    = lunchList[3],
							forbes  = lunchList[4],
							grad    = lunchList[5])

@app.route('/lunch2')
def lunch2():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[0].isoweekday()-1],
							zero    = minidays[lastDate+0],
							one     = minidays[lastDate+1],
							two     = minidays[lastDate+2],
							three   = minidays[lastDate+3],
							four    = minidays[lastDate+4],
							five    = minidays[lastDate+5],
							six     = minidays[lastDate+6], 
							wucox   = lunchFuture[0][0],
							cjl     = lunchFuture[0][1],
							whitman = lunchFuture[0][2],
							roma    = lunchFuture[0][3],
							forbes  = lunchFuture[0][4],
							grad    = lunchFuture[0][5])

@app.route('/lunch3')
def lunch3():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[1].isoweekday()-1],
							zero    = minidays[lastDate+0],
							one     = minidays[lastDate+1],
							two     = minidays[lastDate+2],
							three   = minidays[lastDate+3],
							four    = minidays[lastDate+4],
							five    = minidays[lastDate+5],
							six     = minidays[lastDate+6],
							wucox   = lunchFuture[1][0],
							cjl     = lunchFuture[1][1],
							whitman = lunchFuture[1][2],
							roma    = lunchFuture[1][3],
							forbes  = lunchFuture[1][4],
							grad    = lunchFuture[1][5])

@app.route('/lunch4')
def lunch4():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[2].isoweekday()-1],
							zero    = minidays[lastDate+0],
							one     = minidays[lastDate+1],
							two     = minidays[lastDate+2],
							three   = minidays[lastDate+3],
							four    = minidays[lastDate+4],
							five    = minidays[lastDate+5],
							six     = minidays[lastDate+6],							
							wucox   = lunchFuture[2][0],
							cjl     = lunchFuture[2][1],
							whitman = lunchFuture[2][2],
							roma    = lunchFuture[2][3],
							forbes  = lunchFuture[2][4],
							grad    = lunchFuture[2][5])

@app.route('/lunch5')
def lunch5():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[3].isoweekday()-1],
							zero    = minidays[lastDate+0],
							one     = minidays[lastDate+1],
							two     = minidays[lastDate+2],
							three   = minidays[lastDate+3],
							four    = minidays[lastDate+4],
							five    = minidays[lastDate+5],
							six     = minidays[lastDate+6],
							wucox   = lunchFuture[3][0],
							cjl     = lunchFuture[3][1],
							whitman = lunchFuture[3][2],
							roma    = lunchFuture[3][3],
							forbes  = lunchFuture[3][4],
							grad    = lunchFuture[3][5])

@app.route('/lunch6')
def lunch6():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[4].isoweekday()-1],
							zero    = minidays[lastDate+0],
							one     = minidays[lastDate+1],
							two     = minidays[lastDate+2],
							three   = minidays[lastDate+3],
							four    = minidays[lastDate+4],
							five    = minidays[lastDate+5],
							six     = minidays[lastDate+6],
							wucox   = lunchFuture[4][0],
							cjl     = lunchFuture[4][1],
							whitman = lunchFuture[4][2],
							roma    = lunchFuture[4][3],
							forbes  = lunchFuture[4][4],
							grad    = lunchFuture[4][5])

@app.route('/lunch7')
def lunch7():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[5].isoweekday()-1],
							zero    = minidays[lastDate+0],
							one     = minidays[lastDate+1],
							two     = minidays[lastDate+2],
							three   = minidays[lastDate+3],
							four    = minidays[lastDate+4],
							five    = minidays[lastDate+5],
							six     = minidays[lastDate+6],
							wucox   = lunchFuture[5][0],
							cjl     = lunchFuture[5][1],
							whitman = lunchFuture[5][2],
							roma    = lunchFuture[5][3],
							forbes  = lunchFuture[5][4],
							grad    = lunchFuture[5][5])

@app.route('/dinner')
def dinner():
	checkForUpdate()

	return render_template(	"meal.html",
							day     = days[lastDate],
							zero    = minidays[lastDate+0],
							one     = minidays[lastDate+1],
							two     = minidays[lastDate+2],
							three   = minidays[lastDate+3],
							four    = minidays[lastDate+4],
							five    = minidays[lastDate+5],
							six     = minidays[lastDate+6],
							wucox   = dinnerList[0],
							cjl     = dinnerList[1],
							whitman = dinnerList[2],
							roma    = dinnerList[3],
							forbes  = dinnerList[4],
							grad    = dinnerList[5])

@app.route('/dinner2')
def dinner2():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[0].isoweekday()-1],
							zero    = minidays[lastDate+0],
							one     = minidays[lastDate+1],
							two     = minidays[lastDate+2],
							three   = minidays[lastDate+3],
							four    = minidays[lastDate+4],
							five    = minidays[lastDate+5],
							six     = minidays[lastDate+6],
							wucox   = dinnerFuture[0][0],
							cjl     = dinnerFuture[0][1],
							whitman = dinnerFuture[0][2],
							roma    = dinnerFuture[0][3],
							forbes  = dinnerFuture[0][4],
							grad    = dinnerFuture[0][5])

@app.route('/dinner3')
def dinner3():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[1].isoweekday()-1],
							zero    = minidays[lastDate+0],
							one     = minidays[lastDate+1],
							two     = minidays[lastDate+2],
							three   = minidays[lastDate+3],
							four    = minidays[lastDate+4],
							five    = minidays[lastDate+5],
							six     = minidays[lastDate+6],
							wucox   = dinnerFuture[1][0],
							cjl     = dinnerFuture[1][1],
							whitman = dinnerFuture[1][2],
							roma    = dinnerFuture[1][3],
							forbes  = dinnerFuture[1][4],
							grad    = dinnerFuture[1][5])

@app.route('/dinner4')
def dinner4():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[2].isoweekday()-1],
							zero    = minidays[lastDate+0],
							one     = minidays[lastDate+1],
							two     = minidays[lastDate+2],
							three   = minidays[lastDate+3],
							four    = minidays[lastDate+4],
							five    = minidays[lastDate+5],
							six     = minidays[lastDate+6],
							wucox   = dinnerFuture[2][0],
							cjl     = dinnerFuture[2][1],
							whitman = dinnerFuture[2][2],
							roma    = dinnerFuture[2][3],
							forbes  = dinnerFuture[2][4],
							grad    = dinnerFuture[2][5])

@app.route('/dinner5')
def dinner5():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[3].isoweekday()-1],
							zero    = minidays[lastDate+0],
							one     = minidays[lastDate+1],
							two     = minidays[lastDate+2],
							three   = minidays[lastDate+3],
							four    = minidays[lastDate+4],
							five    = minidays[lastDate+5],
							six     = minidays[lastDate+6],
							wucox   = dinnerFuture[3][0],
							cjl     = dinnerFuture[3][1],
							whitman = dinnerFuture[3][2],
							roma    = dinnerFuture[3][3],
							forbes  = dinnerFuture[3][4],
							grad    = dinnerFuture[3][5])

@app.route('/dinner6')
def dinner6():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[4].isoweekday()-1],
							zero    = minidays[lastDate+0],
							one     = minidays[lastDate+1],
							two     = minidays[lastDate+2],
							three   = minidays[lastDate+3],
							four    = minidays[lastDate+4],
							five    = minidays[lastDate+5],
							six     = minidays[lastDate+6],
							wucox   = dinnerFuture[4][0],
							cjl     = dinnerFuture[4][1],
							whitman = dinnerFuture[4][2],
							roma    = dinnerFuture[4][3],
							forbes  = dinnerFuture[4][4],
							grad    = dinnerFuture[4][5])

@app.route('/dinner7')
def dinner7():
	checkForUpdate()

	return render_template( "meal.html",
							day     = days[future[5].isoweekday()-1],
							zero    = minidays[lastDate+0],
							one     = minidays[lastDate+1],
							two     = minidays[lastDate+2],
							three   = minidays[lastDate+3],
							four    = minidays[lastDate+4],
							five    = minidays[lastDate+5],
							six     = minidays[lastDate+6],
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
		return lunch()
	#else:
	elif now.hour < 20:
		return dinner()
	else: 
		return lunch2()


