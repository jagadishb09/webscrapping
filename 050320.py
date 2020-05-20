from bs4 import BeautifulSoup
from edgar import Company, TXTML, XBRL, XBRLElement
from edgar import Edgar
import lxml.html
import re
import requests
import urllib.request
import codecs
import sys
from classfile1 import Access10K
reqfuncs = Access10K()
qutr = ["QTR1", "QTR2", "QTR3", "QTR4"]
import xlwt
from xlwt import Workbook
wb = Workbook()
cnt=1


for cik in reqfuncs.ciks:
    year=2011

    sheet1 = wb.add_sheet(str(cik))
    while year<2020:

        for qtr in qutr:
            list10ks = reqfuncs.downloadmasteridx(year,qtr, cik)
            for k10 in list10ks:
                print(k10[0])

                numworsdsindoc, sectinfo = reqfuncs.sectioninfo(k10[0])
                numsecs = len(sectinfo)
                for secinfo in sectinfo:

                    sheet1.write(cnt,0, cik)
                    sheet1.write(cnt,1,str(year)+qtr)
                    sheet1.write(cnt,2,k10[1])
                    sheet1.write(cnt,3,k10[0])
                    sheet1.write(cnt,4, secinfo[0])
                    sheet1.write(cnt, 5, secinfo[1])
                    sheet1.write(cnt, 6, secinfo[2])
                    sheet1.write(cnt, 7,numworsdsindoc)
                    sheet1.write(cnt, 8, numsecs)
                    cnt = cnt + 1

        year = year+1

wb.save('white1.xls')






