import re
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


class Query:
    def __init__(self, indexer):
        self.query = None
        self.indexer = indexer

    def expand_query(self):
        if not self.query:
            return
        expanded_query = self.query.split()
        for term in self.query.split():
            synsets = wordnet.synsets(term)
            for synset in synsets:
                for lemma in synset.lemmas():
                    # Only consider lemmas that are not the same as the original term
                    if lemma.name() != term:
                        expanded_query.append(lemma.name())

        # Combine the expanded terms with the original query
        self.query = ' '.join(expanded_query)

    def set_query(self, query):
        # Convert the query to lowercase for case-insensitive search
        query = query.lower()
        stemmer = PorterStemmer()
        tokens = word_tokenize(query)
        stemmed_query = ' '.join([stemmer.stem(token) for token in tokens])
        self.query = stemmed_query

    def execute(self):
        """
        Execute the search query and retrieve matching documents.
        """
        if not self.query:
            return set()  # Return an empty set if the query is not set

        query_terms = re.findall(r'"([^"]+)"|\S+', self.query)
        matching_documents = set()
        boolean_operators = {'AND', 'OR', 'NOT'}
        boolean_terms = []
        current_operator = 'AND'  # Default operator if none is specified

        for term in query_terms:
            if term.startswith('"') and term.endswith('"'):
                # Phrase search
                phrase = term[1:-1]
                matching_documents.update(self.indexer.search_phrase(phrase))
            elif term in boolean_operators:
                current_operator = term
            else:
                boolean_terms.append((current_operator, term))

        # Process the boolean terms and execute the search accordingly
        for operator, term in boolean_terms:
            if term.endswith('*'):
                # Handle wildcard query
                wildcard_term = term.replace('*', '.*')  # Replace * with regex .*
                regex_pattern = re.compile(f"^{wildcard_term}$")
                wildcard_matching_documents = set()
                for indexed_term in self.indexer.get_index_terms():
                    if regex_pattern.match(indexed_term):
                        wildcard_matching_documents.update(self.indexer.search_index(indexed_term))
                if operator == 'AND':
                    matching_documents.intersection_update(wildcard_matching_documents)
                elif operator == 'OR':
                    matching_documents.update(wildcard_matching_documents)
                elif operator == 'NOT':
                    matching_documents.difference_update(wildcard_matching_documents)
            else:
                # Normal term search
                if operator == 'AND':
                    matching_documents.intersection_update(self.indexer.search_index(term))
                elif operator == 'OR':
                    matching_documents.update(self.indexer.search_index(term))
                elif operator == 'NOT':
                    matching_documents.difference_update(self.indexer.search_index(term))

        return matching_documents
