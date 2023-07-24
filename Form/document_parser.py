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

    def parse(self, phrase_sans_punct):
        content = phrase_sans_punct.split
        tokens = word_tokenize(content)
        stemmer = PorterStemmer()
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        stopwords = ["the", "a", "an", "and", "but", "or", "for", "nor", "on", "at", "to", "from", "by", "with", "in", "of", "am", "I", "i", "my", "our", "has", "can", "been", "have", "that", "is", "isn't", "was", "that", "those", "these", "you", "me", "would"]
        processed_words = []

        for i in stemmed_tokens:
            stemmed_tokens.sort()
            if i != stopwords:
                processed_words.append(i)

        Counter = {}
        for word in processed_words:
            Counter[word] = Counter(word, 0) + 1

        return Counter
