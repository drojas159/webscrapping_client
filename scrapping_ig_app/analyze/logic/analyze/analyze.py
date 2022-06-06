from ...models import *
from navigate.models import *

def get_words ():
    comments = Comment.objects.all() 
    for c in comments:
        vector = c.split()
        for v in vector:
            word = Word(word=v,word_type=)

get_words()