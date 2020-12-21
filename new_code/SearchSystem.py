from Util import Constants
from Util import load_pickle
from Util import save_pickle
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
        
        print("Done creating inverted indexes for the complete documents.")
    
    def rank_documents(self):
        """Score and rank each document for each query."""
        
        # Load the inverted indexes and the document lengths
        inverted_indexes = load_pickle(Constants.path_inverted_indexes)
        document_lengths = load_pickle(Constants.path_document_lengths)
        document_lengths_bm25f = load_pickle(Constants.path_document_length_info_bm25f)
        inverted_indexes_bm25f = load_pickle(Constants.path_inverted_indexes_bm25f)
        
        # Rank the documents
        self.document_ranker.rank_documents(inverted_indexes,
                                            document_lengths,
                                            document_lengths_bm25f,
                                            inverted_indexes_bm25f,
                                            Constants.path_topics,
                                            Constants.path_results_dir,
                                            Constants.results_file_name)
        del inverted_indexes, document_lengths
        
        print("Done ranking documents.")
    
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