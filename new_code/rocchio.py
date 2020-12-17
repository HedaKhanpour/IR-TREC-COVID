from doc_scorer import *
from math import log
import pickle
from operator import itemgetter
from index import Index
from data_gatherer import *

def docToTerms(doc):
    # Retrieve the document fields
    author_string = "" if doc.authors == None else " ".join(filter(None, doc.authors))
    sections_string = "" if doc.sections == None else " ".join(filter(None, doc.sections))
    title_string = "" if doc.title == None else doc.title
    abstract_string = "" if doc.abstract == None else doc.abstract
    doc_string = f"{author_string} {sections_string} {title_string} {abstract_string}"

    # Process the raw text to a list of stemmed terms using the processQuery function.
    terms = processQuery(doc_string)
    return terms

def rocchio(query, rel_docs, inverted_index, all_documents, alpha=1.0, beta=0.75):
    # Calculate TF-IDF for each term for the set of relevant documents
    # 

    ## Assigning values to the query 
    expanded_query = dict()
    for q in query:
        expanded_query[q] = 1.0

    ## Collecting every term in the set of relevant documents
    rel_terms = []
    for doc in all_documents:
        if doc.cord_uid in rel_docs:
            rel_terms += docToTerms(doc)
    # Remove duplicate terms
    rel_terms = list(set(rel_terms))
    print("[Rocchio] Extracting relevant terms: DONE")

    ## For every relevant term
    for term in rel_terms:
        ## Term frequency
        tf = 0
        ## Number of relevant documents containing a the term
        nqi = 0

        for cord_uid in inverted_index[term]:
            if cord_uid in rel_docs:
                tf += inverted_index[term][cord_uid]
                nqi += 1

        ## Calculating the IDF of the term
        idf = log((len(rel_docs) - nqi + 0.5) / (nqi + 0.5) + 1)
        ## Calculating the TF*IDF of the term
        tf_idf = tf * idf
        ## Calculating the feedback weight of the term
        feedback_weight = beta * (tf_idf / len(rel_docs))

        if term in expanded_query:
            expanded_query[term] = alpha * expanded_query[term] + feedback_weight
        elif feedback_weight > 0.0:
            expanded_query[term] = feedback_weight    
    return expanded_query

if __name__ == "__main__":
    
    path_inverted_index = "../inverted_indexes.pkl"
    path_doc_lengths = "../doc_lengths.pkl"
    path_documents = "../cord-19_2020-07-16/documents.pkl"
    
    # Load the dictionary containing the inverted index
    with open(path_inverted_index, 'rb') as f:
        inverted_index = pickle.load(f)
    print("Loading inverted index: DONE")
    # Load the dictionary containing the length of each document
    with open(path_doc_lengths, 'rb') as f:
        doc_lengths = pickle.load(f)
    print("Loading doc lenghts: DONE")

    with open(path_documents, 'rb') as f:
        documents = pickle.load(f)
    print("Loading documents: DONE")

    queries = extract_queries(path_topics="topics-rnd5.xml")
    query = queries[0]

    constants = Constants(path_doc_lengths=path_doc_lengths, k=1.2, b=0.75)

    # Transform the query terms to the desired form (i.e. tokenized, stemmed, ...)
    query_terms = processQuery(query)
    
    # Compute the BM25 score for each document for the current query
    doc_scores = compute_doc_scores(query_terms, inverted_index,
                                        doc_lengths, constants)
    print("Calculating BM25 scores: DONE")
   
    ## Set of relevant documents
    top_k = 10
    rel_docs = dict()
    for rank in dict(list(doc_scores.items())[:top_k]):
        rel_docs[rank] = doc_scores[rank]

    expansion = rocchio(query_terms, rel_docs, inverted_index, documents)
    print("Calculating rocchio query expansion: DONE")
    expanded_query = list(expansion.keys())

    # Compute the BM25 score for each document for the current query
    doc_scores_2 = compute_doc_scores(expanded_query, inverted_index,
                                        doc_lengths, constants)
    print("Calculating BM25 scores_2: DONE")
    
    # Sort by score and select the n highest scored documents
    top_n = 20
    top_n_doc_scores = dict(sorted(doc_scores.items(),
                                   key = itemgetter(1), reverse = True)[:top_n])
    
    top_n_doc_scores_2 = dict(sorted(doc_scores_2.items(),
                                   key = itemgetter(1), reverse = True)[:top_n])
    print("Sorting top n scores: DONE")
    for i in range(top_n):
        id_1 = list(top_n_doc_scores.keys())[i]
        id_2 = list(top_n_doc_scores_2.keys())[i]
        score_1 = top_n_doc_scores[id_1]
        score_2 = top_n_doc_scores_2[id_2]
        print("#{}: {}[{}] --- {}[{}]".format(i, id_1, score_1, id_2, score_2))

    
 
    