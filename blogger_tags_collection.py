# -*- coding: utf-8 -*-
"""
Created on Fri Feb 03 22:37:55 2017

@author: Jinzhen Fan
"""
import urllib2
import re
from bs4 import BeautifulSoup
import numpy as np
import sys
import pandas as pd
#Read in the url lists scrapped from google search results "instagram fashion blogger"
sys.path.append("E:\Program_Files\incubator\challenge\fashionblogger")
#df=pd.read_csv('googlesearchlinks.csv',sep='\t',header=0)
df=pd.read_csv('bloggerList.csv',sep=',',header=None)
flag=0;
account_list=[];

def fashion_blogger_tags():
    tag_corpus=[];
    
    #with open('tag_corpus.csv', 'w') as f:
    for i in range(len(df.index)):
        #For each popular fashion blogger
        #Find the account id
        account=df.iloc[i,0].lower();
        #traslate into instagram url
        if account not in account_list:
            links='https://www.instagram.com/'+account[1:]+'/?hl=en';
            posts_count=0;
            try:
                req = urllib2.Request(links);
                req.add_unredirected_header('User-Agent', 'Custom User-Agent');
                page=urllib2.urlopen(req);
                soup = BeautifulSoup(page,'html.parser');
                #scrap for instagram accounts          
    
                for tag in soup.find_all(type="text/javascript",string=re.compile("followed_by")):
                    my_string_list=list(tag.children)[0].split(',');
                    for string in my_string_list:
                        string=str(string);
                        #Find number of followers
                        if ("followed_by" in string) and ("count" in string):
                            #print string;
                            regex = re.compile('[^0-9]');
                            follower_counts=regex.sub('', string);
                            #print account[1:], int(follower_counts);                     
                        #number of total posts
                        if (re.match(" \"count\": .+", string)!=None):
                            #print string;
                            #print "find media counts"
                            regex = re.compile('[^0-9]');
                            posts_count=int(regex.sub('', string));
                            #print 'posts_count', posts_count;
                #Find links of account image
                for icon in soup.find_all(property="og:image"):
                    icon_image= icon['content'];
                    #print icon_image;
                
    
                #Define statistics for each blogger
                blogger_corpus=[];#list of words
                blogger_tags=[];
                blogger_emoji=[];
                comments=[];
                likes=[];
                if (posts_count>0):
                    #Find statistics of first 12 posts             
                    for content in soup.find_all(type="text/javascript", string=re.compile("caption")):       
                        for post in list(content.children):
                            text=post.split(',');
                            for attributes in text: 
                                attributes=str(attributes);
                                # Find captions of all posts of a particular blogger
                                if (re.match(" \"caption\".+", attributes)!=None):
                                    post_content= attributes[12:];
                                    #print post_content;                           
                                    word_list=post_content.split(' ');
                                    blogger_corpus=blogger_corpus+word_list
                                    #Find tags in each caption. 
                                    for tag in word_list:
                                        if (re.match("#.+", tag)!=None):
                                            #print tag;
                                            blogger_tags.append(tag[1:]);
                                    #Find emoji in each caption.
                                    for word in word_list:
                                        emoji = re.compile('\\\\u[0-9a-z]{4}');
                                        emoji_list=emoji.findall(word)
                                        if (emoji_list!=[]):
                                            #print emoji_list;
                                            flag=2;
                                        blogger_emoji=blogger_emoji+emoji_list;
                                #Find comment counts of this post
                                if (re.match(" \"comments\".+", attributes)!=None):
                                    regex = re.compile('[^0-9]');
                                    comment_counts=regex.sub('', attributes);
                                    #print comment_counts; 
                                    if comment_counts=='': 
                                        comments.append(0)
                                    else: comments.append(int(comment_counts));
    
                                #Find likes count of this post
                                if (re.match(" \"likes\".+", attributes)!=None):
                                    regex = re.compile('[^0-9]');
                                    like_counts=regex.sub('', attributes);
                                    #print like_counts; 
                                    if like_counts=='': 
                                        likes.append(0)
                                    else: likes.append(int(like_counts));
                    tag_corpus.append(blogger_tags);
                    #print('\n');
                    
                    """
                    if comments!=[] and likes!=[]: # filter out private mode blogs
                        
                        f.writelines(account[1:]+','+ follower_counts +','+str(posts_count)+','+icon_image+','+
                        str(np.max(comments))+','+str(np.min(comments))+','+str(np.mean(comments))+','+
                        str(np.max(likes))+','+str(np.min(likes))+','+str(np.mean(likes))+'\n');
                        """
                
                
                #f.writelines(account[1:]+','+ follower_counts +','+ posts_count +','+icon_image+','+'\n');
                
            except urllib2.HTTPError:
                flag=1;

    return tag_corpus;

#Find title corpus, classification, and make recommendations, highcharts.

# Find frequency of updating,php use 10 digits timestamp
#http://www.bellogroupltd.com/en/excel-tutorials/10-digit-unix-timestamp-to-date-excel-converter-tutorial