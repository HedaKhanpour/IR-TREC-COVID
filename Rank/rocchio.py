
from math import log

def rocchio(query, rel_docs, alpha=1.0, beta=0.75):
    # Calculate TF-IDF for each term for the set of relevant documents
    # 

    ## Assigning values to the query 
    result = dict()
    for q in query:
        result[q] = 1.0

    ## Collecting every term in the set of relevant documents
    rel_terms = []
    for d in rel_docs:
        doc = rel_docs[d]
        for term in doc:
            if not term in rel_terms:
                rel_terms.append(term)
    #print("Relevant terms: {}".format(rel_terms))

    ## For every relevant term
    for term in rel_terms:
        ## Term frequency
        tf = 0

        ## Number of relevant documents containing a the term
        nqi = 0

        ## For every relevant document
        for doc in rel_docs:
            ## If the term is in the document
            if term in rel_docs[doc]:
                nqi += 1
                ## For every term in the relevant document
                for doc_term in rel_docs[doc]:
                    ## Counting the term frequency 
                    if term == doc_term:
                        tf += 1
        #print("TF[{}]:{}".format(term, tf[term]))
        
        ## Calculating the IDF of the term
        idf = log((len(rel_docs) - nqi + 0.5) / (nqi + 0.5) + 1)

        ## Calculating the TF*IDF of the term
        tf_idf = tf * idf

        ## Calculating the feedback weight of the term
        feedback_weight = beta * (tf_idf / len(rel_docs))

        if term in result:
            result[term] = alpha * result[term] + feedback_weight
        elif feedback_weight > 0.0:
            result[term] = feedback_weight    
    return result
    


def test_bm25(query, doc, avg_doc_len, idf):
    #print("\n----------------------\n")
    k = 1.2
    b = 0.75
    doc_len = len(doc)
    #print("Document length: {}".format(doc_len))
    tf = dict()

    ## Calculating TF
    for q in query:
        tf[q] = 0
        for term in doc:
            if q == term:
                tf[q] = tf[q] + 1
        #print("TF[{}]:{}".format(q, tf[q]))
    
    score = 0
    for q in query:
        numerator = tf[q] * (k + 1)
        #print("Numerator[{}]: {}".format(q, str(numerator)))
        denominator = tf[q] + k * (1 - b + b * (doc_len / avg_doc_len))
        #print("Denominator[{}]: {}".format(q, str(denominator)))
        temp_score = idf[q] * (numerator / denominator)
        #print("Score[{}]: {}".format(q, str(temp_score)))
        score += temp_score
    return score

def calc_bm25(query, doc_dict):

    collection_size = len(doc_dict)
    #print("Collection size: {}".format(collection_size))

    avg_doc_len = 0
    for doc in doc_dict:
        avg_doc_len += len(doc_dict[doc])
    avg_doc_len = avg_doc_len / collection_size
    #print("Average document length: {}".format(avg_doc_len))

    ## Number of documents containing a given term of the query (qi)
    nqi = dict()
    for q in query:
        nqi[q] = 0
        for doc in doc_dict:
            if q in doc_dict[doc]:
                nqi[q] = nqi[q] + 1
        #print("nqi[{}]: {}".format(q, nqi[q]))
    
    ## Calculating IDF
    idf = dict()
    for q in query:
        idf[q] = log((collection_size - nqi[q] + 0.5) / (nqi[q] + 0.5) + 1)
        #print("idf[{}]: {}".format(q, idf[q]))
    
    scores = dict()
    for doc in doc_dict:
        scores[doc] = test_bm25(query, doc_dict[doc], avg_doc_len, idf)

    sorted_scores = dict(sorted(scores.items(), key = lambda item: item[1], reverse=True))
    #print(sorted_scores)
    return sorted_scores

if __name__ == "__main__":
    query = "hello world".split(" ")
    doc_dict = dict()
    doc_dict["d1"] = "hello hello world world good".split(" ")
    doc_dict["d2"] = "hello world world good place".split(" ")
    doc_dict["d3"] = "hello world good place".split(" ")
    doc_dict["d4"] = "hello world something something something".split(" ")
    doc_dict["d5"] = "something something good place good place good place".split(" ")
    
    ranking = calc_bm25(query, doc_dict)
    print("********** BM25 Ranking **********")
    print("For query: {}".format(query))
    for r in ranking:
        print("{}: {}".format(r, ranking[r]))

    ## Number of documents to take as the relevent document set for the rocchio algorithm
    top_k = 3

    ## Set of relevant documents
    rel_docs = dict()
    for rank in dict(list(ranking.items())[:top_k]):
        rel_docs[rank] = doc_dict[rank]

    expansion = rocchio(query, rel_docs)
    print(expansion)
    expanded_query = list(expansion.keys())
    ranking = calc_bm25(expanded_query, doc_dict)
    print("********** BM25 Ranking **********")
    print("For query: {}".format(expanded_query))
    for r in ranking:
        print("{}: {}".format(r, ranking[r]))
    

    
 
    