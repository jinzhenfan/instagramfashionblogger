# -*- coding: utf-8 -*-
"""
Created on Sun Feb 05 00:13:08 2017

@author: Jinzhen Fan
"""

from __future__ import division
from collections import Counter
import re, nltk

WORDS = nltk.corpus.brown.words()#need to incorporate brand names
COUNTS = Counter(WORDS)

def pdist(counter):
    "Make a probability distribution, given evidence from a Counter."
    N = sum(counter.values())
    return lambda x: counter[x]/N

P = pdist(COUNTS)

def Pwords(words):
    "Probability of words, assuming each word is independent of others."
    return product(P(w) for w in words)

def product(nums):
    "Multiply the numbers together.  (Like `sum`, but with multiplication.)"
    result = 1
    for x in nums:
        result *= x
    return result

def splits(text, start=0, L=20):
    "Return a list of all (first, rest) pairs; start <= len(first) <= L."
    return [(text[:i], text[i:]) 
            for i in range(start, min(len(text), L)+1)]

def segment(text):
    "Return a list of words that is the most probable segmentation of text."
    if not text: 
        return []
    if len(text)>20:
        return text;
    else:
        candidates = ([first] + segment(rest) 
                      for (first, rest) in splits(text, 1))
        return max(candidates, key=Pwords)
