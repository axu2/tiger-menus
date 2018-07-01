
# TigerMenus

*	Developed new university dining hall menu website with over 1500+ daily views, 250,000+ lifetime views
*	Optimized web app for iPhone, Android, and Windows phones using Bootstrap and home screen icons 
*	Written in Flask (Python), scraped menu data from 42 different dining hall websites using BeautifulSoup

![desktop](https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/screenshot.png)

<img width=300 src="https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/iphoneicon.png">

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
