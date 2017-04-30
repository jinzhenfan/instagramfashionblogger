# -*- coding: utf-8 -*-
"""
Created on Sat Feb 04 19:55:16 2017

@author: Jinzhen Fan
"""

from nltk.corpus import wordnet as wn
dog = wn.synset('father');
cat = wn.synset('serious')
print dog.path_similarity(cat);