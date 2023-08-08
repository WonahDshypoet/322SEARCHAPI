class Indexer:
    def __init__(self, document_parser, inverted_index=None):
        self.document_parser = document_parser
        if inverted_index is None:
            self.inverted_index = {}
        else:
            self.inverted_index = inverted_index

    def add_document_to_index(self, document):
        """
        Add a document to the inverted index.
        """
        word_count = self.document_parser.parse()
        for word, count in word_count.items():
            if word in self.inverted_index:
                self.inverted_index[word].append((document.fileName, count))
            else:
                self.inverted_index[word] = [(document.fileName, count)]

    def remove_document_from_index(self, document):
        """
        Remove a document from the inverted index.
        """
        word_count = self.document_parser.parse()
        for word, count in word_count.items():
            postings_list = self.inverted_index[word]
            postings_list = [(doc_id, freq) for doc_id, freq in postings_list if doc_id != document.fileName]
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

    def get_term_frequency(self, term, document_id):
        """
        Get the term frequency of a term in a specific document.
        """
        if term in self.inverted_index:
            postings_list = self.inverted_index[term]
            for doc_id, freq in postings_list:
                if doc_id == document_id:
                    return freq
        return 0

    def get_document_frequency(self, term):
        """
        Get the document frequency of a term (number of documents containing the term).
        """
        if term in self.inverted_index:
            return len(self.inverted_index[term])
        return 0

    def get_total_documents(self):
        """
        Get the total number of documents in the inverted index.
        """
        return len(set(doc_id for postings_list in self.inverted_index.values() for doc_id, _ in postings_list))

