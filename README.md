
# TigerMenus

*	Developed new university dining hall menu website with over 1500+ daily views, 250,000+ lifetime views
*	Optimized web app for iPhone, Android, and Windows phones using Bootstrap and home screen icons 
*	Written in Flask (Python), scraped menu data from 42 different dining hall websites using BeautifulSoup
* Hosted at https://tigermenus.herokuapp.com/

![desktop](https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/screenshot.png)

<img width=300 src="https://raw.githubusercontent.com/axu2/tiger_menus/master/app/static/iphoneicon.png">

## Setup (Python 3)
```
$ git clone https://github.com/axu2/tiger-menus.git
$ cd tiger-menus
$ python3 -m venv venv
$ pip install --upgrade pip
$ . venv/bin/activate
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

It takes a while to scrape 7*6=42 webpages, so page will load when scraping is done.
