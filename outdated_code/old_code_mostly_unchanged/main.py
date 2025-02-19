from old_code_mostly_unchanged.Index.index import Index
from old_code_mostly_unchanged.Rank.rank import Rank
from old_code_mostly_unchanged.Index.term import *
from operator import itemgetter


def main():

    # Modify data
    documents = ["John likes to watch movies Mary likes movies too", "Mary also likes to watch football games"]
    query = "Mary watch football"

    # Change free parameters
    k1 = 1.2
    b = 0.75

    # Document calculations
    documents_count = len(documents)
    sentence_avg = sum([len(d) for d in documents]) / documents_count
    score = Rank(k1, b, documents_count, sentence_avg)

    # Execute index once
    index = Index()
    for i in range(0, len(documents)):
        index.processDocument(documents[i], str(i))
        
    # Process query
    query_result = dict()

    terms = processQuery(query)
    for t in terms:
        d = getTerm(t, path="Index/data/")

        s = score.calculate_BM25_score(d.TF)
        
        print("\n",t)
        print(d.payloads)
        print(d.TF)
        print(s)
        
        for i in d.payloads.keys():
            if i in query_result:
                query_result[i] += s
            else:
                query_result[i] = s
    print("\nQuery result:\n")
    print(query_result)

if __name__ == "__main__":
    main()
