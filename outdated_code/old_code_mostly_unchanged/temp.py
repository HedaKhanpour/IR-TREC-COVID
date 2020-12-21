def BM25(k=1.2, b=0.75):
    q = ["Testing", "BM25"]
    d = "This single sentence document is used to test BM25"
    doc_len = len(d.split(" "))
    avg_doc_len = 10
    nr_of_docs = 15
    
    def count(q_i, d):
        dl = d.split(" ")
        
        c = 0
        for t in dl:
            if t == q_i:
                c += 1
        return c
    
    score = 0
    for q_i in q:
        print(f"\n{q_i}:")
        
        num = (k + 1) * count(q_i, d)
        print(f"num={num}")
        
        denom = count(q_i, d) + k*(1 - b + b*doc_len/avg_doc_len)
        print(f"denom={denom}")
        
        docs_containing_q_i = 3
        IDF = log((nr_of_docs + 1)/docs_containing_q_i)
        print(f"IDF={IDF}")
        
        score += num/denom*IDF
    print(f"\nscore={score}")
    
    
    ranker = Rank(k, b, nr_of_docs, avg_doc_len)
    
    print()
    score = 0
    for q_i in q:
        tf = count(q_i, d)
        docs_containing_q_i = 3
        IDF = log((nr_of_docs + 1)/docs_containing_q_i)
        score += ranker.calculate_BM25_score(tf, IDF)
    print(score)
    
    
    print()
    for q_i in q:
        a = log(((nr_of_docs - docs_containing_q_i + 0.5) / (docs_containing_q_i + 0.5)) + 1)
        b = log((nr_of_docs + 1)/docs_containing_q_i)
        print(f"\nwikipedia_IDF={a}")
        print(f"lecture2_IDF={a}")


def process_line():
    pass
            # print(f"\n\n\ncord_uid:\n{cord_uid}\n\ntitle:\n{title}\n\nabstract:\n{abstract}\n\ntemp_str:\n{temp_str}\n\nauthors:\n{authors}\n\ntemp_str:\n{temp_str}\n\npmc_json:\n{pmc_json}\n\npdf_json:\n{pdf_json}")
        
# =============================================================================
#         if pdf_json.split(";")[0] != pdf_json:
#             print("yeah")
#             print(pdf_json)
#         if pmc_json.split(";")[0] != pmc_json:
#             print("yeah")
# =============================================================================
        
# =============================================================================
#         if os.path.isfile(path_doc_parses + r"pmc_json/PMC35282.xml.json"):
#             print ("File exist")
#         else:
#             print ("File not exist")
# =============================================================================
# =============================================================================
#         if not is_empty(pmc_json) and not is_empty(pdf_json):
#             print(f"\n\n\ncord_uid:\n{cord_uid}\n\ntitle:\n{title}\n\nabstract:\n{abstract}\n\ntemp_str:\n{temp_str}\n\nauthors:\n{authors}\n\ntemp_str:\n{temp_str}\n\npmc_json:\n{pmc_json}\n\npdf_json:\n{pdf_json}")
# =============================================================================
# =============================================================================
#             print()
#             print("...")
#             print(cells[self.headers.get("pdf_json_files")])
#             print(cells[self.headers.get("pmc_json_files")])
#             print("...")
#             print()
# =============================================================================
            
# =============================================================================
#             if is_empty(pdf_json):
#                 print("\n\n\n\n\n ---------------------- START ---------------------- ")
#                 i=0
#                 for cell in cells:
#                     print(f"\n{i}: {cell}")
#                     i +=1
#                 print(f"\n\n\ncord_uid:\n{cord_uid}\n\ntitle:\n{title}\n\nabstract:\n{abstract}\n\ntemp_str:\n{temp_str}\n\nauthors:\n{authors}\n\ntemp_str:\n{temp_str}\n\npmc_json:\n{pmc_json}\n\npdf_json:\n{pdf_json}")
# =============================================================================
        
# =============================================================================
#         if is_empty(pmc_json):
#             print("\n\n\n\n\n ---------------------- START ---------------------- ")
#             print(line)
#             i = 0
#             for cell in cells:
#                 print(f"\n{i}: {cell}")
#                 i += 1
#             print(f"\n\n\ncord_uid:\n{cord_uid}\n\ntitle:\n{title}\n\nabstract:\n{abstract}\n\ntemp_str:\n{temp_str}\n\nauthors:\n{authors}\n\ntemp_str:\n{temp_str}\n\npmc_json:\n{pmc_json}")
#             
#             print("\n?????????????????????????????\n")
#             print(temp_str)
#             print(cells[14])
#             print(cells[15])
#             print(cells[16])
#             
#             sys.exit()
#             
#         if is_empty(pmc_json):
#             
#         
# =============================================================================
        
# =============================================================================
#         if is_empty(pmc_json):
#             return None
#         thing
#         if not os.path.isfile(self.cord_path + pmc_json):
#             return None
#         
#         file = open(self.cord_path + pmc_json, "r", encoding="utf-8")
#         obj = json.load(file)
#         
#         if obj == None:
#             return None
#         
#         body_text = obj.get("body_text")
#         sections = []
#         if body_text != None:
#             for key in body_text:
#                 name = key.get("section")
#                 text = key.get("text")
#                 sections.append(Section(name, text))
#                 
#         document = Document(cord_uid, title, abstract, authors, sections)
#         return document
# =============================================================================

# =============================================================================
# import os
# if __name__ == "__main__":
#     path_doc_parses = r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/document_parses/"
#     
#     print("pdf:")
#     if os.path.isfile(path_doc_parses + r"pdf_json/83d82d42b92c964ba7bd7bd9f456a16c9d3cbaaf.json"):
#         print("File exist")
#     else:
#         print("File not exist")
#     
#     print("\npmc")
#     if os.path.isfile(path_doc_parses + r"pmc_json/PMC6408800.xml.json"):
#         print("File exist")
#     else:
#         print("File not exist")
# =============================================================================

# =============================================================================
# if __name__ == "__main__":
#     a = ["aa", "bb", "", "dd"]
#     b = " ".join(filter(None, a))
#     print(a)
#     print(b)
# =============================================================================

if __name__ == "__main__":
    a = {'a':1, 'b':'2', 'c':0}
    print(len(a))
    for item in a:
        print(item)
        
    print(f"{1/2}")