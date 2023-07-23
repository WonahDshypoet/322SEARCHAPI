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
        document = Document.objects.create(fileName=filename, fileContent='', url=url)
        document.save()

if __name__ == '__main__':
    folder_path = 'C:/Users/hp/Documents/School pdf/Year 2 second/shypoet/word press/Godwin Wonah'
    populate(folder_path)
