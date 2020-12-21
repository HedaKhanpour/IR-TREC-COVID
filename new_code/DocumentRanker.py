import re
import sys
from math import log
from operator import itemgetter
import random
from sentence_transformers import SentenceTransformer, util

from Util import processQuery
from Util import Constants
from rocchio import rocchio

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

    def compute_term_BM25(self, term, tf,
                          docs_containing_term_count, doc_count,
                          avg_doc_length, doc_length, k, b):
        """Compute the BM25 score for a document regarding a single query term."""

        numerator = (k + 1) * tf
        denominator = tf + k * ((1 - b) + (b * (doc_length / avg_doc_length)))
        IDF = log((doc_count + 1)/docs_containing_term_count)
        score = (numerator / denominator) * IDF

        return score
    
    def compute_doc_scores_BM25F(self, query_terms, 
                                 inverted_indexes, 
                                 doc_length_info_bm25f,
                                 parameters):
        """Compute the BM25 score for each document given a query."""
        
        doc_scores = dict() # This is to contain each document's score
        for term in query_terms: # For each query term ...
            
            # Retrieve information regarding the current term
            term_info = inverted_indexes[term]
            n_docs_containing_term = len(term_info)
            
            # For each document that contains the term ...
            for cord_uid in term_info.keys():
                
                tf_field_dict = term_info[cord_uid]
                length_info = doc_length_info_bm25f[cord_uid]
                
                # Compute document's score for this term
                score = self.compute_term_BM25F(term, tf_field_dict, n_docs_containing_term, Constants.doc_count,
                          length_info,
                          parameters.k,
                          parameters.weight_title, parameters.weight_author, parameters.weight_abstract, parameters.weight_sections,
                          parameters.b_title, parameters.b_author, parameters.b_abstract, parameters.b_sections,
                          Constants.avg_title_length, Constants.avg_author_length, Constants.avg_abstract_length, Constants.avg_sections_length)
                
                # Store or increment the score
                if cord_uid in doc_scores:
                    doc_scores[cord_uid] += score
                else:
                    doc_scores[cord_uid] = score
        
        return doc_scores

    def compute_term_BM25F(self, term, tf_field_dict, docs_containing_term_count, doc_count,
                           length_info,
                           k,
                           weight_title, weight_author, weight_abstract, weight_sections,
                           b_title, b_author, b_abstract, b_sections,
                           avg_title_length, avg_author_length, avg_abstract_length, avg_sections_length):
        """Compute the BM25F score for a document regarding a single query term."""
        
        tf_title = tf_field_dict['title']
        tf_author = tf_field_dict['author']
        tf_abstract = tf_field_dict['abstract']
        tf_sections = tf_field_dict['sections']
        
        length_title = length_info['title']
        length_author = length_info['author']
        length_abstract = length_info['abstract']
        length_sections = length_info['sections']
        
        title_score = weight_title * tf_title / (1 - b_title + b_title*length_title/avg_title_length)
        author_score = weight_author * tf_author / (1 - b_author + b_author*length_author/avg_author_length)
        abstract_score = weight_abstract * tf_abstract / (1 - b_abstract + b_abstract*length_abstract/avg_abstract_length)
        sections_score = weight_sections * tf_sections / (1 - b_sections + b_sections*length_sections/avg_sections_length)
        accumulated_score = title_score + author_score + abstract_score + sections_score
        
        numerator = (k + 1) * accumulated_score
        denominator = k + accumulated_score
        IDF = log((doc_count + 1)/docs_containing_term_count)
        score = (numerator / denominator) * IDF

        return score
    
    def compute_doc_scores(self, query_terms, inverted_indexes,
                           doc_lengths, parameters):
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
                                          parameters.k, parameters.b)
                
                # Store or increment the score
                if cord_uid in doc_scores:
                    doc_scores[cord_uid] += score
                else:
                    doc_scores[cord_uid] = score
        
        return doc_scores
    
    def rank_at_random(self, path_topics, documents,
                       path_results_dir=r"../trec_eval-master/our_data/",
                       results_file_name="results_random"):
        """Scores and ranks each document for each query at random."""
        
        # Retrieve the queries
        queries = self.extract_queries(path_topics)
        
        # The path to the output file
        output_file_path = path_results_dir + results_file_name + ".txt"
        
        # Clear the contents of the output file
        open(output_file_path, "w").close()
        
        query_nr = 1 # Used to keep track of which query is being processed
        for query in queries: # For each query ...
            print(f"Processing query {query_nr}: '{query}'")
            
            # determine the BM25 score for each document at random
            doc_scores = dict()
            for document in documents:
                doc_scores[document.cord_uid] = random.randint(0, 2)
            
            # Write the top 1000 document scores for this query to a .txt file
            self.write_output_file(query_nr, doc_scores, output_file_path)
            
            # Increment the query number for the next iteration
            query_nr += 1
        

    def rank_documents(self, inverted_indexes,
                        doc_lengths,
                        parameters,
                        path_topics,
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
                                                doc_lengths, parameters)
            
            # Write the top 1000 document scores for this query to a .txt file
            self.write_output_file(query_nr, doc_scores, output_file_path)
            
            # Increment the query number for the next iteration
            query_nr += 1
    
    def rank_documents_bm25f(self, inverted_indexes_bm25f,
                             doc_length_info_bm25f,
                             parameters,
                             path_topics,
                             path_results_dir=r"../trec_eval-master/our_data/",
                             results_file_name="results_BM25F"):
        
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
            doc_scores = self.compute_doc_scores_BM25F(query_terms,
                                                       inverted_indexes_bm25f,
                                                       doc_length_info_bm25f,
                                                       parameters)
            
            # Write the top 1000 document scores for this query to a .txt file
            self.write_output_file(query_nr, doc_scores, output_file_path)
            
            # Increment the query number for the next iteration
            query_nr += 1
    
    def rank_with_reranker(self, inverted_indexes, doc_lengths,
                           documents_dict, parameters, path_topics,
                           path_results_dir=r"../trec_eval-master/our_data/",
                           results_file_name="results_rerank"):
        """
        Scores and ranks each document for each query, then reranks them.
        
        This function first scores each document with BM25, then it reranks
        the highest scored 1000 of them using a BERT model trained on MS MARCO
        (real user queries from Bing seach engine).
        """
        
        def rerank(query, documents_dict, doc_scores, model):
            
            query_embedding = model.encode(query)
            for cord_uid in doc_scores.keys():
                document = documents_dict[cord_uid]
                title = document.title
                abstract = document.abstract
                text_string = title + " " + abstract
    
                passage_embedding = model.encode(text_string)
                rerank_score = util.pytorch_cos_sim(query_embedding, passage_embedding)[0][0].item()
                doc_scores[cord_uid] = doc_scores[cord_uid] + rerank_score
        
        model = SentenceTransformer('distilroberta-base-msmarco-v2')
        
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
                                                 doc_lengths, parameters)
            
            # Sort by score and select the n highest scored documents
            doc_scores = dict(sorted(doc_scores.items(),
                                           key = itemgetter(1), reverse = True)[:1000])
            
            
            rerank(query, documents_dict, doc_scores, model)
            
            # Sort by score and select the n highest scored documents
            doc_scores = dict(sorted(doc_scores.items(),
                                           key = itemgetter(1), reverse = True))
            
            # Write the top 1000 document scores for this query to a .txt file
            self.write_output_file(query_nr, doc_scores, output_file_path)
            
            # Increment the query number for the next iteration
            query_nr += 1
            
            
    def rank_BM25F_with_reranker(self, inverted_indexes_bm25f,
                                           doc_length_info_bm25f,
                                           documents_dict, parameters,
                                           path_topics, 
                                           path_results_dir=r"../trec_eval-master/our_data/",
                                           results_file_name="results__BM25F_rerank"):
        """
        Scores and ranks each document for each query with BM24F, then reranks them.
        
        This function first scores each document with BM25F, then it reranks
        the highest scored 1000 of them using a BERT model trained on MS MARCO
        (real user queries from Bing seach engine).
        """
        
        def rerank(query, documents_dict, doc_scores, model):
            
            query_embedding = model.encode(query)
            for cord_uid in doc_scores.keys():
                document = documents_dict[cord_uid]
                title = document.title
                abstract = document.abstract
                text_string = title + " " + abstract
    
                passage_embedding = model.encode(text_string)
                rerank_score = util.pytorch_cos_sim(query_embedding, passage_embedding)[0][0].item()
                doc_scores[cord_uid] = doc_scores[cord_uid] + rerank_score
        
        model = SentenceTransformer('distilroberta-base-msmarco-v2')
        
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
            doc_scores = self.compute_doc_scores_BM25F(query_terms,
                                                       inverted_indexes_bm25f,
                                                       doc_length_info_bm25f, parameters)
            
            # Sort by score and select the n highest scored documents
            doc_scores = dict(sorted(doc_scores.items(),
                                           key = itemgetter(1), reverse = True)[:1000])
            
            
            rerank(query, documents_dict, doc_scores, model)
            
            # Sort by score and select the n highest scored documents
            doc_scores = dict(sorted(doc_scores.items(),
                                           key = itemgetter(1), reverse = True))
            
            # Write the top 1000 document scores for this query to a .txt file
            self.write_output_file(query_nr, doc_scores, output_file_path)
            
            # Increment the query number for the next iteration
            query_nr += 1

    def rank_documents_rocchio_with_bm25f(self, inverted_indexes,
                               doc_lengths, doc_lengths_bm25f,
                               inverted_indexes_bm25f, documents, path_topics,
                               path_results_dir=r"../trec_eval-master/our_data/",
                               results_file_name="results"):
        """
        Scores and ranks each document for each query, then expand the query and rank it again.

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
        output_file_path_2 = path_results_dir + results_file_name + "_2.txt"

        # Clear the contents of the output file
        open(output_file_path, "w").close()
        open(output_file_path_2, "w").close()

        query_nr = 1  # Used to keep track of which query is being processed
        for query in queries:  # For each query ...
            print(f"Processing query {query_nr}: '{query}'")

            # Transform the query terms to the desired form (i.e. tokenized, stemmed, ...)
            query_terms = processQuery(query)

            # Compute the BM25 score for each document for the current query
            doc_scores = self.compute_doc_scores(query_terms, inverted_indexes,
                                                 doc_lengths, doc_lengths_bm25f,
                                                 inverted_indexes_bm25f)

            # Set of relevant documents
            top_k = 10
            rel_docs = dict()
            for rank in dict(list(doc_scores.items())[:top_k]):
                rel_docs[rank] = doc_scores[rank]

            expansion = rocchio(query_terms, rel_docs, inverted_indexes, documents)

            expanded_query = list(expansion.keys())

            # Compute the BM25 score for each document for the expanded query
            doc_scores_2 = self.compute_doc_scores(expanded_query, inverted_indexes,
                                                   doc_lengths)
            top_n = dict(sorted(doc_scores.items(), key=itemgetter(1), reverse=True)[:10])
            top_n_2 = dict(sorted(doc_scores_2.items(), key=itemgetter(1), reverse=True)[:10])
            for t in top_n:
                print("{}: {}, {}, doc len: {}".format(t, doc_scores[t], doc_scores_2[t], doc_lengths[t]))

            print("----------------------")
            for t in top_n_2:
                print("{}: {}, {}, doc len: {}".format(t, doc_scores[t], doc_scores_2[t], doc_lengths[t]))

            print(query_terms)
            print("***********************")
            print(expanded_query)
            # Write the top 1000 document scores for this query to a .txt file
            self.write_output_file(query_nr, doc_scores, output_file_path)
            self.write_output_file(query_nr, doc_scores_2, output_file_path_2)

            # Increment the query number for the next iteration
            query_nr += 1
            if query_nr > 1:
                break

    def rank_documents_rocchio(self, inverted_indexes, 
                            doc_lengths, documents, path_topics,
                            path_results_dir=r"../trec_eval-master/our_data/",
                            results_file_name="results"):
            """
            Scores and ranks each document for each query, then expand the query and rank it again.
            
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
            output_file_path_2 = path_results_dir + results_file_name + "_2.txt"
            
            # Clear the contents of the output file
            open(output_file_path, "w").close()
            open(output_file_path_2, "w").close()
            
            query_nr = 1 # Used to keep track of which query is being processed
            for query in queries: # For each query ...
                print(f"Processing query {query_nr}: '{query}'")
                
                # Transform the query terms to the desired form (i.e. tokenized, stemmed, ...)
                query_terms = processQuery(query)
                
                # Compute the BM25 score for each document for the current query
                doc_scores = self.compute_doc_scores(query_terms, inverted_indexes,
                                                    doc_lengths)

                # Set of relevant documents
                top_k = 20
                rel_docs = dict()
                for rank in dict(list(doc_scores.items())[:top_k]):
                    rel_docs[rank] = doc_scores[rank]

                expansion = rocchio(query_terms, rel_docs, inverted_indexes, documents)

                expanded_query = list(expansion.keys())

                # Compute the BM25 score for each document for the expanded query
                doc_scores_2 = self.compute_doc_scores(expanded_query, inverted_indexes,
                                                    doc_lengths)
                '''
                top_n = dict(sorted(doc_scores.items(), key = itemgetter(1), reverse = True)[:10])
                top_n_2 = dict(sorted(doc_scores_2.items(), key = itemgetter(1), reverse = True)[:10])
                for t in top_n:
                    print("{}: {}, {}, doc len: {}".format(t, doc_scores[t], doc_scores_2[t], doc_lengths[t]))
                
                print("----------------------")
                for t in top_n_2:
                    print("{}: {}, {}".format(t, doc_scores[t], doc_scores_2[t]))

                print(query_terms)
                print("***********************")
                print(expanded_query)
                '''
                # Write the top 1000 document scores for this query to a .txt file
                self.write_output_file(query_nr, doc_scores, output_file_path)
                self.write_output_file(query_nr, doc_scores_2, output_file_path_2)
                
                # Increment the query number for the next iteration
                query_nr += 1
                if query_nr > 50:
                    break