# -*- coding: utf-8 -*-
"""
Created on Sat Feb 04 16:17:41 2017

@author: Jinzhen Fan
Input your favorite brand name, occasions, or styles, and we will recommend best matched
popular fashion blogger to follow.
"""
import sys
#sys.path.append("E:\Program_Files\incubator\challenge\fashionblogger")
#sys.path.append("./nltk_data/")
from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)
print ("Retrieving all tags...")
#import fashion_blogger_tags
#import nltk
from nltk.corpus import stopwords
#from nltk.corpus import webtext
#from nltk.metrics import BigramAssocMeasures, spearman_correlation, ranks_from_scores
import gensim
import time

from gensim.models import Word2Vec
#import logging
import re
from gensim.parsing import PorterStemmer
from StemmingHelper import StemmingHelper
import pickle
import pandas as pd
from flask import Flask, render_template, request, jsonify
import os.path


"""
from flask import redirect

from bokeh.io import push_notebook, show, output_notebook

from bokeh.layouts import row

from bokeh.plotting import figure

from bokeh.embed import components

from bokeh.util.string import encode_utf8

import quandl
quandl.ApiConfig.api_key = 'Bc6FchAnNSq7zxfjpZGR'
"""
#http://code.runnable.com/UiPhLHanceFYAAAP/how-to-perform-ajax-in-flask-for-python
# Initialize the Flask application

#account_name, fbt=fashion_blogger_tags.fashion_blogger_tags();
    
with open('objs_words_1325.pickle') as f:  # Python 3: open(..., 'wb')
    #pickle.dump([account, follower_counts, posts_count, blogger_words],f)
    [account_name, follower_countsALL, posts_countALL, fbt, icon] = pickle.load(f)
 
# 12331 tags
#25728 corpus
#306659 words
#580 fashion bloggers from 391 recommendation articles




global_stemmer = PorterStemmer()
ignored_words = stopwords.words('english')
#word_filter = lambda w: len(w) < 3 or w.lower() in ignored_words
my_corpus=[]
regex = re.compile('[^a-zA-Z]+');

model = gensim.models.Word2Vec.load('./model/my_word2vec_model')

def MatchScore(word1,word2):
    score=0;
    if word1 not in ignored_words and word2 not in ignored_words:
        stemmed_word1=StemmingHelper.stem(word1);
        stemmed_word2=StemmingHelper.stem(word2);
        if stemmed_word1 in model.vocab and stemmed_word2 in model.vocab:
            score = model.similarity(stemmed_word1, stemmed_word2)

    return score
    
def query_word(query):
    #query = raw_input("Your Fashion Word? \n")
    #print ("Searching database...")
    #writing matching scores in to a csv file
    account_set=[]
    file_path='./output/MatchScore'+query+'.csv'
    if os.path.exists(file_path)== False: 
        with open(file_path, 'w') as f:
            for i in range(len(account_name)):
                if account_name[i] not in account_set: #duplciation check
                    tag_group=fbt[i];
                    blogger_score=[];
                    if len(tag_group)>20:
                        for tag in tag_group:
                            #if len(tag)>1:#newly added 02/13/2017
                            blogger_score=blogger_score+[MatchScore(tag,query)];
                    #if len(tag_group)>10: # scaling fact to correct bias for blogger vocabulary size
                        blogger_sum=sum(blogger_score)/len(tag_group); # scaling fact to correct bias for blogger vocabulary size
                    #print account_name[i], blogger_sum;
                    else: blogger_sum=0
                    f.writelines(account_name[i]+ ','+str(blogger_sum)+'\n');
                    account_set.append(account_name[i])
        f.close()
    else: time.sleep(0.3)
    print ("Searching the database...:\n")
    df = pd.read_csv('./output/MatchScore'+query+'.csv', header=None)
    #get top 3 best match
    top3= df.sort_values(1,ascending=False).head(3)
    #print [top3.iloc[0,0][1:],top3.iloc[1,0][1:],top3.iloc[2,0][1:]]
    return [top3.iloc[0,0][1:],top3.iloc[1,0][1:],top3.iloc[2,0][1:]]
"""
for tag_group in fbt:
    blogger_score=[];
    for tag in tag_group:
        blogger_score=blogger_score+[MatchScore(tag,query)];
    blogger_sum=sum(blogger_score);
    print blogger_sum;
"""
app = Flask(__name__)

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/datasets')
def datasests():
    return render_template('Visual1.html')

@app.route('/hist')
def hist():
    return render_template('Visual2.html')

@app.route('/model')
def model_exp():
    return render_template('model_exp.html')

@app.route('/cluster')
def cluster():
    return render_template('Visual3.html')
# Route that will process the AJAX request, sum up two
# integer numbers (defaulted to zero) and return the
# result as a proper JSON response (Content-Type, etc.)
@app.route('/_word_input')
def word_input():
    a = request.args.get('a', 0, type=str)
    print a
    top3list=query_word(a)
    print top3list
    #return jsonify([a,'zjerrr','sherrywind'])
    return jsonify(top3list)
"""
@app.route('/graph',methods = ['POST', 'GET'])
def graph():
    data = quandl.get_table('WIKI/PRICES', ticker = 'GOOG')          
    #output_notebook()
         
    p=figure(title=a, plot_height=300, plot_width=600,x_axis_label='date',x_axis_type='datetime')
    r=p.line(data.tail(30).date,data.tail(30).close,color="#2222aa",line_width=3)
    #html = file_html(p, CDN, "my plot")
    script,div=components(p)
    html = render_template('graph.html',script=script, div=div)
    return encode_utf8(html) #render_template('index.html')
"""

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("80"),
        debug=True
    )

        
