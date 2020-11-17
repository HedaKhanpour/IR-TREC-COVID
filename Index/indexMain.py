import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize 
import re
from collections import Counter
import time
'''
class TermFrame():
    def __init__(self):
        self.df = pd.DataFrame(columns=["Cord_uid", "docTF"])
    
    def isIn(self, term):
        return term in self.df.index

    def processTerm(self, term, cord_uid):
        if self.isIn(term):
            self.updateTerm(term)
        else:
            self.addTerm(term, cord_uid)
    
    def addTerm(self, term, cord_uid):
        self.df.loc[term] = [cord_uid, 1]
    
    def updateTerm(self, term):
        self.df.loc[term] = [self.df.loc[term][0], self.df.loc[term][1] + 1]
    
    def printDataFrame(self):
        print(self.df)
'''
class TermDict():
    def __init__(self):
        self.td = {}
    
    def isIn(self, term):
        return term in self.td

    def processTerm(self, term, cord_uid):
        if self.isIn(term):
            self.updateTerm(term)
        else:
            self.addTerm(term, cord_uid)
    
    def addTerm(self, term, cord_uid):
        self.td[term] = (cord_uid, 1)
    
    def updateTerm(self, term):
        d = self.td[term]
        self.td[term] = (d[0], d[1] + 1)
    
    def printDict(self):
        print(self.td)

def getTestText():
    file = open("Index/testdoc.txt", "r")
    i = 0
    result = ""
    for line in file:
        result += line
    file.close()
    return result
    
def bagOfWords(text):
    return re.sub(' +', ' ', re.sub('[^A-Za-z]', ' ', text)).lower()

def removeStopwords(text, stopWords):
    return [word for word in text.split() if not word in stopWords]

def stemming(bow):
    stemmer = PorterStemmer()
    return [stemmer.stem(word) for word in bow]

def index(bow, cord_uid):
    td = TermDict()

    startTime  = time.time()
    for word in bow:
        td.processTerm(word, cord_uid)
    print("Dict: ", time.time() - startTime)
    td.printDict()


def main():
    stopwords_dict = Counter(stopwords.words('english'))
    rawText = getTestText()
    bow = bagOfWords(rawText)
    cleanUnstemmedBoW = removeStopwords(bow, stopwords_dict)
    cleanStemmedBoW = stemming(cleanUnstemmedBoW)
    cord_uid = '???'
    index(cleanStemmedBoW, cord_uid)


    print("***** Program Done *****")




main()
