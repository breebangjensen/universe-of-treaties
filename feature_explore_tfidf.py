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
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from sklearn.metrics import accuracy_score
# Load your data we might start with one doc to test
data = pd.read_csv('data/final_labels.csv', error_bad_lines=False) # WIP: Bree created new data 
data['content'].dtypes # check data type 
data['content'] = data['content'].astype(str) # convert to string 
data.columns

# Clean up Y
data.replace('N/a', np.nan, inplace=True)

# Replace typos with proper values by creating dict and passing to df.replace()
replace = {
    'precision 1 (Y/N)': {'n':'N', 'y':'Y'},
    'precision 4 (Y/N)': {'17':'Y', 'Y?':'Y', 'y':'Y', 'n':'N'},

    'obligation 1 (Y/N)': {'Y?':'Y', 'n':'N', 'y':'Y'},
    'obligation 2 (Y/N)': {'y':'Y'},
    'obligation 3 (Y/N)': {'Y?':'Y', 'y':'Y', 'N?':'N'},
    'obligation 5 (Y/N)': {'M':'N', 'Y?':'Y', 'y':'Y', 'n':'N'},
    
    'delegation 1 (Y/N)': {'M':'N', 'n':'N', 'y':'Y'}, 
    'delegation 2 (Y/N)': {'n':'N', 'y':'Y'}, 
    'delegation 3 (Y/N)': {'n':'N', 'y':'Y'}
}

data.replace(replace, inplace=True)

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
# OTHER NOTES: There's a page count feature

# isolate labels
precision = ['precision 1 (Y/N)', 'precision 4 (Y/N)']
obligation = ['obligation 1 (Y/N)', 'obligation 2 (Y/N)', 'obligation 3 (Y/N)', 'obligation 5 (Y/N)']
delegation = ['delegation 1 (Y/N)', 'delegation 2 (Y/N)', 'delegation 3 (Y/N)']

# Create dummies and concat back to main df
# We can choose to drop the first by setting 'drop_first=True'
# Another minor issue the 'nan' values are their own column and they are given a '0' in the 'Y' and 'N' columns totally not correct 
# We will fix after combining back thinking we can loop over the columns and replace using the nan column indicator
# See issue here: 
precision_dummies = pd.get_dummies(data[precision], dummy_na=True) 
obligation_dummies = pd.get_dummies(data[obligation],dummy_na=True)
delegation_dummies = pd.get_dummies(data[delegation],dummy_na=True)

data = pd.concat([data, precision_dummies, obligation_dummies, delegation_dummies], axis=1)

# Normalize scaled columns 'precision 2 (1-4)' and 'obligation 4 (1-5)'
data['precision_2_norm'] = data['precision 2 (1-4)'].astype(float).div(4)
data['obligation_4_norm'] = data['obligation 4 (1-5)'].astype(float).div(5)

# create 1,0 using >= .50 as cutoff and take care of nan values 
data['precision_2_dummy'] = np.where(data['precision_2_norm'] >= 0.50, 1, 0)
data['precision_2_dummy'].mask(data['precision_2_norm'].isna(), np.nan, inplace=True)

data['obligation_4_dummy'] = np.where(data['obligation_4_norm'] >= 0.50, 1, 0)
data['obligation_4_dummy'].mask(data['obligation_4_norm'].isna(), np.nan, inplace=True)

# mask '0' values that should be nan in the other dummy variables
dummies = ['precision 1 (Y/N)_Y', 'precision 4 (Y/N)_Y', 'obligation 1 (Y/N)_Y', 
    'obligation 2 (Y/N)_Y', 'obligation 3 (Y/N)_Y', 'obligation 5 (Y/N)_Y',
    'delegation 1 (Y/N)_Y', 'delegation 2 (Y/N)_Y', 'delegation 3 (Y/N)_Y']

nan_values = ['precision 1 (Y/N)_nan', 'precision 4 (Y/N)_nan', 'obligation 1 (Y/N)_nan', 
    'obligation 2 (Y/N)_nan', 'obligation 3 (Y/N)_nan', 'obligation 5 (Y/N)_nan',
    'delegation 1 (Y/N)_nan', 'delegation 2 (Y/N)_nan', 'delegation 3 (Y/N)_nan']

# this maps the nan values using the column created by 'get_dummies'...R is so much better with this stuff honestly
for nan_column, dummy_columm in zip(nan_values, dummies):
    data.loc[data[nan_column] == 1, [dummy_columm]] = np.nan

# Finally, create the Y composite by adding the values and creating the cut-offs
precision_cols = ['precision 1 (Y/N)_Y', 'precision_2_dummy', 'precision 4 (Y/N)_Y']
obligation_cols = ['obligation 1 (Y/N)_Y', 'obligation 2 (Y/N)_Y','obligation 3 (Y/N)_Y', 'obligation_4_dummy', 'obligation 5 (Y/N)_Y']
delegation_cols =  ['delegation 1 (Y/N)_Y', 'delegation 2 (Y/N)_Y', 'delegation 3 (Y/N)_Y']

data['precision_sum'] =  data.loc[:, precision_cols].sum(axis=1)

data['obligation_sum'] = data.loc[:, obligation_cols].sum(axis=1)

data['delegation_sum'] = data.loc[:, delegation_cols].sum(axis=1)

# same issue as before we want to combine even if some have nan values but not if all are nan
# this creates 0 for all nan instances 
# we can fix by creating an indicator for when all are missing and use the previous method to mask these
data['precision_na'] = data[precision_cols].isnull().apply(lambda x: all(x), axis=1) 
data.loc[data['precision_na'] == True, ['precision_sum']] = np.nan

data['obligation_na'] = data[obligation_cols].isnull().apply(lambda x: all(x), axis=1) 
data.loc[data['obligation_na'] == True, ['obligation_sum']] = np.nan

data['delegation_na'] = data[delegation_cols].isnull().apply(lambda x: all(x), axis=1) 
data.loc[data['delegation_na'] == True, ['delegation_sum']] = np.nan

# last bit for cutoff 
data['precision_high'] = np.where(data['precision_sum'] >= 3, 1, 0)
data['obligation_high'] = np.where(data['obligation_sum'] >= 3, 1, 0)
data['delegation_high'] = np.where(data['delegation_sum'] >= 3, 1, 0)

# only keep complete outcome cases we can use any of the sum_na columns for this
complete_y_cases = data[data.delegation_na == False]

# complete cases relative to actual documents 'content' isolate y and x 
model_df = complete_y_cases[['content', 'precision_high', 'obligation_high', 'delegation_high']]


# Cleaning documents
#probably a way to string this together better
##get rid of special characters and "accidental" punctuation
bad_characters = list("?!~﻿\/_-'[]»")

for punctuation in bad_characters:
    model_df['content']  = model_df['content'].str.replace(punctuation, "")

#get rid of multiple periods without getting rid of single periods helpful for 
#denoting sentences
model_df['content']= model_df['content'].str.replace(r"\.{2,}", "")

#Do we need to get rid of things like (a) as a list tool?
model_df['content']= model_df['content'].str.replace(r"\(\w\)", "")

#Getting rid of extra whitespace
model_df['content']= model_df['content'].str.replace(r" +", " ")

# you need to convert to lower case 
model_df['content'] = model_df['content'].str.lower() 

model_df['content'] = model_df['content'].str.replace(r"\d+", "")

# isolate the documents convert to list and Y outcomes 
# First replace empty documents to nan 
model_df['content'] = model_df['content'].replace('', np.nan)

# listwise delete model_df 
model_df = model_df.dropna().reset_index()

clean_documents  = model_df['content'].to_list()

# remove empty entries for now, are they supposed to be missing? (not needed after clean up)
clean_documents = [i for i in clean_documents if i] # don't really need this now 

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
df_outcomes = model_df.drop(['index', 'content'], axis = 1)

# look at the coverage across individual categories 
counts = []
cats = list(df_outcomes.columns.values)
for i in cats:
    counts.append((i, df_outcomes[i].sum()))

df_summary = pd.DataFrame(counts, columns=['outcome', 'number of documents'])
df_summary

# look at the multi-label
rowsums = df_outcomes.iloc[:,0:].sum(axis=1)
x=rowsums.value_counts()
x

# 0    210
# 1    128
# 2     87
# 3     42

# split train and test (WIP until we have all the possible text)
x_train, x_test, y_train, y_test = train_test_split(doc_stop_rm, df_outcomes, test_size=0.2, random_state=40)

# we can use our existing tfidf pipeline but incorporate our classifiers 
model_feat = Pipeline([('vect', CountVectorizer(ngram_range=(1, 2), analyzer='word')),
    ('tfidf', TfidfTransformer(use_idf= True))
    ])

# let's try naive bayes 
model = Pipeline( steps = [ ('feat_pipeline', model_feat),
                            ('clf', OneVsRestClassifier(MultinomialNB(fit_prior=True, class_prior=None))) 
                                  ])

for category in cats:
    print('... Processing {}'.format(category))
    # train the model using X_dtm & y
    model.fit(x_train, y_train[category])
    # compute the testing accuracy
    prediction = model.predict(x_test)
    print('Test accuracy is {}'.format(accuracy_score(y_test[category], prediction)))
    print(classification_report(y_test[category], prediction))
    print(confusion_matrix(y_test[category], prediction))

# logistic regression
model = Pipeline( steps = [ ('feat_pipeline', model_feat),
                            ('clf',  OneVsRestClassifier(LogisticRegression(solver='sag'), n_jobs=1)) 
                                  ])

for category in cats:
    print('... Processing {}'.format(category))
    # train the model using X_dtm & y
    model.fit(x_train, y_train[category])
    # compute the testing accuracy
    prediction = model.predict(x_test)
    print('Test accuracy is {}'.format(accuracy_score(y_test[category], prediction)))
    print(classification_report(y_test[category], prediction))
    print(confusion_matrix(y_test[category], prediction))

# SVC
model = Pipeline( steps = [ ('feat_pipeline', model_feat),
                            ('clf',  OneVsRestClassifier(LinearSVC(), n_jobs=1)) 
                                  ])

for category in cats:
    print('... Processing {}'.format(category))
    # train the model using X_dtm & y
    model.fit(x_train, y_train[category])
    # compute the testing accuracy
    prediction = model.predict(x_test)
    print('Test accuracy is {}'.format(accuracy_score(y_test[category], prediction)))
    print(classification_report(y_test[category], prediction))
    print(confusion_matrix(y_test[category], prediction))

# SVC seems to be doing the best.
# Next steps:
# 1. Parameter tuning 
# 2. Inspect classifications (this will be tricky for the multi label case)