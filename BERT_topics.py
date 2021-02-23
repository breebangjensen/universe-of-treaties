# Begin exploring similarity between predefined word categories

import pandas as pd
import numpy as np
import re
import nltk
import gensim
import gensim.downloader as gensim_api
from gensim.parsing.preprocessing import remove_stopwords
# New libraries you will also need to install Tensorflow 
import transformers
from sklearn import metrics, manifold

import os
import operator
import json

# Load pretrained model
# this is the glove model (slighty smaller, but we can try others)
wiki_embed = gensim_api.load("glove-wiki-gigaword-300") # create function to load pickle or download 
google_embed = gensim_api.load("word2vec-google-news-300")
# FOR A LIST OF MODELS AVAILABLE THROUGH THE API: https://radimrehurek.com/gensim/models/word2vec.html

# Load your data we might start with one doc to test
data = pd.read_csv('data/final_labels.csv', error_bad_lines=False);
data['content'].dtypes # check data type 
data_text = data['content'].astype(str) # convert to string 
data_text['index'] = data_text.index
documents = data_text.to_list()

test_doc = documents[3] # lets begin with n=1

# Clean up documents THIS STILL NEEDS TO HAPPEN SO WILL USE EXCERPT

test_doc = """
Declaring their intention to achieve at the earliest possible date the cessation of the nuclear arms race and to undertake effective measures in the direction of nuclear disarmament, Urging the co-operation of all States in the attainment of this objective,
Recalling the determination expressed by the Parties to the 1963 Treaty1 banning nuclear weapon tests in the atmosphere, in outer space and under water in its Preamble to seek to achieve the discontinuance of all test explosions of nuclear weapons for all time and to continue negotiations to this end, Desiring to further the easing of international tension and the strengthening of trust between States in order to facilitate the cessation of the manufacture of nuclear weapons, the liquidation of all their existing stockpiles, and the elimina tion from national arsenals of nuclear weapons and the means of their delivery pursuant to a Treaty on general and complete disarmament under strict and effective international control, 
Recalling that, in accordance with the Charter of the United Nations, States must refrain in their international relations from the threat or use of force against the territorial integrity or political independence of any State, or in any other manner inconsistent with the Purposes of the United Nations, and that the establishment and maintenance of international peace and security are to be promoted with the least diversion for armaments of the world's human and economic resources,
Have agreed as follows
Article I
Each nuclear-weapon State Party to the Treaty undertakes not to transfer to any recipient whatsoever nuclear weapons or other nuclear explosive devices or control over such weapons or explosive devices directly, or indirectly; and not in any way to assist, encourage, or induce any non-nuclear-weapon State to manufacture or otherwise acquire nuclear weapons or other nuclear explosive devices, or control over such weapons or explosive devices.
Article II
Each non-nuclear-weapon State Party to the Treaty undertakes not to receive the transfer from any transferor whatsoever of nuclear weapons or other nuclear explosive devices or of control over such weapons or explosive devices directly, or indirectly ; not to manufacture or otherwise acquire nuclear weapons or other nuclear explosive devices; and not to seek or receive any assistance in the manufacture of nuclear weapons or other nuclear explosive devices.
Article III
1.Each non-nuclear-weapon State Party to the Treaty undertakes to accept safeguards, as set forth in an agreement to be negotiated and concluded with the International Atomic Energy Agency in accordance with the Statute of the International Atomic Energy Agency1 and the Agency's safeguards system, for the exclusive purpose of verification of the fulfilment of its obligations assumed under this Treaty with a view to preventing diversion of nuclear energy from peaceful uses to nuclear weapons or other nuclear explosive devices. Procedures for the safeguards required by this Article shall be followed with respect to source or special fissionable material whether it is being produced, processed or used in any principal nuclear facility or is outside any such facility. The safeguards required by this Article shall be applied on all source or special fissionable material in all peaceful nuclear activities within the territory of such State, under its jurisdiction, or carried out under its control anywhere.
2.Each State Party to the Treaty undertakes not to provide: (a) source or special fissionable material, or (b) equipment or material especially designed or prepared for the processing, use or production of special fissionable material, to any non-nuclear-weapon State for peaceful purposes, unless the source or special fissionable material shall be subject to the safeguards required by this Article.
3.The safeguards required by this Article shall be implemented in a manner designed to comply with Article IV of this Treaty, and to avoid hamper ing the economic or technological development of the Parties or international co-operation in the field of peaceful nuclear activities, including the international exchange of nuclear material and equipment for the processing, use or production of nuclear material for peaceful purposes in accordance with the provisions of this Article and the principle of safeguarding set forth in the Preamble of the Treaty.
4.Non-nuclear-weapon States Party to the Treaty shall conclude agreements with the International Atomic Energy Agency to meet the requirements of this Article either individually or together with other States in accordance with the Statute of the International Atomic Energy Agency. Negotiation of such agree ments shall commence within 180 days from the original entry into force of this Treaty. For States depositing their instruments of ratification or accession after the 180-day period, negotiation of such agreements shall commence not later than the date of such deposit. Such agreements shall enter into force not later than eighteen months after the date of initiation of negotiations.
Article IV
Nothing in this Treaty shall be interpreted as affecting the inalienable
"""

REM_NUM = re.compile(r'\d{1}.')    
text = REM_NUM.sub(' ', test_doc)
text = text.lower()

# remove stop words
text = remove_stopwords(text)

# Load keywords json
# use this function 
def get_metadata_dict(metadata_file):
    metadata_handle = open(metadata_file)
    metadata = json.loads(metadata_handle.read())
    return metadata

cat_keyw = get_metadata_dict("/Users/josehernandez/Documents/eScience/projects/universe-of-treaties/qualitative_keywords.json")

# BERT  models that you will use to get embeddings 
tokenizer = transformers.BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
m_bert = transformers.TFBertModel.from_pretrained('bert-base-uncased')

def utils_bert_embedding(txt, tokenizer, bert_model): # handle truncation here 
    idx = tokenizer.encode(txt,truncation=True, max_length=512) 
    idx = np.array(idx)[None,:]  
    embedding = bert_model(idx)
    X = np.array(embedding[0][0][1:-1])
    return X

# See how the truncation works ########
test = "how the heck do we do this now if this is being truncated"
idx = tokenizer.encode(test,truncation=True, max_length=5)
#########

# mean_vec = [utils_bert_embedding(txt, tokenizer, m_bert).mean(0) for txt in text]    
mean_vec = utils_bert_embedding(text, tokenizer, m_bert).mean(0) # single entry case
## create the feature matrix (observations x 768)
X = np.array(mean_vec)
X.shape

# Create dict of context 
# use this function to get similar words
def get_similar_words(list_words, top, wb_model):
    list_out = list_words
    for w in wb_model.most_similar(list_words, topn=top):
        list_out.append(w[0])
    return list(set(list_out))

## DIF IN GOOGLE VS GLOVE not surprised. 
## We might not use these to create keywords
## We can try with the topic model results --> TF-IDF and Topics
dict_codes_google = {key: None for key in cat_keyw.keys()}

# This creates a dictionary of words using your predefined keywords from the model
# uses 30 words but you can add more 
# This step is also not necessary if you have many keywords
for k in cat_keyw.keys():
    dict_codes_google[k] = get_similar_words(cat_keyw[k],10, gl_embed)
###########
#GLOVE
dict_codes_glove = {key: None for key in cat_keyw.keys()}

# This creates a dictionary of words using your predefined keywords from the model
# uses 30 words but you can add more 
# This step is also not necessary if you have many keywords
for k in cat_keyw.keys():
    dict_codes_glove[k] = get_similar_words(cat_keyw[k],10, wiki_embed)
###

dict_y = {k:utils_bert_embedding(v, tokenizer, m_bert).mean(0) for k,v in cat_keyw.items()}

# Create model when we need to iterate over multiple documents 
similarities = np.array([metrics.pairwise.cosine_similarity(X,[y]).T.tolist()[0] for y in dict_y.values()]).T

# using one case 
similarities = np.array([metrics.pairwise.cosine_similarity(X.reshape(1,-1),y.reshape(1,-1)).T.tolist()[0] for y in dict_y.values()]).T

labels = list(dict_y.keys())

for i in range(len(similarities)):
    if sum(similarities[i]) == 0:
        similarities[i] = [0]*len(labels)
        similarities[i][np.random.choice(range(len(labels)))] = 1
    similarities[i] = similarities[i] / sum(similarities[i])

# Classify based on Cosine Similarity score
labels_pred = {labels: similarities[0][idx] for idx, labels in enumerate(labels)}
sorted(labels_pred, key=labels_pred.get, reverse=True)
sorted(similarities[0], reverse=True) 
# these are all kind of represented not a lot of seperation but 
# We used a small text sample

# Other Promising similar approaches...
# https://towardsdatascience.com/topic-modeling-with-bert-779f7db187e6
# https://www.kaggle.com/dskswu/topic-modeling-bert-lda