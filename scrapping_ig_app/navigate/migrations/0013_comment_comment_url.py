# Generated by Django 4.0.3 on 2022-05-19 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navigate', '0012_remove_publication_caption_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_url',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
