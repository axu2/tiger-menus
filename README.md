
# TigerMenus
## Overview
Convenient to use dining hall menu website for Princeton University with 33,333+ views and ~333 daily users

Hosted at https://tigermenus.herokuapp.com/

It sure was fun learning Python, Flask, BeautifulSoup, MongoDB, GitHub, and Heroku in order to develop this!

Make sure you checkout the mobile versions too!

![alt tag](https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/favicons/apple-touch-icon.png)


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
$ source venv/bin/activate
```
Install requirements with pip in the venv:
```
(venv) $ pip install -r requirements.txt
```
To run development server:
```
(venv) $ python run.py
```
It takes a while to scrape 7*6=42 webpages.

So wait until you see something like (ignore any error messages you get if you use an old version of Python):
```
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 630-870-627
```
Open http://localhost:5000/
