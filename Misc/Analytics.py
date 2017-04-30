#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 14:31:06 2017

@author: Hans
"""
import pickle
import csv
import sys
from collections import Counter



with open('objs_words_1325.pickle') as f:  # Python 3: open(..., 'wb')
    #pickle.dump([account, follower_counts, posts_count, blogger_words],f)
    [accountALL, follower_countsALL, posts_countALL, filtered_blog_vocal, icon] = pickle.load(f)
    
tag_length=[len(tag) for tag in filtered_blog_vocal]
length_count=sorted(Counter(tag_length).most_common())

bin=10
result=[0]*100
    
for i,j in length_count:
    result[i/10]=result[i/10]+j
    
f = open("./static/data/visual2.csv", 'wt')
try:
    writer = csv.writer(f)
    writer.writerow( ('tag_length', 'count') )
    for i in range(100):
        writer.writerow( (i*10, result[i]) )
finally:
    f.close()


