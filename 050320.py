from bs4 import BeautifulSoup
from edgar import Company, TXTML, XBRL, XBRLElement
from edgar import Edgar
import lxml.html
import re
import requests
import urllib.request
import codecs
from classfile import Access10K
reqfuncs = Access10K()
year = 2015
qutr = ["QTR1", "QTR2", "QTR3", "QTR4"]
import xlwt
from xlwt import Workbook
wb = Workbook()
cnt=1
#for qtr in qutr:
for cik in reqfuncs.ciks:

    sheet1 = wb.add_sheet(str(cik))
    while year<2020:
        for qtr in qutr:
            list10ks = reqfuncs.downloadmasteridx(year,qtr, cik)
            for k10 in list10ks:
                print(k10[0])
                sheet1.write(cnt,0, cik)
                sheet1.write(cnt,1,str(year)+qtr)
                sheet1.write(cnt,2,k10[1])
                sheet1.write(cnt,3,k10[0])
                reqfuncs.sectioninfo(k10[0])
                cnt = cnt+1

        year = year+1

wb.save('white1.xls')
    #for each 10k
    #print(reqfuncs)
    #for cik in reqfuncs.ciks:

        #get 10-K's list and dates filed for the cik in the file
        # for each 10-K:
        #{
            # get number of sections
            # for each section
            #{
                # get number of words
                # get readability
                # get number of headings
                # for each heading
                #{
                    # get number of words
                    # get readability
                #}
            #}
        #}
    #delete file master idx file







