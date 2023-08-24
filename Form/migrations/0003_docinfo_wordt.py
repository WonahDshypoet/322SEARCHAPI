# Generated by Django 3.2.20 on 2023-08-12 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Form', '0002_auto_20230723_1656'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wordt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Docinfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_path', models.CharField(max_length=20)),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Form.word')),
            ],
        ),
    ]
