# Generated by Django 4.0.3 on 2022-06-02 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0005_alter_word_word'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='count',
            field=models.IntegerField(default=1, null=True),
        ),
    ]