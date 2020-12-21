def inspect_judgements(output_path=r"trec_eval-master/our_data/test_results.txt",
                       gold_path=r"trec_eval-master/our_data/CRJ.txt",
                       metadata_path=r"D:/Universiteit/Master (Large Files)/IR Project/2020-07-16/metadata.csv"):
    
    output = []
    with open(output_path, "r") as f:
        for line in f:
            split = line.split(" ")
            #              Topic NR  useless   Doc ID    Rank      Score     Run-tag
            output.append((split[0], split[1], split[2], split[3], split[4], re.sub("\\n", "", split[5])))
    
    gold = []
    with open(gold_path, "r") as f:
        for line in f:
            split = line.split(" ")
            #            Topic NR  ????      Doc ID    Score
            gold.append((split[0], split[1], split[2], re.sub("\\n", "", split[3])))   
    print(f"len(output)={len(output)}")
    print(f"len(gold)={len(gold)}")
    print()
    
    unique_output_ids = set([x[2] for x in output])
    unique_gold_ids = set([x[2] for x in gold])
    print(f"len(unique_output_ids)={len(unique_output_ids)}")
    print(f"len(unique_gold_ids)={len(unique_gold_ids)}")
    print()
    
    only_output = unique_output_ids - unique_gold_ids
    only_gold = unique_gold_ids - unique_output_ids
    symmetric_difference = unique_output_ids.symmetric_difference(unique_gold_ids)
    intersection = unique_output_ids.intersection(unique_gold_ids)
    print(f"len(only_output)={len(only_output)}")
    print(f"len(only_gold)={len(only_gold)}")
    print(f"len(symmetric_difference)={len(symmetric_difference)}")
    print(f"len(intersection)={len(intersection)}")
    print()
    print()
    print()
    
    all_doc_ids = []
    with open(metadata_path, "r",  encoding="utf-8") as f:
        f.readline()
        for line in f:
            all_doc_ids.append(line.split(",")[0])
    unique_doc_ids = set(all_doc_ids)
    print(f"len(all_doc_ids)={len(all_doc_ids)}")
    print(f"len(unique_doc_ids)={len(unique_doc_ids)}")
    print()
    
    sd_all_vs_output = unique_doc_ids.symmetric_difference(unique_output_ids)
    int_all_vs_output = unique_doc_ids.intersection(unique_output_ids)
    print(f"len(sd_all_vs_output)={len(sd_all_vs_output)}")
    print(f"len(int_all_vs_output)={len(int_all_vs_output)}") # This is as should be
    print()
    
    sd_all_vs_gold = unique_doc_ids.symmetric_difference(unique_gold_ids)
    int_all_vs_gold = unique_doc_ids.intersection(unique_gold_ids)
    print(f"len(sd_all_vs_gold)={len(sd_all_vs_gold)}")
    print(f"len(int_all_vs_gold)={len(int_all_vs_gold)}") # This is as should be
    print()
    
# =============================================================================
# 
# from sentence_transformers import SentenceTransformer
# 
# embedder = SentenceTransformer('bert_base-nli-mean-tokens') # BERT BASE
# # embedder = SentenceTransformer('bert-large-nli-stsb-mean-tokens') # LARGE BERT
# 
# #corpus_embeddings = embedder.encode(raw_data['text']).to_list())
# 
# import torch
# =============================================================================


# =============================================================================
# from sentence_transformers import SentenceTransformer
# model = SentenceTransformer('distilbert-base-nli-mean-tokens')
# 
# 
# sentences = ['This framework generates embeddings for each input sentence',
#     'Sentences are passed as a list of string.', 
#     'The quick brown fox jumps over the lazy dog.']
# sentence_embeddings = model.encode(sentences)
# 
# 
# for sentence, embedding in zip(sentences, sentence_embeddings):
#     print("Sentence:", sentence)
#     print("Embedding:", embedding)
#     print("")
# =============================================================================


from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('distilroberta-base-msmarco-v2')

query_embedding = model.encode('How big is London')
passage_embedding = model.encode('London has 9,787,426 inhabitants at the 2011 census')
print("Similarity:", util.pytorch_cos_sim(query_embedding, passage_embedding))

query_embedding = model.encode('How big is London')
passage_embedding = model.encode('London has 9,787,426 inhabitants')
print("Similarity:", util.pytorch_cos_sim(query_embedding, passage_embedding))

query_embedding = model.encode('How big is London')
passage_embedding = model.encode('London')
print("Similarity:", util.pytorch_cos_sim(query_embedding, passage_embedding))

query_embedding = model.encode('How big is London')
passage_embedding = model.encode('Paris has 9,787,426 inhabitants')
print("Similarity:", util.pytorch_cos_sim(query_embedding, passage_embedding))
a  = util.pytorch_cos_sim(query_embedding, passage_embedding)
print(a[0][0].item())


# =============================================================================
# JUDGED STUFF
# JUDGED STUFF
# JUDGED STUFF
# JUDGED STUFF
# JUDGED STUFF
# =============================================================================

# =============================================================================
#     judged_inverted_indexes = load_pickle(Constants.path_judged_inverted_indexes)
#     judged_doc_lengths = load_pickle(Constants.path_judged_document_lengths)
#     search_system.document_ranker.rank_documents(judged_inverted_indexes,
#                                                  judged_doc_lengths,
#                                                  Constants.path_topics, 
#                                                  results_file_name="results_judged")
#     del judged_inverted_indexes
#     del judged_doc_lengths
# =============================================================================
    
    
# =============================================================================
#     judged_documents = load_pickle(Constants.path_judged_documents)
#     judged_document_lengths = load_pickle(Constants.path_judged_document_lengths)
#     Util.compute_document_statistics(judged_documents, judged_document_lengths,
#                                      Constants.path_relevance_judgements)
#     del judged_documents
#     del judged_document_lengths
# =============================================================================
from Util import load_pickle
inverted_indexes = load_pickle(Constants.path_inverted_indexes)
doc_lengths = load_pickle(Constants.path_document_lengths)
documents_dict = load_pickle(Constants.path_doc_dict)

search_system.document_ranker.rank_with_rerank_light(inverted_indexes,
                    doc_lengths, Constants.path_topics, documents_dict,
                    path_results_dir=r"../trec_eval-master/our_data/",
                    results_file_name="results_rerank")


def filter_judged_documents(self, path_final_documents, 
                            path_relevance_judgements,
                            path_judged_documents):
    
    judged_cord_uids = set()
    with open(path_relevance_judgements, 'r') as f:
        for line in f:
            judged_cord_uid = line.split(" ")[2]
            judged_cord_uids.add(judged_cord_uid)
    print(f"Retrieved {len(judged_cord_uids)} cord_uids of judged documents.")
    
    final_documents = load_pickle(path_final_documents)
    judged_documents = []
    for document in final_documents:
        if document.cord_uid in judged_cord_uids:
            judged_documents.append(document)
    print(f"Filtered {len(judged_documents)} judged documents.")
    
    save_pickle(judged_documents, path_judged_documents)


        
path_judged_documents = path_pickles + "judged_documents.pkl"
path_judged_inverted_indexes = path_pickles + "judged_inverted_indexes.pkl"
path_judged_document_lengths = path_pickles + "judged_document_lengths.pkl"



    
# =============================================================================
#         ks = [5.0]
#         bs = [0.8]
#         
#         weights_title = [0.3, 0.5]
#         weights_author = [0.3, 0.5]
#         weights_abstract = [0.3, 0.5]
#         weights_sections = [0.3, 0.5]
#         
#         bs_title = [0.8]
#         bs_author = [0.8]
#         bs_abstract = [0.8]
#         bs_sections = [0.8]
#         
#         parameters = ParametersBM25F(k=5.0, b=0.8, 
#                                      weight_title=1.0, weight_author=1.0,
#                                      weight_abstract=1.0, weight_sections=1.0,
#                                      b_title=0.8, b_author=0.8, 
#                                      b_abstract=0.8, b_sections=0.8)
#         
#         for k in ks:
#             for b in bs:
#                 for weight_title in weights_title:
#                     for weight_author in weights_author:
#                         for weight_abstract in weights_abstract:
#                             for weight_sections in weights_sections:
#                                 for b_title in bs_title:
#                                     for b_author in bs_author:
#                                         for b_abstract in bs_abstract:
#                                             for b_sections in bs_sections:
#                                                 parameters = ParametersBM25F(k=k, b=b, 
#                                                             weight_title=weight_title, weight_author=weight_author,
#                                                             weight_abstract=weight_abstract, weight_sections=weight_sections,
#                                                             b_title=b_title, b_author=b_author, 
#                                                             b_abstract=b_abstract, b_sections=b_sections)
#                                                 
#                                                 path_results_dir = Constants.path_results_dir + r"BM25F_parameter_tests/"
#                                                 
#                                                 results_file_name = (f"results_BM25F-k={k}-b={b}-weight_titel={weight_title}-weight_author={weight_author}-"
#                                                       + f"weight_abstract={weight_abstract}-weight_sections={weight_sections}"
#                                                       + f"-b_title={b_title}-b_author={b_author}-"
#                                                       + f"b_abstract={b_abstract}-b_sections={b_sections}")
#                                                 
#                 
#                                                 parameters.print_parameters()
#                                                 
#                                                 self.document_ranker.rank_documents_bm25f(inverted_indexes_bm25f,
#                                                   doc_length_info_bm25f,
#                                                   parameters,
#                                                   Constants.path_topics,
#                                                   path_results_dir,
#                                                   results_file_name)
#                                                 
#         
#         del inverted_indexes_bm25f, doc_length_info_bm25f
# =============================================================================