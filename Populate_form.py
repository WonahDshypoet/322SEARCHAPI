import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SEARCHAPI_project.settings')

django.setup()
from Form.models import Document


def populate(folderpath):
    files = os.listdir(folderpath)

    for filename in files:
        with open(os.path.join(folderpath, filename), 'r') as file:
            content = file.read()

        title = os.path.splitext(filename)[0]
        url = f'http:/{title}.com/'
        document = Document.objects.create(fileName=filename, fileContent=content, url=url)
        document.save()

if __name__ == '__main__':
    folder_path = 'C:/Users/hp/Documents/School pdf/Year 2 second/shypoet/word press/Godwin Wonah'
    populate(folder_path)


"""
# index_documents.py

# Import Django settings
import os
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

# Import your Indexer class and Django model for documents
from your_app.indexer import Indexer
from your_app.models import Document

def index_documents():
    # Create an instance of the Indexer class
    indexer = Indexer()

    # Iterate through documents and add them to the inverted index
    for document in Document.objects.all():
        # Assuming you have a field named 'content' in your Document model
        content = document.fileContent

        # Index the document using your Indexer
        indexer.add_document_to_index(document, fileContent)

if __name__ == '__main__':
    # Run the indexing function when the script is executed
    index_documents()

"""