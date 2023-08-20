from django.db import models


class Document(models.Model):
    fileName = models.CharField(max_length=255)
    fileContent = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.fileName


class Word(models.Model):
    word = models.CharField(max_length=50)

    def __str__(self):
        return self.word


class Docinfo(models.Model):
    term = models.ForeignKey(Word, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=5)
    doc_path = models.CharField(max_length=30)
    # snippet = models.CharField(max_length=126)

    def __str__(self):
        return self.doc_path
