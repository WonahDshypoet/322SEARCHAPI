from django.db import models


class Document(models.Model):
    fileName = models.CharField(max_length=255)
    fileContent = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.fileName


class Word(models.Model):
    word = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.word


class InvertedIndex(models.Model):
    term = models.ForeignKey(Word, on_delete=models.CASCADE)
    documents = models.ManyToManyField(Document)

    def __str__(self):
        return str(self.term)

