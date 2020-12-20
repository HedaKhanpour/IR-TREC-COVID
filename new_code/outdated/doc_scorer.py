import re
import sys
from math import log
from index import processQuery
from operator import itemgetter
import pickle


# self.N should be the number of documents for calculating IDF, but the document length for the denominator
# docSize in calculate_IDF should be the number of documents
# termSize in the calculate_IDF should be the term frequency
# Solved

class Constants():

    def __init__(self, path_doc_lengths, k=1.2, b=0.75):
<<<<<<< HEAD:new_code/doc_scorer.py
        self.k = k  # Free BM25 parameter in the range [0, +inf)
        self.b = b  # Free BM25 parameter in the range [0, 1]

        self.doc_count = 84143
        self.avg_doc_length = 2669.2203629535434
=======
        self.k = k # Free BM25 parameter in the range [0, +inf)
        self.b = b # Free BM25 parameter in the range [0, 1]
            
        self.doc_count = 99447
        self.avg_doc_length = 2448.7878166259416
>>>>>>> 74096615efde529daa8928fd3e72c4871c4228d8:new_code/outdated/doc_scorer.py


def extract_queries(path_topics="../topics-rnd5.xml", nr_of_queries=50):
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
                                   key=itemgetter(1), reverse=True)[:top_n])

    with open(output_file_path, "a") as f:
        doc_rank = 1
        for cord_uid, doc_score in top_n_doc_scores.items():
            string = f"{query_nr} Q0 {cord_uid} {doc_rank} {doc_score} TEST-RUN-0\n"
            f.write(string)
            doc_rank += 1


def compute_term_BM25(term, tf, docs_containing_term_count, doc_count,
                      avg_doc_length, doc_length, k, b):
    """Compute the BM25 score for a document with regard to a single query term"""

    numerator = (k + 1) * tf
    denominator = tf + k * (1 - b + b * doc_length / avg_doc_length)
    IDF = log((doc_count + 1) / docs_containing_term_count)
    score = numerator / denominator * IDF

    return score


def compute_term_BM25F(term, document, tf, docs_containing_term_count, doc_count,
                       terms_count, average_terms_length, boost, k, b):
    first_formula_part = compute_weighted_fields(document, tf, boost, b, terms_count, average_terms_length) / (
                k + compute_weighted_fields(term, document, tf, boost, terms_count, average_terms_length))
    second_formula_part = (doc_count - docs_containing_term_count + 0.5) / (docs_containing_term_count + 0.5)
    score = first_formula_part * log(second_formula_part)
    return score


def compute_weighted_fields(fields, tf, boost, b, terms_size, average_term_size):
    weighted_fields_score = 0

    for f in fields:
        weighted_fields_score += (tf[f] * boost[f]) / ((1 - b[f]) + b[f] * terms_size[f] / average_term_size[f])

    return weighted_fields_score


def compute_improved_doc_scores(query_terms, boost, inverted_indexes, doc_lengths, constants):
    """Compute the BM25F score for each document given a query."""

    doc_scores = dict()  # This is to contain each document's score

    for term in query_terms:  # For each query term ...
        # Retrieve information regarding the current term
        term_info = inverted_indexes[term]
        n_docs_containing_term = len(term_info)

        # For each document that contains the term ...
        for cord_uid in term_info.keys():
            tf = term_info[cord_uid]  # Retrieve the term frequency

            # Compute document's score for this term
            score = compute_term_BM25F(term, cord_uid, tf, n_docs_containing_term,
                                       constants.doc_count,
                                       constants.term_count,
                                       constants.avg_term_coumt,
                                       constants.avg_doc_length,
                                       boost, constants.k, constants.b)

            # (term, document, tf, docs_containing_term_count, doc_count,
            #  terms_count, average_terms_length, boost, k, b)

            # Store or increment the score
            if cord_uid in doc_scores:
                doc_scores[cord_uid] += score
            else:
                doc_scores[cord_uid] = score

    return doc_scores


def compute_doc_scores(query_terms, inverted_indexes, doc_lengths, constants):
    """Compute the BM25 score for each document given a query."""

    doc_scores = dict()  # This is to contain each document's score

    for term in query_terms:  # For each query term ...

        # Retrieve information regarding the current term
        term_info = inverted_indexes[term]
        n_docs_containing_term = len(term_info)

        # For each document that contains the term ...
        for cord_uid in term_info.keys():
            tf = term_info[cord_uid]  # Retrieve the term frequency
            doc_length = doc_lengths[cord_uid]  # Retrieve the document length

            # Compute document's score for this term
            score = compute_term_BM25(term, tf, n_docs_containing_term,
                                      constants.doc_count,
                                      constants.avg_doc_length, doc_length,
                                      constants.k, constants.b)

            # Store or increment the score
            if cord_uid in doc_scores:
                doc_scores[cord_uid] += score
            else:
                doc_scores[cord_uid] = score

    return doc_scores


def score_documents(queries, inverted_indexes, doc_lengths, constants,
                    output_file_dir=r"../trec_eval-master/our_data/",
                    output_file_name="results"):
    """For each given query: scores documents, saving the best 10,000 scores."""

    # The path to the output file
    output_file_path = output_file_dir + output_file_name + ".txt"

    # Clear the contents of the output file
    open(output_file_path, "w").close()

    query_nr = 1  # Used to keep track of which query is being processed
    for query in queries:  # For each query ...
        print(f"Processing query {query_nr}: '{query}'")

        # Transform the query terms to the desired form (i.e. tokenized, stemmed, ...)
        query_terms = processQuery(query)

        # Compute the BM25 score for each document for the current query
        doc_scores = compute_doc_scores(query_terms, inverted_indexes,
                                        doc_lengths, constants)

        # Write the top 1000 document scores for this query to a .txt file
        write_output_file(query_nr, doc_scores, output_file_path)

        # Increment the query number for the next iteration
        query_nr += 1


if __name__ == "__main__":
    path_dataComplete = r"D:/Universiteit/Master (Large Files)/IR Project/dataComplete/"
    path_metadata = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/metadata.csv"
    path_doc_parses = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/document_parses/"
<<<<<<< HEAD:new_code/doc_scorer.py
    path_inverted_indexes = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/inverted_indexes.pkl"
    path_doc_lengths = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/doc_lengths.pkl"

    # Load the dictionary containing the length of each document
=======
    path_inverted_indexes = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/pickle_files/inverted_indexes.pkl"
    path_doc_lengths = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/pickle_files/document_lengths.pkl"
        
    # Load the dictionary containing the inverted indexes
>>>>>>> 74096615efde529daa8928fd3e72c4871c4228d8:new_code/outdated/doc_scorer.py
    with open(path_inverted_indexes, 'rb') as f:
        inverted_indexes = pickle.load(f)

    # Load the dictionary containing the length of each document
    with open(path_doc_lengths, 'rb') as f:
        doc_lengths = pickle.load(f)

    queries = extract_queries()
    constants = Constants(path_doc_lengths=path_doc_lengths, k=1.2, b=0.75)
    score_documents(queries, inverted_indexes, doc_lengths, constants, output_file_name="results")
