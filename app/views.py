roma    = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=01'
wucox   = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=02'
forbes  = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=03'
grad    = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=04'
cjl     = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=05'
whitman = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=08'

halls = [wucox, whitman, cjl]

import urllib2
from bs4 import BeautifulSoup

wucoxLunch = []
wucoxDinner = []

cjlLunch = []
cjlDinner = []

#####################################################
response = urllib2.urlopen(wucox)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')

lunch = False
dinner = False

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
		wucoxLunch.append(string)
	if dinner:
		wucoxDinner.append(string)
#####################################################
response = urllib2.urlopen(cjl)
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
		cjlLunch.append(string)
	if dinner:
		cjlDinner.append(string)
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
                           food1 = wucoxLunch,
                           food2 = cjlLunch)

@app.route('/dinner')
def dinner():
    user = {'nickname': 'Ready for Dinner?'}  # fake user
    return render_template("index.html",
                           title='Lunch',
                           user=user,
                           food1 = wucoxDinner,
                           food2 = cjlDinner)
