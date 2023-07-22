from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=100)

    def __str__(self):
        return self.word

class SearchResult(models.Model):
    tern = models.ForeignKey(Word, on_delete=models.CASCADE())
    doc_path = models.URLField(null=False)
    relevanceScore = models.IntegerField()

    def __init__(self):
        return f"(self.doc_path.URLField) - {self.relevanceScore}"


