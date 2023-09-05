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
        # Add a document to the inverted index.
        """
        word_count = self.document_parser.parse()
        for word, count in word_count.items():
            # Get or create the Word model instance for this word
            word_instance, created = Word.objects.get_or_create(word=word)

            # Get or create the InvertedIndex instance for this word
            inverted_index, created = InvertedIndex.objects.get_or_create(term=word_instance)

            # Add the document to the documents field of InvertedIndex
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
        # Get the existing terms in the index for this document
        existing_terms = set(self.inverted_index.keys())

        # Parse the updated document content
        updated_word_count = self.document_parser.parse()

        for word, updated_count in updated_word_count.items():
            # Check if the word is already in the index
            if word in self.inverted_index:
                postings_list = self.inverted_index[word]
                # Find the posting entry for this document
                for i, (doc_id, freq, positions) in enumerate(postings_list):
                    if doc_id == document.id:
                        # Update the frequency and positions for this document
                        postings_list[i] = (doc_id, updated_count, positions)
                        break
                else:
                    # If the document is not in the posting list, add it
                    postings_list.append((document.id, updated_count, []))
            else:
                # If the word is not in the index, create a new postings list
                self.inverted_index[word] = [(document.id, updated_count, [])]

        # Remove terms that are no longer in the document
        removed_terms = existing_terms - set(updated_word_count.keys())
        for word in removed_terms:
            del self.inverted_index[word]

    def search_index(self, query):
        """
        Search the inverted index for documents that match the query.
        """
        query_terms = self.document_parser.parse_query(query)
        result_docs = {}  # Use a dictionary to store positions for each document
        for term in query_terms:
            if term in self.inverted_index:
                postings_list = self.inverted_index[term]
                for doc_info in postings_list:
                    doc_name = doc_info['fileName']
                    positions = doc_info['positions']
                    if doc_name not in result_docs:
                        result_docs[doc_name] = positions
                    else:
                        result_docs[doc_name].extend(positions)  # Extend positions list
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



