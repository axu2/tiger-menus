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

It takes a while to scrape 7*6=42 webpages, so page will load when scraping is done.

## Environment Variables

In production, don't forget to set:

```
TZ=America/New_York 
```

since scraping updates on the Princeton time zone.
