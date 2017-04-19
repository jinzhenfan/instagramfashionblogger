# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 22:54:42 2017
This script generated Instagram account strings in a list of list from Google search
@author: Jinzhen Fan
"""
import urllib, urllib2
import re
import numpy as np
import sys
import pandas as pd
from bs4 import BeautifulSoup
import requests
import dill
from requests_futures.sessions import FuturesSession


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
    #print soup.prettify()
    blks = soup.find_all('h3',attrs={"class":"r"})#, span.field-content a.href')
    return [get_link(blk) for blk in blks]



# get instagram account names of popular fashion bloggers in search result
def get_id(future_get):
    id_set=[]
    try:
        soup = BeautifulSoup(future_get.result().content,"lxml")
        #scrap for instagram accountss starting with @
        #print soup.prettify()
        '''
        for tag in soup.find_all(string=re.compile("^@")):
            #Character Limit on Instagram Usernames- 30 symbols. Username must 
            #contains only letters, numbers, periods and underscores
            if len(tag)<=30 and re.match('^@+[A-Za-z0-9_.]+$', tag)!=None:
                #if str(tag) not in bloggerList:
                    #print(tag);
                id_set.append(tag)
        '''
        #print soup.prettify()
        id_set=soup.find_all(string=re.compile("^@"))
        #print id_set
        
        #print id_set
        return filter(lambda x: len(x)<=30 and re.match('^@+[A-Za-z0-9_.]+$', x), id_set)
    except:# urllib2.HTTPError:
        flag=1
        return id_set

#send request for google search result
pages_link=[]
flag=0
bloggerList=[]

for i in range(Google_page_num):
    url = "http://www.google.com/search?"
    google_page = requests.get(url, params={"start": i*10, "q":"instagram fashion blogger to follow"}, headers={'Accept-Encoding': 'identity', 'User-Agent': 'python-requests/1.2.0'}, auth=('user', 'pass'))
    #review link on each page
    page_link=get_links(google_page)
    #print page_link
    #a list stores all review links
    pages_link=pages_link+page_link
    print "page="+str(i+1)
    print page_link
    #build a list of list of bloggers
    session = FuturesSession(max_workers=5)
    futures = [session.get(url) for url in page_link]
    bloggerList=bloggerList+map(lambda x: get_id(x), futures)

#In Python, recursion is limited to 999 calls. Use iteratives instead of recurtion.
#pickle maximum recursion depth exceeded in 
flat_bloggerList=list(set([y for x in bloggerList if x for y in x if y]))

with open('bloggerList.csv', 'w') as f:
    for account in flat_bloggerList:
            f.writelines(account+'\n')
f.close()

