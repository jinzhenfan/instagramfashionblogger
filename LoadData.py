# -*- coding: utf-8 -*-
"""
Created on Mon Feb 06 00:51:04 2017

@author: Jinzhen Fan
"""
import re
import numpy as np
import sys
import pandas as pd



#Read in the url lists scrapped from google search results "instagram fashion blogger"
sys.path.append("E://Program_Files//incubator//challenge//Q2")
#df=pd.read_csv('googlesearchlinks.csv',sep='\t',header=0)
df=pd.read_csv('PartD_Prescriber_PUF_NPI_14.txt',sep='\t',header=0)