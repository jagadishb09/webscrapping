import requests
import re

class Access10K:
    def __init__(self):
        self.ciks=[320193]
        self.index=0
    def getnextcik(self):
        self.index = self.index+1
        return self.ciks[self.index-1]

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
                    #print(startline, line, m.start())
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

    def sectioninfo(self, link):
        print(link)
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

        regex = re.compile(r'(>Item(\s|&#160;|&nbsp;)(1A)\.{0,1})|(ITEM\s(1A))')
        matches = regex.finditer(document['10-K'])

        # Write a for loop to print the matches
        for match in matches:
            print(match)
        return 'hello world'

    def get10klinksdates(self, cik):
        return "10k links"

    def numsecsubsecs(self, link10k):
        print("process table of contents")
        print( "number of headings under each section/sub-section")
        print("num words in each sec/subsec")
        print ('readability of each sec/sub-sec')

    def numgraphs(self, link10k):
        print ("num graphs") # graph vs pics
        print("num pictures") #
        print("directors and ceo numbers") # different sections for directors and ceos

    def numnewwords(self, old10klink, current10klink):
        print("num new owrds per sec/sub-sec") # what if section is not present in the previous once or vice versa
        print("num new headings or sections")

