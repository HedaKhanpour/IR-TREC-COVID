'''
    # Sort by score and select the n highest scored documents
    top_n = 20
    top_n_doc_scores = dict(sorted(doc_scores.items(),
                                key = itemgetter(1), reverse = True)[:top_n])
    
    top_n_doc_scores_2 = dict(sorted(doc_scores_2.items(),
                                key = itemgetter(1), reverse = True)[:top_n])
    print("Sorting top n scores: DONE")
    for i in range(top_n):
        id_1 = list(top_n_doc_scores.keys())[i]
        id_2 = list(top_n_doc_scores_2.keys())[i]
        score_1 = top_n_doc_scores[id_1]
        score_2 = top_n_doc_scores_2[id_2]
        print("#{}: {}[{}] --- {}[{}]".format(i, id_1, score_1, id_2, score_2))
    '''
