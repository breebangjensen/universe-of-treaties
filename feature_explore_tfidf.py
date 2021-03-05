# Looking at tf-idf
# Original code was adapted from this post: https://buhrmann.github.io/tfidf-analysis.html
# Thank you, Thomas Buhrmann
import numpy as np
import pandas as pd
import os
import re
import sys
from pathlib import Path
import matplotlib.pyplot as plt

import gensim
from gensim.parsing.preprocessing import remove_stopwords

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

# Load your data we might start with one doc to test
data = pd.read_csv('data/final_labels.csv', error_bad_lines=False) # WIP: Bree created new data 
data['content'].dtypes # check data type 
data['content'] = data['content'].astype(str) # convert to string 
data.columns

# create outcome
# y = [precision_high, obligation_high, delegation_high]
# We have a scale to work with here:
# PRECISION: 
# Mutations to make:
# 1. 'precision 1 (Y/N)' is 'Y' or 'N' we need to convert to (0,1)
# 2. 'precision 2 (1-4)' 
# 3. 'precision 4 (Y/N)' convert to (0,1)
# 'precision_high = sum of all the precision measure >= 3
# OBLIGATION:
# Mutations to make
# 1. 'obligation 1 (Y/N)' we need to convert to (0,1)
# 2. 'obligation 2 (Y/N)' we need to convert to (0,1)
# 3. 'obligation 3 (Y/N)' we need t0 convert to (0,1)
# 'obligation_high = sum of all the obligation measure >= 3
# DELEGATION:
# Mutations to make
# 1. 'delegation 1 (Y/N)' we need to convert to (0,1)
# 2. 'delegation 2 (Y/N)' we need to convert to (0,1)
# 3. 'delegation 3 (Y/N)' we need t0 convert to (0,1)
# 'delegation_high = sum of all the delegation measure >= 3

# isolate labels
precision = ['precision 1 (Y/N)', 'precision 4 (Y/N)']
obligation = ['obligation 1 (Y/N)', 'obligation 2 (Y/N)', 'obligation 3 (Y/N)', 'obligation 5 (Y/N)']
delegation = ['delegation 1 (Y/N)', 'delegation 2 (Y/N)', 'delegation 3 (Y/N)']

# create dummies and concat back to main df
precision_dummies = pd.get_dummies(data[delegation])

# create Precision dummies

#cleaning data
#probably a way to string this together better
##get rid of special characters and "accidental" punctuation
bad_characters = list("?!~﻿\/_-'[]»")

for punctuation in bad_characters:
    data['content']  = data['content'].str.replace(punctuation, "")

#get rid of multiple periods without getting rid of single periods helpful for 
#denoting sentences
data['content']= data['content'].str.replace(r"\.{2,}", "")

#Do we need to get rid of things like (a) as a list tool?
data['content']= data['content'].str.replace(r"\(\w\)", "")

#Getting rid of extra whitespace
data['content']= data['content'].str.replace(r" +", " ")

# you need to convert to lower case 
data['content'] = data['content'].str.lower() 

data['content'] = data['content'].str.replace(r"\d+", "")

# isolate the documents convert to list 
clean_documents  = data['content'].to_list()

# remove empty entries for now, are they supposed to be missing? 
clean_documents = [i for i in clean_documents if i] 

# remove stop words
doc_stop_rm = [0]* len(clean_documents)
for i, d, in enumerate(clean_documents):
    doc_stop_rm[i] = remove_stopwords(d)

# clean documents is our ffeature matrix here, we will explore what signals our words can 
# contribute, we still need to create our outcome list that corresponds to each text
# we can explore the features without the outcome for now

# when we build our model we will be using scikit-learn and specifically
# the model pipelining feature, I can go over in detail if needed 
# makes things easier to test and adjust

# Pipeline
# Here we will be using tf-idf with single and n_gram words of 2 
# when we model we will have to fine tune this for classification using something like 
# gridsearch but for now let's keep it like this for exploration purposes
model_feat = Pipeline([('vect', CountVectorizer(ngram_range=(1, 2), analyzer='word')),
    ('tfidf', TfidfTransformer(use_idf= True))
    ])

# the pipeline builder lets us add steps to our model this one is:
# 1. "vectorize" words, you do this same step in the word_count function I shared
#   but this time it creates both single and 2-word vector
# 2. get tf-idf weights using the word counts within documents

# the pipeline allows you to call these when you're modeling and inspect
# Analyse tfidf
# X_matrix is the tf-idf feature matrix, very sparse
# vec = vectorizer, we can pull thigs out of this like the vocab dictionary of corpus
# features = # you can inspect this its all the features in you potential model
X_matrix = model_feat.fit_transform(doc_stop_rm)
vec = model_feat.named_steps['vect']
features = vec.get_feature_names() 

# we can't directly manipulate the X_matrix so this is a helper function for that
def top_tfidf_feats(row, features, top_n=25):
    ''' Get top n tfidf values in row and return them with their corresponding feature names.'''
    topn_ids = np.argsort(row)[::-1][:top_n]
    top_feats = [(features[i], row[i]) for i in topn_ids]
    df = pd.DataFrame(top_feats)
    df.columns = ['feature', 'tfidf']
    return df

# Using the tf-idf matrix X take the docuement (by row_id) and give me the top tf-idf features
def top_feats_in_doc(X, features, doc_row_id, top_n=25):
    ''' Top tfidf features in specific document (matrix row) '''
    row = np.squeeze(X[doc_row_id].toarray())
    return top_tfidf_feats(row, features, top_n)

# we can inspect the first document by using doc_row_id = 1
top_feats_in_doc(X=X_matrix, doc_row_id = 1,features=features, top_n=25)

# we would prob benefit from removing stop words

# WE CAN ALSO INSPECT THE MAIN FEATURES CORPUS WIDE 
def corpus_top_mean_feats(X, features, grp_ids=None, min_tfidf=0.1, top_n=25):
    ''' Return the top n features that on average are most important amongst documents in rows
        indentified by indices in grp_ids. '''
    if grp_ids:
        D = X[grp_ids].toarray()
    else:
        D = X.toarray()

    D[D < min_tfidf] = 0
    tfidf_means = np.mean(D, axis=0)
    return top_tfidf_feats(tfidf_means, features, top_n)

corpus_top_mean_feats(X=X_matrix, features=features, grp_ids=None, min_tfidf=0.1, top_n=25)

# can def trim out some of these words to start getting better signals 

# after this we can now begin modeling! 
# Create the y outcome 
# precision, obligation, delegation [high or low][0,1]
# 1 decision with more cats (all 3) 
# This document has more indicators for precision versus some other things  
