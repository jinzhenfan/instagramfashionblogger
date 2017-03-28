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
df=pd.read_csv('Follower_avg_Likes_0.csv',sep=',',header=None)


with open('translator0_names.txt', 'w') as f:
    for i in range(len(df.index)):
        f.write("["+str(df.iloc[i,1])+', '+str(df.iloc[i,2])+']'+', ');