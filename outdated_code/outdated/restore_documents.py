import os
import sys
import json
import re
import csv
import pickle
from data_gatherer import Document
from difflib import SequenceMatcher

def clean_title(title):
    title = re.sub("\n", "", title)
    title = ' '.join(title.split())
    #title = re.sub("[^A-Za-z0-9]", "", title)
    title = title.lower()
    return title
    

def process_document_parses(parse_type):
    """Process the (json) document parses: parse type should be either 'pmc' or 'pdf'"""
    
    path = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/document_parses/{}_json/".format(parse_type)
    parse_dir = os.fsencode(path)
    documents_info = dict()
    i = 0
    for file in os.listdir(parse_dir):
        filename = os.fsdecode(file)
        with open(path+filename, encoding="utf-8") as f:
            json_obj = json.load(f)
        
        # Retrieve a list of dictionaries which together contain the body text
        body_text = json_obj.get("body_text")
        
        # Retrieve and clean the title
        title = json_obj['metadata']['title']
        title = clean_title(title)
        
        # Do not process the document if the title or the text is empty
        if title == None or title == "" or len(body_text) == 0:
            continue
        
        # Retrieve and process the abstract(s) into a single string
        abstract_string = ""
        if parse_type == 'pdf': # Only pdf parses have an abstract attached
            abstracts = json_obj['abstract']
            for abstract in abstracts:
                abstract_string += abstract['text'] + " "      
        
        # Retrieve author information as a list of the last names of the authors
        authors = json_obj['metadata']['authors']
        last_names = [author['last'] for author in authors if not author['last'] == '']
        
        # Store the text in a list of different text segments
        text_sections = []
        for item in body_text:
            # section_name = dictionary.get("section") # Not all files have section names # MAY BE MISTAKEN IN THIS, OR MAY BE A SMALLER FRACTION THAN I THOUGH ***
            text = item.get("text")
            text_sections.append(text)
        
        # Store the retrieved document information
        documents_info[title] = (abstract_string, last_names, text_sections)
        i += 1
        if i % 1000 == 0:
            print(f"Processed {i} {parse_type} document parses ...")
        
    return documents_info

def get_linkless_docs(path_metadata):
    """Store info on document metadata that do not include the name of the fully parsed document"""
    
    def is_empty(string):
        return string == None or re.sub("\\s+", "", string) == ""
    
    doc_data = dict()
    with open(path_metadata, encoding='utf-8') as f:
        
        reader = csv.DictReader(f)
        i = 0
        for row in reader:
            
            # If the document does not include a reference to the file name of the parsed document
            if is_empty(row['pdf_json_files']) and is_empty(row['pmc_json_files']):
                
                # Retrieve and clean the title
                title = clean_title(row['title'])
                
                # Do not process the document if there is no title
                if title == None or title == "":
                    continue
                
                # Retrieve the remaining relevant fields
                cord_uid = row['cord_uid']
                abstract = row['abstract']
                authors = row['authors']
                
                # Save the relevant document info
                doc_data[title] = (cord_uid, abstract, authors)
                
            i += 1
            if i % 1000 == 0:
                print(f"Iterated over {i} metadata rows ...")
            
    return doc_data

def restore_document_info(linkless_documents, pmc_documents, pdf_documents):
    """Combine information to restore documents that are otherwise incomplete."""
    
    restored_documents = []
    for title in linkless_documents.keys():
        
        # Find a document parse with the same title as the document from the metadata
        if title in pmc_documents.keys():
            parsed_doc = pmc_documents[title]
        elif title in pdf_documents.keys():
            parsed_doc = pdf_documents[title]
        else:
            continue
            
        # Load the linkless documents
        linkless_doc = linkless_documents[title]
        
        # Retrieve the cord_uid from the linkless document
        cord_uid = linkless_doc[0]
        
        # Take the linkless doc's abstract (a pmc parse never has one)
        abstract = linkless_doc[1] if linkless_doc[1] != "" else parsed_doc[0]
        
        # Prefer author information from the linkless document
        authors = linkless_doc[2].split(";") if linkless_doc[2] != "" else parsed_doc[1]
        
        # Retrieve the sections of body text
        sections = parsed_doc[2]
        
        restored_document = Document(cord_uid, title, abstract, authors, sections)
        restored_documents.append(restored_document)
            
    return restored_documents

if __name__ == "__main__":
    path_pmc_documents = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/pickle_files/pmc_documents.pkl"
    path_pdf_documents = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/pickle_files/pdf_documents.pkl"
    path_metadata = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/metadata.csv"
    path_linkless_documents = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/pickle_files/linkless_documents.pkl"
    path_restored_documents = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/pickle_files/restored_documents.pkl"
    
# =============================================================================
#     # Process and gather all eligible pmc documents
#     pmc_documents = process_document_parses('pmc')
#     print(f"Done: {len(pmc_documents)} pmc documents processed and gathered.")
#     
#     # Store the pmc documents
#     with open(path_pmc_documents, 'wb') as f:
#         pickle.dump(pmc_documents, f)
# =============================================================================
    
# =============================================================================
#     # Process and gather all eligible pdc documents
#     pdf_documents = process_document_parses('pdf')
#     print(f"Done: {len(pdf_documents)} pdf documents processed and gathered.")
#     
#     # Store the pdf documents
#     with open(path_pdf_documents, 'wb') as f:
#         pickle.dump(pdf_documents, f)
# =============================================================================
    
    
# =============================================================================
#     # Gather info on document metadata that do not include the name of the fully parsed document
#     linkless_documents = get_linkless_docs(path_metadata)
#     print(f"Done: {len(linkless_documents)} linkless documents processed and gathered.")
#     
#     # Store the linkless documents
#     with open(path_linkless_documents, 'wb') as f:
#         pickle.dump(linkless_documents, f)
# =============================================================================
    
    
# =============================================================================
#     # Load the stored pmc documents
#     with open(path_pmc_documents, 'rb') as f:
#         pmc_documents = pickle.load(f)
#     print(f"Loaded {len(pmc_documents)} pmc documents.")
#     
#     # Load the stored pdf documents
#     with open(path_pdf_documents, 'rb') as f:
#         pdf_documents = pickle.load(f)
#     print(f"Loaded {len(pdf_documents)} pdf documents.")
#     
#     # Load the stored linkless documents
#     with open(path_linkless_documents, 'rb') as f:
#         linkless_documents = pickle.load(f)
#     print(f"Loaded {len(linkless_documents)} linkless documents.")
#     
#     
#     # Combine document information to restore otherwise incomplete documents
#     restored_documents = restore_document_info(linkless_documents, pmc_documents, pdf_documents)
#     print(f"Done: {len(restored_documents)} documents restored.")
#     
#     # Store the complete documents
#     with open(path_restored_documents, 'wb') as f:
#         pickle.dump(restored_documents, f)
# =============================================================================
    

    
    global complete_match_count, partial_match_count, no_match_count
    complete_match_count = partial_match_count = no_match_count = 0
    
    global partially_matched_titles
    partially_matched_titles = []
    
    def prune_list(item, l):
        length = len(l)
        if length < 100:
            find_match(item, l)
            return
        
        middle = math.ceil(length/2)
        if item < l[middle]:
            prune_list(item, l[:middle])
        else:
            prune_list(item, l[middle:])
    
    def find_match(item, l):
        for title in l:
            if item == title:
                #print(f"Complete match: {title}")
                global complete_match_count
                complete_match_count += 1
                return
            elif SequenceMatcher(a=item, b=title).ratio() > 0.95:
# =============================================================================
#                 print(f"\nMatch ratio: {SequenceMatcher(a=item, b=title).ratio()}")
#                 print(f"title_linkless={item}")
#                 print(f"   title_parse={title}\n")
# =============================================================================
                global partial_match_count
                partial_match_count += 1
                global partially_matched_titles
                partially_matched_titles.append((item, title))
                return
        global no_match_count
        no_match_count += 1
    
    import math
    
# =============================================================================
#     with open('linkless_title', 'rb') as f:
#         linkless_titles = pickle.load(f)
#     print(f"Loaded {len(linkless_titles)} linkless titles.")
#     
#     with open('pmc_titles', 'rb') as f:
#         pmc_titles = pickle.load(f)
#     print(f"Loaded {len(pmc_titles)} pmc titles.")
#     
#     with open('pdf_titles', 'rb') as f:
#         pdf_titles = pickle.load(f)
#     print(f"Loaded {len(pdf_titles)} pdf titles.")
#     
#     i = 0
#     for item in linkless_titles:
#         prune_list(item, pmc_titles)
#         i += 1
#         if i % 100 == 0:
#             print(f"Processed {i} pmc titles with {complete_match_count} complete matches and {partial_match_count} partial matches ...")
#     
#     with open('partially_matched_pmc_titles.pkl', 'wb') as f:
#         pickle.dump(partially_matched_titles, f)
# =============================================================================
    
# =============================================================================
#     i = 0
#     for item in linkless_titles:
#         prune_list(item, pdf_titles)
#         i += 1
#         if i % 100 == 0:
#             print(f"Processed {i} pdf titles with {complete_match_count} complete matches and {partial_match_count} partial matches ...")
#     
#     with open('partially_matched_pdf_titles.pkl', 'wb') as f:
#         pickle.dump(partially_matched_titles, f)
# =============================================================================
    

    with open('partially_matched_pmc_titles.pkl', 'rb') as f:
        partially_matched_pmc_titles = pickle.load(f)
    print(f"Loaded {len(partially_matched_pmc_titles)} partially matched pmc titles.")
    
    with open('partially_matched_pdf_titles.pkl', 'rb') as f:
        partially_matched_pdf_titles = pickle.load(f)
    print(f"Loaded {len(partially_matched_pdf_titles)} partially matched pdf titles.")
    
    # Load the stored pmc documents
    with open(path_pmc_documents, 'rb') as f:
        pmc_documents = pickle.load(f)
    print(f"Loaded {len(pmc_documents)} pmc documents.")
    
    # Load the stored pdf documents
    with open(path_pdf_documents, 'rb') as f:
        pdf_documents = pickle.load(f)
    print(f"Loaded {len(pdf_documents)} pdf documents.")
    
    # Load the stored linkless documents
    with open(path_linkless_documents, 'rb') as f:
        linkless_documents = pickle.load(f)
    print(f"Loaded {len(linkless_documents)} linkless documents.")
    
    partially_matched_linkless_documents = dict()
    for (linkless_title, pdf_title) in partially_matched_pdf_titles:
        partially_matched_linkless_documents[pdf_title] = linkless_documents[linkless_title]
    for (linkless_title, pmc_title) in partially_matched_pmc_titles:
        partially_matched_linkless_documents[pmc_title] = linkless_documents[linkless_title]
    
    # Combine document information to restore otherwise incomplete documents
    partially_matched_restored_documents = restore_document_info(partially_matched_linkless_documents, pmc_documents, pdf_documents)
    print(f"Done: {len(partially_matched_restored_documents)} partially matched restored documents restored.")
    
    path_partially_matched_restored_documents = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/pickle_files/partially_matched_restored_documents.pkl"
    # Store the complete documents
    with open(path_partially_matched_restored_documents, 'wb') as f:
        pickle.dump(partially_matched_restored_documents, f)
