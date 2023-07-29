from .document_parser import DocumentParser


class indexer:
    def __init__(self, document_parser, db_repository):
        self.document_parser = document_parser
        self.db_repository = db_repository
        self.inverted_index = {}

    def add_document_to_index(self, document):
        """
        Add a document to the inverted index.
        """
        word_count = self.document_parser.parse(document)
        for word, count in word_count.items():
            self.inverted_index[word].append((document.fileName, count))

    def remove_document_from_index(self, document):
        """
        Remove a document from the inverted index.
        """
        word_count = self.document_parser.parse(document)
        for word, count in word_count.items():
            postings_list = self.inverted_index[word]
            postings_list = [(doc_id, freq) for doc_id, freq in postings_list if doc_id != document.id]
            self.inverted_index[word] = postings_list

    def update_document_in_index(self, document):
        """
        Update the inverted index after a document is modified.
        """
        self.remove_document_from_index(document)
        self.add_document_to_index(document)

    def search_index(self, query):
        """
        Search the inverted index for documents that match the query.
        """
        query_terms = self.document_parser.parse_query(query)
        result_docs = set()
        for term in query_terms:
            if term in self.inverted_index:
                postings_list = self.inverted_index[term]
                result_docs.update(doc_id for doc_id, _ in postings_list)
        return result_docs

"""
Bruh You havent done shii in this yet just copy and paste
"""