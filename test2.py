# -*- coding: utf-8 -*-
"""
Created on Sat Feb 04 18:11:56 2017

@author: Jinzhen Fan
"""

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

#unicode sentences
#transform into strings
for file in webtext.fileids():
    my_sentences=[]
    for sentences in webtext.sents(file):
        words = [StemmingHelper.stem(str(regex.sub('', word))).lower() for word in sentences 
        if StemmingHelper.stem(str(regex.sub('', word))).lower()!='']
        print words
        my_sentences.append(words)
    my_corpus=my_corpus+my_sentences
print my_corpus

min_count = 2
size = 50
window = 4

model = Word2Vec(my_corpus, min_count=min_count, size=size, window=window)

print model.similarity(StemmingHelper.stem('Paris'), StemmingHelper.stem('fashion'))
print model.similarity(StemmingHelper.stem('work'), StemmingHelper.stem('fashion'))


"""
sentences=[]            
for raw_sentences in list_sentences:
    alphanum=[StemmingHelper.stem(str(regex.sub('', word))) for word in raw_sentences.split()];
    sentences.append(alphanum);           
                 

    cf = nltk.collocations.BigramCollocationFinder.from_words(words)
    cf.apply_freq_filter(3)
    cf.apply_word_filter(word_filter)

    corr = spearman_correlation(ranks_from_scores(cf.score_ngrams(scorer)),
                                ranks_from_scores(cf.score_ngrams(compare_scorer)))
    print(file)
    print('\t', [' '.join(tup) for tup in cf.nbest(scorer, 15)])
    print('\t Correlation to %s: %0.4f' % (compare_scorer.__name__, corr))
#fbt=fashion_blogger_tags.fashion_blogger_tags();
# 12331 tags
#bigram_measures = nltk.collocations.BigramAssocMeasures()
#trigram_measures = nltk.collocations.TrigramAssocMeasures()

#use Web and Chat Text to train the machine learning algorithm

#finder = nltk.collocations.BigramCollocationFinder.from_words(text)
#finder.nbest(bigram_measures.pmi, 10)

#finder = nltk.collocations.TrigramCollocationFinder.from_words(nltk.corpus.genesis.words('english-web.txt'))
#finder.nbest(bigram_measures.pmi, 10)
#word2vec, deeplearning model
#scorer = BigramAssocMeasures.likelihood_ratio

#compare_scorer = BigramAssocMeasures.raw_freq

"""       
        