# -*- coding: utf-8 -*-
"""
Created on Sat Feb 04 00:37:41 2017

@author: Jinzhen Fan
"""

import urllib2
import re
from bs4 import BeautifulSoup
import numpy as np
import sys
import pandas as pd
#Read in the url lists scrapped from google search results "instagram fashion blogger"



links='https://www.instagram.com/'+'styleheroine'+'/?hl=en';
try:
    req = urllib2.Request(links);
    req.add_unredirected_header('User-Agent', 'Custom User-Agent');
    page=urllib2.urlopen(req);
    soup = BeautifulSoup(page,'html.parser');
#scrap for instagram accountss starting with @
#print soup.prettify();
#bad user experience using instagram api

#Find number of followers
    for tag in soup.find_all(type="text/javascript",string=re.compile("followed_by")):
        my_string_list=list(tag.children)[0].split(',');
        print my_string_list;
        for string in my_string_list:
            string=str(string);
            if ("followed_by" in string) and ("count" in string):
                #print string;
                regex = re.compile('[^0-9]');
                counts=regex.sub('', string);
                print 'styleheroine', int(counts);
            if ("media" in string) and ("count" in string):
                #print string;
                regex = re.compile('[^0-9]');
                counts=regex.sub('', string);
                print 'posts_count', int(counts);
#Find icon image
    for icon in soup.find_all(property="og:image"):
        print icon['content'];
#"media": {"count": 5521
#Find all posts 
    for content in soup.find_all(type="text/javascript", string=re.compile("caption")):

        for post in list(content.children):
            text=post.split(',');
            for attributes in text: 
                attributes=str(attributes);
                print attributes;
                # Find captions of all posts of a particular blogger
                if (re.match(" \"caption\".+", attributes)!=None):
                    post_content= attributes[12:];
                    print post_content;
                    word_list=post_content.split(' ');
                    #Find tags in each caption. 
                    for tag in word_list:
                        if (re.match("#.+", tag)!=None):
                            print tag;
                    #Find emoji in each caption.
                    for word in word_list:
                        emoji = re.compile('\\\\u[0-9a-z]{4}');
                        emoji_list=emoji.findall(word)
                        if (emoji_list!=[]):
                            print emoji_list;
                #Find comment counts of this post
                if (re.match(" \"comments\".+", attributes)!=None):
                    regex = re.compile('[^0-9]');
                    counts=regex.sub('', attributes);
                    print counts; 
                #Find likes count of this post
                if (re.match(" \"likes\".+", attributes)!=None):
                    regex = re.compile('[^0-9]');
                    counts=regex.sub('', attributes);
                    print counts; 
        
#print soup.prettify(); 
        
except urllib2.HTTPError:
    flag=1;

