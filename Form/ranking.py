from math import log


class Ranking:
    def __init__(self, indexer):
        self.indexer = indexer

    def tf_idf(self, term, document_id):
        """
        Calculate the TF-IDF score for a given term in a document.
        """
        # Calculate the Term Frequency (TF) of the term in the document
        term_frequency = self.indexer.get_term_frequency(term, document_id)

        # Calculate the Document Frequency (DF) of the term
        document_frequency = self.indexer.get_document_frequency(term)

        # Calculate the Total Documents (N) in the collection
        total_documents = self.indexer.get_total_documents()

        # Calculate the IDF (Inverse Document Frequency) for the term
        idf = log(total_documents / (document_frequency + 1))

        # Calculate the TF-IDF score
        tf_idf_score = term_frequency * idf

        return tf_idf_score

    def rank_results(self, query, search_results):

        # Implement the logic to rank results
        query_terms = query.split()
        ranked_results = []

        # Get all the documents that match the query
        matched_documents = self.indexer.search_index(query)

        # Calculate TF-IDF scores for each document and sort them in descending order
        for document_id in matched_documents:
            tf_idf_sum = sum(self.tf_idf(term, document_id) for term in query_terms)
            ranked_results.append((document_id, tf_idf_sum))

        # sort the results in descending order of TF-IDF scores
        ranked_results.sort(key=lambda x: x[1], reverse=True)

        return ranked_results
