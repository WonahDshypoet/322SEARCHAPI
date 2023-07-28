from django.test import TestCase
from .models import Document
from .document_parser import DocumentParser


class DocumentParserTestCase(TestCase):
    def setUp(self):
        # Create a test document with dummy content for testing
        doc = Document.objects.create(fileName='Test Document', fileContent="This is a test, document containing? some words, well that one for sure.", url='http://example.com')
        self.document_parser = DocumentParser(doc)

    def test_remove_punctuation(self):
        # Test if punctuation is removed correctly
        processed_content = self.document_parser.remove_punctuation()
        expected_content = 'This is a test document containing some words well that one for sure'
        self.assertEqual(processed_content, expected_content)

    def test_parse_word_count(self):
        # Test if word counting works correctly
        word_count = self.document_parser.parse()
        expected_word_count = {
            'test': 1, 'document': 1, 'contain': 1, 'some': 1, 'word': 1, 'one': 1, 'sure': 1, 'well': 1
        }
        self.assertEqual(word_count, expected_word_count)


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
