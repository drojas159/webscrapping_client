from navigate.models import *
from analyze.models import *

def main():
    split_words()

def remove_special_caracters(word):
    list=[',','.',' ','?', '!',':',')','(','\'','"'] 
    word="".join(i for i in word if i not in list) 
    return word

def split_words():
    try:
        comment = Comment.objects.filter(is_reviewed = False)
        for c in comment:
            splitted_comment=c.text.split()
            order = 0
            for sc in splitted_comment:
                word = sc.lower()
                word = remove_special_caracters(word)
                w = Word(word = word )
                w.save_word()
                word_from_db = Word.objects.get(word=w.word)
                word_in_comment = WordInComment(word = word_from_db, comment=c, order= order)
                word_in_comment.save()
                order += 1
                c.is_reviewed = True
                c.save()
                
    except Exception as e:
        print(e)