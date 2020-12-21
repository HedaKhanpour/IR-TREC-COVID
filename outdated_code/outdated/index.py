import os
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re
from collections import Counter
import time

def processQuery(query):
    index = Index()
    bow = index.bagOfWords(query)
    cleanUnstemmedBoW = index.removeStopwords(bow)
    cleanStemmedBoW = index.stemming(cleanUnstemmedBoW)
    return cleanStemmedBoW

class TermDict():
    def __init__(self):
        self.td = {}

    def clear(self):
        self.td.clear()

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

    def getKeys(self):
        return self.td.keys()

    def getValue(self, key):
        return self.td[key]

    def printDict(self):
        print(self.td)

class Index():
    def __init__(self):
        self.stopwords_dict = Counter(stopwords.words('english'))

    def getTestText(self):
        file = open("Index/testdoc.txt", "r")
        i = 0
        result = ""
        for line in file:
            result += line
        file.close()
        return result

    def bagOfWords(self, text):
        return re.sub(' +', ' ', re.sub('[^A-Za-z]', ' ', text)).lower()

    def removeStopwords(self, text):
        return [word for word in text.split() if not word in self.stopwords_dict]

    def stemming(self, bow):
        stemmer = PorterStemmer()
        return [stemmer.stem(word) for word in bow]

    def index(self, bow, cord_uid, inverted_indexes):
        td = TermDict()
        for word in bow:
            td.processTerm(word, cord_uid)
        self.writeToIndex(td, inverted_indexes)
        td.clear()
        del td

    def writeToIndex(self, termDict, inverted_indexes):
        for term in termDict.getKeys():
            if (len(term) > 255):
                continue

            cord_uid = termDict.getValue(term)[0]
            docTF = termDict.getValue(term)[1]
            
            if term in inverted_indexes:
                inverted_indexes[term][cord_uid] = docTF
            else:
                inverted_indexes[term] = dict()
                inverted_indexes[term][cord_uid] = docTF
        return inverted_indexes

    def processDocument(self, rawText, cord_uid, inverted_indexes):
        bow = self.bagOfWords(rawText)
        cleanUnstemmedBoW = self.removeStopwords(bow)
        cleanStemmedBoW = self.stemming(cleanUnstemmedBoW)
        self.index(cleanStemmedBoW, cord_uid, inverted_indexes)
        return len(cleanStemmedBoW)
        
