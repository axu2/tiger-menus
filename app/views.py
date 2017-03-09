import urllib2
from bs4 import BeautifulSoup

roma    = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=01'
wucox   = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=02'
forbes  = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=03'
grad    = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=04'
cjl     = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=05'
whitman = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=08'

halls = [wucox, cjl, whitman, roma, forbes, grad]
######################################################
from flask import render_template
from app import app

@app.route('/')
@app.route('/lunch')
def lunch():

	lunchList = [[] for x in range(6)]
	dinnerList = [[] for x in range(6)]
	lunch = False
	dinner = False

	for i in range(6):
		response = urllib2.urlopen(halls[i])
		html = response.read()
		soup = BeautifulSoup(html, 'html.parser')

		#repr?
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
	return render_template(
							"index.html", 
							wucox = lunchList[0],
							cjl = lunchList[1],
							whitman = lunchList[2],
							roma = lunchList[3],
							forbes = lunchList[4],
							grad = lunchList[5])
@app.route('/dinner')
def dinner():

	lunchList = [[] for x in range(6)]
	dinnerList = [[] for x in range(6)]
	lunch = False
	dinner = False

	for i in range(6):
		response = urllib2.urlopen(halls[i])
		html = response.read()
		soup = BeautifulSoup(html, 'html.parser')

		#repr?
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
	return render_template(	"index.html",
							wucox = dinnerList[0],
							cjl = dinnerList[1],
							whitman = dinnerList[2],
							roma = dinnerList[3],
							forbes = dinnerList[4],
							grad = lunchList[5]
							)
