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
year = 2019
qutr = ["QTR1", "QTR2", "QTR3", "QTR4"]

#for qtr in qutr:
for cik in reqfuncs.ciks:
    print(reqfuncs.downloadmasteridx(year,qutr[3], cik))
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







