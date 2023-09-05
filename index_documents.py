"""
Indexer file to create inverted_index
"""
import os
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SEARCHAPI_project.settings')
django.setup()

# Import your Indexer class and Django model for documents
from Form.indexer import Indexer
from Form.models import Document, InvertedIndex
from Form.document_parser import DocumentParser


def index_documents(folder_path):
    # Create an instance of the Indexer class
    inverted_index = {}

    # Iterate through files in the folder and create Document instances
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            content = file.read()

        # Create a Document instance for each file
        document = Document(fileName=filename, fileContent=content)
        document.save()

        # Index the document using your Indexer
        document_parser = DocumentParser(document)
        indexer = Indexer(document_parser, inverted_index)
        indexer.add_document_to_index(document)

    # Now, you can save the inverted index to your database
    # Assuming you have already populated the 'InvertedIndex' model
    for term, documents in inverted_index.items():
        inverted_index_entry, created = InvertedIndex.objects.get_or_create(term=term)
        inverted_index_entry.documents.add(*documents)


if __name__ == '__main__':

    folder_path = 'C:/Users/hp/Documents/School pdf/Year 2 second/shypoet/word press/Godwin Wonah'
    # Run the indexing function when the script is executed
    index_documents(folder_path)

