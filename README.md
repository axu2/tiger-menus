# TigerMenus

[TigerMenus](https://tigermenus.herokuapp.com/) is a web application that presents Princeton dining hall menu options **organized by meal**, unlike the official dining hall website.

It solves the problem of needing to open 6 different websites just to compare menu options!

It's viewed 2000+ times every day, with nearly 1 million lifetime views!

![desktop](https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/screenshot2019.png)

Through their phone's default web browser, anyone on iOS, Android, and even Windows phone can install the app to their phone!

<img width=250 src="https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/iphoneicon.png"/><img width=250 src="https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/androidicon.png"/><img width=250 src="https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/windows.png"/>

On mobile, it's a simple scrolling interace, since scrolling is faster than clicking.

<img width=300 src="https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/iphone.png"/>

Hosted at https://tigermenus.herokuapp.com/

# Testimonials

* Please don't make this website bloated with features. **The simplicity is the best part.**

* thanks so much for creating this app! i practically use it everyday to find the best dining hall for each meal :D

* I use this every day! Thanks for making and maintaining it. It unironically improves my quality of life a lot.

* Nice job Alex and everyone involved for making a great, convenient website that is so useful!

* Looking at TigerMenus is one of my most enjoyable (& exciting) study breaks. :) Thanks!

* Saved my life given I cannot swipe into the dhalls without wasting a swipe

* I use this site all the time, it's a quick way to compare options.

* it's fantastic :) use it every day

* I love tigermenus! you rock! keep it up!

* I would cry without this.

* tiger menus is life <3

# Setup (Python 3)
```
$ git clone https://github.com/axu2/tiger-menus.git
$ cd tiger-menus
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install -r requirements.txt
```
Protip:
```
alias venv='python3 -m venv venv && . venv/bin/activate && pip install --upgrade pip'
```
To run development server:
```
(venv) $ python run.py
```
Open http://localhost:5000/

By default, it loads menus from the test_menus.py file, so you don't have to wait for the server to scrape data.

It takes a while to scrape 7*6=42 webpages, so page will load when scraping is done if you set a HEROKU environment variable.

In production, don't forget to set TZ='America/New_York' and HEROKU=1 environment variables.
