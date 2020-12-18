from difflib import SequenceMatcher
import math

from Util import Document
from Util import save_pickle
from Util import load_pickle

class DocumentProcessor():
    
    """ 
    Once the different types of documents are gathered, this class may be
    used to put them together into the final list of documents that will be
    used to created the inverted indexes.
    """
    
    def find_near_matches(self, unlinked_documents, parsed_documents):
        """
        Finds titles that nearly match.
        
        In order to used the unlinked documents, we need to link them to
        parsed documents. There are a decent number of instances where
        the titles between the two nearly match, but something caused a
        tiny difference to occur between the two (e.g. a '-' to become the
        slightly different '—'). This function detects these instances and
        returns a list of tuples which each contain two nearly matching titles.
        """
    
        def prune_list(item, l, near_matches):
            length = len(l)
            if length < 100:
                find_match(item, l, near_matches)
                return 
            
            middle = math.ceil(length/2)
            if item < l[middle]:
                prune_list(item, l[:middle], near_matches)
            else:
                prune_list(item, l[middle:], near_matches)
        
        def find_match(item, l, near_matches):
            for title in l:
                if item == title:
                    return
                elif SequenceMatcher(a=item, b=title).ratio() > 0.95:
                    near_matches.append((item, title))
                    return
        
        unlinked_doc_titles = list(unlinked_documents.keys())
        parsed_doc_titles = list(parsed_documents.keys())
        parsed_doc_titles.sort()
        
        i = 0
        near_matches = []
        for title in unlinked_doc_titles:
            prune_list(title, parsed_doc_titles, near_matches)
            i += 1
            if i % 1000 == 0:
                print(f"Processed {i} titles {len(near_matches)} near matches ...")
        
        return near_matches
    
    def merge_documents(self, unlinked_documents, parsed_documents, near_matches):
        """Merge two incomplete documents into a single complete one."""
        
        def merge(unlinked_doc, parsed_doc):
            """Merge two documents."""
            
            # Retrieve the cord_uid from the unlinked document
            cord_uid = unlinked_doc.cord_uid
            
            # Prefer the unlinked document's abstract
            abstract = unlinked_doc.abstract if unlinked_doc.abstract != "" else parsed_doc.abstract
            
            # Prefer author information from the unlinked document
            authors = unlinked_doc.authors if unlinked_doc.authors != "" else parsed_doc.authors
            
            # Retrieve the sections of body text
            sections = parsed_doc.sections
            
            merged_document = Document(cord_uid, title, abstract, authors, sections)
            return merged_document
        
        merged_documents = []
        for title in unlinked_documents.keys():
            
            # Find a document parse with the same title as the document from the metadata
            if title in parsed_documents.keys():
                parsed_doc = parsed_documents[title]
            else:
                continue
                
            # Load the unlinked documents
            unlinked_doc = unlinked_documents[title]
            
            # Merge the two documents and save it
            merged_document = merge(unlinked_doc, parsed_doc)
            merged_documents.append(merged_document)
        print(f"Merged {len(merged_documents)} documents with completely matching titles.")
        
        # Merge the documents which have a nearly matching title
        for unlinked_doc_title, parsed_doc_title in near_matches:
            
            # Load the parsed document
            parsed_doc = parsed_documents[parsed_doc_title]
            
            # Load the unlinked documents
            unlinked_doc = unlinked_documents[unlinked_doc_title]
            
            # Merge the two documents and save it
            merged_document = merge(unlinked_doc, parsed_doc)
            merged_documents.append(merged_document)
            
        print(f"Merged {len(merged_documents)} documents in total.")
        return merged_documents
    
    def process_documents(self, path_linked_documents, path_unlinked_documents,
                          path_parsed_documents, path_final_documents):
        """Process the documents into their final form and store them."""
        
        # Load all document info
        linked_documents = load_pickle(path_linked_documents)
        unlinked_documents = load_pickle(path_unlinked_documents)
        parsed_documents = load_pickle(path_parsed_documents)
        
        # Merge the appropriate documents
        near_matches = self.find_near_matches(unlinked_documents, parsed_documents)
        merged_documents = self.merge_documents(unlinked_documents, parsed_documents, near_matches)
        
        # Create a final list of documents and store it
        final_documents = linked_documents + merged_documents
        save_pickle(final_documents, path_final_documents)