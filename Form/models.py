from django.db import models


class Document(models.Model):
    num = models.IntegerField()
    fileName = models.CharField(max_length=255)
    fileContent = models.TextField()
    documentUrl = models.URLField()

    def __str__(self):
        return self.fileName

class SearchResult(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    relevanceScore = models.IntegerField()

    def __init__(self):
        return f"(self.document.fileName) - {self.relevanceScore}"


