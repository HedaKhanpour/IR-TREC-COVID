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
        results_rerank_file_name = "results_rerank"
        
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
        
        path_inverted_indexes_bm25f = path_pickles + "inverted_indexes_bm25f.pkl"
        path_doc_length_info_bm25f = path_pickles + "doc_length_info_bm25f.pkl"
    elif user == "anass":
        path_cord = "../cord-19_2020-07-16/"
        path_metadata = path_cord + "metadata.csv"
        
        path_pickles = "../pickels/"
        path_linked_documents = path_pickles + "linked_documents.pkl"
        path_unlinked_documents = path_pickles + "unlinked_documents.pkl"
        path_parsed_documents = path_pickles + "parsed_documents.pkl"
        path_final_documents = path_pickles + "final_documents.pkl"
        
        #path_inverted_indexes = path_pickles + "inverted_indexes.pkl"
        #path_document_lengths = path_pickles + "document_lengths.pkl"

        path_topics = "trec_eval-master/our_data/topics-rnd5.xml"
        path_relevance_judgements = "trec_eval-master/our_data/CRJ.txt"
        path_results_dir = "trec_eval-master/our_data/"
        results_file_name = "results"
    elif user == "heda":
        path_cord = r"C:/Users/hedak/Downloads/2020-07-16/"
        path_metadata = path_cord + "metadata.csv"

        path_pickles = r"C:/Users/hedak/Downloads/"
        path_linked_documents = path_pickles + "linked_documents.pkl"
        path_unlinked_documents = path_pickles + "unlinked_documents.pkl"
        path_parsed_documents = path_pickles + "parsed_documents.pkl"
        path_final_documents = path_pickles + "complete_documents.pkl"

        path_inverted_indexes = path_pickles + "complete_inverted_indexes.pkl"
        path_document_lengths = path_pickles + "complete_document_lengths.pkl"
        path_document_length_info_bm25f = path_pickles + "doc_length_info_bm25f.pkl"
        path_inverted_indexes_bm25f = path_pickles + "inverted_indexes_bm25f.pkl"

        path_topics = r"C:/Users/hedak/Downloads/topics-rnd5.xml"
        path_relevance_judgements = r"C:/Users/hedak/PycharmProjects/IR-TREC-COVID/trec_eval-master/our_data/CRJ.txt"
        path_results_dir = r"C:/Users/hedak/PycharmProjects/IR-TREC-COVID/trec_eval-master/our_data/"
        results_file_name = "results_bm25f"
    
    weight_title = 0.3
    weight_author = 0.0
    weight_abstract = 0.6
    weight_sections = 0.1
    
    b_title = 0.7 # Free BM25F parameter in the range [0, 1]
    b_author = 0.7 # Free BM25F parameter in the range [0, 1]
    b_abstract = 0.7 # Free BM25F parameter in the range [0, 1]
    b_sections = 0.7 # Free BM25F parameter in the range [0, 1]
    
    avg_author_length =12.910542696482281
    avg_sections_length = 1213.091026546358
    avg_title_length = 9.355851968092063
    avg_abstract_length = 89.43707597750752
    avg_total_length = 1324.79449718844
    
    # Statistic regarding the complete documents set
    doc_count = 191175 # The total number of complete documents
    avg_doc_length = 1231.9501399241533 # The average complete document length
    
    rerank_multiplier = 8

class ParametersBM25():
    """Used to pass the parameters of the BM25 algorithm."""
    
    def __init__(self, k=5.0, b=0.8):
        self.k = k # Free BM25 parameter in the range [0, +inf)
        self.b = b # Free BM25 parameter in the range [0, 1]
    
    def print_parameters(self):
        print(f"\n\n\nParameters BM25: k={self.k}, b={self.b}\n")
        
class ParametersBM25F():
    """Used to pass the parameters of the BM25F algorithm."""
    
    def __init__(self, k=3.0,
                 weight_title=3.0, weight_author=0.0, weight_abstract=2.0, weight_sections=0.3,
                 b_title=0.7, b_author=0.8, b_abstract=0.4, b_sections=0.8):
        self.k = k
        
        self.weight_title = weight_title
        self.weight_author = weight_author
        self.weight_abstract = weight_abstract
        self.weight_sections = weight_sections
        
        self.b_title = b_title
        self.b_author = b_author
        self.b_abstract = b_abstract
        self.b_sections = b_sections
    
    def print_parameters(self):
        print("\n\n\nParameters BM25F: \n"
              + f"  k={self.k}, b={self.b}\n  weight_title={self.weight_title}, weight_author={self.weight_author},"
              + f" weight_abstract={self.weight_abstract}, weight_sections={self.weight_sections}\n"
              + f"  b_title={self.b_title}, b_author={self.b_author},"
              + f" b_abstract={self.b_abstract}, b_sections={self.b_sections}\n")
        
        
    
def print_bm25_field_length_info(path_doc_length_info_bm25f):
    """Prints information regarding the (average) number of terms per field."""

    doc_length_info = load_pickle(path_doc_length_info_bm25f)
    
    n_terms_author_total = 0
    n_terms_sections_total = 0
    n_terms_title_total = 0
    n_terms_abstract_total = 0
    for cord_uid in doc_length_info.keys():
        
        info = doc_length_info[cord_uid]
        
        n_terms_author_total += info['author']
        n_terms_sections_total += info['sections']
        n_terms_title_total += info['title']
        n_terms_abstract_total += info['abstract']
        
    n_terms_total = n_terms_author_total + n_terms_sections_total + n_terms_title_total + n_terms_abstract_total
        
    print(len(doc_length_info))
    print(f"n_terms_author_total  = {n_terms_author_total},     average={n_terms_author_total/len(doc_length_info)}")
    print(f"n_terms_sections_total= {n_terms_sections_total},   average={n_terms_sections_total/len(doc_length_info)}")
    print(f"n_terms_title_total   = {n_terms_title_total},      average={n_terms_title_total/len(doc_length_info)}")
    print(f"n_terms_abstract_total= {n_terms_abstract_total},   average={n_terms_abstract_total/len(doc_length_info)}")
    print(f"n_terms_total         = {n_terms_total},            average={n_terms_total/len(doc_length_info)}")
                            
def print_inverted_indexes_BM25F(self, inverted_indexes):
    for term in inverted_indexes.keys():
        print(f"\nterm={term}")
        term_dict = inverted_indexes[term]
        for cord_uid in term_dict.keys():
            print(f"  cord_uid={cord_uid}")
            field_dict = term_dict[cord_uid]
            for field in field_dict.keys():
                frequency = field_dict[field]
                print(f"    field={field} : frequency={frequency}")
                
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
        
class term_dict_BM25F():
    def __init__(self):
        self.td = dict()

    def clear(self):
        self.td.clear()

    def is_in(self, term):
        return term in self.td

    def process_term(self, term, cord_uid, field):
        if self.is_in(term):
            self.update_term(term, field)
        else:
            self.add_term(term, cord_uid, field)

    def add_term(self, term, cord_uid, field):
        
        field_dict = dict()
        field_dict['author'] = 0
        field_dict['sections'] = 0
        field_dict['title'] = 0
        field_dict['abstract'] = 0
        
        field_dict[field] += 1
        self.td[term] = (cord_uid, field_dict)

    def update_term(self, term, field):
        self.td[term][1][field] += 1

    def get_keys(self):
        return self.td.keys()

    def get_value(self, key):
        return self.td[key]

    def print_dict(self):
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

    def write_to_Index_BM25F(self, term_dict_bm25f, inverted_indexes):
        """Add a document's field-specific term frequencies to inverted_indexes."""
        for term in term_dict_bm25f.get_keys():
            if (len(term) > 255):
                continue

            cord_uid = term_dict_bm25f.get_value(term)[0]
            field_dict = term_dict_bm25f.get_value(term)[1]
            
            if term in inverted_indexes:
                inverted_indexes[term][cord_uid] = field_dict
            else:
                inverted_indexes[term] = dict()
                inverted_indexes[term][cord_uid] = field_dict
        return inverted_indexes

    def processDocument(self, rawText, cord_uid, inverted_indexes):
        bow = self.bagOfWords(rawText)
        cleanUnstemmedBoW = self.removeStopwords(bow)
        cleanStemmedBoW = self.stemming(cleanUnstemmedBoW)
        self.index(cleanStemmedBoW, cord_uid, inverted_indexes)
        return len(cleanStemmedBoW)