from Util import Index

class IndexCreator():
    
    """
    Used to create inverted indexes for documents and to determine
    document lengths.
    """
    
    def create_inverted_indexes(self, documents):
        """Given a list of documents returns inverted indexes and document lengths."""
        
        print(f"There are {len(documents)} documents to be processed.")
        
        i = 0
        index = Index()
        inverted_indexes = dict()
        doc_lengths = dict()
        for doc in documents:
            
            # Retrieve the document fields
            author_string = "" if doc.authors == None else " ".join(filter(None, doc.authors))
            sections_string = "" if doc.sections == None else " ".join(filter(None, doc.sections))
            title_string = "" if doc.title == None else doc.title
            abstract_string = "" if doc.abstract == None else doc.abstract
            doc_string = f"{author_string} {sections_string} {title_string} {abstract_string}"
            
            # Process the document and write term frequencies to the appropriate file
            doc_length = index.processDocument(doc_string, doc.cord_uid, inverted_indexes)
            
             # Store the document length
            doc_lengths[doc.cord_uid] = doc_length
            
            i += 1
            if i % 1000 == 0:
                print(f"Processed {i} documents ...")
        print(f"Done: processed {i} documents, created {len(inverted_indexes)} inverted indexes")
        
        return inverted_indexes, doc_lengths
    
    def add_inverted_indexes(self, inverted_indexes, document_lengths, documents):
        """Create new inverted indexes to add to existing ones."""
        
        print(f"There are already {len(inverted_indexes)} inverted indexes.")
        print(f"There are {len(documents)} documents to be processed.")
        
        i = 0
        index = Index()
        for doc in documents:
        
            # Retrieve the document fields
            author_string = "" if doc.authors == None else " ".join(filter(None, doc.authors))
            sections_string = "" if doc.sections == None else " ".join(filter(None, doc.sections))
            title_string = "" if doc.title == None else doc.title
            abstract_string = "" if doc.abstract == None else doc.abstract
            doc_string = f"{author_string} {sections_string} {title_string} {abstract_string}"
            
            # Process the document and write term frequencies to the appropriate file
            doc_length = index.processDocument(doc_string, doc.cord_uid, inverted_indexes)
            
             # Store the document length
            document_lengths[doc.cord_uid] = doc_length
            
            i += 1
            if i % 1000 == 0:
                print(f"Processed {i} documents ...")
        print(f"Done: processed {i} additional documents, there are now {len(inverted_indexes)} inverted indexes")
        
        return inverted_indexes, document_lengths