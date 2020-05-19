import requests
import re
import pandas as pd
import sys
from bs4 import BeautifulSoup

class Access10K:
    def __init__(self):
        self.ciks=[320193]
        self.index=0
    def getnextcik(self):
        self.index = self.index+1
        return self.ciks[self.index-1]

    def search_for_bolded_tags(self, tag):
        criteria1 = tag.name == 'b'
        criteria2 = tag.parent.name != 'td'

        if criteria1:
            return tag.get_text(strip = True).replace('\n',' ')

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

        with open('10k.txt', 'wt', encoding="ISO-8859-1") as file:
            file.write(document['10-K'])

        #regex = re.compile(r'(>Item(\s|&#160;|&nbsp;)(1|1A|1B|2|3|4|5|6|7|7A|8|9|9A|9B|10|11|12|13|14|15)\.{0,1})|(ITEM\s(1|1A|1B|2|3|4|5|6|7|7A|8|9|9A|9B|10|11|12|13|14|15))')
        regex = re.compile(
            r'(>Item(\s|&#160;|&nbsp;)(1A|1B|7A|7|8)\.{0,1})|(ITEM\s(1A|1B|7A|7|8))')
        #regex = re.compile(r'(>Item(\s|&#160;|&nbsp;)(5|6|7A|7)\.{0,1})|(ITEM\s(5|6|7A|7))')
        #regex = re.compile(r'(>Item(\s|&#160;|&nbsp;)([+-]?\d+(?:\.\d+)?)\.{0,1})|(ITEM\s)([+-]?\d+(?:\.\d+)?)')
        docstr = str(document['10-K'])
        matches = regex.finditer(docstr)

        test_df = pd.DataFrame([(x.group(), x.start(), x.end()) for x in matches])
        test_df.columns = ['item', 'start', 'end']
        test_df['item'] = test_df.item.str.lower()
        test_df.replace('&#160;', ' ', regex=True, inplace=True)
        test_df.replace('&nbsp;', ' ', regex=True, inplace=True)
        test_df.replace(' ', '', regex=True, inplace=True)
        test_df.replace('\.', '', regex=True, inplace=True)
        test_df.replace('>', '', regex=True, inplace=True)
        print(test_df)
        print('righttttttttttttttttttttttt')
        df = self.removedups(docstr,test_df)
        print(df)
        #test_df=test_df.reset_index()
        test_df = test_df.reset_index(drop = True)
        sys.exit()
        #test_df.set_index('item', inplace=True)
        #test_df.set_index('item', inplace=True)
        #print(str(document['10-K']))
        #doc10k= str(document['10-K'])
        #print(doc10k)
        #print (doc10k[410500:410600])

        #print(item_1a_raw)
        #item_1a_raw = document['10-K'][test_df['start'].loc[0]:test_df['start'].loc[1]]

        numsubsecs=[]
        numwords = []
        for i in range(len(test_df)-1):
            item_1a_raw = document['10-K'][test_df['start'].loc[i]:test_df['start'].loc[i+1]]
            #print(item_1a_raw)
            item_1a_content = BeautifulSoup(item_1a_raw, 'lxml')
            numwords.append(len(item_1a_content.get_text("\n\n")))
            bTags = []

            for i in item_1a_content.findAll('b'):
                tagtd = True
                for j in i.parents:
                    if j.name == 'td':
                        tagtd = False

                if tagtd:
                    bTags.append(i.text)

                #if(i.parent.name == 'p' and i.parents.name != 'td'):
                 #   bTags.append(i.text)
            numsubsecs.append(len(bTags))
        numsubsecs.append(0)
        numwords.append(0)
        test_df['numsubsecs'] = numsubsecs
        test_df['numwords'] = numwords
        print(test_df)
            #print(item_1a_content)
            #print('jdhgfjsdfjhdsddddddddddddddddddddddddddddddd')
            #data = [b.string for b in item_1a_content.findAll('b')]
            #print(data)
            #bold_texts = item_1a_content.find_all(self.search_for_bolded_tags)
            #print(bold_texts)
            #print(item_1a_content)
            #print(item_1a_content.get_text("\n\n"))
        sys.exit()

    def removedups(self, doc, testdf):
        print('dfsjdhfjhsdgfksdgfdksgf')
        df=[]
        doc=doc.lower()
        print(doc)
        try:
            result = doc.index('<b>')
            print(result)

            stack=[]
            stack.append(['<b>', result])
            result = result + 2
            while True:
                try:
                    result1 = doc.index('</b>', result)
                    print(result1)
                    #result1 = result1+2
                    try:
                        resulte = doc.index('<b>',result)
                        #result = resulte+2
                        if(result1<resulte):
                            print('yesssssssssssssssssssssssssssssssssssss')
                            for index, row in testdf.head().iterrows():
                                if row['start'] >= stack[-1][1] and row['start'] <= result1:
                                    df.append(row['start'])

                            stack.pop()
                            result = result1+2
                        else:
                            stack.append(['<b>', resulte])
                            result = resulte+2
                    except:
                        print('yesssssssssssssssssssssssssssssssssssss')
                        for index, row in testdf.head().iterrows():
                            if row['start'] >= stack[- 1][1] and row['start'] <= result1:
                                df.append(row['start'])
                        stack.pop()
                        result = result1+2

                except:
                    return df


        except:
            return df

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

