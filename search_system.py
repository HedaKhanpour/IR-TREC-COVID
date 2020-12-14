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
# Result for the 2020-07-16 data set: 159729133
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
# Result for the 2020-07-16 data set: 192509
def count_documents(path_metadata):
    with open(path_metadata, "r", encoding="utf-8") as f:
        print(len(list(f))-1)

def inspect_judgements(output_path=r"trec_eval-master/our_data/test_results.txt",
                       gold_path=r"trec_eval-master/our_data/CRJ.txt",
                       metadata_path=r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/metadata.csv"):
    
    output = []
    with open(output_path, "r") as f:
        for line in f:
            split = line.split(" ")
            #              Topic NR  useless   Doc ID    Rank      Score     Run-tag
            output.append((split[0], split[1], split[2], split[3], split[4], re.sub("\\n", "", split[5])))
    
    gold = []
    with open(gold_path, "r") as f:
        for line in f:
            split = line.split(" ")
            #            Topic NR  ????      Doc ID    Score
            gold.append((split[0], split[1], split[2], re.sub("\\n", "", split[3])))   
    print(f"len(output)={len(output)}")
    print(f"len(gold)={len(gold)}")
    print()
    
    unique_output_ids = set([x[2] for x in output])
    unique_gold_ids = set([x[2] for x in gold])
    print(f"len(unique_output_ids)={len(unique_output_ids)}")
    print(f"len(unique_gold_ids)={len(unique_gold_ids)}")
    print()
    
    only_output = unique_output_ids - unique_gold_ids
    only_gold = unique_gold_ids - unique_output_ids
    symmetric_difference = unique_output_ids.symmetric_difference(unique_gold_ids)
    intersection = unique_output_ids.intersection(unique_gold_ids)
    print(f"len(only_output)={len(only_output)}")
    print(f"len(only_gold)={len(only_gold)}")
    print(f"len(symmetric_difference)={len(symmetric_difference)}")
    print(f"len(intersection)={len(intersection)}")
    print()
    print()
    print()
    
    all_doc_ids = []
    with open(metadata_path, "r",  encoding="utf-8") as f:
        f.readline()
        for line in f:
            all_doc_ids.append(line.split(",")[0])
    unique_doc_ids = set(all_doc_ids)
    print(f"len(all_doc_ids)={len(all_doc_ids)}")
    print(f"len(unique_doc_ids)={len(unique_doc_ids)}")
    print()
    
    sd_all_vs_output = unique_doc_ids.symmetric_difference(unique_output_ids)
    int_all_vs_output = unique_doc_ids.intersection(unique_output_ids)
    print(f"len(sd_all_vs_output)={len(sd_all_vs_output)}")
    print(f"len(int_all_vs_output)={len(int_all_vs_output)}") # This is as should be
    print()
    
    sd_all_vs_gold = unique_doc_ids.symmetric_difference(unique_gold_ids)
    int_all_vs_gold = unique_doc_ids.intersection(unique_gold_ids)
    print(f"len(sd_all_vs_gold)={len(sd_all_vs_gold)}")
    print(f"len(int_all_vs_gold)={len(int_all_vs_gold)}") # This is as should be
    print()
        

def make_rank_object(k1, b):
    
    # Document calculations
    documents_count = 192509
    doc_length = 159712070 / documents_count # Based on the output of the count_tokens() and count_documents() functions respectively
    ranker = Rank(k1, b, documents_count, doc_length)
    return ranker

def cheat(path_dataComplete, k1=1.2, b=0.75): # May not work exactly as intended
    
    gold = []
    with open(r"trec_eval-master/our_data/CRJ.txt", "r") as f:
        for line in f:
            split = line.split(" ")
            #            Topic NR  ????      Doc ID    Score
            gold.append((split[0], split[1], split[2], re.sub("\\n", "", split[3]))) 
    unique_gold_ids = set([x[2] for x in gold])
    
    topic_nr_list = [x[0] for x in gold]
    topic_nr_dict = {}
    for i in range(len(topic_nr_list)):
        topic_nr_dict[i] = topic_nr_list[i]
    doc_id_list = [x[2] for x in gold]
    doc_score_list = [x[3] for x in gold]
    #doc_gold_scores = {doc_id_list[i]:doc_score_list[i] for i in range(len(doc_id_list))} # gold judgements
    
    doc_gold_scores = []
    for topic_nr in range(1, 51):
        doc_gold_scores.append({doc_id_list[i]:int(doc_score_list[i]) for i in range(len(doc_id_list)) if int(topic_nr_list[i]) == topic_nr})
        
    
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
    results_file_path = r"trec_eval-master/our_data/results_cheating.txt"
    open(results_file_path, "w").close() # Clear the contents of the file
    ranker = make_rank_object(k1=1.2, b=0.75)
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
                if doc_id not in doc_gold_scores[query_nr-1].keys():
                    score = 0
                else:
                    score = doc_gold_scores[query_nr-1][doc_id]
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

def main(path_dataComplete, k1=1.2, b=0.75, output_file_name="results"):
    
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
    results_file_path = r"trec_eval-master/our_data/{}.txt".format(output_file_name)
    open(results_file_path, "w").close() # Clear the contents of the file
    ranker = make_rank_object(k1, b)
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
    #path_dataComplete = "../dataComplete/"
    #main(path_dataComplete)
    
    #inspect_judgements()
# =============================================================================
#     k1s = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
#     bs = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
# =============================================================================
    k1s = [0.1, 0.2, 0.3, 0.4]
    bs = [0.05, 0.1, 0.15, 0.2]
    for k1 in k1s:
        for b in bs:
            main(path_dataComplete, k1=k1, b=b, output_file_name="results_{}_{}".format(k1, b))