#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 10:53:09 2018

@author: SeanOMalley1
"""

# Respondology Tweet Valuation Engine
# Sean O'Malley
# Principia Analytics

# Packages & Working Directory

import os
os.chdir('/Users/SeanOMalley1/AnacondaProjects/AdHocDataScience/Respondology')
import pandas as pd
import numpy as np

# NLP Specific Packages

from textblob import TextBlob
import nltk
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer

# Import  

tweet_df = pd.read_csv('TweetResponseSample.csv')

############################

# Tokenizing Function

esw = nltk.corpus.stopwords.words('english') #i think we want to keep stopwords here
word_pattern = re.compile("^\w+$")

def get_text(text):
    tokens = nltk.tokenize.WordPunctTokenizer().tokenize(PorterStemmer().stem(text))
    tokens = [token for token in tokens if re.match(word_pattern, token)]
    return(tokens)
    
############################
    
# Get Unigram Values by client for each 

def unigram_vals(tweet_df):
        
    '''prerequisite functions: get_text'''
    
    # Read in just what we want
    
    df = tweet_df.loc[:,['business_name','conversations_status','tweet_message']]
    
    # Convert conversations status to binary
    
    df['conversations_status'] = np.where(df['conversations_status'] == 'replied_to', 1, 0)
    
    # Choose Unique business names
    
    business_names = list(df['business_name'].unique())
    
    # initialize final dataframe
    
    df_final = pd.DataFrame()
    
    # Iterate by business to get unigrams and corresponding score
    
    for i in range(0,len(business_names)):
        
        # dynamically filter to business
        
        dfx = df[df['business_name'].str.contains(business_names[i])].reset_index() # make i
    
        # tokenize each tweet
        
        unigrams = list(dfx.apply(lambda row: get_text(row['tweet_message']), axis=1))
        
        # merge into df
        
        dfx['unigrams'] = unigrams
        
        dfx = pd.concat([dfx['conversations_status'],pd.DataFrame(dfx.unigrams.tolist())],1)
        
        # isolate column names without conversion status
        
        col_names = dfx.columns[1:]
        
        # melt dataframe to just words and statuses
        
        dfx = pd.melt(dfx, id_vars = 'conversations_status', value_name = 'unigrams', value_vars = col_names).reset_index()
        
        # keep just what we want and remove None values
        
        dfx = dfx[['unigrams','conversations_status']].dropna().reset_index()
            
        # group by unigrams, get average conversion status and total count
        
        dfx = dfx.groupby('unigrams')['conversations_status'].agg(['mean', 'count']).reset_index()
        
        dfx.columns = ['unigrams','value','count']
        
        dfx['business_name'] = business_names[i]
        
        dfx = dfx[dfx['count'] >= 5].sort_values(by=['count','value'],ascending = False)
        
        print("Client " + str(i + 1) + " is completed")
        
        df_final = df_final.append(dfx)
        
        print(df_final.head())
        
    return df_final

############################

# Get Bigram Values by client for each 

#def bigram_vals(tweet_df):

############################

# Get Trigram Values by client for each 

#def trigram_vals(tweet_df):

############################
'''
def Engine(tweet_df):
    
    # Evaluate n-gram average values and place result in df
    
    unigram_vals_df = unigram_vals(tweet_df)
    bigram_vals_df = bigram_vals(tweet_df)
    trigram_vals_df = trigram_vals(tweet_df)
    
    # Initialize n-gram columns in tweet_df, broadcast 0
    
    tweet_df['unigram_val'] = 0
    tweet_df['bigram_val'] = 0
    tweet_df['trigram_val'] = 0
    
    # For every tweet sum the average uni-gram, bi-gram and tri-gram values for each tweet (will be useful when we encounter unknown tweets)
    
    for i in tweet_df.index:
        
        for a in unigram_vals_df.index:
            
            if (tweet_df.loc[i,['tweet_message']].str.contains(unigram_vals_df.loc[a,['gram']]) == True) & (tweet_df.loc[i,['business_name']] == unigram_vals_df.loc[a,['business_name']]) :
                tweet_df.loc[i,['unigram_val']] = tweet_df.loc[i,['unigram_val']] + unigram_vals_df.loc[a,['val']]
            
        for b in bigram_vals_df.index:
            
            if (tweet_df.loc[i,['tweet_message']].str.contains(bigram_vals_df.loc[a,['gram']]) == True) & (tweet_df.loc[i,['business_name']] == bigram_vals_df.loc[a,['business_name']]):
                tweet_df.loc[i,['bigram_val']] = tweet_df.loc[i,['bigram_val']] + bigram_vals_df.loc[a,['val']]
            
        for c in trigram_vals_df.index:
            
            if (tweet_df.loc[i,['tweet_message']].str.contains(trigram_vals_df.loc[a,['gram']]) == True) & (tweet_df.loc[i,['business_name']] == trigram_vals_df.loc[a,['business_name']]):
                tweet_df.loc[i,['trigram_val']] = tweet_df.loc[i,['trigram_val']] + trigram_vals_df.loc[a,['val']]
                
    # Term frequency, inverse document frequency
    
        # tweet_df['tfidf']
    
    # Part of speech tagging
    
        # tweet_df['verbs'] 
        # tweet_df['nouns']
        # tweet_df['adverb']
        # tweet_df['adjective']
        # tweet_df['pronoun']
        
        # tweet_df['emojis']
        # tweet_df['punctuation']
    
    # Polarity
    
        # tweet_df['polarity']
    
    # Subjectivity
    
        # tweet_df['subjectivity']
    
    # Intensity
    
        # tweet_df['intensity']
    
    # Word count
    
        # tweet_df['word_count']
    
    # Character length
    
        # tweet_df['char_len']
        
    all_results = [tweet_df,unigram_vals_df,bigram_vals_df,trigram_vals_df] # return list of df's...will it work, idk? # return globals of ngram outputs?
        
    return all_results
'''
   
############################
    
                
                