from app import app
from datetime import datetime, timedelta
from app.models import Menu
from flask import jsonify
from app import views

@app.route('/api/<int:month>/<int:day>/<int:year>')
def api(month, day, year):
    """Return past menu JSON from database."""
    start = datetime(year, month, day)
    end = start + timedelta(days=1)
    menu = Menu.objects(date_modified__gte=start, date_modified__lt=end).first_or_404()
    return jsonify(menu)


@app.route('/api/<int:m0>/<int:d0>/<int:y0>/<int:m1>/<int:d1>/<int:y1>')
def api2(m0, d0, y0, m1, d1, y1):
    """Return past menu JSON from database."""
    start = datetime(y0, m0, d0)
    end = datetime(y1, m1, d1)
    menus = Menu.objects(date_modified__gte=start, date_modified__lte=end)
    return jsonify(menus)

@app.route('/api2')
def api3():
    """Return week's menus in JSON."""
    return jsonify([views.breakfastLists, views.lunchLists, views.dinnerLists])