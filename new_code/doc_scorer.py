import re
import sys
from math import log
from term import processQuery
from term import getTerm
from operator import itemgetter
import pickle

# self.N should be the number of documents for calculating IDF, but the document length for the denominator
# docSize in calculate_IDF should be the number of documents
# termSize in the calculate_IDF should be the term frequency
# Solved


class Constants():
    
    def __init__(self, path_doc_lengths, k=1.2, b=0.75):
        self.k = k # Free BM25 parameter in the range [0, +inf)
        self.b = b # Free BM25 parameter in the range [0, 1]
        
        # Load the dictionary containing the length of each document
        with open(path_doc_lengths, 'rb') as f:
            self.doc_lengths = pickle.load(f)
            
        self.doc_count = 192509 # SHOULD BE UPDATED ONCE THE DOCUMENT_LENGTHS ARE IN ***
        self.avg_doc_length = 159712070 / self.doc_count # SHOULD BE UPDATED ONCE THE DOCUMENT_LENTHS ARE IN ***

def extract_queries(path_topics="topics-rnd5.xml", nr_of_queries=50):
    """Extracts queries from a list of topics."""
    
    topic_queries = []
    with open(path_topics, "r") as f:
        for line in f:
            match = re.match(".*<query>([^<]*)<\/query>.*", line)
            if match:
                topic_queries.append(match.group(1))
    if len(topic_queries) != nr_of_queries:
        sys.exit("There should be {} topics, found {}".format(
                nr_of_queries, len(topic_queries)))
    
    return topic_queries

def write_output_file(query_nr, doc_scores, output_file_path, top_n=1000):
    """Write the top n document scores with regard to some query to a .txt file"""
    
    # Sort by score and select the n highest scored documents
    top_n_doc_scores = dict(sorted(doc_scores.items(),
                                   key = itemgetter(1), reverse = True)[:top_n])
    
    with open(output_file_path, "a") as f:
        doc_rank = 1
        for doc_id, doc_score in top_n_doc_scores.items():
            string = f"{query_nr} Q0 {doc_id} {doc_rank} {doc_score} TEST-RUN-0\n"
            f.write(string)
            doc_rank += 1
    
def compute_term_BM25(term, tf, docs_containing_term_count, doc_count,
                      avg_doc_length, doc_length, k, b):
    """Compute the BM25 score for a document with regard to a single query term"""
    
    numerator = (k + 1)*tf
    denominator = tf + k*(1 - b + b*doc_length/avg_doc_length)
    IDF = log((doc_count + 1)/docs_containing_term_count)
    score = numerator/denominator*IDF
    
    return score

def compute_doc_scores(query_terms, constants):
    """Compute the BM25 score for each document given a query."""
    
    doc_scores = dict() # This is to contain each document's score
    
    for term in query_terms: # For each query term ...
    
        # Retrieve information regarding the current term
        term_info = getTerm(term, path=path_dataComplete)
        
        # For each document that contains the term ...
        for doc_id in term_info.payloads.keys():
            tf = term_info.payloads[doc_id] # Retrieve the term frequency
            doc_length = constants.doc_lengths[doc_id] # Retrieve the document length
            
            # Compute document's score for this term
            score = compute_term_BM25(term, tf, term_info.n_docs_containing_term,
                                      constants.doc_count,
                                      constants.avg_doc_length, doc_length,
                                      constants.k, constants.b)
            
            # Store or increment the score
            if doc_id in doc_scores:
                doc_scores[doc_id] += score
            else:
                doc_scores[doc_id] = score
    
    return doc_scores

def score_documents(queries, constants, output_file_dir=r"trec_eval-master/our_data/",
                    output_file_name="results"):
    """For each given query: scores documents, saving the best 10,000 scores."""
    
    # The path to the output file
    output_file_path = output_file_dir + output_file_name + ".txt"
    
    # Clear the contents of the output file
    open(output_file_path, "w").close()
    
    query_nr = 1 # Used to keep track of which query is being processed
    for query in queries: # For each query ...
        print(f"Processing query {query_nr}: '{query}'")
        
        # Transform the query terms to the desired form (i.e. tokenized, stemmed, ...)
        query_terms = processQuery(query)
        
        # Compute the BM25 score for each document for the current query
        doc_scores = compute_doc_scores(query_terms, constants)
        
        # Write the top 1000 document scores for this query to a .txt file
        write_output_file(query_nr, doc_scores, output_file_path)
        
        # Increment the query number for the next iteration
        query_nr += 1
    

if __name__ == "__main__":
    path_dataComplete = r"D:/Universiteit/Master (Large Files)/IR Project/dataComplete/"
    path_metadata = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/metadata.csv"
    path_doc_parses = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/document_parses/"
    path_doc_lengths = "doc_lengths.pkl"
    
# =============================================================================
#     queries = extract_queries()
#     constants = Constants(path_doc_lengths=path_doc_lengths, k=1.2, b=0.75)
#     score_documents(queries, constants, output_file_name="results_new")
# =============================================================================
    
    
    
    