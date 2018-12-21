from app import views
# messy

def compose_email(matches):
    from datetime import datetime
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
            'Saturday', 'Sunday']

    days = [ "-- " + day + " --\n" for day in days]
    title = ["Breakfast", "Lunch", "Dinner"]

    now = datetime.now()
    lastDate = now.weekday()
    week = [days[(lastDate + i) % 7] for i in range(7)]

    text = "Your weekly meals digest:\n\n"

    for i in range(7):
        if matches[i] != [[] for i in range(3)]:
            text += week[i] + "\n"
            for j, meal in enumerate(matches[i]):
                if meal != []:
                    text += title[j] + ":\n"
                    for food, hall in meal:
                        text += food + " in " + hall + "\n"
                    text += "\n"

    text += "Best,\n\nAlex Xu '20\n"

    return text

def getMatches(user):
    l = [
        views.breakfastLists,
        views.lunchLists,
        views.dinnerLists
    ]

    halls = ['Butler', 'CJL', 'Whitman', 'Roma', 'Forbes', 'Grad']
    matches = [[[] for i in range(3)] for j in range(7)]

    for k, mealListList in enumerate(l):
        for j, mealList in enumerate(mealListList): #each day
            for i, hall in enumerate(mealList): #each hall
                for food in hall:
                    for pref in user.prefs:
                        if pref.lower() in food.lower():
                            p = (food, halls[i])
                            if p not in matches[j][k]:
                                matches[j][k].append(p)

    return matches