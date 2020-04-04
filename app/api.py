from app import app
from flask import jsonify
from app import views


@app.route('/api2')
def api3():
    """Return week's menus in JSON."""
    return jsonify([views.breakfastLists, views.lunchLists, views.dinnerLists])