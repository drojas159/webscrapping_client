# Generated by Django 4.0.3 on 2022-05-19 04:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('navigate', '0010_public_article'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='Public',
        ),
    ]
