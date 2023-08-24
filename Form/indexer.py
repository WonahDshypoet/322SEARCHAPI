from .models import InvertedIndex, Word


class Indexer:
    """
    Creates the inverted_index, adds to the inverted_index, removes from the inverted_index
    Updates the inverted_index, searches the inverted_index, gets total term frequency
    Gets num of docs words from query appears in, gets total document frequency
    """
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
            inverted_index, created = InvertedIndex.objects.get_or_create(term=Word.objects.get_or_create(word=word)[0])
            inverted_index.documents.add(document)

    def remove_document_from_index(self, document):
        """
        Remove a document from the inverted index.
        """
        for word in self.inverted_index.keys():
            postings_list = self.inverted_index[word]
            postings_list = [(doc_id, freq, positions) for doc_id, freq, positions in postings_list if
                             doc_id != document.id]
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
                for doc_info in postings_list:
                    result_docs.add(doc_info['fileName'])
        return result_docs

    def get_term_frequency(self, term, document_id):
        """
        Get the term frequency of a term in a specific document.
        """
        if term in self.inverted_index:
            postings_list = self.inverted_index[term]
            for doc_id, freq, position in postings_list:
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
        return len(set(
            posting['document_id'] for postings_list in self.inverted_index.values() for posting in postings_list))



