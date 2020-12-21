from SearchSystem import SearchSystem
import Util
from Util import Document # A necessary import
from Util import Constants
from Util import load_pickle
from Util import save_pickle
from ParameterTests import ParameterTests

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
    
    # Rank the stored documents with BM25F
    #search_system.rank_documents_BM25F()
    
    # Rank the stored documents then rerank them
    #search_system.rank_documents_with_reranker()
    
    # Rank the stored documents with BM25F then rerank them
    search_system.rank_documents_BM25F_with_reranker()

    #search_system.rank_documents_rocchio()