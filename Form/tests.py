from django.test import TestCase
from .models import Document
from .document_parser import DocumentParser
from .query import Query
from .indexer import Indexer


class DocumentParserTestCase(TestCase):
    def setUp(self):
        # Create a test document with dummy content for testing
        doc = Document.objects.create(fileName='Test Document', fileContent="This is a test, document containing? "
                                                                            "some words, well that one for sure."
                                      , url='http://example.com')
        self.document_parser = DocumentParser(doc)

    def test_remove_punctuation(self):
        # Test if punctuation is removed correctly
        processed_content = self.document_parser.remove_punctuation("This is a test, document containing? "
                                                                    "some words, well that one for sure.")
        expected_content = 'This is a test document containing some words well that one for sure'
        self.assertEqual(processed_content, expected_content)

    def test_parse_word_count(self):
        # Test if word counting works correctly
        word_count = self.document_parser.parse()
        expected_word_count = {
            'test': 1, 'document': 1, 'contain': 1, 'some': 1, 'word': 1, 'one': 1, 'sure': 1, 'well': 1
        }
        self.assertEqual(word_count, expected_word_count)

    def test_parse_query(self):
        query = 'This is a Test Containing'
        cleaned_query = self.document_parser.parse_query(query)
        expected_cleaned_query = ['test', 'contain']
        self.assertEqual(cleaned_query, expected_cleaned_query)

    def test_add_document_to_index(self):
        # Test if the document is added to the inverted index correctly
        inverted_index = {}
        self.document_parser.add_document_to_index(inverted_index)
        # Check if the words in the document are present in the inverted index
        self.assertTrue('test' in inverted_index)
        self.assertTrue('document' in inverted_index)
        self.assertTrue('contain' in inverted_index)
        self.assertTrue('some' in inverted_index)
        self.assertTrue('word' in inverted_index)
        self.assertTrue('one' in inverted_index)
        self.assertTrue('sure' in inverted_index)
        self.assertTrue('well' in inverted_index)

        # Check if the document is correctly added to the postings list for each word
        self.assertEqual(inverted_index['test'], [('Test Document', 1)])
        self.assertEqual(inverted_index['document'], [('Test Document', 1)])
        self.assertEqual(inverted_index['contain'], [('Test Document', 1)])
        self.assertEqual(inverted_index['some'], [('Test Document', 1)])
        self.assertEqual(inverted_index['word'], [('Test Document', 1)])
        self.assertEqual(inverted_index['one'], [('Test Document', 1)])
        self.assertEqual(inverted_index['sure'], [('Test Document', 1)])
        self.assertEqual(inverted_index['well'], [('Test Document', 1)])


class DocumentModelTestCase(TestCase):
    def setUp(self):
        Document.objects.create(fileName='test_file', fileContent='Jack went up the hill to fetch', url='http://example.com')

    def test_document_title(self):
        doc = Document.objects.get(fileName='test_file')
        self.assertEqual(doc.fileName, 'test_file')

    def test_document_content(self):
        doc = Document.objects.get(fileName='test_file')
        self.assertIn('Jack went up the hill to fetch', doc.fileContent)

    def test_document_URL(self):
        doc = Document.objects.get(fileName='test_file')
        expected_url = 'http://example.com'
        self.assertEqual(doc.url, expected_url)


class IndexerTestCase(TestCase):
    def setUp(self):
        # Create test document with dummy content for testing
        doc1 = Document.objects.create(fileName='Document One', fileContent="This is the first, first, first test document containing some words.", url='http://example.com/doc1')
        doc2 = Document.objects.create(fileName='Document Two', fileContent="This is the second document with different words.", url='http://example.com/doc2')
        doc3 = Document.objects.create(fileName='Document Three', fileContent="This is the third document with more words. God", url='http://example.com/doc3')

        # Create an empty dictionary for the inverted index
        self.inverted_index = {}
        # Create an instance of the DocumentParser and Indexer
        self.document_parser1 = DocumentParser(doc1)
        self.document_parser2 = DocumentParser(doc2)
        self.document_parser3 = DocumentParser(doc3)
        self.indexer = Indexer(self.document_parser1, self.inverted_index)
        # Add the documents to the inverted index
        self.indexer.add_document_to_index(doc1)
        self.indexer.add_document_to_index(doc2)
        self.indexer.add_document_to_index(doc3)

    def test_add_document_to_index(self):
        # Test if documents are added to the inverted index correctly
        self.assertTrue('test' in self.inverted_index)
        self.assertTrue('document' in self.inverted_index)

        # Check the content of the inverted index for "test"
        test_postings_list = self.inverted_index['first']
        print(test_postings_list)
        self.assertEqual(len(test_postings_list), 3)
        self.assertEqual(test_postings_list[0][0], 'Document One')  # Document name
        self.assertEqual(test_postings_list[0][1], 1)  # Term freq

        # Check the content of the inverted index for 'document'
        document_postings_list = self.inverted_index['document']
        self.assertEqual(len(document_postings_list), 3)

        doc1_posting = next((posting for posting in document_postings_list if posting[0] == 'Document One'), None)
        doc2_posting = next((posting for posting in document_postings_list if posting[0] == 'Document Two'), None)
        doc3_posting = next((posting for posting in document_postings_list if posting[0] == 'Document Three'), None)

        self.assertIsNotNone(doc1_posting)
        self.assertIsNotNone(doc2_posting)
        self.assertIsNotNone(doc3_posting)

        self.assertEqual(doc1_posting[1], 1)  # Term frequency for Document One
        self.assertEqual(doc2_posting[1], 1)  # Term frequency for Document Two
        self.assertEqual(doc2_posting[1], 1)  # Tern frequency for Document Three

    def test_get_total_documents(self):
        # Test if get_total_documents returns the correct total number of documents
        total_docs = self.indexer.get_total_documents()
        self.assertEqual(total_docs, 3)

    def test_get_document_frequency(self):
        # Test if get_document_frequency returns the correct document frequency
        doc_freq = self.indexer.get_document_frequency('word')
        self.assertEqual(doc_freq, 3)

    def test_get_term_frequency(self):
        # Test if get_term_frequency returns the correct term frequency
        term_freq = self.indexer.get_term_frequency('God', 'Document Three')
        self.assertEqual(term_freq, 1)

    def test_search_index(self):
        # Test if search_index returns the correct set of documents
        query = "first containing"  # Query with terms that should match doc1
        result_docs = self.indexer.search_index(query)

        expected_docs = {'Document One'}  # Expected result documents
        self.assertEqual(result_docs, expected_docs)

        query = "second"  # Query with a term that should match doc2
        result_docs = self.indexer.search_index(query)

        expected_docs = {'Document Two'}  # Expected result documents
        self.assertEqual(result_docs, expected_docs)

        query = "nonexistent"  # Query with a term that should not match any documents
        result_docs = self.indexer.search_index(query)

        expected_docs = set()  # No expected result documents
        self.assertEqual(result_docs, expected_docs)


class QueryTestCase(TestCase):
    def setUp(self):
        # Create a test document with dummy content for testing
        doc1 = Document.objects.create(fileName='Document One', fileContent="This is the first document containing some words.", url='http://example.com/doc1')
        doc2 = Document.objects.create(fileName='Document Two', fileContent="This is the second document with different words.", url='http://example.com/doc2')
        inverted_index = {}  # Create an empty dictionary for the inverted index
        self.indexer = Indexer(DocumentParser(doc1))
        self.indexer.add_document_to_index(doc1)
        self.indexer.add_document_to_index(doc2)
        self.query = Query(self.indexer)

    def test_expand_query(self):
        # Test if the query is expanded with synonyms
        self.query.set_query("test document")
        self.query.expand_query()
        self.assertEqual(self.query.query, "test document trial trial_run tryout mental_test mental_testing psychometric_test examination exam trial trial run prove try try_out examine essay screen quiz written_document papers text_file")

    def test_set_query(self):
        # Set a query using set_query method
        self.query.set_query("First Document")

        # Check if the query has been stemmed and lowercased correctly
        self.assertEqual(self.query.query, "first document")

        # Check if stemming and lowercasing was applied to each individual word
        query_words = self.query.query.split()
        expected_stemmed_words = ['first', 'document']
        self.assertEqual(query_words, expected_stemmed_words)

