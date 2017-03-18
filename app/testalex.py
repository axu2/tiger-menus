import urllib2
from bs4 import BeautifulSoup
from flask import render_template
from app import app

response = urllib2.urlopen('https://reg-captiva.princeton.edu/chart/index.php?terminfo=1164&courseinfo=007998')
html = response.read()
soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify())