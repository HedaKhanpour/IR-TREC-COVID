import re
import sys
from math import log
from operator import itemgetter

from Util import processQuery
from Util import Constants

class DocumentRanker():

    def extract_queries(self, path_topics="../topics-rnd5.xml"):
        """Extracts the 50 queries from the list of 50 topics."""
        
        topic_queries = []
        with open(path_topics, "r") as f:
            for line in f:
                match = re.match(".*<query>([^<]*)<\/query>.*", line)
                if match:
                    topic_queries.append(match.group(1))
        if len(topic_queries) != 50:
            sys.exit("There should be 50 topics, found {}".format(
                    len(topic_queries)))
        
        return topic_queries
    
    def write_output_file(self, query_nr, doc_scores,
                          output_file_path, top_n=1000):
        """Write the top n document scores regarding some query to a .txt file."""
        
        # Sort by score and select the n highest scored documents
        top_n_doc_scores = dict(sorted(doc_scores.items(),
                                       key = itemgetter(1), reverse = True)[:top_n])
        
        with open(output_file_path, "a") as f:
            doc_rank = 1
            for cord_uid, doc_score in top_n_doc_scores.items():
                string = f"{query_nr} Q0 {cord_uid} {doc_rank} {doc_score} TEST-RUN-0\n"
                f.write(string)
                doc_rank += 1
    
    def compute_term_BM25(self, term, tf, docs_containing_term_count, doc_count,
                          avg_doc_length, doc_length, k, b):
        """Compute the BM25 score for a document regarding a single query term."""
        
        numerator = (k + 1)*tf
        denominator = tf + k*(1 - b + b*doc_length/avg_doc_length)
        IDF = log((doc_count + 1)/docs_containing_term_count)
        score = numerator/denominator*IDF
        
        return score
    
    def compute_doc_scores(self, query_terms, inverted_indexes,
                           doc_lengths):
        """Compute the BM25 score for each document given a query."""
        
        doc_scores = dict() # This is to contain each document's score
        for term in query_terms: # For each query term ...
            
            # Retrieve information regarding the current term
            term_info = inverted_indexes[term]
            n_docs_containing_term = len(term_info)
            
            # For each document that contains the term ...
            for cord_uid in term_info.keys():
                tf = term_info[cord_uid] # Retrieve the term frequency
                doc_length = doc_lengths[cord_uid] # Retrieve the document length
                
                # Compute document's score for this term
                score = self.compute_term_BM25(term, tf, n_docs_containing_term,
                                          Constants.doc_count,
                                          Constants.avg_doc_length, doc_length,
                                          Constants.k, Constants.b)
                
                # Store or increment the score
                if cord_uid in doc_scores:
                    doc_scores[cord_uid] += score
                else:
                    doc_scores[cord_uid] = score
        
        return doc_scores

    def rank_documents(self, inverted_indexes,
                        doc_lengths, path_topics,
                        path_results_dir=r"../trec_eval-master/our_data/",
                        results_file_name="results"):
        """
        Scores and ranks each document for each query.
        
        Given a list of queries this function determines for each query the
        BM25 score for each document. For each query the best 10,000 documents
        are then ranked based on their score (higher is better) and the
        results are written to a .txt file in such a form that it can be used
        as input to the TREC evaluation tool.
        """
        
        # Retrieve the queries
        queries = self.extract_queries(path_topics)
        
        # The path to the output file
        output_file_path = path_results_dir + results_file_name + ".txt"
        
        # Clear the contents of the output file
        open(output_file_path, "w").close()
        
        query_nr = 1 # Used to keep track of which query is being processed
        for query in queries: # For each query ...
            print(f"Processing query {query_nr}: '{query}'")
            
            # Transform the query terms to the desired form (i.e. tokenized, stemmed, ...)
            query_terms = processQuery(query)
            
            # Compute the BM25 score for each document for the current query
            doc_scores = self.compute_doc_scores(query_terms, inverted_indexes,
                                                 doc_lengths)
            
            # Write the top 1000 document scores for this query to a .txt file
            self.write_output_file(query_nr, doc_scores, output_file_path)
            
            # Increment the query number for the next iteration
            query_nr += 1
    
    