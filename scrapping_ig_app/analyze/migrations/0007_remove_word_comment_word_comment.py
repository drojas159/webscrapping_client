# Generated by Django 4.0.3 on 2022-06-02 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navigate', '0025_image_publication_publication_number_likes_and_more'),
        ('analyze', '0006_word_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='comment',
        ),
        migrations.AddField(
            model_name='word',
            name='comment',
            field=models.ManyToManyField(to='navigate.comment'),
        ),
    ]