from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import string


class DocumentParser:
    def __init__(self, document):
        self.document = document

    def remove_punctuation(self):
        phrase_sans_punct = ""
        for letter in self.document.fileContent:
            if letter not in string.punctuation:
                phrase_sans_punct += letter
        return phrase_sans_punct

    def parse(self):
        phrase_sans_punct = self.remove_punctuation()
        stemmer = PorterStemmer()
        stopwords = {"the", "a", "an", "and", "but", "or", "for", "nor", "on", "at", "to", "from", "by", "with", "in", "of", "am", "I", "i", "my", "our", "has", "can", "been", "have", "that", "is", "this", "isn't", "was", "that", "those", "these", "you", "me", "would"}
        tokens = word_tokenize(phrase_sans_punct)
        processed_words = [stemmer.stem(token) for token in tokens if token.lower() not in stopwords]
        word_counter = {}
        for word in processed_words:
            if word in word_counter:
                word_counter[word] += 1
            else:
                word_counter[word] = 1
        return word_counter
