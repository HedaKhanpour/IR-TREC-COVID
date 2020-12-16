from Index.index import Index
import sys

def processQuery(query):
    index = Index()
    bow = index.bagOfWords(query)
    cleanUnstemmedBoW = index.removeStopwords(bow)
    cleanStemmedBoW = index.stemming(cleanUnstemmedBoW)
    return cleanStemmedBoW

def getTerm(termStr, path="../dataComplete/"):
    subDir = termStr[0:2]
    tf_over_all_docs = 0
    payloads = {}
    with open(path + subDir + "/" + termStr + ".txt", "r") as termFile:
        for line in termFile:
            cord_uid, docTF = line.split(",")
            #Remove the newline character and convert into a integer.
            docTF = int(docTF[:-1])
            payloads[cord_uid] = docTF
            tf_over_all_docs += docTF
    return Term(termStr, tf_over_all_docs, payloads)

class Term:
    def __init__(self, term, tf_over_all_docs, payloads, n_docs_containing_term):
        #String
        self.term = term
        #Integer
        self.tf_over_all_docs = tf_over_all_docs
        #{cord_uid(String): docTF(Integer)}
        self.payloads = payloads
        self.n_docs_containing_term = len(payloads)
    
    def printTerm(self):
        print("*******************")
        print("Term: ", self.term)
        print("tf_over_all_docs: ", str(self.tf_over_all_docs))
        for key in self.payloads.keys():
            print("Cord_uid: ", key, ", docTF: ", str(self.payloads[key]))