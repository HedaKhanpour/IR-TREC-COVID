from Index.index import Index

def processQuery(query):
    index = Index()
    bow = index.bagOfWords(query)
    cleanUnstemmedBoW = index.removeStopwords(bow)
    cleanStemmedBoW = index.stemming(cleanUnstemmedBoW)
    return cleanStemmedBoW

def getTerm(termStr):
    path = "Index/data/"
    subDir = termStr[0:2]
    TF = 0
    payloads = {}
    with open(path + subDir + "/" + termStr + ".txt", "r") as termFile:
        for line in termFile:
            cord_uid, docTF = line.split(",")
            #Remove the newline character and convert into a integer.
            docTF = int(docTF[:-1])
            payloads[cord_uid] = docTF
            TF += docTF
    return Term(termStr, TF, payloads)

class Term:
    def __init__(self, term, TF, payloads):
        #String
        self.term = term
        #Integer
        self.TF = TF
        #{cord_uid(String): docTF(Integer)}
        self.payloads = payloads
    
    def printTerm(self):
        print("*******************")
        print("Term: ", self.term)
        print("TF: ", str(self.TF))
        for key in self.payloads.keys():
            print("Cord_uid: ", key, ", docTF: ", str(self.payloads[key]))