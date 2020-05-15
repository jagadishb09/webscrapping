import requests
import re
import pandas as pd
import sys

class Access10K:
    def __init__(self):
        self.ciks=[320193]
        self.index=0
    def getnextcik(self):
        self.index = self.index+1
        return self.ciks[self.index-1]

    def removedups(self, doc, testdf):
        try:
            result = doc.index('<TABLE')
            result = result+5
            stack=[]
            stack.append(['<TABLE', result])
            print(stack)
            while True:
                try:
                    print('try1'+str(result))
                    result1 = doc.index('</TABLE', result)
                    result1 = result1+5
                    print('try2'+str(result1))
                    #sys.exit()
                    try:
                        resulte = doc.index('<TABLE',result)
                        result = resulte+5
                        print('try3'+str(result))
                        if(result1<result):
                            print('try6' + str(result1))
                            for index, row in testdf.head().iterrows():
                                if row['start'] > stack[len(stack)-1][1] and row['start'] < result1:
                                    print("hello word")
                                    testdf=testdf.drop(index)
                            stack.pop()
                            result = result1
                            print('try4'+str(result))
                        else:
                            stack.append(['<TABLE', result])
                    except:
                        for index,row in testdf.head().iterrows()():
                            if row['start']>stack[len(stack)-1][1] and row['start']<result1:
                                print("hello word")
                                testdf=testdf.drop(index)
                        result = result1
                        stack.pop()
                except:
                    print('try5'+str(result))
                    return testdf


        except:
            return testdf

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

        test_df = pd.DataFrame([(x.group(), x.start(), x.end()) for x in matches])
        test_df.columns = ['item', 'start', 'end']
        test_df['item'] = test_df.item.str.lower()
        test_df.replace('&#160;', ' ', regex=True, inplace=True)
        test_df.replace('&nbsp;', ' ', regex=True, inplace=True)
        test_df.replace(' ', '', regex=True, inplace=True)
        test_df.replace('\.', '', regex=True, inplace=True)
        test_df.replace('>', '', regex=True, inplace=True)
        print(self.removedups(document['10-K'],test_df))
        sys.exit()

        #implement stack to delete duplicate matches

        #

        # Write a for loop to print the matches
        #for match in matches:
            #print(match)
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

