from django.db import models
from navigate.models import *

class Word (models.Model):
    word  = models.CharField(max_length=500)
    word_type = models.CharField(max_length=250, blank=True)
    count = models.IntegerField(null=True, default=1)

    def save_word(self):
        if (Word.objects.filter(word=self.word).count()==0):
            self.save()
        else:
            w = Word.objects.get(word=self.word)
            w.count += 1
            w.save()

class WordInComment (models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    order = models.IntegerField(null=True, default=1)

class Clause (models.Model):
    group  = models.CharField(max_length=50)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)

class NormalizedWords (models.Model):
    word  = models.ForeignKey(Word, on_delete=models.CASCADE)
    catalog_word = models.ForeignKey(Catalog, on_delete=models.CASCADE)

    def save_normal_word(self):
        if (NormalizedWords.objects.filter(word=self.word, catalog_word=self.catalog_word ).count()==0):
            self.save()

