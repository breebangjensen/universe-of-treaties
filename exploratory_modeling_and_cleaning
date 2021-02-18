#load packages
import pandas as pd
import re 
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
np.random.seed(2018)
import nltk
nltk.download('wordnet')

#set up dataframe
data = pd.read_csv('data/final_labels.csv', error_bad_lines=False);
data['content'].dtypes # check data type 
data_text = data['content'].astype(str) # convert to string 
data_text['index'] = data_text.index
documents = data_text.to_list()
documents
# What do we want to do to this text?
# We will go through it row by row as it is in the df 
# A good thing to do first is to test with one entry and run that through each step of the pipeline
# when we are satistifed we can loop.
test_doc = documents[1] # try things one-by one

# we can break this up a little 
# we need to tekenize first 
# then we need to check if the word is in the stop word dictionary 

# We should convert to lower as a preprocessing step
# Preprocessing Only what is needed 
# 1. Do anything that leverages caps first 
# ARE THESE NEEDED?
test_doc = re.findall('[A-Z][^A-Z]*', test_doc) 

test_doc = ' '.join(test_doc) 

# ONCE YOU DEFINE WHAT IS NEEDED DO LOWER

test_doc = test_doc.lower()

# BREAK UP INTO STEPS
# test_doc = " ".join(w for w in nltk.wordpunct_tokenize(test_doc) if w.lower() in words or not w.isalpha())

#1. Tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize

doc_tokens = word_tokenize(test_doc)

# remove the stop words
tokens_no_stop = [word for word in doc_tokens if not word in stopwords.words()] # we can use any dictionary we want
# we can combine again 
processed_doc = (" ").join(tokens_no_stop) 

print(processed_doc) # IS THIS LOOKING OKAY? 

#prelim text cleaning from Jose's script
#the text below doesn't work because documents isn't a string
#Do I need to feed it one string at a time (more loops?). Probably. 
#should we lemmetize next?)
#documents = re.findall('[A-Z][^A-Z]*', documents)
#documents = ' '.join(documents)
#documents = " ".join(w for w in nltk.wordpunct_tokenize(documents) if w.lower() in words or not w.isalpha())
#copying a different version from here: https://towardsdatascience.com/topic-modeling-and-latent-dirichlet-allocation-in-python-9bf156893c24
##doesn't quite work-- can return to later
#def lemmatize_stemming(text):
#    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))
#def preprocess(text):
#    result = []
#    for token in gensim.utils.simple_preprocess(text):
#       if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
#            result.append(lemmatize_stemming(token))
#    return result

##check if it worked
#doc_sample = documents[documents['index'] == 543].values[0][0]
#print('original document: ')
#words = []
#for word in doc_sample.split(' '):
#    words.append(word)
#print(words)
#print('\n\n tokenized and lemmatized document: ')
#print(preprocess(doc_sample))

##process docs
#processed_docs = documents['headline_text'].map(preprocess)
#processed_docs[:10]

#ok let's pretend we processed it
##make dictionary based on term frequency
documents["documents"].to.list()
dictionary = gensim.corpora.Dictionary(documents)
count = 0
for k, v in dictionary.iteritems():
    print(k, v)
    count += 1
    if count > 10:
        break
