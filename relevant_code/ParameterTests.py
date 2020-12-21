from Util import Constants
from Util import load_pickle
from Util import ParametersBM25
from Util import ParametersBM25F
from DocumentRanker import DocumentRanker

class ParameterTests():
    
    def BM25_parameter_tests(self):
        
        # Load the inverted indexes and the document lengths
        inverted_indexes = load_pickle(Constants.path_inverted_indexes)
        document_lengths = load_pickle(Constants.path_document_lengths)
    
        ks = [5.0] # 5.0 appears to be more or less the best value for k
        bs = [0.8] # 0.8 appears to be more or less the best value for b
        
        for k in ks:
            for b in bs:
                parameters = ParametersBM25(k=k, b=b)
                                
                path_results_dir = Constants.path_results_dir + r"BM25_parameter_tests/"
                
                results_file_name = (f"results_BM25-k={k}-b={b}")
                
                parameters.print_parameters()
        
                # Rank the documents
                document_ranker = DocumentRanker()
                document_ranker.rank_documents(inverted_indexes,
                                                    document_lengths,
                                                    parameters,
                                                    Constants.path_topics,
                                                    path_results_dir,
                                                    results_file_name)
                                                
        
        del inverted_indexes, document_lengths
        
        print("Done ranking documents.")
    
# =============================================================================
#         # BM25 parameter test results (mAP metric):
#         # round 1
#         map_bm25_k5_b1 = 0.1479
#         map_bm25_k5_b3 = 0.1739
#         map_bm25_k5_b5 = 0.1950
#         map_bm25_k5_b7 = 0.2105
#         map_bm25_k5_b9 = 0.2022
#         map_bm25_k5_b99 = 0.1750
#         
#         map_bm25_k9_b1 = 0.1508
#         map_bm25_k9_b3 = 0.1783
#         map_bm25_k9_b5 = 0.2010
#         map_bm25_k9_b7 = 0.2188
#         map_bm25_k9_b9 = 0.2111
#         map_bm25_k9_b99 = 0.1828
#         
#         map_bm25_k12_b1 = 0.1524
#         map_bm25_k12_b3 = 0.1806
#         map_bm25_k12_b5 = 0.2042
#         map_bm25_k12_b7 = 0.2229
#         map_bm25_k12_b9 = 0.2158
#         map_bm25_k12_b99 = 0.1865
#         
#         map_bm25_k15_b1 = 0.1535
#         map_bm25_k15_b3 = 0.1826
#         map_bm25_k15_b5 = 0.2069
#         map_bm25_k15_b7 = 0.2263
#         map_bm25_k15_b9 = 0.2198
#         map_bm25_k15_b99 = 0.1892
#         
#         map_bm25_k18_b1 = 0.1546
#         map_bm25_k18_b3 = 0.1842
#         map_bm25_k18_b5 = 0.2088
#         map_bm25_k18_b7 = 0.2297
#         map_bm25_k18_b9 = 0.2235
#         map_bm25_k18_b99 = 0.1911
#         
#         # round 2
#         map_bm25_k15_b6 = 0.2174
#         map_bm25_k15_b7 = 0.2263
#         map_bm25_k15_b8 = 0.2298
#         
#         map_bm25_k21_b6 = 0.2220
#         map_bm25_k21_b7 = 0.2322
#         map_bm25_k21_b8 = 0.2368
#         
#         map_bm25_k24_b6 = 0.2341
#         map_bm25_k24_b7 = 0.2393
#         map_bm25_k24_b8 = 0.2393
#         
#         # round 3
#         map_bm25_k24_b75 = 0.2397
#         map_bm25_k24_b8  = 0.2413
#         map_bm25_k24_b85 = 0.2391
#         
#         map_bm25_k33_b75 = 0.2416
#         map_bm25_k33_b8  = 0.2434
#         map_bm25_k33_b85 = 0.2420
#         
#         map_bm25_k39_b75 = 0.2423
#         map_bm25_k39_b8  = 0.2449
#         map_bm25_k39_b85 = 0.2436
#         
#         # round 4
#         map_bm25_k45_b8 = 0.2450
#         map_bm25_k51_b8 = 0.2453
#         map_bm25_k57_b8 = 0.2444
#         map_bm25_k63_b8 = 0.2436
#         map_bm25_k69_b8 = 0.2426
#         map_bm25_k75_b8 = 0.2414
#         
#         # round 5
#         map_bm25_k48_b8 = 0.2453
#         map_bm25_k49_b8 = 0.2453
#         map_bm25_k50_b8 = 0.2453
#         map_bm25_k51_b8 = 0.2453
#         map_bm25_k52_b8 = 0.2450
#         
#         # round 5
#         map_bm25_k50_b75 = 0.2421
#         map_bm25_k50_b8  = 0.2453
#         map_bm25_k50_b85 = 0.2447
# 
#         Conclusion (more or less) best parameters at k=5.0 and b=0.8
#
# =============================================================================
    
    def BM25F_parameter_tests(self):
        
        # The (non-field-specific) 'b' parameter is included by mistake
        def run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                     k, b, 
                     weight_title, weight_author,
                     weight_abstract, weight_sections,
                     b_title, b_author, 
                     b_abstract, b_sections):
        
            parameters = ParametersBM25F(k=k,
                     weight_title=weight_title, weight_author=weight_author,
                     weight_abstract=weight_abstract, weight_sections=weight_sections,
                     b_title=b_title, b_author=b_author, 
                     b_abstract=b_abstract, b_sections=b_sections)
                
            parameters.print_parameters()
                                                
            path_results_dir = Constants.path_results_dir + r"BM25F_parameter_tests/"
            
            results_file_name = (f"results_BM25F_test_{test_id}")
            
            document_ranker = DocumentRanker()
            document_ranker.rank_documents_bm25f(inverted_indexes_bm25f,
                                                      doc_length_info_bm25f,
                                                      parameters,
                                                      Constants.path_topics,
                                                      path_results_dir,
                                                      results_file_name)
        
        inverted_indexes_bm25f = load_pickle(Constants.path_inverted_indexes_bm25f)
        doc_length_info_bm25f = load_pickle(Constants.path_doc_length_info_bm25f)
        
        round_nr = 11
        if round_nr == 0: # round 0 - getting a feel of impact field weights
            test_id = "00"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=1.0, weight_author=1.0,
                                         weight_abstract=1.0, weight_sections=1.0,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.1872
            
            test_id = "01"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=1.0, weight_author=0.2,
                                         weight_abstract=1.0, weight_sections=1.0,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.1872
            
            test_id = "02"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=1.0, weight_author=1.0,
                                         weight_abstract=1.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2331
            
            test_id = "03"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=1.0, weight_author=1.0,
                                         weight_abstract=1.0, weight_sections=0.5,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2093
            
            test_id = "04"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=1.0, weight_author=1.0,
                                         weight_abstract=1.0, weight_sections=1.5,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.1754
            
            # Conclusions:
            #   -author field can probably be disregarded (as expected)
            #   -section field should have relatively low weight
            
        elif round_nr == 1: # round 1 - getting a better feel of field weights
            test_id = "10"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=1.0, weight_author=0.0,
                                         weight_abstract=1.0, weight_sections=1.0,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.1872
            
            test_id = "11"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=1.0, weight_author=5.0,
                                         weight_abstract=1.0, weight_sections=1.0,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.1871
            
            test_id = "12"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=1.0, weight_author=0.0,
                                         weight_abstract=0.5, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2132
            
            test_id = "13"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=1.0, weight_author=0.0,
                                         weight_abstract=1.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2331
            
            test_id = "14"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=1.0, weight_author=0.0,
                                         weight_abstract=1.5, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2390
            
            test_id = "15"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=0.5, weight_author=0.0,
                                         weight_abstract=1.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2218
            
            test_id = "16"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=1.0, weight_author=0.0,
                                         weight_abstract=1.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2331
            
            test_id = "17"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=1.5, weight_author=0.0,
                                         weight_abstract=1.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2398
            
            # Conclusions:
            #   -author field be disregarded set to 0
            #   -abstract field should have a relatively high weight (as expected)
            #   -title field should have a relatively hight weight (as expected)
            
        elif round_nr == 2: # round 2 - focussing on abstract weights
            test_id = "20"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=1.0, weight_author=0.0,
                                         weight_abstract=1.0, weight_sections=0.01,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2016
            
            test_id = "21"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=1.0, weight_author=0.0,
                                         weight_abstract=1.0, weight_sections=0.05,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2210
            
            test_id = "22"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=1.0, weight_author=0.0,
                                         weight_abstract=1.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2331
            
            test_id = "23"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=1.0, weight_author=0.0,
                                         weight_abstract=1.0, weight_sections=0.3,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2248
            
            # Conclusions:
            #   -With the other weights as they are, sections weight of 0.2 is good
            
        elif round_nr == 3: # round 3
            test_id = "30"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=0.8, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2409
            
            test_id = "31"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=1.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2465
            
            test_id = "32"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=1.5, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=2536
            
            test_id = "33"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2540
            
            test_id = "34"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=3.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2493
            
            test_id = "35"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=5.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2348
            
            # Conclusions:
            #   -With the other weights as they are, abstract weight of 2.0 is good
            
        elif round_nr == 4: # round 4 - focussing on title weights
            test_id = "40"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=0.8, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2357
            
            test_id = "41"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=1.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2390
            
            test_id = "42"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=1.5, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2459
            
            test_id = "43"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=2.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2499
            
            test_id = "44"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2536
            
            test_id = "45"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=5.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2514
            
            # Conclusions:
            #   -With the other weights as they are, title weight of 3.0 is good
            
        elif round_nr == 5: # round 5 - focussing on parameter 'k'
            test_id = "50"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=1.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2371
            
            test_id = "51"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=2.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2480
            
            test_id = "52"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2510
            
            test_id = "53"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=4.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            
            # map=0.2509
            
            test_id = "54"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=4.5, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2502
            
            test_id = "55"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2493
            
            test_id = "56"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=5.5, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2481
            
            test_id = "57"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=6.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2470
            
            test_id = "58"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=7.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2449
            
            # Conclusions:
            #   -With the other weights as they are, a 'k' of 3.0 is good
            
        elif round_nr == 6: # round 6 - focussing on parameter 'b' (which does not exist)
            test_id = "60"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.2, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2596
            
            test_id = "61"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.5, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2596
            
            test_id = "62"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.6, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2596
            
            test_id = "63"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.7, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2596
            
            test_id = "64"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2596
            
            test_id = "65"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.9, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2596
            
            # Conclusions:
            #   -There is no general b parameter...
            
        elif round_nr == 7: # round 7 - focussing on field 'b' parameters
            test_id = "70"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.7, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2596
            
            test_id = "71"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.9, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.8)
            # map=0.2595
            
            test_id = "72"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.7, b_sections=0.8)
            # map=0.2615
            
            test_id = "73"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.9, b_sections=0.8)
            # map=0.2563
            
            test_id = "74"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.7)
            # map=0.2595
            
            test_id = "75"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.8, b_sections=0.9)
            # map=0.2589
            
            test_id = "76"
            b_fields = 0.7
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=b_fields, b_author=b_fields, 
                                         b_abstract=b_fields, b_sections=b_fields)
            # map=0.2613
            
            test_id = "77"
            b_fields = 0.9
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=b_fields, b_author=b_fields, 
                                         b_abstract=b_fields, b_sections=b_fields)
            # map=0.2556
            
            # Conclusions:
            #   -Except for sections 0.7 appears to be a better 'b' than 0.8
            
        elif round_nr == 8: # round 8 - Focussing again on field 'b' parameters
            test_id = "80"
            b_fields = 0.4
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=b_fields, b_author=b_fields, 
                                         b_abstract=b_fields, b_sections=0.8)
            # map=0.2637
            
            test_id = "81"
            b_fields = 0.5
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=b_fields, b_author=b_fields, 
                                         b_abstract=b_fields, b_sections=0.8)
            # map=0.2634
            
            test_id = "82"
            b_fields = 0.6
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=b_fields, b_author=b_fields, 
                                         b_abstract=b_fields, b_sections=0.8)
            # map=0.2628
            
            test_id = "83"
            b_fields = 0.7
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=b_fields, b_author=b_fields, 
                                         b_abstract=b_fields, b_sections=0.8)
            # map=0.2615
            
            test_id = "84"
            b_fields = 0.8
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=b_fields, b_author=b_fields, 
                                         b_abstract=b_fields, b_sections=0.8)
            # map=0.2596
            
            test_id = "85"
            b_fields = 0.9
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=b_fields, b_author=b_fields, 
                                         b_abstract=b_fields, b_sections=0.8)
            # map=0.2562
            
            test_id = "86"
            b_fields = 0.7
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=b_fields, b_author=b_fields, 
                                         b_abstract=b_fields, b_sections=0.7)
            # map=0.2613
            
            # Conclusions:
            #   -For sections the 'b' parameter of 0.8 is good
            #   -For title and abstract the 'b' parameter of either or both
            #      may be best below 0.4
            
        elif round_nr == 9: # round 9 - Focussing again on field 'b' parameters
            test_id = "90"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.3, b_author=0.8, 
                                         b_abstract=0.4, b_sections=0.8)
            # map=0.2633
            
            test_id = "91"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.5, b_author=0.8, 
                                         b_abstract=0.4, b_sections=0.8)
            # map=0.2638
            
            test_id = "92"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.4, b_author=0.8, 
                                         b_abstract=0.3, b_sections=0.8)
            # map=0.2634
            
            test_id = "93"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.4, b_author=0.8, 
                                         b_abstract=0.5, b_sections=0.8)
            # map=0.2632
            
            test_id = "94"
            b_fields = 0.4
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=b_fields, b_author=b_fields, 
                                         b_abstract=b_fields, b_sections=0.8)
            # map=0.2637
            
            test_id = "95"
            b_fields = 0.4
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=b_fields, b_author=0.8, 
                                         b_abstract=b_fields, b_sections=0.8)
            # map=0.2637
            
            test_id = "96"
            b_fields = 0.3
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=b_fields, b_author=0.8, 
                                         b_abstract=b_fields, b_sections=0.8)
            # map=0.2632
            
            test_id = "97"
            b_fields = 0.2
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=b_fields, b_author=0.8, 
                                         b_abstract=b_fields, b_sections=0.8)
            # map=0.2617
            
            test_id = "98"
            b_fields = 0.1
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=b_fields, b_author=0.8, 
                                         b_abstract=b_fields, b_sections=0.8)
            # map=0.2587
            
            # Conclusions:
            #   -For the title a 'b' parameter of 0.5 or higher appears best
            #   -For the abstract a 'b' parameter of 0.4 appears best
        
            
        elif round_nr == 10: # round 10 - Final b test for title
            test_id = "100"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.3, b_author=0.8, 
                                         b_abstract=0.4, b_sections=0.8)
            # map=0.2633
            
            test_id = "101"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.4, b_author=0.8, 
                                         b_abstract=0.4, b_sections=0.8)
            # map=0.2637
            
            test_id = "102"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.5, b_author=0.8, 
                                         b_abstract=0.4, b_sections=0.8)
            # map=0.2638
            
            test_id = "103"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.6, b_author=0.8, 
                                         b_abstract=0.4, b_sections=0.8)
            # map=0.2640
            
            test_id = "104"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.7, b_author=0.8, 
                                         b_abstract=0.4, b_sections=0.8)
            # map=0.2642
            
            test_id = "105"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.8, b_author=0.8, 
                                         b_abstract=0.4, b_sections=0.8)
            # map=0.2641
            
            test_id = "106"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.2,
                                         b_title=0.9, b_author=0.8, 
                                         b_abstract=0.4, b_sections=0.8)
            # map=0.2641
            
            # Conclusions:
            #   -For the title a 'b' parameter of 0.7 appears best
            
        elif round_nr == 11: # round 11 - Some final tweaking
            test_id = "110"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.1,
                                         b_title=0.7, b_author=0.8, 
                                         b_abstract=0.4, b_sections=0.8)
            # map=0.2537
            
            test_id = "111"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.3,
                                         b_title=0.7, b_author=0.8, 
                                         b_abstract=0.4, b_sections=0.8)
            # map=0.2648
            
            test_id = "112"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.4,
                                         b_title=0.7, b_author=0.8, 
                                         b_abstract=0.4, b_sections=0.8)
            # map=0.2601
            
            test_id = "113"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.5,
                                         b_title=0.7, b_author=0.8, 
                                         b_abstract=0.4, b_sections=0.8)
            # map=0.2528
            
            test_id = "114"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.7,
                                         b_title=0.7, b_author=0.8, 
                                         b_abstract=0.4, b_sections=0.8)
            # map=0.2373
            
            test_id = "115"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=0.8,
                                         b_title=0.7, b_author=0.8, 
                                         b_abstract=0.4, b_sections=0.8)
            # map=0.2300
            
            test_id = "116"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=1.0,
                                         b_title=0.7, b_author=0.8, 
                                         b_abstract=0.4, b_sections=0.8)
            # map=0.2173
            
            test_id = "117"
            run_test(test_id, inverted_indexes_bm25f, doc_length_info_bm25f,
                                         k=3.0, b=0.8, 
                                         weight_title=3.0, weight_author=0.0,
                                         weight_abstract=2.0, weight_sections=1.5,
                                         b_title=0.7, b_author=0.8, 
                                         b_abstract=0.4, b_sections=0.8)
            # map=0.1937
            
            # Conclusions:
            #   - The following appear to be good parameters:
            #   -   k=3.0, b=0.8
            #   -   weight_title=3.0, weight_author=0.0, weight_abstract=2.0, weight_sections=0.3
            #   -   b_title=0.7, b_author=0.8, b_abstract=0.4, b_sections=0.8
    
        
        print("Done testing BM25F parameters.")