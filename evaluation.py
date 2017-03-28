# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 22:59:14 2017

@author: Jinzhen Fan
"""

import sys
sys.path.append("E:\Program_Files\incubator\challenge\fashionblogger")
print ("Retrieving all tags...")
import nltk
from nltk.corpus import stopwords, webtext
from nltk.metrics import BigramAssocMeasures, spearman_correlation, ranks_from_scores
import gensim

from gensim.models import Word2Vec
import logging
import re
from gensim.parsing import PorterStemmer
from StemmingHelper import StemmingHelper

global_stemmer = PorterStemmer()
ignored_words = stopwords.words('english')
word_filter = lambda w: len(w) < 3 or w.lower() in ignored_words
my_corpus=[]
regex = re.compile('[^a-zA-Z]+');


print ("Importing webtext corpus...")
#Get corpus from webtext in sentence format
for file in webtext.fileids():
    my_sentences=[]
    for sentences in webtext.sents(file):
        words = [StemmingHelper.stem(str(regex.sub('', word))).lower() for word in sentences 
        if StemmingHelper.stem(str(regex.sub('', word))).lower()!='']
        #print words
        my_sentences.append(words)
    my_corpus=my_corpus+my_sentences
#print my_corpus
#Model parameter setting
min_count = 2 #0-100count smaller than this is not of interest
size = 200 #tens to hundreds, size of neural network layer, bigger size lead to better model, more training data
window = 4
#train the word2vec model with webtext corpus

model0 = Word2Vec(my_corpus, min_count=min_count, size=size, window=window, iter=1)
model1 = Word2Vec(my_corpus, min_count=min_count, size=size, window=window, iter=5)
model2= Word2Vec(my_corpus, min_count=min_count, size=size, window=window, iter=10)
model3 = Word2Vec(my_corpus, min_count=min_count, size=size, window=window, iter=20)
model4 = Word2Vec(my_corpus, min_count=min_count, size=size, window=window, iter=50)
model5 = Word2Vec(my_corpus, min_count=min_count, size=size, window=window, iter=80)
model6 = Word2Vec(my_corpus, min_count=min_count, size=size, window=window, iter=100)
model7 = Word2Vec(my_corpus, min_count=min_count, size=size, window=window, iter=150)
model8 = Word2Vec(my_corpus, min_count=min_count, size=size, window=window, iter=200)
model9 = Word2Vec(my_corpus, min_count=min_count, size=size, window=window, iter=250)
model10 = Word2Vec(my_corpus, min_count=min_count, size=size, window=window, iter=300)
#default iteration is 5, must be larger than 2. First iteration is to collect frequency.
#Some demo of this model


#new_model = gensim.models.Word2Vec.load('/model/my_word2vec_model')
"""
model1= Word2Vec(my_corpus, min_count=min_count, size=5, window=window, iter=100)
model2= Word2Vec(my_corpus, min_count=min_count, size=10, window=window, iter=100)
model4= Word2Vec(my_corpus, min_count=min_count, size=25, window=window, iter=100)
model5= Word2Vec(my_corpus, min_count=min_count, size=50, window=window, iter=100)
model6= Word2Vec(my_corpus, min_count=min_count, size=100, window=window, iter=100)
model7= Word2Vec(my_corpus, min_count=min_count, size=150, window=window, iter=100)
model8= Word2Vec(my_corpus, min_count=min_count, size=200, window=window, iter=100)
model9= Word2Vec(my_corpus, min_count=min_count, size=250, window=window, iter=100)
model10= Word2Vec(my_corpus, min_count=min_count, size=300, window=window, iter=100)
"""
model8.save('./model/my_word2vec_model')
def w2v_model_accuracy(model):

    accuracy = model.accuracy('evaluation.txt')
    
    sum_corr = len(accuracy[-1]['correct'])
    sum_incorr = len(accuracy[-1]['incorrect'])
    total = sum_corr + sum_incorr
    percent = lambda a: a *1.0/ total * 100
    
    print('Total sentences: {}, Correct: {:.2f}%, Incorrect: {:.2f}%'.format(total, percent(sum_corr), percent(sum_incorr)))
#evaluation
"""
w2v_model_accuracy(model3)
w2v_model_accuracy(model4)
w2v_model_accuracy(model5)
w2v_model_accuracy(model6)
"""
w2v_model_accuracy(model0)
w2v_model_accuracy(model1)
w2v_model_accuracy(model2)
w2v_model_accuracy(model3)
w2v_model_accuracy(model4)
w2v_model_accuracy(model5)
w2v_model_accuracy(model6)
w2v_model_accuracy(model7)
w2v_model_accuracy(model8)
w2v_model_accuracy(model9)
w2v_model_accuracy(model10)


print model.similarity(StemmingHelper.stem('Paris'), StemmingHelper.stem('fashion'))
print model.similarity(StemmingHelper.stem('work'), StemmingHelper.stem('fashion'))
