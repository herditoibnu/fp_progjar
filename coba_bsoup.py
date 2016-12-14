# get short tutorial here: http://www.pythonforbeginners.com/python-on-the-web/beautifulsoup-4-python/
import urllib2
from bs4 import BeautifulSoup

response = urllib2.urlopen('http://www.studiawan.com').read()
soup = BeautifulSoup(response)

print soup.title.string
print soup.get_text()
