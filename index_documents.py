import os
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SEARCHAPI_project.settings')
django.setup()

# Import your Indexer class and Django model for documents
from Form.indexer import Indexer
from Form.models import Document, Word, InvertedIndex
from Form.document_parser import DocumentParser


def index_documents():
    # Create an instance of the Indexer class
    inverted_index = {}
    document_parser = DocumentParser(Document)
    indexer = Indexer(document_parser, inverted_index)

    print(Document.objects.all())

    # Iterate through documents and add them to the inverted index
    for document in Document.objects.all():

        # Index the document using your Indexer
        indexer.add_document_to_index(document)

if __name__ == '__main__':
    # Run the indexing function when the script is executed
    index_documents()
