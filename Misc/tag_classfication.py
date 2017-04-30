# -*- coding: utf-8 -*-
"""
Created on Sat Feb 04 16:17:41 2017

@author: Jinzhen Fan
Input your favorite brand name, occasions, or styles, and we will recommend best matched
popular fashion blogger to follow.
"""
import sys
sys.path.append("E:\Program_Files\incubator\challenge\fashionblogger")
print ("Retrieving all tags...")
#import fashion_blogger_tags
#import nltk
from nltk.corpus import stopwords
#from nltk.corpus import webtext
#from nltk.metrics import BigramAssocMeasures, spearman_correlation, ranks_from_scores
import gensim

from gensim.models import Word2Vec
import logging
import re
from gensim.parsing import PorterStemmer
from StemmingHelper import StemmingHelper
import pickle
import pandas as pd


#account_name, fbt=fashion_blogger_tags.fashion_blogger_tags();

with open('objs_words.pickle') as f:  # Python 3: open(..., 'rb')
    account_name, fbt = pickle.load(f)
# 12331 tags
#25728 corpus
#306659 words
#580 fashion bloggers from 391 recommendation articles
account_set=[]

query = raw_input("Your Fashion Word? \n")
print ("Searching database...")

global_stemmer = PorterStemmer()
ignored_words = stopwords.words('english')
word_filter = lambda w: len(w) < 3 or w.lower() in ignored_words
my_corpus=[]
regex = re.compile('[^a-zA-Z]+');

"""
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
print my_corpus

#Model parameter setting
min_count = 2 #0-100count smaller than this is not of interest
size = 50 #tens to hundreds, size of neural network layer, bigger size lead to better model, more training data
window = 4
#train the word2vec model with webtext corpus
model = Word2Vec(my_corpus, min_count=min_count, size=size, window=window)
#default iteration is 5, must be larger than 2. First iteration is to collect frequency.
#Some demo of this model
"""
#model = gensim.models.Word2Vec.load_word2vec_format('./model/GoogleNews-vectors-negative300.bin', binary=True)  
"""
def w2v_model_accuracy(model):

    accuracy = model.accuracy('questions-words.txt')
    
    sum_corr = len(accuracy[-1]['correct'])
    sum_incorr = len(accuracy[-1]['incorrect'])
    total = sum_corr + sum_incorr
    percent = lambda a: a *1.0/ total * 100
    
    print('Total sentences: {}, Correct: {:.2f}%, Incorrect: {:.2f}%'.format(total, percent(sum_corr), percent(sum_incorr)))
#evaluation
w2v_model_accuracy(model)
print model.similarity(StemmingHelper.stem('Paris'), StemmingHelper.stem('fashion'))
print model.similarity(StemmingHelper.stem('work'), StemmingHelper.stem('fashion'))
#store and loading models
#model.save('/tmp/mymodel')
#new_model = gensim.models.Word2Vec.load('/tmp/mymodel')
#Get matching score of two input  words 
"""
model = gensim.models.Word2Vec.load('./model/my_word2vec_model')

def MatchScore(word1,word2):
    """
    stemmed_word1=StemmingHelper.stem(word1);
    stemmed_word2=StemmingHelper.stem(word2);
    if stemmed_word1 in model.vocab and stemmed_word2 in model.vocab:
        score = model.similarity(stemmed_word1, stemmed_word2)
    else:
        score=0;
    
    return score
    """
    score=0;
    if word1 not in ignored_words and word2 not in ignored_words:
        stemmed_word1=StemmingHelper.stem(word1);
        stemmed_word2=StemmingHelper.stem(word2);
        if stemmed_word1 in model.vocab and stemmed_word2 in model.vocab:
            score = model.similarity(stemmed_word1, stemmed_word2)

    return score
    
print ("Your matching score is:\n")

account_set=[]
with open('.\output\MatchScore'+query+'.csv', 'w') as f:
    for i in range(len(fbt)):
        if account_name[i] not in account_set: #duplciation check
            tag_group=fbt[i];
            blogger_score=[];
            if len(tag_group)>20:
                for tag in tag_group:
                    if len(tag)>1:#remove meaningless word seg
                        blogger_score=blogger_score+[MatchScore(tag,query)];
                        #if len(tag_group)>10: # scaling fact to correct bias for blogger vocabulary size
                blogger_sum=sum(blogger_score)/len(tag_group); # scaling fact to correct bias for blogger vocabulary size
                #print account_name[i], blogger_sum;
            f.writelines(account_name[i]+ ','+str(blogger_sum)+'\n');
            account_set.append(account_name[i]);
print ("Searching the database...:\n")
df = pd.read_csv('.\output\MatchScore'+query+'.csv', header=None)
#get top 3 best match
print df.sort_values(1,ascending=False).head(3)
"""
for tag_group in fbt:
    blogger_score=[];
    for tag in tag_group:
        blogger_score=blogger_score+[MatchScore(tag,query)];
    blogger_sum=sum(blogger_score);
    print blogger_sum;
"""


        