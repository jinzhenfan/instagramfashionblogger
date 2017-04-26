#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 17:46:18 2017

@author: Hans
"""

import json
import pickle
import csv
import sys
from collections import Counter
from itertools import combinations

import gensim
import time
from nltk.corpus import stopwords
from gensim.models import Word2Vec
#import logging
import re
from gensim.parsing import PorterStemmer
from StemmingHelper import StemmingHelper
import pickle
import pandas as pd
    
global_stemmer = PorterStemmer()
ignored_words = stopwords.words('english')
#word_filter = lambda w: len(w) < 3 or w.lower() in ignored_words
my_corpus=[]
regex = re.compile('[^a-zA-Z]+');

model = gensim.models.Word2Vec.load('./model/my_word2vec_model')

def MatchScore(word1,word2):
    score=0;
    if word1 not in ignored_words and word2 not in ignored_words:
        stemmed_word1=StemmingHelper.stem(word1);
        stemmed_word2=StemmingHelper.stem(word2);
        if stemmed_word1 in model.vocab and stemmed_word2 in model.vocab:
            score = model.similarity(stemmed_word1, stemmed_word2)

    return score

def CommonCorpus(account1, account2):
    index1=accountALL.index(account1)
    index2=accountALL.index(account2)
    corpus1=filtered_blog_vocal[index1]
    corpus2=filtered_blog_vocal[index2]
    commonscore=0
    for word1 in corpus1:
        for word2 in corpus2:
            commonscore=commonscore+MatchScore(word1,word2)
    return commonscore
    
with open('objs_words_1325.pickle') as f:  # Python 3: open(..., 'wb')
    #pickle.dump([account, follower_counts, posts_count, blogger_words],f)
    [accountALL, follower_countsALL, posts_countALL, filtered_blog_vocal, icon] = pickle.load(f)
    
accountALL=accountALL[:50]
filtered_blog_vocal=filtered_blog_vocal[:50]
    
tag_length=[len(tag) for tag in filtered_blog_vocal]
length_count=sorted(Counter(tag_length).most_common())
nodes=[]
for account in accountALL:
    nodes.append({"id": account, "group": 1})

links=[]
for i,j in combinations(accountALL, 2):
    score=int(round(CommonCorpus(i,j),-1))    
    print i, j, score
    if score>250:
        links.append({"source": i, "target": j, "value": score/10})

data={"nodes":nodes, "links":links}


with open('cluster.json', 'w') as outfile:
    json.dump(data, outfile)
    

