
# TigerMenus

* Created Flask (Python) web app that presents dining hall menu options organized by meal on a single page
* Solved problem of needing to open 6 different dining hall websites to compare options for a given meal
* Is viewed 2500+ times a day, nearly 1 million lifetime views; scrapes menu data daily using BeautifulSoup
* Optimized web app for iPhone, Android, and Windows phones using Bootstrap 3 and home screen icons 
* Hosted at https://tigermenus.herokuapp.com/

![desktop](https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/screenshot2019.png)

<img width=300 src="https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/iphoneicon.png">

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
