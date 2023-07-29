from django.db import models


class Document(models.Model):
    Id = models.IntegerField()
    fileName = models.CharField(max_length=255)
    fileContent = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.fileName


class Word(models.Model):
    word = models.CharField(max_length=100)

    def __str__(self):
        return self.word
