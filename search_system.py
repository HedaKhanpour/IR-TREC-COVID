from Rank.rank import Rank
from Index.term import processQuery
from Index.term import getTerm
import sys
import re
from operator import itemgetter
import os.path

# Counts the termfrequency of each term found in dataComplete, for each
# document, and adds it up. When divided by the total number of documents
# this should yield the average document length. Takes a while to complete.
# Result is: 627448052
def count_tokens(path_dataComplete):
    n_tokens = 0
    for sub_directory in os.listdir(path_dataComplete):
        sub_dir_path = r"{}{}".format(path_dataComplete, sub_directory)
        for file in os.listdir(sub_dir_path):
            file_path = sub_dir_path + "/{}".format(file)
            with open(file_path, "r") as f:
                for line in f:
                    m = re.match("[^,]+,(\d+)", line)
                    n_tokens += int(m.group(1))
        print("{} tokens counted after directory {}".format(n_tokens, sub_directory))

# Counts the number of documents: 336596
def count_documents(path_metadata):
    with open(path_metadata, "r", encoding="utf-8") as f:
        print(len(list(f))-1)

def make_rank_object():
    # Change free parameters
    k1 = 1.2
    b = 0.75

    # Document calculations
    documents_count = 336596
    doc_length = 627448052 / 192509 # THE NUMERATOR NEEDS TO BE UPDATED WITH THE COUNTS FOR THE NEW DATACOMPLETE # Based on the output of the count_tokens() and count_documents() functions respectively
    ranker = Rank(k1, b, documents_count, doc_length)
    return ranker

def main(path_dataComplete):
    
    # Extract the 50 topic queries from topics-rnd5.xml
    topic_queries = []
    with open("topics-rnd5.xml", "r") as f:
        for line in f:
            match = re.match(".*<query>([^<]*)<\/query>.*", line)
            if match:
                topic_queries.append(match.group(1))
    if len(topic_queries) != 50:
        sys.exit("There should be 50 topics, found {}".format(len(topic_queries)))
    
    # For each query: compute a score for each document and select the 1000 documents with the highest score
    results_file_path = r"trec_eval-master/our_data/test_results.txt"
    open(results_file_path, "w").close() # Clear the contents of the file
    ranker = make_rank_object()
    query_nr = 1
    for query in topic_queries:
        doc_scores = dict()
        terms = processQuery(query)
        
        print()
        print(terms)
        for term in terms:
            doc = getTerm(term, path=path_dataComplete)
            for doc_id in doc.payloads.keys():
                tf = doc.payloads[doc_id]
                score = ranker.calculate_BM25_score(tf)
                if doc_id in doc_scores:
                    doc_scores[doc_id] += score
                else:
                    doc_scores[doc_id] = score
        
        # Sort the results and select the 1000 highest scored documents
        top_1000 = dict(sorted(doc_scores.items(), key = itemgetter(1), reverse = True)[:1000])
        print("Number of documents for query number {}: {}".format(query_nr, len(doc_scores)))
                
        # Write the top 1000 document scores for this query to a .txt file
        with open(results_file_path, "a") as f:
            doc_rank = 1
            for doc_id, doc_score in top_1000.items():
                string = "{} Q0 {} {} {} TEST-RUN-0\n".format(query_nr, doc_id, doc_rank, doc_score)
                f.write(string)
                doc_rank += 1
            query_nr += 1

if __name__ == "__main__":
    path_dataComplete = r"D:/Universiteit/Master (Large Files)/IR Project/dataComplete/"
    path_metadata = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/metadata.csv"
    
    #count_tokens(path_dataComplete)
    #count_documents(path_metadata)
    path_dataComplete = "../dataComplete/"
    main(path_dataComplete)
