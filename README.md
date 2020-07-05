# TigerMenus

[TigerMenus](https://tigermenus.herokuapp.com/) is a web application that presents Princeton dining hall menu options organized by meal, unlike the official dining hall website.

It's viewed nearly 2500+ times every day, and usage has been growing every semester since its launch on March 12, 2017. Now it has nearly 1 million lifetime views!

![desktop](https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/screenshot2019.png)

# Motivation

At Princeton University, there are 6 different dining halls, each with its own webpage for the menus. At some point, I got tired of opening up 6 different tabs every meal just to compare menu options to decide where to eat.

So I decided to learn Python, web scraping using BeautifulSoup, and full stack web develepment using Flask to pull all the information I wanted into a single convenient site just for myself.

After posting the app to Facebook, it blew up and has since become a popular student app!

If you want, please continue this app's legacy and contribute on GitHub! It's been a great way for me to learn about web development and learning how to learn!

# Design Decisions

I chose to make TigerMenus a web app to make development and maintenance a lot easier, since I didn't need the features and performance of native apps. (Moreover, I wouldn't have to update code after each major iOS update.)

Now through their phone's default web browser, anyone on iOS, Android, and even Windows phone can install the app to their phone!

<img width=250 src="https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/iphoneicon.png"/><img width=250 src="https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/androidicon.png"/><img width=250 src="https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/windows.png"/>

The column layout is designed to minimize the number of clicks a user has to do, since scrolling is faster than clicking.

I intentionally used no Javascript to make the site as lightweight as possible. 

I originally tested this to use on an iPhone 4 in 2017.

# Analytics

<img width=200 src="https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/usage/views.jpg"/><img width=200 src="https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/usage/cat.jpg"/><img width=200 src="https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/usage/os.jpg"/><img width=200 src="https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/usage/brand.jpg"/>

# Credits

Created by Alex Xu '20 (ax2)

Icon designed by Alice Wang '19

Named by Ji-Sung Kim '19 and Sherry Bai '19

Other contributions by William Li '21

Lauched March 12, 2017

# Feedback + Reviews

Please don't make this website bloated with features. The simplicity is the best part.

thanks so much for creating this app! i practically use it everyday to find the best dining hall for each meal :D

I use this every day! Thanks for making and maintaining it. It unironically improves my quality of life a lot.

Nice job Alex and everyone involved for making a great, convenient website that is so useful!

Looking at TigerMenus is one of my most enjoyable (& exciting) study breaks. :) Thanks!

Saved my life given I cannot swipe into the dhalls without wasting a swipe

I use this site all the time, it's a quick way to compare options.

it's fantastic :) use it every day

I love tigermenus! you rock! keep it up!

I would cry without this.

tiger menus is life <3

## Setup (Python 3)
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
