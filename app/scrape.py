import requests
from datetime import timedelta
from bs4 import BeautifulSoup
from collections import OrderedDict


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
    breakfast = ["No Data Available"]
    lunch = ["No Data Available"]
    dinner = ["No Data Available"]

    b = "Breakfast"
    l = "Lunch"
    d = ["Dinner", "Din"]

    try:
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        for card in soup.findAll(class_="card"):
            mealName = card.find(class_='card-header').contents[0].strip()
            items = card.find(class_='card-body').findAll(class_=["mealStation", "title"])
            formatted_items = []
            for item in items:
                if 'mealStation' in item['class']:
                    formatted_items.append(f"-- {item.text.strip()} --")
                else:
                    formatted_items.append(item.text.strip())
            items = floatMainEntrees(formatted_items)
            if mealName == b:
                breakfast = [b] + items
            elif mealName == l:
                lunch = [l] + items
            elif mealName in d:
                dinner = ["Dinner"] + items
    except Exception as e:
        print(e)
        pass

    return breakfast, lunch, dinner


hallToId = OrderedDict([
    ('Wu / Wilcox', '02'),
    ('CJL',         '05'),
    ('Whitman',     '08'),
    ('Ro / Ma',     '01'),
    ('Forbes',      '03'),
    ('Yeh',         '06'),
    ('Grad',        '04'),
])


def scrapeDay(m, d, y):
    dayBreakfast = []
    dayLunch = []
    dayDinner = []

    prefix = "https://menus.princeton.edu/dining/_Foodpro/online-menu/menuDetails.asp?myaction=read&"
    prefix += "dtdate={}%2F{}%2F{}&locationNum=".format(m, d, y)

    halls = [prefix + i for i in hallToId.values()]

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
        breakfast, lunch, dinner = scrapeDay(m, d, y)
        weekBreakfast.append(breakfast)
        weekLunch.append(lunch)
        weekDinner.append(dinner)

    return weekBreakfast, weekLunch, weekDinner

