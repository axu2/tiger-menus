import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


def floatMainEntrees(items):
    """Return items with main entrees at the top."""
    itemsMain = []
    itemsEntree = []
    itemsAfter = []

    main = False
    entree = True

    for item in items:
        if 'Main Entree' in item:
            main = True
            entree = False
        elif "Entree" in item:
            main = False
            entree = True
        elif "--" in item:
            main = False
            entree = False

        if main:
            itemsMain.append(item)
        elif entree:
            itemsEntree.append(item)
        else:
            itemsAfter.append(item)
    return itemsMain + itemsEntree + itemsAfter


def scrapeHall(url):
    breakfast = []
    lunch = []
    dinner = []

    b = "Breakfast"
    l = "Lunch"
    d = "Dinner"

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    for card in soup.findAll(class_="card"):
        mealName = card.h5.text
        items = floatMainEntrees(list(card.ul.stripped_strings))
        if mealName == b:
            breakfast = [b] + items
        elif mealName == l:
            lunch = [l] + items
        elif mealName == d:
            dinner = [d] + items

    return breakfast, lunch, dinner


def scrapeDay(m, d, y):
    dayBreakfast = []
    dayLunch = []
    dayDinner = []

    prefix = "https://menus.princeton.edu/dining/_Foodpro/online-menu/menuDetails.asp?"
    prefix += "dtdate={}%2F{}%2F{}&locationNum=".format(m, d, y)

    # For reference
    hallId = {
        'roma' : '01',
        'wucox': '02',
        'forbes' : '03',
        # 'grad' : '04',
        # 'cjl' : '05',
        'whitman' : '08'
    }
    halls = [prefix + i for i in ('02', '08', '01', '03')]
    # halls = [prefix + i for i in ('02', '05', '08', '01', '03', '04')]

    for hall in halls:
        breakfast, lunch, dinner = scrapeHall(hall)
        dayBreakfast.append(breakfast)
        dayLunch.append(lunch)
        dayDinner.append(dinner)

    return dayBreakfast, dayLunch, dayDinner


def scrapeWeek(dt):
    weekBreakfast = []
    weekLunch = []
    weekDinner = []

    for i in range(7):
        day = dt + timedelta(days=i)
        m, d, y = day.month, day.day, day.year
        breakfast, lunch, dinner = scrapeDay(m,d,y)
        weekBreakfast.append(breakfast)
        weekLunch.append(lunch)
        weekDinner.append(dinner)

    return weekBreakfast, weekLunch, weekDinner
