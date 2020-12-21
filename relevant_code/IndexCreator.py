from Util import Index
from Util import term_dict_BM25F

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
    
    def create_BM25_inverted_indexes(self, documents):
        """
        Given a list of documents returns field specific inverted indexes, and
        information on the number of terms per field (and in total) for a
        document. The field-specific information is required for the BM25F
        algorithm.
        """
        
        print(f"There are {len(documents)} documents to be processed.")
        
        i = 0
        index = Index()
        inverted_indexes = dict()
        doc_length_info = dict()
        for doc in documents:
            
            # Retrieve all information required regarding the current document
            (td_bm25f, n_terms_author, n_terms_sections, n_terms_title,
             n_terms_abstract, n_terms_total) = self.process_BM25F_document(doc, index)
            
            # Use the retrieved document information to add inverted indexes
            inverted_indexes = index.write_to_Index_BM25F(td_bm25f, inverted_indexes)
            
            # Store the document's number of terms per field and in total
            doc_length_info[doc.cord_uid] = {'author':n_terms_author, 
                           'sections':n_terms_sections, 'title':n_terms_title,
                           'abstract':n_terms_abstract, 'total':n_terms_total}
            
            i += 1
            if i % 1000 == 0:
                print(f"Processed {i} documents ...")
        print(f"Done: processed {i} documents, created inverted indexes for"
              + f" {len(inverted_indexes)} terms.")
        
        return inverted_indexes, doc_length_info    
    
    def process_BM25F_document(self, doc, index):
        """
        Given a document, returns the term frequencies per field and the
        number of terms per field.
        """
        
        # Retrieve the document's cord_uid
        cord_uid = doc.cord_uid
        
        # Retrieve information for each document field in string form
        author_string = "" if doc.authors == None else " ".join(filter(None, doc.authors))
        sections_string = "" if doc.sections == None else " ".join(filter(None, doc.sections))
        title_string = "" if doc.title == None else doc.title
        abstract_string = "" if doc.abstract == None else doc.abstract
    
        def process_field(raw_text, index):
            """Turn the given text into a stemmed bag-of-words without stop-words."""
            bow = index.bagOfWords(raw_text)
            clean_unstemmed_bow = index.removeStopwords(bow)
            clean_stemmed_bow = index.stemming(clean_unstemmed_bow)
            return clean_stemmed_bow
        
        # Process (bag-of-words, stem, ...) the string associated with each field
        author_bow = process_field(author_string, index)
        sections_bow = process_field(sections_string, index)
        title_bow = process_field(title_string, index)
        abstract_bow = process_field(abstract_string, index)
        
        # Retrieve the number of terms contained in each field and in total
        n_terms_author = len(author_bow)
        n_terms_sections = len(sections_bow)
        n_terms_title = len(title_bow)
        n_terms_abstract = len(abstract_bow)
        n_terms_total = n_terms_author + n_terms_sections + n_terms_title + n_terms_abstract
        
        def get_term_dict_BM25F(author_bow, sections_bow, title_bow, abstract_bow):
            """Return a dictionary of term frequencies for each document field."""
            
            td_bm25f = term_dict_BM25F()
            for word in author_bow:
                td_bm25f.process_term(word, cord_uid, "author")
            for word in sections_bow:
                td_bm25f.process_term(word, cord_uid, "sections")
            for word in title_bow:
                td_bm25f.process_term(word, cord_uid, "title")
            for word in abstract_bow:
                td_bm25f.process_term(word, cord_uid, "abstract")
            return td_bm25f
        
        # Create a dictionary of term frequencies for each document field.
        td = get_term_dict_BM25F(author_bow, sections_bow, title_bow, abstract_bow)
        
        # Return the term frequencies per field, and the number of terms per field
        return (td, n_terms_author, n_terms_sections, n_terms_title,
                n_terms_abstract, n_terms_total)


        
        
        
        