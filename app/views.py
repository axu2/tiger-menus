import urllib2
from bs4 import BeautifulSoup

roma    = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=01'
wucox   = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=02'
forbes  = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=03'
cjl     = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=05'
whitman = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=08'

halls = [wucox, cjl, whitman]

lunchList  = [[]]*3
dinnerList = [[]]*3
lunch = False
dinner = False

for i in range(3):
	if i == 0:
		response = urllib2.urlopen(wucox)
	if i == 1:
		response = urllib2.urlopen(cjl)
	if i == 2:
		response = urllib2.urlopen(whitman)
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
######################################################
from flask import render_template
from app import app

@app.route('/')
@app.route('/lunch')
def lunch():
    user = {'nickname': 'Ready for Lunch?'}  # fake user
    return render_template("index.html",
                           title='Lunch',
                           user=user,
                           wucox = lunchList[0],
                           cjl = lunchList[1],
						   whitman = lunchList[2])

@app.route('/dinner')
def dinner():
    user = {'nickname': 'Ready for Dinner?'}  # fake user
    return render_template("index.html",
                           title='Lunch',
                           user=user,
                           wucox = dinnerList[0],
                           cjl = dinnerList[1],
						   whitman = dinnerList[2])
