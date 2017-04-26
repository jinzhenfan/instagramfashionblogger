# -*- coding: utf-8 -*-
"""
Created on Fri Feb 03 22:37:55 2017

@author: Jinzhen Fan
"""

import urllib2
import re
from bs4 import BeautifulSoup
#import numpy as np
#import sys
import pandas as pd
import pickle
import string
#import spacy
#from requests_futures.sessions import FuturesSession
#import enchant
#from enchant.checker import SpellChecker
import splitter
from time import sleep


#Read in the url lists scrapped from google search results "instagram fashion blogger"
#sys.path.append("E:\Program_Files\incubator\challenge\fashionblogger")
#df=pd.read_csv('googlesearchlinks.csv',sep='\t',header=0)
'''
def split_words(text):
    checker = SpellChecker("en_US", text)

    for error in checker:
        for suggestion in error.suggest():
            if error.word.replace(' ', '') == suggestion.replace(' ', ''):  # make sure the suggestion has exact same characters as error in the same order as error and without considering spaces
                                 error.replace(suggestion)
    return checker.get_text().split()
    
    #tags usually contain words without spaces, split first
'''
def fashion_blogger_tags(account):
    
    #with open('tag_corpus.csv', 'w') as f:
    links='https://www.instagram.com/'+account[1:]+'/?hl=en';
    follower_counts=0    
    posts_count=0
    #blogger_tags=[]
    blogger_words=[]
    blogger_emoji=[]
    comments=[]
    likes=[]
    icon_image=''
    flag=0
              
    try:
        req = urllib2.Request(links);
        req.add_unredirected_header('User-Agent', 'Custom User-Agent');
        '''
        proxy = "YOUR_PROXY_GOES_HERE"
        proxies = {"http":"http://%s" % proxy}
        headers={'User-agent' : 'Mozilla/5.0'}
        proxy_support = urllib2.ProxyHandler(proxies)
        opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler(debuglevel=1))
        urllib2.install_opener(opener)    
        req = urllib2.Request(links, None, headers)
        '''                        
        page=urllib2.urlopen(req);
        soup = BeautifulSoup(page,'html.parser')
        #scrap for instagram accounts          

        for tag in soup.find_all(type="text/javascript",string=re.compile("followed_by")):
            my_string_list=list(tag.children)[0].split(',')
            for string1 in my_string_list:
                string1=str(string1);
                #Find number of followers
                if ("followed_by" in string1) and ("count" in string1):
                    #print string;
                    regex = re.compile('[^0-9]');
                    follower_counts=int(regex.sub('', string1))
                    #print account[1:], int(follower_counts);                     
                #number of total posts
                if (re.match(" \"count\": .+", string1)!=None):
                    #print string;
                    #print "find media counts"
                    regex = re.compile('[^0-9]');
                    posts_count=int(regex.sub('', string1))
                    #print 'posts_count', posts_count;
        #Find links of account image
        for icon in soup.find_all(property="og:image"):
            icon_image= icon['content'];
            #print icon_image;        

        #Define statistics for each blogger

        if posts_count>0:
            
            #Find statistics of first 12 posts             
            for content in soup.find_all(type="text/javascript", string=re.compile("caption")):       
                for post in list(content.children):
                    text=post.split(',')
                    for attributes in text: 
                        attributes=str(attributes)
                        # Find captions of all posts of a particular blogger
                        if (re.match(" \"caption\".+", attributes)!=None):
                            post_content= attributes[12:].replace('\\n',' ')
                            post_content= post_content.replace('#',' ')
                            #print post_content
                            #print post_content;
                            #remove punctuation
                            word_list=post_content.translate(None, string.punctuation).split(" ")
                            word_list=[word for word in word_list if len(word)!=0]
                            #blogger_corpus=blogger_corpus+word_list
                            #Find tags in each caption. 
                            for tag in word_list:
                                #original tags
                                '''
                                if (re.match("#[a-zA-Z]+$", tag)!=None):
                                    print tag
                                    Split_tag=splitter.split(tag)
                                    blogger_tags=blogger_tags+Split_tag
                                    print("# : ", Split_tag)
                                '''
                                #find all words in posts
                                if (re.match("^[a-zA-Z]+$", tag)!=None):
                                    #print tag;
                                    
                                    Split_word=splitter.split(tag.lower())                                      
                                    #print Split_word;            
                                    #Remove all string with length=1.
                                    if type(Split_word)==list:
                                        Split_word=filter(lambda a: len(a) !=1 , Split_word) 
                                        blogger_words=blogger_words+Split_word
                                    else:                                          
                                        blogger_words.append(tag.lower())
                                    #print(Split_word)
                                                                                  
                            #Find emoji in each caption.
                            for word in post_content.split(" "):
                                emoji = re.compile('\\\\u[0-9a-z]{4}');
                                emoji_list=emoji.findall(word)
                                if (emoji_list!=[]):
                                    #print emoji_list;
                                    flag=2;
                                blogger_emoji=blogger_emoji+emoji_list;
                        #Find comment counts of this post
                        if (re.match(" \"comments\".+", attributes)!=None):
                            regex = re.compile('[^0-9]');
                            comment_counts=regex.sub('', attributes)
                            #print comment_counts; 
                            if comment_counts=='': 
                                comments.append(0)
                            else: comments.append(int(comment_counts))

                        #Find likes count of this post
                        if (re.match(" \"likes\".+", attributes)!=None):
                            regex = re.compile('[^0-9]');
                            like_counts=regex.sub('', attributes)
                            #print like_counts; 
                            if like_counts=='': 
                                likes.append(0)
                            else: likes.append(int(like_counts))


        """
            if comments!=[] and likes!=[]: # filter out private mode blogs
                
                f.writelines(account[1:]+','+ follower_counts +','+str(posts_count)+','+icon_image+','+
                str(np.max(comments))+','+str(np.min(comments))+','+str(np.mean(comments))+','+
                str(np.max(likes))+','+str(np.min(likes))+','+str(np.mean(likes))+'\n');
                """
        
        
        #f.writelines(account[1:]+','+ follower_counts +','+ posts_count +','+icon_image+','+'\n');
        
    except: #urllib2.HTTPError:
        flag=1
        pass
        

    return account, follower_counts, posts_count, blogger_words
    #account, follower_counts, posts_count, blogger_words, blogger_emoji, comments, likes, icon_image, flag



df=pd.read_csv('bloggerList.csv',sep=',',header=None)    

accountALL=[]
follower_countsALL=[]
posts_countALL=[]
blogger_wordsALL=[]
blogger_emojiALL=[]
commentsALL=[]
likesALL=[]
icon_imageALL=[]
flagALL=[]

        
for i in range(1000, len(df.index)):   
    account=df.iloc[i,0].lower()
    print i, account
    account, follower_counts, posts_count, blogger_words =fashion_blogger_tags(account)
    #984,1086 took long time.
    accountALL.append(account)
    follower_countsALL.append(follower_counts)
    posts_countALL.append(posts_count)
    blogger_wordsALL.append(blogger_words)
    #blogger_emojiALL.append(blogger_emoji)
    #commentsALL.append(comments)
    #likesALL.append(likes)
    #icon_imageALL.append(icon_image)
    #flagALL.append(flag)
    sleep(0.1)

with open('objs_words_last500.pickle', 'w') as f:  # Python 3: open(..., 'wb')
    #pickle.dump([account, follower_counts, posts_count, blogger_words],f)
    pickle.dump([accountALL, follower_countsALL, posts_countALL, blogger_wordsALL],f)
        #blogger_emojiALL, commentsALL, likesALL, icon_imageALL, flagALL], f)
'''
with open(PIK, "wb") as f:
    pickle.dump(len(data), f)
    for value in data:
        pickle.dump(value, f)
data2 = []

with open('objs_words_2.pickle', 'r') as f:
    for _ in range(pickle.load(f)):
        data2.append(pickle.load(f))
print data2[0]
'''




#Find title corpus, classification, and make recommendations, highcharts.

# Find frequency of updating,php use 10 digits timestamp
#http://www.bellogroupltd.com/en/excel-tutorials/10-digit-unix-timestamp-to-date-excel-converter-tutorial