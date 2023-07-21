from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

class Query:
    def __init__(self, indexer):
        self.query = None
        self.indexer = indexer

    def set_query(self, query):
        stemmer = PorterStemmer()
        tokens = word_tokenize(query)
        stemmed_query = ' '.join([stemmer.stem(token) for token in tokens])
        self.query = stemmed_query

    def execute(self):
        return self.indexer.search_index(self.query)
        pass
