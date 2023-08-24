from django.contrib import admin
from .models import Document, Word, InvertedIndex


admin.site.register(Document)
admin.site.register(Word)
admin.site.register(InvertedIndex)

