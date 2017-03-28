# -*- coding: utf-8 -*-
"""
Created on Sat Feb 04 23:24:24 2017

@author: Jinzhen Fan
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Feb 04 16:17:41 2017

@author: Jinzhen Fan
Input your favorite brand name, occasions, or styles, and we will recommend best matched
popular fashion blogger to follow.
"""

import fashion_blogger_tags
import gensim
#fbt=fashion_blogger_tags.fashion_blogger_tags();
# 12331 tags

#word2vec, deeplearning model
from gensim.models import word2vec
import logging
import re
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#sentences = word2vec.Text8Corpus('text8')
#model = word2vec.Word2Vec(sentences, size=200)
#'title' denotes the exact title of the article to be fetched
title = "Machine learning"
from wikipedia import page
wikipage = page(title)
from wikipedia import search, page
titles = search('machine learning')
wikipage = page(titles[0])
from gensim.parsing import PorterStemmer
global_stemmer = PorterStemmer()
from StemmingHelper import StemmingHelper
            
from gensim.models import Word2Vec
min_count = 2
size = 50
window = 4
list_sentences=wikipage.content.split('.')
print list_sentences
regex = re.compile('[^a-zA-Z]+');
sentences=[]
for raw_sentences in list_sentences:
    alphanum=[StemmingHelper.stem(str(regex.sub('', word))) for word in raw_sentences.split()];
    sentences.append(alphanum);
#sentences=[StemmingHelper.stem(item) for item in alphanum]
print sentences
model = Word2Vec(sentences, min_count=min_count, size=size, window=window)
print model[StemmingHelper.stem('machine')]
print model.similarity(StemmingHelper.stem('machine'), StemmingHelper.stem('course'))
print model.similarity(StemmingHelper.stem('learning'), StemmingHelper.stem('course'))