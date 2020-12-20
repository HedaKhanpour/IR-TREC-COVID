from SearchSystem import SearchSystem
import Util
from Util import Document # A necessary import
from Util import Constants
from Util import load_pickle
from Util import save_pickle

if __name__ == "__main__":
    search_system = SearchSystem()
    
    # Gather and store documents
    #search_system.gather_documents()
    
    # Process the stored documents
    #search_system.process_documents()
    
    # Create inverted indexes
    #search_system.create_inverted_indexes()
    
    # Rank the stored documents
    #search_system.rank_documents()

# Still working on the stuff below (reranker)
# =============================================================================
#     inverted_indexes = load_pickle(Constants.path_inverted_indexes)
#     doc_lengths = load_pickle(Constants.path_document_lengths)
#     documents_dictionary = load_pickle(Constants.path_documents_dictionary)
#     
# # =============================================================================
# #     search_system.document_ranker.rank_with_rerank(inverted_indexes,
# #                         doc_lengths, Constants.path_topics, documents_dict,
# #                         path_results_dir=r"../trec_eval-master/our_data/",
# #                         results_file_name="results_rerank")
# # =============================================================================
#     search_system.document_ranker.rank_with_rerank_light(inverted_indexes,
#                         doc_lengths, Constants.path_topics, documents_dictionary,
#                         path_results_dir=r"../trec_eval-master/our_data/",
#                         results_file_name="results_rerank_light")
# =============================================================================
    