from math import log
import pickle
import time
from operator import itemgetter
from Util import processQuery

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

def rocchio_old(query, rel_docs, inverted_index, all_documents, 
    alpha=0.25, beta=0.75, gamma=0.25, weight_cutoff=0.75):
    # Calculate TF-IDF for each term for the set of relevant documents
    # 
    len_non_rel_docs = len(all_documents) - len(rel_docs)
    ## Assigning values to the query 
    expanded_query = dict()
    for q in query:
        expanded_query[q] = 0.9

    ## Collecting every term in the set of relevant documents
    startTime = time.time()
    rel_terms = []
    for doc in all_documents:
        if doc.cord_uid in rel_docs:
            rel_terms += docToTerms(doc)
    # Remove duplicate terms
    rel_terms = list(set(rel_terms))
    #print("[Rocchio] Extracting relevant terms: DONE")

    ## For every relevant term
    for term in rel_terms:
        ## Term frequency relevant document
        rel_tf = 0
        ## Term frequency non relevant document
        non_rel_tf = 0
        ## Number of relevant documents containing the term
        nqi = 0

        for cord_uid in inverted_index[term]:
            if cord_uid in rel_docs:
                rel_tf += inverted_index[term][cord_uid]
                nqi += 1
            else:
                non_rel_tf += inverted_index[term][cord_uid]

        ## Calculating the IDF of the term
        idf = log(float(len(all_documents)) / float(len(inverted_index[term])))
        #idf = log((len(rel_docs) + 1) / nqi)
        ## Calculating the TF*IDF of the term
        #tf_idf = tf * idf
        ## Calculating the feedback weight of the term
        feedback_weight = 0
        for cord_uid in inverted_index[term]:
            if cord_uid in rel_docs:
                feedback_weight += beta * idf * (rel_tf / len(rel_docs))
            else:
                feedback_weight -= gamma * idf * (non_rel_tf / len_non_rel_docs)

        if term in expanded_query:
            expanded_query[term] = (alpha * expanded_query[term]) + feedback_weight
        elif feedback_weight > weight_cutoff:
            expanded_query[term] = feedback_weight  
    return expanded_query

def rocchio(query, rel_docs, inverted_index, all_documents, 
    alpha=0.5, beta=0.75, gamma=0.25, top_k_terms=4):

    ## Assigning values to the query 
    expanded_query = dict()
    for q in query:
        expanded_query[q] = alpha * 1.0

    term_weight = dict()
    ## Sum the term weight for every relevant document
    for doc in all_documents:
        ## If the document is relevant
        if doc.cord_uid in rel_docs:
            ## Get every term in the relevant document
            rel_terms = docToTerms(doc)
            for term in rel_terms:
                doc_tf = inverted_index[term][doc.cord_uid]
                if term in term_weight:
                    term_weight[term] = term_weight[term] + doc_tf
                else:
                    term_weight[term] = doc_tf
    
    for term in term_weight:
        rel_docs_containing_term = 0
        ## Count the relevant documents containting the term
        for cord_uid in inverted_index[term]:
            if cord_uid in rel_docs:
                rel_docs_containing_term += 1
        
        ## Calculate the IDF of the term for the relevant document set
        idf = log(len(rel_docs) / rel_docs_containing_term)
        tf_idf = term_weight[term] * idf
        normalized_weight = beta * (1 / len(rel_docs)) * tf_idf
        term_weight[term] = normalized_weight

    term_weight = dict(sorted(term_weight.items(), key = itemgetter(1), reverse = True)[:top_k_terms])

    for term in term_weight:
        if term in expanded_query:
            expanded_query[term] = expanded_query[term] + term_weight[term]
        elif term_weight[term] > 0.0:
            expanded_query[term] = term_weight[term]
    return expanded_query

                



if __name__ == "__main__":
    '''
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
    #query = queries[0]

    output_file_path = "trec_eval-master/our_data/results.txt"
    output_file_path_2 = "trec_eval-master/our_data/results_2.txt"
    # Clear the contents of the output file
    open(output_file_path, "w").close()
    open(output_file_path_2, "w").close()

    query_nr = 1 # Used to keep track of which query is being processed
    for query in queries:
        print(f"Processing query {query_nr}: '{query}'")
        # Transform the query terms to the desired form (i.e. tokenized, stemmed, ...)
        query_terms = processQuery(query)
        
        # Compute the BM25 score for each document for the current query
        bm25_time = time.time()
        doc_scores = compute_doc_scores(query_terms, inverted_index,
                                            doc_lengths)
        #print("Calculating BM25 scores: DONE, time: {}".format(time.time() - bm25_time))

        ## Set of relevant documents
        top_k = 1
        rel_docs = dict()
        for rank in dict(list(doc_scores.items())[:top_k]):
            rel_docs[rank] = doc_scores[rank]
        #rocchio_time = time.time()
        expansion = rocchio(query_terms, rel_docs, inverted_index, documents)
        #print("Calculating rocchio query expansion: DONE, time: {}".format(time.time() - rocchio_time))
        expanded_query = list(expansion.keys())
        #for key in expansion:
        #print("{}:{}".format(key, expansion[key]))
        #print("Expanded query length: {}".format(len(expanded_query)))

        # Compute the BM25 score for each document for the current query
        #bm25_time_2 = time.time()
        doc_scores_2 = compute_doc_scores(expanded_query, inverted_index,
                                            doc_lengths)
        #print("Calculating BM25 scores_2: DONE, time: {}".format(time.time() - bm25_time_2))

        
        # Write the top 1000 document scores for this query to a .txt file
        write_output_file(query_nr, doc_scores, output_file_path)
        write_output_file(query_nr, doc_scores_2, output_file_path_2)
        #print("Calculating BM25 scores_2: DONE")
        
        # Increment the query number for the next iteration
        query_nr += 1
        if query_nr > 50:
            break
    '''

    '''
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
    '''

 
    