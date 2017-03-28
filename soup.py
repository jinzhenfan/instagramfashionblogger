# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 22:54:42 2017

@author: Jinzhen Fan
"""
import urllib2
import re
import numpy as np
import sys
import pandas as pd
from bs4 import BeautifulSoup


#Read in the url lists scrapped from google search results "instagram fashion blogger"
sys.path.append("E:\Program_Files\incubator\challenge\fashionblogger")
#df=pd.read_csv('googlesearchlinks.csv',sep='\t',header=0)
df=pd.read_csv('googlesearchlinks.csv',sep=',',header=None)

flag=0;
bloggerList=[];
for i in range(len(df.index)):
    links=df.iloc[i,1];
    #page = urllib2.urlopen(links);
    #print soup.prettify();
    #add header to avoid HTTP bad request
    try:
        req = urllib2.Request(links);
        req.add_unredirected_header('User-Agent', 'Custom User-Agent');
        page=urllib2.urlopen(req);
        soup = BeautifulSoup(page);
        #scrap for instagram accountss starting with @
        for tag in soup.find_all(string=re.compile("^@")):
            #Character Limit on Instagram Usernames- 30 symbols. Username must 
            #contains only letters, numbers, periods and underscores
            if len(tag)<=30 and re.match('^@+[A-Za-z0-9_.]+$', tag)!=None:
                if str(tag) not in bloggerList:
                    print(tag);
                    bloggerList.append(str(tag));
    except urllib2.HTTPError:
        flag=1;
        
#write blogger accounts in to a summary file
with open('bloggerList.csv', 'w') as f:
    for account in bloggerList:
            f.writelines(account+'\n');

