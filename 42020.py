from bs4 import BeautifulSoup
from edgar import Company, TXTML, XBRL, XBRLElement
from edgar import Edgar
import lxml.html
import re
import requests
import urllib.request
import codecs
'''
with open("appledoc.html", "r", encoding='utf-8', errors='ignore') as f:
    contents = f.read()

    soup = BeautifulSoup(contents, 'lxml')
    #print(soup.prettify())

    table = soup.find_all('table')

    print(len(table))

    table_rows = table[11].find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        print(row)

'''
source = urllib.request.urlopen('https://www.sec.gov/Archives/edgar/data/320193/000032019319000119/a10-k20199282019.htm').read()
soup = BeautifulSoup(source, 'lxml')
#print(soup.prettify())

table = soup.find_all('table')

print(len(table))

table_rows = table[11].find_all('tr')
for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text for i in td]
    print(row)



'''
table = soup.find_all('table')

print(len(table))

table_rows = table[10].find_all('tr')
for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text for i in td]
    print(row)

xbrl_resp = requests.get(xbrl_link)
xbrl_str = xbrl_resp.text

# Find and print stockholder's equity
soup = BeautifulSoup(xbrl_str, 'lxml')
tag_list = soup.find_all()
for tag in tag_list:
    if tag.name == 'us-gaap:stockholdersequity':
        print("Stockholder's equity: " + tag.text)
'''