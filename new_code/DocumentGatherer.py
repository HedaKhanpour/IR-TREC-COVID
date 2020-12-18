import os
import json
import csv

from Util import Document
from Util import is_empty
from Util import clean_title
from Util import save_pickle

class DocumentGatherer():
    
    """
    This class is used to parse the pmc or pdf document parses that are stored
    as .json files in the cord folder (2020-07-16/document_parses/). MORE INFO
    """
    
    def get_linked_documents(self, path_cord, path_metadata):
        """Retrieve all documents for which the relevant metadata is available."""
        
        with open(path_metadata, encoding='utf-8') as f:
            
            i = 0
            documents = []
            reader = csv.DictReader(f)
            for row in reader:
                if i > 0 and i % 1000 == 0:
                    print(f"Encountered {i} documents, {len(documents)}"
                          + " linked documents were gathered ...")
                i += 1
                
                # Retrieve the file paths of the document's parses if directly available
                if row['pmc_json_files']:
                    file_paths = [path_cord+path for path in row['pmc_json_files'].split("; ")]
                elif row['pdf_json_files']:
                    file_paths = [path_cord+path for path in row['pdf_json_files'].split("; ")]
                else: # Otherwise stop processing the 'unlinked' document
                    continue
                
                # Retrieve the full text as a list of text sections
                text_sections = []
                for path in file_paths: # For each file path ...
                    
                    # Load the file and convert it to a json object
                    with open(path, "r", encoding="utf-8") as f:
                        json_obj = json.load(f)
                    
                    # Check whether the json object is properly instantiated
                    if json_obj == None:
                        return None
                    
                    # Retrieve a list of dictionaries which together contain the body text
                    body_text = json_obj.get("body_text")
                    
                    # Check whether the body text is properly instantiated
                    if body_text == None:
                        return None
                    
                    # Seperate each section of the body text
                    for item in body_text:
                        text = item.get("text")
                        text_sections.append(text)
                
                # Retrieve the remaining relevant document information
                cord_uid = row['cord_uid']
                title = row['title'].strip("\"")
                abstract = row['abstract'].strip("\"")
                if is_empty(row['authors']):
                    authors = None
                else:
                    authors = row['authors'].split(";")
                
                # Save the relevant document metadata
                document = Document(cord_uid, title, abstract, authors, text_sections)
                documents.append(document)
        
            return documents
        
    def get_unlinked_documents(self, path_metadata):
        """
        Retrieves info on documents for which essential information is missing.
        
        The metadata.csv file contains information with which we coordinate
        the processing of documents. However more than half the metadata rows
        lack file names of both the pmc and pdf parses of the corresponding
        document. This function retrieves information regarding these
        files, storing the cord_uid, the abstract, and author information as a
        Document object in a dictionary, where a simplified version of
        the document title is the key. Since the metadata do not contain 
        body text, this field of the Document object is None (we will later
        attempt to find the corresponding body text in the document parses).
        """
        
        documents_metadata = dict()
        with open(path_metadata, encoding='utf-8') as f:
            
            i = 0
            reader = csv.DictReader(f)
            for row in reader:
                if i > 0 and i % 1000 == 0:
                    print(f"Encountered {i} documents, {len(documents_metadata)}"
                          + " unlinked documents were gathered ...")
                i += 1
                
                # If the document does not include a reference to the file name of the parsed document
                if is_empty(row['pdf_json_files']) and is_empty(row['pmc_json_files']):
                    
                    # Retrieve and clean the title
                    title = row['title'].strip("\"")
                    cleaned_title = clean_title(title)
                    
                    # Do not process the document if there is no title
                    if title == None or title == "":
                        continue
                    
                    # Retrieve the remaining relevant fields
                    cord_uid = row['cord_uid']
                    abstract = row['abstract'].strip("\"")
                    if is_empty(row['authors']):
                        authors = None
                    else:
                        authors = row['authors'].split(";")
                    
                    # Save the relevant document metadata
                    document = Document(cord_uid, title, abstract, authors, None)
                    documents_metadata[cleaned_title] = document
        return documents_metadata
                
    def get_document_parses(self, path_cord):
        """
        Retrieves relevant information from pmc and pdf document parses.
        
        This function can be used to parse the pmc and pdf document parses that are
        stored as .json files in the cord folder (2020-07-16/document_parses/).
        
        For each parsed document it stores the abstract, the authors' last names, 
        and the body text as a Document object in a dictionary, where a 
        simplified version of the document title is the key. Since the document
        parses do not contain a cord_uid, this field of the Document object is
        None (we will later attempt to find the corresponding cord_uid in
        the metadata.csv file).
        
        Keyword arguments:
        parse_type -- should be valued either 'pmc' or 'pdf'
        """
        
        def get_parses(documents, parse_type, i, path_cord):
        
            # Retrieve the folder containing the document parses
            path = r"{}/document_parses/{}_json/".format(path_cord, parse_type)
            parse_dir = os.fsencode(path)
            
            for file in os.listdir(parse_dir):
                i += 1
                if i > 0 and i % 1000 == 0:
                    print(f"Encountered {i} document parses, of which "
                          + f" {len(documents)} were gathered ...")
                
                # Load the current file
                filename = os.fsdecode(file) # Retrieve the current file's name
                with open(path+filename, encoding="utf-8") as f:
                    json_obj = json.load(f)
                
                # Retrieve a list of dictionaries which together contain the body text
                body_text = json_obj.get("body_text")
                
                # Retrieve and clean the title
                title = json_obj['metadata']['title'].strip("\"")
                cleaned_title = clean_title(title)
                
                # Do not process the document under certain conditions
                if (cleaned_title == None or cleaned_title == "" or 
                    cleaned_title in documents.keys() or len(body_text) == 0):
                    continue
                
                # Retrieve and process the abstract(s) into a single string
                abstract_string = ""
                if parse_type == 'pdf': # Only pdf parses have an abstract attached
                    abstracts = json_obj['abstract']
                    for abstract in abstracts:
                        abstract_string += abstract['text'].strip("\"") + " "      
                
                # Retrieve author information as a list of the last names of the authors
                authors = json_obj['metadata']['authors']
                last_names = [author['last'] for author in authors if not author['last'] == '']
                
                # Store the text in a list of different text segments
                text_sections = []
                for item in body_text:
                    text = item.get("text")
                    text_sections.append(text)
                
                # Store the retrieved document information
                document = Document(None, title, abstract_string, last_names, text_sections)
                documents[cleaned_title] = document
                
            return documents, i
            
        i = 0
        documents = dict()
        documents, i = get_parses(documents, 'pmc', i, path_cord)
        documents, i = get_parses(documents, 'pdf', i, path_cord)
            
        return documents
    
    def gather_and_save_all(self, path_cord, path_metadata, 
                            path_linked_documents, path_unlinked_documents, 
                            path_parsed_documents):
        """Gather and store all documents that this class can retrieve."""
                
        # Gather and save linked documents
        linked_documents = self.get_linked_documents(path_cord, path_metadata)
        save_pickle(linked_documents, path_linked_documents)
        
        # Gather and save unlinked documents
        unlinked_documents = self.get_unlinked_documents(path_metadata)
        save_pickle(unlinked_documents, path_unlinked_documents)
        
        # Gather and save relevant info from pmc and pdf document parses
        parsed_documents = self.get_document_parses(path_cord)
        save_pickle(parsed_documents, path_parsed_documents)