#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 22:01:57 2017

@author: Hans
"""
import pickle
with open('objs_words_first500.pickle') as f1:  # Python 3: open(..., 'rb')
    #account_name, fbt = 
    accountALL1, follower_countsALL1, posts_countALL1, blogger_wordsALL1 = pickle.load(f1)

with open('objs_words_middle500.pickle') as f2:  # Python 3: open(..., 'rb')
    #account_name, fbt = 
    accountALL2, follower_countsALL2, posts_countALL2, blogger_wordsALL2 = pickle.load(f2)

with open('objs_words_last500.pickle') as f3:  # Python 3: open(..., 'rb')
    #account_name, fbt = 
    accountALL3, follower_countsALL3, posts_countALL3, blogger_wordsALL3 = pickle.load(f3)
           
accountALL=accountALL1+accountALL2+accountALL3
follower_countsALL=follower_countsALL1+follower_countsALL2+follower_countsALL3
posts_countALL=posts_countALL1+posts_countALL2+posts_countALL3
blogger_wordsALL=blogger_wordsALL1+blogger_wordsALL2+blogger_wordsALL3

# 0.25 million words in the corpus, truncate the top 45 most popular words
length_dist=[len(item) for item in blogger_wordsALL]

blog_vocal=[item for blogger in blogger_wordsALL for item in blogger]
from collections import Counter

#import nltk
high_freq=[i for i, j in Counter(blog_vocal).most_common(45)]
# remove top 45
filtered_blog_vocal= [filter(lambda x: len(x)>2 and x not in high_freq, item) for item in blogger_wordsALL]
mean=sum([len(item) for item in filtered_blog_vocal])/len(filtered_blog_vocal)
weight=[len(item)*1.0/mean for item in filtered_blog_vocal]

import pandas as pd
icon=[]
df=pd.read_csv('Follower_Posts_Nums_Comments_Likes_2.csv',sep=',',header=None)
for i in range(len(accountALL)):
    icon.append(df.iloc[i,3])


with open('objs_words_1325.pickle', 'w') as f:  # Python 3: open(..., 'wb')
    #pickle.dump([account, follower_counts, posts_count, blogger_words],f)
    pickle.dump([accountALL, follower_countsALL, posts_countALL, filtered_blog_vocal, icon],f)
    
