import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SEARCHAPI_project.settings')

import django
django.setup()
from .models import Document


def populate():
    Documents = [{
        "num": '1',
        "fileName": 'Day 1',
        "fileContent": "Finesse, if I broke na my business",
        "documentUrl": "C:\Users\hp\Documents\School pdf\Year 2 second\shypoet\word press\Godwin Wonah"
    },
        {
            "num": '2',
            "fileName": 'Day 1',
            "fileContent": "seems I be Mr Money with the vibes right now",
            "documentUrl": 'C/:\Users\hp\Documents\School pdf\Year 2 second\shypoet\word press\Godwin Wonah'
        }]

if __name__ == '__main__':
     print("Starting SEARCHAPI population script...")
     populate()
