from Util import Constants
from Util import load_pickle
from Util import save_pickle
from Util import Index
from Util import ParametersBM25
from Util import ParametersBM25F
from DocumentGatherer import DocumentGatherer
from DocumentProcessor import DocumentProcessor
from IndexCreator import IndexCreator
from DocumentRanker import DocumentRanker

class SearchSystem():
    
    """Contains all components of our search system."""
    
    def __init__(self):
        
        # Initialize each component of the search system
        self.document_gatherer = DocumentGatherer()
        self.document_processor = DocumentProcessor()
        self.index_creator = IndexCreator()
        self.document_ranker = DocumentRanker()
        
    def gather_documents(self):
        """Perform every gathering function of the document gatherer and save the results."""
        self.document_gatherer.gather_and_save_everything(Constants.path_cord, 
                                                   Constants.path_metadata, 
                                                   Constants.path_linked_documents,
                                                   Constants.path_unlinked_documents,
                                                   Constants.path_parsed_documents,
                                                   Constants.path_all_documents)
        
        print("Done gathering documents.")
    
    def process_documents(self):
        """Deprecated!"""
        self.document_processor.process_documents(Constants.path_linked_documents, 
                                                  Constants.path_unlinked_documents,
                                                  Constants.path_parsed_documents,
                                                  Constants.path_final_documents)
        
        print("Done processing documents.")
    
    def create_inverted_indexes(self):
        """
        For the complete documents: create inverted indexes and determine the
        length of each document.
        """
        
        # Load the documents
        documents = load_pickle(Constants.path_documents)
        
        # Create the inverted indexes
        inverted_indexes, document_lengths = self.index_creator.create_inverted_indexes(documents)
        
        # Store the inverted indexes and the document lengths
        save_pickle(inverted_indexes, Constants.path_inverted_indexes)
        save_pickle(document_lengths, Constants.path_document_lengths)
        del inverted_indexes, document_lengths
        
        print("Done creating inverted indexes for the complete documents.")
    
    def create_inverted_indexes_bm25f(self):
        
        # Load the documents
        documents = load_pickle(Constants.path_documents)
        
        # Create the inverted indexes, also retrieve information on number of terms per field
        inverted_indexes, doc_length_info = self.index_creator.create_BM25_inverted_indexes(documents)
        
        # Save the retrieved information
        save_pickle(inverted_indexes, 'inverted_indexes_bm25f')
        save_pickle(doc_length_info, 'doc_length_info_bm25f')
        del inverted_indexes, doc_length_info
        
        print("Done creating inverted indexes for the bm25f algorithm.")
        
    
    def rank_documents(self):
        """Score and rank each document for each query."""
        
        # Load the inverted indexes and the document lengths
        inverted_indexes = load_pickle(Constants.path_inverted_indexes)
        document_lengths = load_pickle(Constants.path_document_lengths)
        
        parameters = ParametersBM25()
        
        # Rank the documents
        self.document_ranker.rank_documents(inverted_indexes,
                                            document_lengths,
                                            parameters,
                                            Constants.path_topics,
                                            Constants.path_results_dir,
                                            Constants.results_file_name)
        del inverted_indexes, document_lengths
        
        print("Done ranking documents.")
        
    
    def rank_documents_BM25F(self):
        """Score and rank each document for each query."""
        
        # Load the inverted indexes and the document lengths
        inverted_indexes_bm25f = load_pickle(Constants.path_inverted_indexes_bm25f)
        doc_length_info_bm25f = load_pickle(Constants.path_doc_length_info_bm25f)
        
        parameters = ParametersBM25F()
        
        # Rank the documents
        self.document_ranker.rank_documents_bm25f(inverted_indexes_bm25f,
                                                  doc_length_info_bm25f,
                                                  parameters,
                                                  Constants.path_topics,
                                                  Constants.path_results_dir,
                                                  "results_BM25F")
        del inverted_indexes_bm25f, doc_length_info_bm25f
        
        print("Done ranking documents.")
    
    def rank_documents_with_reranker(self):
        """Score and rank each document for each query, then rerank them."""
        
        # Load the required data
        inverted_indexes = load_pickle(Constants.path_inverted_indexes)
        doc_lengths = load_pickle(Constants.path_document_lengths)
        documents_dictionary = load_pickle(Constants.path_documents_dictionary)
        
        parameters = ParametersBM25()
        
        self.document_ranker.rank_with_reranker(inverted_indexes, doc_lengths,
                                                documents_dictionary,
                                                parameters,
                                                Constants.path_topics,
                                                Constants.path_results_dir,
                                                Constants.results_rerank_file_name)
        del inverted_indexes, doc_lengths, documents_dictionary
    
    def rank_documents_BM25F_with_reranker(self):
        """Score and rank each document for each query with BM25F, then rerank them."""
        
        # Load the required data
        inverted_indexes_bm25f = load_pickle(Constants.path_inverted_indexes_bm25f)
        doc_length_info_bm25f = load_pickle(Constants.path_doc_length_info_bm25f)
        documents_dictionary = load_pickle(Constants.path_documents_dictionary)
        
        parameters = ParametersBM25F()
        
        self.document_ranker.rank_BM25F_with_reranker(inverted_indexes_bm25f,
                                                                doc_length_info_bm25f,
                                                                documents_dictionary, 
                                                                parameters,
                                                                Constants.path_topics, 
                                                                Constants.path_results_dir,
                                                                results_file_name="results_BM25F_rerank")
        del inverted_indexes_bm25f, doc_length_info_bm25f, documents_dictionary
    
    def rank_documents_rocchio(self):
        """Score and rank each document for each query."""
        
        # Load the inverted indexes and the document lengths
        inverted_indexes = load_pickle(Constants.path_inverted_indexes)
        document_lengths = load_pickle(Constants.path_document_lengths)

        documents = load_pickle(Constants.path_final_documents)
        document_lengths_bm25f = load_pickle(Constants.path_document_length_info_bm25f)
        inverted_indexes_bm25f = load_pickle(Constants.path_inverted_indexes_bm25f)

        # Rank the documents
        # self.document_ranker.rank_documents_rocchio(inverted_indexes,
        #                                                        document_lengths,
        #                                                        documents,
        #                                                        Constants.path_topics,
        #                                                        Constants.path_results_dir,
        #                                                        Constants.results_file_name)

        self.document_ranker.rank_documents_rocchio_with_bm25f(inverted_indexes,
                                            document_lengths,
                                            document_lengths_bm25f,
                                            inverted_indexes_bm25f,
                                            documents,
                                            Constants.path_topics,
                                            Constants.path_results_dir,
                                            Constants.results_file_name)
        print("Done ranking documents.")
        del inverted_indexes, document_lengths, documents