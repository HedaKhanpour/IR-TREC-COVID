import re
import pickle
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter

class Constants():
    
    user = "otto"
    if user == "otto":
        path_cord = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/"
        path_metadata = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/metadata.csv"
        
        path_pickles = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/pickle_files/"
        path_linked_documents = path_pickles + "linked_documents.pkl"
        path_unlinked_documents = path_pickles + "unlinked_documents.pkl"
        path_parsed_documents = path_pickles + "parsed_documents.pkl"
        path_final_documents = path_pickles + "final_documents.pkl" # Deprecated!
        
        path_topics = r"D:/Universiteit/Master (External Repositories)/IR-TREC-COVID/topics-rnd5.xml"
        path_relevance_judgements = r"D:/Universiteit/Master (External Repositories)/IR-TREC-COVID/trec_eval-master/our_data/CRJ.txt"
        path_results_dir = r"D:/Universiteit/Master (External Repositories)/IR-TREC-COVID/trec_eval-master/our_data/"
        results_file_name = "results"
        
        path_all_documents = path_pickles + "all_documents.pkl"
        path_all_document_lengths = path_pickles + "all_document_lengths.pkl"
        path_all_inverted_indexes = path_pickles + "all_inverted_indexes.pkl"
        
        path_linked_cord_uids = path_pickles + "linked_cord_uids.pkl"
        path_merged_documents = path_pickles + "merged_documents.pkl"
        
        # This is the data that will be used to rank documents
        path_documents = path_pickles + "complete_documents.pkl"
        path_document_lengths = path_pickles + "complete_document_lengths.pkl"
        path_inverted_indexes = path_pickles + "complete_inverted_indexes.pkl"
        path_documents_dictionary = path_pickles + "complete_documents_dictionary.pkl"
        
    
    k = 1.2 # Free BM25 parameter in the range [0, +inf)
    b = 0.7 # Free BM25 parameter in the range [0, 1]
    
    # Statistic regarding the complete documents set
    doc_count = 191175 # The total number of complete documents
    avg_doc_length = 1231.9501399241533 # The average complete document length

        
def create_document_dictionary(documents):
    """Returns a document dictionary with cord_uids as keys."""
    
    document_dictionary = dict()
    for document in documents:
        document_dictionary[document.cord_uid] = document
    return document_dictionary

def is_empty(string):
    """Returns true if a string consists of nothing other than whitespaces."""
    return string == None or re.sub("\\s+", "", string) == ""

def clean_title(title):
    """Simplifies a title for more dependable title comparisons."""
    title = re.sub("\n", "", title) # Remove newlines
    title = ' '.join(title.split()) # Turn multiple whitespaces into a single one
    title = title.lower() # Make everything lowercase
    return title

def save_pickle(file, path):
    """Save the given file using pickle."""
    with open(path, 'wb') as f:
        pickle.dump(file, f)
    file_name = re.findall(r"/?[^/]+", path)[-1].strip("/")
    print(f"Stored {file_name}.")

def load_pickle(path):
    """Load a pickle file"""
    with open(path, 'rb') as f:
        pickle_file = pickle.load(f)
    file_name = re.findall(r"/?[^/]+", path)[-1].strip("/")
    print(f"Loaded {file_name}.")
    return pickle_file

def compute_document_statistics(documents, doc_lengths, path_relevance_judgements):
    """Compute and print several relevant statistics"""
    
    print("\n------------- Computing document statistics -------------")
    print(f"{len(doc_lengths)/len(documents) * 100}% of stored documents are unique.")
    
    print("\nThe following should be taken into account with the coming calculations:")
    print("    - Only terms that were not remove by the cleaning/stemming/... process were included.")
    print("    - If a term occurs multiple times in a file or across files, it is (of course) counted multiple times as well.")
    
    total_nr_of_terms = 0
    for key in doc_lengths.keys():
        total_nr_of_terms += doc_lengths[key]
    print(f"\nThere are {total_nr_of_terms} terms in total accross all documents.")
    print(f"The average document length is {total_nr_of_terms/len(doc_lengths)}")
    
    # Rest of the code is to test for the presence of relevant documents
    print("\n-------- Testing for the presence of relevant documents --------")
    processed_docs = set()
    for doc in documents:
        processed_docs.add(doc.cord_uid)
    
    crj_docs = set()
    # Load the stored documents
    with open(path_relevance_judgements, 'r') as f:
        for line in f:
            crj = line.split(" ")
            cord_uid = crj[2]
            crj_docs.add(cord_uid)
    
    only_processed = processed_docs - crj_docs
    only_crj = crj_docs - processed_docs
    symmetric_difference = processed_docs.symmetric_difference(crj_docs)
    intersection = processed_docs.intersection(crj_docs)
    print(f"There are {len(processed_docs)} unique processed documents.")
    print(f"There are {len(crj_docs)} unique documents in the relevance judgements.")
    print(f"There are {len(only_processed)} documents that were processed, but are not present in the relevance judgements.")
    print(f"There are {len(only_crj)} documents that are present in the relevance judgements, but were not processed.")
    print(f"There are {len(symmetric_difference)} documents that were both processed and are present in the relevance judgements.")
    print(f"There are {len(intersection)} documents that were either processed or were present in the relevance judgements, but not both.")

def processQuery(query):
    index = Index()
    bow = index.bagOfWords(query)
    cleanUnstemmedBoW = index.removeStopwords(bow)
    cleanStemmedBoW = index.stemming(cleanUnstemmedBoW)
    return cleanStemmedBoW

class Document():
    """Used to store relevant document information in a consistent form."""
    
    def __init__(self, cord_uid, title, abstract, authors, sections):
        self.cord_uid = cord_uid
        self.title = title
        self.abstract = abstract
        self.authors = None if authors == None else authors.copy()
        self.sections = None if sections == None else sections.copy()
    
    def __str__(self):
        string = "\n********** Document **********\n"
        string += "cord_uid:\n{}\n".format(self.cord_uid)
        string += "\ntitle:\n{}\n".format(self.title)
        
        string += "\nauthors:\n"
        if self.authors == None:
            string += "None\n"
        else:
            for author in self.authors:
                string += "{}\t".format(author)
            string += "\n"
        
        string +=  "\nabstract:\n{}\n".format(self.abstract)
        
        string += "\nsections:\n"
        if self.sections == None:
            string += "None\n"
        else:
            for section in self.sections:
                string += "{}\n".format(section.__str__())
        
        return string

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