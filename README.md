
# TigerMenus
## Overview
Developed new university dining hall menu website with 300+ daily active users and 33,000+ total views

Designed interface that consolidated all 6 university dining hall menus into a single page, mobile website with app icon for iPhone/Android, and JSON web API for historical menu data stored in MongoDB

Hosted at http://tigermenus.herokuapp.com/

Programmed backend in Flask (Python) using BeautifulSoup (scraping) and MongoEngine (database)


<table>
  <tr>
    <th><img src="https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/iphoneicon.png"  style="width: 160px;"/></th>
    <th><img src="https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/iphone.png"  style="width: 160px;"/></th>
    <th><img src="https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/androidicon.png" style="width: 160px;"/></th>
    <th><img src="https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/android.png"  style="width: 160px;"/></th>
  </tr>
</table>

![alt tag](https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/screenshot.png)
How it looks.

![alt tag](https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/analytics.png)
How popular it was

## Setup
Recommended Python 2.7.9+. Older versions will give you error messages, but you can probably ignore them.

Fork repository (optional) and clone it into your own directory. Then:
```
$ cd tiger-menus
```
To set up a virtual environment, run the commands from http://flask.pocoo.org/docs/0.12/installation/#installation:
For example, if you are using Bash on Ubuntu on Windows like me, the commands might look like:
```
$ sudo apt-get install python-virtualenv
$ virtualenv venv
$ . venv/bin/activate
```
Install requirements with pip in the venv:
```
(venv) $ pip install -r requirements.txt
```

Start a local MongoDB server.
```
(venv) $ service mongodb start
```
To run development server:
```
(venv) $ python run.py
```

Ignore any error messages you get if you use an old version of Python.

Open http://localhost:5000/

It takes a while to scrape 7*6=42 webpages, so page will load when scraping is done.
