 
# TigerMenus
## Overview
Scrapes menu data for all six dining halls and displays each meal on a single page for easy comparison.

Hosted at https://tigermenus.herokuapp.com/

It sure was fun learning Python, Flask, BeautifulSoup, MongoDB, GitHub, and Heroku in order to develop this!

I plan to add more features to it (user accounts, email notifications when dumplings are being served, better UI and design overall, making a version of the site for grad students to use since they actually go frist/frick cafe, equad cafe, eating club menus) Please tell me about features you want added or even submit a pull request! You can use the feedback form on the website (which I shamelessly stole from TigerBook).

![alt tag](https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/screenshot.png)

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
