# Generated by Django 3.2.20 on 2023-07-23 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Form', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='document',
            name='num',
        ),
        migrations.DeleteModel(
            name='SearchResult',
        ),
    ]