from Index.term import *
from search_system import *
'''
query = "this is a apple and this is a pear"
p = processQuery(query)
for b in p:
    t = getTerm(b, path="../dataComplete_2020-07-16/")
    print(t.term)
'''
count_documents("../cord-19_2020-07-16/metadata.csv")