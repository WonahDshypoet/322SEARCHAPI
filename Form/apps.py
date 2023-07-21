from django.apps import AppConfig
import nltk


class FormConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Form'

    def ready(self):
        nltk.download('punkt')
