from django.test import TestCase
from .models import Document


class DocumentModelTestCase(TestCase):
    def setUp(self):
        Document.objects.create(num=1, fileName='test_file', fileContent='Jack went up the hill to fetch', documentUrl='file:///C:/Users/hp/Documents/School%20pdf/Year%202%20second/shypoet/word%20press/Godwin%20Wonah/Day%201.txt')

    def test_document_title(self):
        doc = Document.objects.get(num=1)
        self.assertEqual(doc.fileName, 'test_file')

    def test_document_content(self):
        doc = Document.objects.get(num=1)
        self.assertIn('Jack went up the hill to ', doc.fileContent)

    def test_document_URL(self):
        doc = Document.objects.get(num=1)
        self.assertIn('file:///C:/Users/hp/Documents/School%20pdf/Year%202%20second/shypoet/word%20press/Godwin%20Wonah/Day%201.txt', doc.documentUrl)
