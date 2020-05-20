import requests
import re
import pandas as pd
import sys
from bs4 import BeautifulSoup

class Access10K:
    def __init__(self):
        #add all ciks to this list like [51143, 10274, 320193]
        self.ciks=[51143]

    #function to get the tags with bold style in the html
    def bold_only(self,tag):
        is_b = tag.name == 'b'
        is_strong = tag.name == 'strong'
        is_bold_font = tag.name == 'font' and 'style' in tag.attrs and 'bold' in tag['style']

        return is_b or is_strong or is_bold_font

    #search for the given word in the link
    def searchword(self, link, searchword):
        r = requests.get(link)
        raw_10k = r.text
        bsoup = BeautifulSoup(raw_10k, "html.parser")
        words = bsoup.get_text().split()
        if searchword in words:
            return True

    #function to get section info from the text which contains html
    #gets number of sections, number of words in each section and number of subsections in each section
    def sectioninfo(self, link):
        r = requests.get(link)
        raw_10k = r.text
        doc_start_pattern = re.compile(r'<DOCUMENT>')
        doc_end_pattern = re.compile(r'</DOCUMENT>')
        type_pattern = re.compile(r'<TYPE>[^\n]+')
        doc_start_is = [x.end() for x in doc_start_pattern.finditer(raw_10k)]
        doc_end_is = [x.start() for x in doc_end_pattern.finditer(raw_10k)]
        doc_types = [x[len('<TYPE>'):] for x in type_pattern.findall(raw_10k)]
        document = {}

        # Create a loop to go through each section type and save only the 10-K section in the dictionary
        for doc_type, doc_start, doc_end in zip(doc_types, doc_start_is, doc_end_is):
            if doc_type == '10-K':
                document[doc_type] = raw_10k[doc_start:doc_end]

        html = document['10-K']
        soup = BeautifulSoup(html, "html.parser")
        numwordsindoc = len(soup.get_text().split())
        document = str(soup)
        #with open('10k.txt', 'wt') as file:
            #file.write(document)

        bold=[bold for bold in soup.find_all(self.bold_only)]

        regex = re.compile(
            r'(Item(\s|&#160;|&nbsp;)([+-]?\d+(?:\.\d+)?)([a-z]|[A-Z])*\.{1})|(ITEM\s([+-]?\d+(?:\.\d+)?)\.{1}([a-z]|[A-Z])*\.{1})')

        indices=[]
        for x in bold:
            matches=[]
            matches=regex.findall(x.get_text())
            if(len(matches) > 0):
                indices.append([x,document.index(str(x)), x.get_text()])

        sectioninfo=[]
        for index in range(len(indices) - 1):
            item_1a_raw = document[indices[index][1]:indices[index+1][1]]
            item_1a_content = BeautifulSoup(item_1a_raw, 'lxml')
            numwords = len(item_1a_content.get_text("\n\n").split())

            bTags = []
            for i in item_1a_content.findAll(self.bold_only):
                tagtd = True
                for j in i.parents:
                    if j.name == 'td':
                        tagtd = False

                if tagtd:
                    bTags.append(i.text)

            numsubsecs = len(bTags)
            sectioninfo.append([numwords,numsubsecs, indices[index][2]])

        item_1a_raw = document[indices[len(indices)-1][1]:]
        item_1a_content = BeautifulSoup(item_1a_raw, 'lxml')
        numwords = len(item_1a_content.get_text("\n\n"))

        bTags = []
        for i in item_1a_content.findAll(self.bold_only):
            tagtd = True
            for j in i.parents:
                if j.name == 'td':
                    tagtd = False

            if tagtd:
                bTags.append(i.text)

        numsubsecs = len(bTags)
        sectioninfo.append([numwords,numsubsecs,indices[len(indices)-1][2]])

        return numwordsindoc, sectioninfo

    #gets master index file for a given year,quarter and cik
    def downloadmasteridx(self, year, qtr, cik):

        base_url = r"https://www.sec.gov/Archives/edgar/full-index"
        url = '{}/{}'.format(base_url,year)
        url = '{}/{}'.format(url,qtr)
        url = '{}/{}'.format(url,'master.idx')

        content = requests.get(url).content

        with open('masteridx.txt', 'wb') as file:
            file.write(content)

        with open('masteridx.txt', 'r', encoding = "ISO-8859-1") as file:
            startline=0
            line = file.readline()
            m = None
            while line:
                m = re.search(r"\d", line)
                if m is not None and m.start()==0 :
                    break
                else:
                    startline = startline + 1
                    line = file.readline()
            list10k = []
            url1 = r"https://www.sec.gov/Archives/edgar/data/"+str(cik)
            if m is not None and m.start() == 0:
                while line:
                    parts = line.split('|')
                    if(parts[0] == str(cik) and parts[2] == '10-K'):
                        split10k = parts[4].split('/')
                        lastappend = split10k[3]
                        split10k[3] = split10k[3].replace("-","")
                        split10k[3] = split10k[3].replace(".txt\n","")
                        list10k.append([url1+'/'+split10k[3]+'/'+lastappend, parts[3]])
                    line = file.readline()
            return list10k
