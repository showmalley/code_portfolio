#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 12:23:38 2018

@author: SeanOMalley1
"""

# TweetValuation Driver
import pandas as pd
import os
os.chdir('/Users/SeanOMalley1/AnacondaProjects/AdHocDataScience/Respondology')
from TweetValuation import *

tweet_df = pd.read_csv('TweetResponseSample.csv')

'''

# Unigrams

unigram_vals = unigram_vals(tweet_df)

unigram_vals.to_csv('unigram_vals.csv', index = False)

# Bigrams

bigram_vals = bigram_vals(tweet_df)

bigram_vals.to_csv('bigram_vals.csv', index = False)

# Trigrams 

trigram_vals = trigram_vals(tweet_df)

trigram_vals.to_csv('trigram_vals.csv', index = False)

'''

############################ Engine

#def Engine(tweet_df):
    
# Evaluate n-gram average values and place result in df

unigram_vals_df = pd.DataFrame(unigram_vals(tweet_df))
bigram_vals_df = pd.DataFrame(bigram_vals(tweet_df))
trigram_vals_df = pd.DataFrame(trigram_vals(tweet_df))

# Initialize n-gram columns in tweet_df, broadcast 0

tweet_df['unigram_val'] = pd.to_numeric(0)
tweet_df['bigram_val'] = pd.to_numeric(0)
tweet_df['trigram_val'] = pd.to_numeric(0)

# Clean the tweet similar to gram process

clean_tweets = list(tweet_df['tweet_message'].apply(clean_up))

# Change back into strings
 
clean_tweets = [' '.join(i) for i in clean_tweets] 

# Put in DataFrame

tweet_df['clean_tweet'] = clean_tweets

# For every tweet sum the average uni-gram, bi-gram and tri-gram values for each tweet (will be useful when we encounter unknown tweets)

# First, for speed, lets filter out all 0 values of each n-gram in dict with values

unigram_vals_ls = unigram_vals_df.loc[:,['unigrams','value']][unigram_vals_df['value'] > 0]
unigram_vals_dict = dict(zip(unigram_vals_ls['unigrams'], unigram_vals_ls['value']))

bigram_vals_ls = bigram_vals_df.loc[:,['bigrams','value']][bigram_vals_df['value'] > 0]
unigram_vals_dict = dict(zip(bigram_vals_ls['bigrams'], bigram_vals_ls['value']))

trigram_vals_ls = trigram_vals_df.loc[:,['trigrams','value']][trigram_vals_df['value'] > 0]
unigram_vals_dict = dict(zip(trigram_vals_ls['trigrams'], trigram_vals_ls['value']))

# 

list(map(lambda clean_tweets: clean_tweets.str.contains(unigram_vals_dict.keys()), unigram_vals_dict.values())

#{k:v for (k,v) in unigram_vals_dict.items()}

# Now Do a list comprehension checking for gram vals in tweets

#[s for s in my_list if any(xs in s for xs in matchers)]

'''
# Legacy Engine
for i in tweet_df.index:
    
    for a in range(0,len(unigram_vals_df)):
        
        if ((tweet_df.loc[i,['clean_tweet']].str.contains(unigram_vals_df.iloc[a,1])) & (tweet_df.iloc[i,1] == unigram_vals_df.iloc[a,0])).all():
            tweet_df.loc[i,['unigram_val']] = tweet_df.loc[i,['unigram_val']] + unigram_vals_df.iloc[a,2]
        
    for b in range(0,len(bigram_vals_df)):
        
        if ((tweet_df.loc[i,['clean_tweet']].str.contains(bigram_vals_df.iloc[b,1]) == True) & (tweet_df.iloc[i,1] == bigram_vals_df.iloc[b,0])).all():
            tweet_df.loc[i,['bigram_val']] = tweet_df.loc[i,['bigram_val']] + bigram_vals_df.iloc[b,2]
        
    for c in range(0,len(trigram_vals_df)):
        
        if ((tweet_df.loc[i,['clean_tweet']].str.contains(trigram_vals_df.iloc[c,1]) == True) & (tweet_df.iloc[i,1] == trigram_vals_df.iloc[c,0])).all():
            tweet_df.loc[i,['trigram_val']] = tweet_df.loc[i,['trigram_val']] + trigram_vals_df.iloc[c,2]
'''
       
# Word Count

#tweet_df['word_count'] = 
        
# Total Score As a Proportion to max score possible
            
tweet_df['total_max_score'] = tweet_df['word_count'] * 3 - 3 

tweet_df['total_score'] = tweet_df['unigram_val'] + tweet_df['bigram_val'] + tweet_df['trigram_val']

tweet_df['quality_score'] = tweet_df['total_score'] / tweet_df['total_max_score']

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
    
#all_results = [tweet_df,unigram_vals_df,bigram_vals_df,trigram_vals_df] # return list of df's...will it work, idk? # return globals of ngram outputs?
        
    #return all_results

   
############################