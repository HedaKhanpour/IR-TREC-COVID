import sys
import re
import os.path
import json
    
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

class CsvReader():
    
    def __init__(self, cord_path="D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/",
                 file_name="metadata.csv"):
        
        self.cord_path = cord_path
        metadata_path = self.cord_path + file_name
        self.file = open(metadata_path, "r", encoding="utf-8")
        
        self.headers = {}
        h = re.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", self.file.readline())
        for i in range(len(h)):
            self.headers[h[i]] = i
            
    def get_next(self, line):
        cells = re.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", line)
        
        def is_empty(string):
            return string == None or re.sub("\\s+", "", string) == ""
        
        cord_uid = cells[self.headers.get("cord_uid")]
        title = cells[self.headers.get("title")].strip("\"")
        abstract = cells[self.headers.get("abstract")].strip("\"")
        temp_str = cells[self.headers.get("authors")].strip("\"")
        authors = None if is_empty(temp_str) else temp_str.split(";")
        temp_str = cells[self.headers.get("pmc_json_files")]
        pmc_json = None if is_empty(temp_str) else (temp_str.split(";")[0])
        
        if is_empty(pmc_json):
            return None
        
        if not os.path.isfile(self.cord_path + pmc_json):
            return None
        
        file = open(self.cord_path + pmc_json, "r", encoding="utf-8")
        obj = json.load(file)
        
        if obj == None:
            return None
        
        body_text = obj.get("body_text")
        sections = []
        if body_text != None:
            for key in body_text:
                name = key.get("section")
                text = key.get("text")
                sections.append(Section(name, text))
                
        document = Document(cord_uid, title, abstract, authors, sections)
        return document

class Document():
    
    def __init__(self, cord_uid, title, abstract, authors, sections):
        self.cord_uid = cord_uid
        self.title = title
        self.abstract = abstract
        self.authors = None if authors == None else authors.copy()
        self.sections = None if sections == None else sections.copy()
        
    def get_raw_text(self):
        
        author_string = "" if self.authors == None else " ".join(self.authors)
        sections_string = "" if self.sections == None else " ".join(
                [section.get_raw_text() for section in self.sections])
        title_string = " " if self.title == None else self.title
        abstract_string = " " if self.abstract == None else self.abstract
        return "{:s} {:s} {:s} {:s}".format(
                author_string, sections_string, title_string, abstract_string)
    
    def any_null(self):
        if self.sections == None:
            return True
        for section in self.sections:
            if section.any_null():
                return True
        return (self.cord_uid == None or self.title == None 
                or self.abstract == None or self.authors == None)
    
    def count_nulls(self):
        null_counter = DocumentNullCounter()
        null_counter.cord_uid += 1 if self.cord_uid == None else 0
        null_counter.title += 1 if self.title == None else 0
        null_counter.abstract += 1 if self.abstract == None else 0
        null_counter.authors += 1 if self.authors == None else 0
        if self.sections == None:
            null_counter.sections += 1
        else:
            for section in self.sections:
                null_counter.add(section.count_nulls())
        return null_counter
    
    def __str__(self):
        string = "\n********** Document **********\n"
        string += "cord_uid: {}\n".format(self.cord_uid)
        string += "title: {}\n".format(self.title)
        
        string += "authors: "
        for author in self.authors:
            string += "{}\t".format(author)
        string += "\n"
        
        string +=  "abstract: {}\n".format(self.abstract)
        
        for section in self.sections:
            string += "{}\n".format(section.__str__())
        
        return string

class Section():
    
    def __init__(self, name, text):
        self.name = name
        self.text = text
    
    def get_raw_text(self):
        name_string = " " if self.name == None else self.name
        text_string = " " if self.text == None else self.text
        return "{:s} {:s}".format(name_string, text_string)
    
    def any_null(self):
        return self.name == None or self.text == None
    
    def count_nulls(self):
        null_counter = DocumentNullCounter()
        null_counter.sections_title += 1 if self.name == None else 0
        null_counter.sections_text += 1 if self.text == None else 0
        return null_counter
    
    def __str__(self):
        return "[{:s}] \t{:s}".format(self.name, self.text)
        
class DocumentNullCounter():
    
    def __init__(self):
        self.cord_uid = 0
        self.title = 0
        self.abstract = 0
        self.authors = 0
        self.sections= 0
        self.sections_title = 0
        self.sections_text = 0
    
    def add(self, doc_null_counter):
        self.cord_uid += doc_null_counter.cord_uid
        self.title += doc_null_counter.title
        self.abstract += doc_null_counter.abstract
        self.authors += doc_null_counter.authors
        self.sections+= doc_null_counter.sections
        self.sections_title += doc_null_counter.sections_title
        self.sections_text += doc_null_counter.sections_text
        
    def print_count(self):
        print("cord_uid nulls = {}".format(self.cord_uid))
        print("title nulls = {}".format(self.title))
        print("abstract nulls = {}".format(self.abstract))
        print("authors nulls = {}".format(self.authors))
        print("sections nulls = {}".format(self.sections))
        print("sectionsTitle nulls = {}".format(self.sections_title))
        print("SectionsText nulls = {}".format(self.sections_text))

if __name__ == "__main__":
    csv_reader = CsvReader(
            cord_path="D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/",
            file_name="metadata.csv")
    null_counter = DocumentNullCounter()
    doc_null_count = 0
    i = 0
    for line in csv_reader.file:
        if i % 1000 == 0 and i > 0:
            print("Iteration %d"%i)
        document = csv_reader.get_next(line)
        if document == None:
            doc_null_count += 1
        else:
            null_counter.add(document.count_nulls())    
        i +=1
        
        #print(document)
# =============================================================================
#         if i == 30000:
#             print("Breaking at iteration: %d"%i)
#             break
# =============================================================================
        
    
    print("No documents left")
    csv_reader.file.close()
    
    print("Total nr of documents: %d"%i)
    print("doc_null_count: %d"%doc_null_count)
    null_counter.print_count()
    
    print("***** Program done *****")

    
