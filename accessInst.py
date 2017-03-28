# -*- coding: utf-8 -*-
"""
Created on Fri Feb 03 22:23:30 2017

@author: Jinzhen Fan
"""
from instagram.client import InstagramAPI
import urllib2
import re
import numpy as np
import sys
import pandas as pd

access_token = '2008495471.2f53c66.e39e6fbb7828472684d4ba6235580730'

api = InstagramAPI(client_secret='6206cb3cd63845648411869a9e1a006e', access_token = '2008495471.2f53c66.e39e6fbb7828472684d4ba6235580730')
usr = api.user_search('vivid')
# need to access public-content
print usr
my_usr = usr[0]
print 'User id is', my_usr.id, 'and name is ', my_usr.username

"""
api = InstagramAPI(client_id='2f53c661f6ed418bb7bc9483e2b29d94', client_secret='6206cb3cd63845648411869a9e1a006e')
popular_media = api.media_popular(count=20)
for media in popular_media:
    print media.images['standard_resolution'].url

recent_media, next_ = api.user_recent_media(user_id="vivid", count=10)
for media in recent_media:
   print media.caption.text
   print media.id
   likes = api.media_likes(media.id)
 
#   https://www.instagram.com/styleheroine/?hl=en
links='https://www.instagram.com/'+'styleheroine'+'/?hl=en';
req = urllib2.Request(links);
req.add_unredirected_header('User-Agent', 'Custom User-Agent');
page=urllib2.urlopen(req);
soup = BeautifulSoup(page);
#scrap for instagram accountss starting with @
for tag in soup.find_all(string=re.compile("posts$")):
    #Character Limit on Instagram Usernames- 30 symbols. Username must 
    #contains only letters, numbers, periods and underscores
    print(tag);
"""