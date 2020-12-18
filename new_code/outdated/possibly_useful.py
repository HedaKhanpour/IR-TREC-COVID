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


# =============================================================================
# from sentence_transformers import SentenceTransformer, util
# model = SentenceTransformer('distilroberta-base-msmarco-v2')
# 
# query_embedding = model.encode('How big is London')
# passage_embedding = model.encode('London has 9,787,426 inhabitants at the 2011 census')
# print("Similarity:", util.pytorch_cos_sim(query_embedding, passage_embedding))
# 
# query_embedding = model.encode('How big is London')
# passage_embedding = model.encode('London has 9,787,426 inhabitants')
# print("Similarity:", util.pytorch_cos_sim(query_embedding, passage_embedding))
# 
# query_embedding = model.encode('How big is London')
# passage_embedding = model.encode('London')
# print("Similarity:", util.pytorch_cos_sim(query_embedding, passage_embedding))
# 
# query_embedding = model.encode('How big is London')
# passage_embedding = model.encode('Paris has 9,787,426 inhabitants')
# print("Similarity:", util.pytorch_cos_sim(query_embedding, passage_embedding))
# =============================================================================