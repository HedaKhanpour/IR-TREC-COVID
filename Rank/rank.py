from math import log

class Rank:

    def __init__(self, k1, b, N, avgdl):
        self.k1 = k1
        self.b = b
        self.N = N
        self.avgdl = avgdl

    def calculate_BM25_score(self, tf):
        idf = self.calculate_IDF(self.N, tf)
        total_score = (idf * ((tf * (self.k1 + 1)) / (tf + self.k1 * ((1 - self.b) + (self.b * (self.N / self.avgdl))))))
        return total_score

    def calculate_IDF(self, docSize, termSize):
        return log(((docSize - termSize + 0.5) / (termSize + 0.5)) + 1)

