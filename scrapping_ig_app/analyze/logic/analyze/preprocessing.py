from navigate.models import *
from analyze.models import *
import numpy as np 
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from .dataSource import *

def main():
    split_words()
    dataset=createDataset()
    return dataset

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
        normalize_words()
        #build_clauses()
        #selectComments()
    except Exception as e:
        print(e)

def normalize_words():
    try:
        parent_word = Catalog.objects.filter(parent =Catalog.objects.get(variable = 'CATALOG_WORDS'))
        for pw in parent_word:
            specific_word = Catalog.objects.filter(parent =pw)
            for sw in specific_word:    
                words = Word.objects.filter(word__startswith=sw.name[0:5])
                save_normalized_word(words , sw)        
    except Exception as e:
        print(e)

def save_normalized_word(words , sw):
    for w in words:
        normal_word = NormalizedWords(word= w, catalog_word=sw )
        normal_word.save_normal_word()

def build_clauses():
    normalized_words = NormalizedWords.objects.all().distinct('catalog_word')
    
    for nw in normalized_words:
        word_in_comment = WordInComment.objects.filter(word = nw.word).first()
        group = []
        left_neighbor_1 = WordInComment.objects.filter(comment = word_in_comment.comment, order = word_in_comment.order - 1).first()
        left_neighbor_2 = WordInComment.objects.filter(comment = word_in_comment.comment, order = word_in_comment.order - 2).first()
        right_neighbor_1 = WordInComment.objects.filter(comment = word_in_comment.comment, order = word_in_comment.order + 1).first()
        right_neighbor_2 = WordInComment.objects.filter(comment = word_in_comment.comment, order = word_in_comment.order + 2).first()

        group.append(left_neighbor_1.word.word)
        group.append(left_neighbor_2.word.word)
        group.append(word_in_comment.word.word)
        group.append(right_neighbor_1.word.word)
        group.append(right_neighbor_2.word.word)

        print(group)
        
def selectComments():
    normalized_words = NormalizedWords.objects.all().distinct('catalog_word')
    comments = []
    count= CountVectorizer()
    for nw in normalized_words:
        word_in_comment = WordInComment.objects.filter(word = nw.word).first()
        comments.append(word_in_comment.comment.text)
    
    arr = np.array(comments)
    
    bag = count.fit_transform(arr)
    print(count.vocabulary_)
    print(bag.toarray() )

def createDataset():

    dataset = get_dataset()

    df = pd.DataFrame(dataset,columns=('catalog_word_id', 'catalog_word', 'symptom','comment_text','comment_id','username','user_id') )
    arr = df.to_numpy()
    
    return arr