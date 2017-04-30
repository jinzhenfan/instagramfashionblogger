#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 15:27:25 2017

@author: Hans
"""
        
import csv

with open('visual1.csv', 'wb') as outcsv:
    writer = csv.DictWriter(outcsv, fieldnames = ["ID", "followers", "posts","avatar","max_comments","min_comments", "mean_comments", "max_likes", "min_likes", "mean_likes"])
    writer.writeheader()

    with open('Follower_Posts_Nums_Comments_Likes_1.csv', 'rb') as incsv:
        reader = csv.reader(incsv)
        writer.writerows({"ID": row[0], 'followers': row[1], 'posts': row[2], \
        "avatar": row[3],"max_comments": row[4],"min_comments":row[5], "mean_comments":row[6], "max_likes":row[7], "min_likes":row[8], "mean_likes":row[9]} for row in reader)

