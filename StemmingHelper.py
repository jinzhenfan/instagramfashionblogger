# -*- coding: utf-8 -*-
"""
Created on Sat Feb 04 23:32:12 2017

@author: Jinzhen Fan
"""
#import fashion_blogger_tags
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

from gensim.parsing import PorterStemmer
global_stemmer = PorterStemmer()

class StemmingHelper(object):
    """
    Class to aid the stemming process - from word to stemmed form,
    and vice versa.
    The 'original' form of a stemmed word will be returned as the
    form in which its been used the most number of times in the text.
    """
 
    #This reverse lookup will remember the original forms of the stemmed
    #words
    word_lookup = {}
 
    @classmethod
    def stem(cls, word):
        """
        Stems a word and updates the reverse lookup.
        """
 
        #Stem the word
        stemmed = global_stemmer.stem(word)
 
        #Update the word lookup
        if stemmed not in cls.word_lookup:
            cls.word_lookup[stemmed] = {}
        cls.word_lookup[stemmed][word] = (
            cls.word_lookup[stemmed].get(word, 0) + 1)
 
        return stemmed
 
    @classmethod
    def original_form(cls, word):
        """
        Returns original form of a word given the stemmed version,
        as stored in the word lookup.
        """
 
        if word in cls.word_lookup:
            return max(cls.word_lookup[word].keys(),
                       key=lambda x: cls.word_lookup[word][x])
        else:
            return word