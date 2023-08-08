from .models import Document  # Import your Document model from the models.py file


class DBRepository:
    def insert_document(self, num, fileName, fileContent, documentUrl):
        """
        Insert a new document into the database.
        """
        document = Document(num=num, fileName=fileName, fileContent=fileContent, documentUrl=documentUrl)
        document.save()

    def update_document(self, document_id, data):
        """
        Update an existing document in the database.
        """
        try:
            document = Document.objects.get(id=document_id)
            for key, value in data.items():
                if hasattr(document, key):
                    setattr(document, key, value)
            document.save()
            return True  # Return True to indicate successful update
        except Document.DoesNotExist:
            return False

    def delete_document(self, document_id):
        """
        Delete a document from the database.
        """
        Document.objects.filter(id=document_id).delete()

    def get_document_by_id(self, document_id):
        """
        Get a document by its ID from the database.
        """
        try:
            document = Document.objects.get(id=document_id)
            return document
        except Document.DoesNotExist:
            return None
