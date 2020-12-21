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
    
    # Rank the stored documents then rerank them
    #search_system.rank_documents_with_reranker()

    #search_system.rank_documents_rocchio()


    #Util.print_bm25_field_length_info('doc_length_info_bm25f.pkl') # average total doesnt match up with 'complete_document_lengths' ??????????????
