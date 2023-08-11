from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import string


class DocumentParser:
    def __init__(self, document):
        self.document = document

    def remove_punctuation(self, input_string):
        phrase_sans_punct = ""
        for letter in input_string:
            if letter not in string.punctuation:
                phrase_sans_punct += letter
        return phrase_sans_punct

    def parse(self):
        phrase_sans_punct = self.remove_punctuation(self.document.fileContent)
        stemmer = PorterStemmer()
        stopwords = {"the", "a", "an", "and", "but", "or", "for", "nor", "on", "at", "to", "from", "by", "with", "in",
                     "of", "am", "i", "my", "our", "has", "can", "been", "have", "that", "is", "this", "isn't", "was",
                     "that", "those", "these", "you", "me", "would"}
        tokens = word_tokenize(phrase_sans_punct)
        processed_words = [stemmer.stem(token) for token in tokens if token.lower() not in stopwords]
        word_counter = {}
        for word in processed_words:
            if word in word_counter:
                word_counter[word] += 1
            else:
                word_counter[word] = 1
        return word_counter

    def parse_query(self, query):
        # Convert the query to lowercase for case-insensitive search
        phrase_sans_punct = self.remove_punctuation(query)
        stemmer = PorterStemmer()
        stopwords = {"the", "a", "an", "and", "but", "or", "for", "nor", "on", "at", "to", "from", "by", "with", "in",
                     "of", "am", "i", "my", "our", "has", "can", "been", "have", "that", "is", "this", "isn't", "was",
                     "that", "those", "these", "you", "me", "would"}  # Your set of stopwords
        tokens = word_tokenize(phrase_sans_punct)
        processed_words = [stemmer.stem(token) for token in tokens if token.lower() not in stopwords]
        return processed_words

    def add_document_to_index(self, inverted_index):
        """
        Add the current document to the inverted index.
        """
        word_count = self.parse()
        for word, count in word_count.items():
            if word in inverted_index:
                inverted_index[word].append((self.document.fileName, count))
            else:
                inverted_index[word] = [(self.document.fileName, count)]

    def get_word_positions(self, document, word):
        # Implement the logic to retrieve positions of the given word in the document
        # You can return a list of positions or None if not found
        positions = []
        words = self.remove_punctuation(document.fileContent).lower().split()
        for i, w in enumerate(words):
            if w == word:
                positions.append(i)
        return positions

    def search_phrase(self, phrase):
        word_count = self.parse()
        stemmed_phrase = ' '.join([word for word in word_tokenize(phrase.lower())])
        return [doc_id for doc_id in word_count if stemmed_phrase in doc_id]

    def get_index_terms(self):
        return list(self.parse().keys())
