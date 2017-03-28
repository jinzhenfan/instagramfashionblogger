# -*- coding: utf-8 -*-
"""
Created on Sun Feb 05 13:32:09 2017

@author: Jinzhen Fan
"""

import re
import numpy as np
import sys
import pandas as pd
#Read in the url lists scrapped from google search results "instagram fashion blogger"
sys.path.append("E:\Program_Files\incubator\challenge\fashionblogger")
#df=pd.read_csv('googlesearchlinks.csv',sep='\t',header=0)
df=pd.read_csv('MatchScore_long3.csv',sep=',',header=None)


with open('translator1.txt', 'w') as f:
    for i in range(20):
        f.write("[\'"+df.iloc[i,0]+'\', '+str(df.iloc[i,1])+']'+', ');