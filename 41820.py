from edgar import Company, TXTML, XBRL, XBRLElement
from edgar import Edgar
import lxml.html

from bs4 import BeautifulSoup

edgar = Edgar()

company = Company(edgar.get_company_name_by_cik('0000320193'), "0000320193")

results = company.get_all_filings('10-K')

soup = BeautifulSoup(lxml.html.tostring(results),'lxml')


table = soup.find_all('table')
print(len(table))

table_rows = table[2].find_all('tr')
for tr in table_rows:
    cols = tr.findAll('td')
    if len(cols) >= 4 :
        link = cols[1].find('a').get('href')
        print(link)

