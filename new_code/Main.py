from SearchSystem import SearchSystem
from Util import Document # A necessary import

if __name__ == "__main__":
    search_system = SearchSystem()
    
    # Gather and store documents
    #search_system.gather_documents()
    
    # Process the stored documents
    #search_system.process_documents()
    
    # Create inverted indexes
    #search_system.create_inverted_indexes()
    
    # Rank the stored documents
    search_system.rank_documents()