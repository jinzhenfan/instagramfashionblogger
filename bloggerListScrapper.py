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
import requests
import dill

Google_page_num=50

#url selector for each selected css block
def get_link(blk):
    link=blk.select('a')[0]['href']
    regex=re.compile('/url\?q=(http.*?)&sa=U.*')
    m=re.match(regex,link)
    if m:
        return m.groups()[0]

#css selector for each html page
def get_links(page):
    soup = BeautifulSoup(page.text,"lxml")
    blks = soup.find_all('h3',attrs={"class":"r"})#, span.field-content a.href')
    return [get_link(blk) for blk in blks]


# get instagram account names of popular fashion bloggers in search result
def get_id(google_link):
    id_set=[]
    print google_link
    try:
        review_page = requests.get(google_link)
        soup = BeautifulSoup(review_page.text,"lxml")
        #scrap for instagram accountss starting with @
        for tag in soup.find_all(string=re.compile("^@")):
            #Character Limit on Instagram Usernames- 30 symbols. Username must 
            #contains only letters, numbers, periods and underscores
            if len(tag)<=30 and re.match('^@+[A-Za-z0-9_.]+$', tag)!=None:
                #if str(tag) not in bloggerList:
                    #print(tag);
                id_set.append(tag)
        return id_set
    except urllib2.HTTPError:
        flag=1
        return id_set
  

#send request for google search result
pages_link=[]
flag=0
bloggerList=[]
for i in range(Google_page_num):
    url = "http://www.google.com/search?"
    google_page = requests.get(url, params={"start": i*10, "q":"instagram fashion blogger to follow"})
    #review link on each page
    page_link=get_links(google_page)
    #a list stores all review links
    pages_link=pages_link+page_link
    #build a list of list of bloggers
    bloggerList=bloggerList+map(lambda x: get_id(x), page_link)
    
#print page_link
dill.dump(bloggerList, open('account_in_double_list.pkd', 'w'))

    

'''
df=pd.read_csv('googlesearchlinks.csv',sep=',',header=None)


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
'''
