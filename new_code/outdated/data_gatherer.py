import sys
import re
import os.path
import json
import pickle
from index import Index

# ***
# I haven't made sure yet, but I have the feeling we've disregarded all 
# pdf_json files thus far. After looking some more, I am fairly certain we
# have.
#
# For pdf_json stuff it is sometimes the case that there are two files, I think
# in this case one is supplementary material or something.
# It is also possible for there to be both a pmc and a pdf file, in this case
# I am unsure if there is a difference, and if so what, this shall have to be
# investigated.
#
# It appears that if a pdf or pmc file name is included, then it always exists.
#
# Not all json files appear to have section names.
#
# The number of text things that are empty is miniscule, there appear to be no
# 'None' instances here.
#
# May want to consider including author names and such in bag of words, also
# may want to consider BM25F (with field weights).
#
# Since quite many files appear not to have a section name that can be
# retrieved, I do not include this at all. The only consequence that I've seen
# thus far is that the section names are not included in the bag of words
# representations. May need to consider this more carefully.
#
# Are all articles in English? Otherwise we will have to alter some things,
# for instance we will have to consider adding additional stopword lists, and
# perhaps select one based on language detection.
#
# BIG PROBLEM: ***
#   More than half the articles do not have their json file name listed in the
#   metadata. I think we will have to find a way another way to obtain them.
#   If there is no better solution we may try using the internet links to the 
#   articles, which often (or always) seem to be provided when the file name
#   is missing.
#   One thing that I find strange is that there appear to be ~192,509 lines in
#   the metadata file, there are 62,736+84,420 = 147,156 json files, but only
#   ~84,145 json file names listed in the metadata.
#
#   I've tested some things and there appear to be 12,180 documents in the
#   the relevance judgements that we cannot access in our current manner.
#   Example: 2xky1wse
#  
# I am going to base the document length on the clean, stemmed, bag of words
# representation of a document, I am not 100% sure whether this is how it
# should be.
#
# We must remember: "When including CORD-19 data in a publication or
# redistribution, please cite our arXiv preprint". 
# (https://www.semanticscholar.org/paper/CORD-19%3A-The-Covid-19-Open-Research-Dataset-Wang-Lo/4a10dffca6dcce9c570cb75aa4d76522c34a2fd4)
    
# =============================================================================
# cord_uid: 0
# sha: 1
# source_x: 2
# title: 3
# doi: 4
# pmcid: 5
# pubmed_id: 6
# license: 7
# abstract: 8
# publish_time: 9
# authors: 10
# journal: 11
# mag_id: 12
# who_covidence_id: 13
# arxiv_id: 14
# pdf_json_files: 15
# pmc_json_files: 16
# url: 17
# s2_id: 18
# =============================================================================


class Document():
    
    def __init__(self, cord_uid, title, abstract, authors, sections):
        self.cord_uid = cord_uid
        self.title = title
        self.abstract = abstract
        self.authors = None if authors == None else authors.copy()
        self.sections = None if sections == None else sections.copy()
    
    def __str__(self):
        string = "\n********** Document **********\n"
        string += "cord_uid:\n{}\n".format(self.cord_uid)
        string += "\ntitle:\n{}\n".format(self.title)
        
        string += "\nauthors:\n"
        for author in self.authors:
            string += "{}\t".format(author)
        string += "\n"
        
        string +=  "\nabstract:\n{}\n".format(self.abstract)
        
        string += "\nsections:\n"
        for section in self.sections:
            string += "{}\n".format(section.__str__())
        
        return string

class DocumentGatherer():
    
    def __init__(self, path_metadata, path_cord):
        self.path_metadata = path_metadata
        self.path_cord = path_cord
                
    def gather_documents(self):
        """Create a document for each eligible line in metadata.csv"""
        
        documents = []
        with open(path_metadata, "r", encoding="utf-8") as f:
            
            # Retrieve the headers (column names)
            self.headers = {}
            line = re.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", f.readline())
            for i in range(len(line)):
                header = re.sub("\n", "", line[i])
                self.headers[header] = i
            
            i = 0
            for line in f: # For each line in the metadata.csv file ...
                # Use the info to create a document object
                document = self.process_line(line)
                
                # Store the document if is not None
                if document != None:
                    documents.append(document)
                    
                    i += 1
                    if i > 0 and i % 10000 == 0:
                        print(f"{i} documents gathered ...")
        
        return documents
    
    def process_line(self, line):
        """Create a document with a line of information from metadata.csv"""
        
        cells = re.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", line)
        
        def is_empty(string):
            return string == None or re.sub("\\s+", "", string) == ""
        
        # Retrieve the relevant fields
        cord_uid = cells[self.headers.get("cord_uid")]
        title = cells[self.headers.get("title")].strip("\"")
        abstract = cells[self.headers.get("abstract")].strip("\"")
        temp_str = cells[self.headers.get("authors")].strip("\"")
        authors = None if is_empty(temp_str) else temp_str.split(";")
        pmc_json = cells[self.headers.get("pmc_json_files")]
        pdf_jsons = None
        
         # Make a list for the pmc file path (is always a single path)
        file_paths = [self.path_cord + pmc_json]
        
        if not os.path.isfile(file_paths[0]): # If the pmc file does not exist ...
            
            # Retrieve the pmc file paths (can be more than one path)
            pdf_jsons = cells[self.headers.get("pdf_json_files")].split("; ")
            
            # Make a list containing all pdf file paths
            file_paths = [self.path_cord + pdf_json for pdf_json in pdf_jsons]
            for path in file_paths: # For each pdf file path
                if not os.path.isfile(path): # If the pdf file does not exist ...                    
                    return None # The full text is unavailable, so return
                
        sections = []
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
                sections.append(text)
            
        # Return a number of the most important fields as a Document object
        document = Document(cord_uid, title, abstract, authors, sections)
        return document
        
def create_inverted_indexes(documents, path_inverted_indexes, path_doc_lengths):
    print(f"There are {len(documents)} documents to be processed.")
    
    inverted_indexes = dict()
    doc_lengths = dict()
    index = Index()
    i = 0
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
    
    # Store the great dictionary
    with open(path_inverted_indexes, 'wb') as f:
        pickle.dump(inverted_indexes, f)
    
    # Store the document length dictionary
    with open(path_doc_lengths, 'wb') as f:
        pickle.dump(doc_lengths, f)

def add_inverted_indexes(inverted_indexes, doc_lengths, documents,
                         path_inverted_indexes, path_doc_lengths):
    print(f"There are already {len(inverted_indexes)} inverted indexes.")
    print(f"There are {len(documents)} documents to be processed.")
    
    index = Index()
    i = 0
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
    print(f"Done: processed {i} additional documents, there are now {len(inverted_indexes)} inverted indexes")
    
    # Store the great dictionary
    with open(path_inverted_indexes, 'wb') as f:
        pickle.dump(inverted_indexes, f)
    
    # Store the document length dictionary
    with open(path_doc_lengths, 'wb') as f:
        pickle.dump(doc_lengths, f)
        
def compute_document_statistics(documents, doc_lengths, path_CRJ):
    """Compute and print several relevant stastics"""
    
    print("\n------------- Computing document statistics -------------")
    print(f"{len(doc_lengths)/len(documents) * 100}% of stored documents are unique.")
    
    print("\nThe following should be taken into account with the coming calculations:")
    print("    - Only terms that were not remove by the cleaning/stemming/... process were included.")
    print("    - If a term occurs multiple times in a file or across files, it is (of course) counted multiple times as well.")
    
    total_nr_of_terms = 0
    for key in doc_lengths.keys():
        total_nr_of_terms += doc_lengths[key]
    print(f"\nThere are {total_nr_of_terms} terms in total accross all documents.")
    print(f"The average document length is {total_nr_of_terms/len(doc_lengths)}")
    
    # Rest of the code is to test for the presence of relevant documents
    print("\n-------- Testing for the presence of relevant documents --------")
    processed_docs = set()
    for doc in documents:
        processed_docs.add(doc.cord_uid)
    
    crj_docs = set()
    # Load the stored documents
    with open(path_CRJ, 'r') as f:
        for line in f:
            crj = line.split(" ")
            cord_uid = crj[2]
            crj_docs.add(cord_uid)
    
    only_processed = processed_docs - crj_docs
    only_crj = crj_docs - processed_docs
    symmetric_difference = processed_docs.symmetric_difference(crj_docs)
    intersection = processed_docs.intersection(crj_docs)
    print(f"There are {len(processed_docs)} unique processed documents.")
    print(f"There are {len(crj_docs)} unique documents in the relevance judgements.")
    print(f"There are {len(only_processed)} documents that were processed, but are not present in the relevance judgements.")
    print(f"There are {len(only_crj)} documents that are present in the relevance judgements, but were not processed.")
    print(f"There are {len(symmetric_difference)} documents that were both processed and are present in the relevance judgements.")
    print(f"There are {len(intersection)} documents that were either processed or were present in the relevance judgements, but not both.")

        
if __name__ == "__main__":
    path_metadata = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/metadata.csv"
    path_cord = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/"
    path_documents = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/pickle_files/documents.pkl"
    path_doc_lengths = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/pickle_files/doc_lengths.pkl"
    path_CRJ = r"D:/Universiteit/Master (External Repositories)/IR-TREC-COVID/trec_eval-master/our_data/CRJ.txt"
    path_restored_documents = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/pickle_files/restored_documents.pkl"
    path_documents_complete = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/pickle_files/documents_complete.pkl"
    path_inverted_indexes = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/pickle_files/inverted_indexes.pkl"
    path_doc_lengths = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/pickle_files/doc_lengths.pkl"
    path_partially_matched_restored_documents = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/pickle_files/partially_matched_restored_documents.pkl"

# =============================================================================
#     # Gather all documents with retrievable text
#     document_gatherer = DocumentGatherer(path_metadata, path_cord)
#     documents = document_gatherer.gather_documents()
#     print(f"Done: {len(documents)} documents gathered.")
#     
#     # Store the documents
#     with open(path_documents, 'wb') as f:
#         pickle.dump(documents, f)
# =============================================================================
    
# =============================================================================
#     # Load the stored documents
#     with open(path_documents, 'rb') as f:
#         documents = pickle.load(f)
#     print(f"Loaded {len(documents)} documents")
#     
#     # Load the stored restored documents
#     with open(path_restored_documents, 'rb') as f:
#         restored_documents = pickle.load(f)
#     print(f"Loaded {len(restored_documents)} restored documents.")
#     
#     # Combine the normally processed documents with the restored documents
#     documents_complete = documents + restored_documents
#     with open(path_documents_complete, 'wb') as f:
#         pickle.dump(documents_complete, f)
#     print(f"Stored the complete collection of {len(documents_complete)} documents.")
# =============================================================================
    
    # Load the stored documents
    with open(path_documents, 'rb') as f:
        documents = pickle.load(f)
    print(f"Loaded {len(documents)} normally processed documents")
    
    # Load the complete collection of documents
    with open(path_documents_complete, 'rb') as f:
        documents_complete = pickle.load(f)
    print(f"Loaded the complete collection of {len(documents_complete)} documents")
    
    with open(path_doc_lengths, 'rb') as f:
        doc_lengths = pickle.load(f)
    print(f"Loaded {len(doc_lengths)} document lengths")
    
    # Load the stored partially matched restored documents
    with open(path_partially_matched_restored_documents, 'rb') as f:
        partially_matched_restored_documents = pickle.load(f)
    print(f"Loaded {len(partially_matched_restored_documents)} partially matched documents")
        
    
    print("\n\n\nStatistics for solely the normally processed documents:")
    compute_document_statistics(documents, doc_lengths, path_CRJ)
    
    print("\n\n\nStatistics for the complete collection of documents:")
    compute_document_statistics(documents_complete, doc_lengths, path_CRJ)
    
    print("\n\n\nStatistics including the partially matched stuff:")
    compute_document_statistics(documents_complete + partially_matched_restored_documents, doc_lengths, path_CRJ)
    
        
# =============================================================================
#     # Load the dictionary containing the already existing inverted indexes
#     with open(path_inverted_indexes, 'rb') as f:
#         inverted_indexes = pickle.load(f)
#         
#     # Load the dictionary containing the length of each document
#     with open(path_doc_lengths, 'rb') as f:
#         doc_lengths = pickle.load(f)
#     
#     # Load the stored restored documents
#     with open(path_restored_documents, 'rb') as f:
#         restored_documents = pickle.load(f)
#     print(f"Loaded {len(restored_documents)} restored documents.")
#     
#     # Add new inverted indexes to the existing ones
#     add_inverted_indexes(inverted_indexes, doc_lengths, restored_documents,
#                          path_inverted_indexes, path_doc_lengths)
# =============================================================================
    
# =============================================================================
#     def cdl(inverted_indexes, doc_lengths, documents, path_doc_lengths):
#         print(f"There are already {len(inverted_indexes)} inverted indexes.")
#         print(f"There are {len(documents)} documents to be processed.")
#         
#         index = Index()
#         i = 0
#         for doc in documents:
#             
#             if doc.cord_uid in doc_lengths:
#                 continue
#             
#             # Retrieve the document fields
#             author_string = "" if doc.authors == None else " ".join(filter(None, doc.authors))
#             sections_string = "" if doc.sections == None else " ".join(filter(None, doc.sections))
#             title_string = "" if doc.title == None else doc.title
#             abstract_string = "" if doc.abstract == None else doc.abstract
#             doc_string = f"{author_string} {sections_string} {title_string} {abstract_string}"
#             
#             # Process the document and write term frequencies to the appropriate file
#             doc_length = index.processDocument(doc_string, doc.cord_uid, inverted_indexes)
#             
#              # Store the document length
#             doc_lengths[doc.cord_uid] = doc_length
#             
#             i += 1
#             if i % 1000 == 0:
#                 print(f"Processed {i} documents ...")
#         print(f"Done: processed {i} additional documents, there are now {len(inverted_indexes)} inverted indexes")
#         
#         # Store the document length dictionary
#         with open(path_doc_lengths, 'wb') as f:
#             pickle.dump(doc_lengths, f)
#             
#     # Load the dictionary containing the already existing inverted indexes
#     with open(path_inverted_indexes, 'rb') as f:
#         inverted_indexes = pickle.load(f)
#         
#     # Load the dictionary containing the length of each document
#     with open(path_doc_lengths, 'rb') as f:
#         doc_lengths = pickle.load(f)
#     
#     # Load the stored restored documents
#     with open(path_restored_documents, 'rb') as f:
#         restored_documents = pickle.load(f)
#     print(f"Loaded {len(restored_documents)} restored documents.")
#         
#     cdl(inverted_indexes, doc_lengths, restored_documents, path_doc_lengths)
# =============================================================================
    
# =============================================================================
#     def cdl(inverted_indexes, doc_lengths, documents, path_doc_lengths):
#         print(f"There are already {len(inverted_indexes)} inverted indexes.")
#         print(f"There are {len(documents)} documents to be processed.")
#         
#         index = Index()
#         i = 0
#         for doc in documents:
#             
#             if doc.cord_uid in doc_lengths:
#                 continue
#             
#             # Retrieve the document fields
#             author_string = "" if doc.authors == None else " ".join(filter(None, doc.authors))
#             sections_string = "" if doc.sections == None else " ".join(filter(None, doc.sections))
#             title_string = "" if doc.title == None else doc.title
#             abstract_string = "" if doc.abstract == None else doc.abstract
#             doc_string = f"{author_string} {sections_string} {title_string} {abstract_string}"
#             
#             # Process the document and write term frequencies to the appropriate file
#             doc_length = index.processDocument(doc_string, doc.cord_uid, inverted_indexes)
#             
#              # Store the document length
#             doc_lengths[doc.cord_uid] = doc_length
#             
#             i += 1
#             if i % 1000 == 0:
#                 print(f"Processed {i} documents ...")
#         print(f"Done: processed {i} additional documents, there are now {len(inverted_indexes)} inverted indexes")
#         
#         # Store the document length dictionary
#         with open(path_doc_lengths, 'wb') as f:
#             pickle.dump(doc_lengths, f)
#                 
#     # Load the dictionary containing the already existing inverted indexes
#     with open(path_inverted_indexes, 'rb') as f:
#         inverted_indexes = pickle.load(f)
#         
#     # Load the dictionary containing the length of each document
#     with open(path_doc_lengths, 'rb') as f:
#         doc_lengths = pickle.load(f)
#     
#     # Load the stored partially matched restored documents
#     with open(path_partially_matched_restored_documents, 'rb') as f:
#         partially_matched_restored_documents = pickle.load(f)
#     print(f"Loaded {len(partially_matched_restored_documents)} partially matched restored documents.")
#         
#     cdl(inverted_indexes, doc_lengths, partially_matched_restored_documents, path_doc_lengths)
# =============================================================================
