from bs4 import BeautifulSoup
from edgar import Company, TXTML, XBRL, XBRLElement
from edgar import Edgar
import lxml.html
import re
import requests
import urllib.request
import codecs

source = urllib.request.urlopen('https://www.sec.gov/Archives/edgar/data/320193/000032019319000119/a10-k20199282019.htm').read()
soup = BeautifulSoup(source, 'lxml')
#print(soup.prettify())

table = soup.find_all('table')

tablist = []
tablef = []
start = 0

for tablel in table:
    table_rows = tablel.find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        tablist.append(row)
    i=0
    while i<len(tablist):
        if(re.match("(Item )(1)(.)",tablist[i][0])):
            start = i
            tablef=tablist
            break
        i=i+1
    if start!=0:
        break

print(start)
print(tablef[start])