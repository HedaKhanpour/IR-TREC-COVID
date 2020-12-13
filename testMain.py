from Index.term import *

query = "this is a apple and this is a pear"
p = processQuery(query)
for b in p:
    t = getTerm(b, path="../dataComplete_2020-07-16/")
    print(t.term)