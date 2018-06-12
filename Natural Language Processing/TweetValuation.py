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
from string import punctuation
#from nltk.stem import PorterStemmer
#from nltk.tokenize import WordPunctTokenizer
from nltk import bigrams as bi_grams
from nltk import trigrams as tri_grams

# Import  

tweet_df = pd.read_csv('TweetResponseSample.csv')

############################ Tokenizing Function

#esw = nltk.corpus.stopwords.words('english') #i think we want to keep stopwords here
word_pattern = re.compile("^\w+$")

def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

def clean_up(tweet):
    low_tweet = tweet.lower()
    nopun_tweet = strip_punctuation(low_tweet)
    noweb_tweet = nopun_tweet.replace('http','')
    split_tweet = re.split(r'\s',noweb_tweet)
    clean_tweet = [split_tweet for split_tweet in split_tweet if re.match(word_pattern, split_tweet)]
    return clean_tweet
    
############################ Unigram

def unigram_vals(tweet_df):
        
    '''prerequisite functions: clean_up'''
    
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
        
        dfx = df[df['business_name'].str.contains(business_names[i])].reset_index() 
        
        print("The length of " + str(dfx['business_name'].unique()) + " is " + str(len(dfx)))
    
        # tokenize each tweet
        
        unigrams = list(dfx.apply(lambda row: clean_up(row['tweet_message']), axis=1))
        
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
        
        # add business column names
        
        dfx['business_name'] = business_names[i]
        
        # Filter to phrases that occur 5 times
        
        dfx = dfx[dfx['count'] >= 5]
        
        # Add weight column to order by
        
        dfx['weight'] = dfx['count'] * dfx['value'] 
                
        # Clean up output a little
        
        dfx = dfx.loc[:,['business_name','unigrams','value','count','weight']].sort_values(by= 'weight',ascending = False).reset_index(drop=True)
        
        print(str(business_names[i]) + " is completed")
        
        df_final = df_final.append(dfx)
        
        #print(dfx.head())
        
    return df_final

############################ Bigram

def bigram_vals(tweet_df):
        
    '''prerequisite functions: clean_up'''
    
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
        
        dfx = df[df['business_name'].str.contains(business_names[i])].reset_index() 
        
        print("The length of " + str(dfx['business_name'].unique()) + " is " + str(len(dfx)))
    
        # tokenize each tweet
        
        unigrams = list(dfx.apply(lambda row: clean_up(row['tweet_message']), axis=1))
        
        # put unigrams in their own column
        
        dfx['unigrams'] = unigrams
        
        # create a list of bigrams given unigram list (renamed function so i could keep object naming consistent)
        
        bigrams = [list(bi_grams(x)) for x in unigrams]
        
        # turn bigrams into something more readable
        
        bigrams = [[("%s "*len(x)%x).strip() for x in y] for y in bigrams]
        
        # put bigrams in their own column
        
        dfx['bigrams'] = bigrams
        
        # place into each into their own columns
        
        dfx = pd.concat([dfx['conversations_status'],pd.DataFrame(dfx.bigrams.tolist())],1)
        
        # isolate column names without conversion status
        
        col_names = dfx.columns[1:]
        
        # melt dataframe to just words and statuses
        
        dfx = pd.melt(dfx, id_vars = 'conversations_status', value_name = 'bigrams', value_vars = col_names).reset_index()
        
        # keep just what we want and remove None values
        
        dfx = dfx[['bigrams','conversations_status']].dropna().reset_index()
            
        # group by unigrams, get average conversion status and total count
        
        dfx = dfx.groupby('bigrams')['conversations_status'].agg(['mean', 'count']).reset_index()
        
        dfx.columns = ['bigrams','value','count']
        
        # add business column names
        
        dfx['business_name'] = business_names[i]
        
        # Filter to phrases that occur 5 times
        
        dfx = dfx[dfx['count'] >= 5]
        
        # Add weight column to order by
        
        dfx['weight'] = dfx['count'] * dfx['value'] 
                
        # Clean up output a little
        
        dfx = dfx.loc[:,['business_name','bigrams','value','count','weight']].sort_values(by= 'weight',ascending = False).reset_index(drop=True)
                    
        print(str(business_names[i]) + " is completed")
        
        df_final = df_final.append(dfx)
        
        #print(dfx.head())
        
    return df_final

############################ Trigram 

def trigram_vals(tweet_df):
        
    '''prerequisite functions: clean_up'''
    
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
        
        dfx = df[df['business_name'].str.contains(business_names[i])].reset_index()
    
        print("The length of " + str(dfx['business_name'].unique()) + " is " + str(len(dfx)))
    
        # tokenize each tweet
        
        unigrams = list(dfx.apply(lambda row: clean_up(row['tweet_message']), axis=1))
        
        # put unigrams in their own column
        
        dfx['unigrams'] = unigrams
        
        # create a list of trigrams given unigram list (renamed function so i could keep object naming consistent)
        
        trigrams = [list(tri_grams(x)) for x in unigrams]
        
        # turn trigrams into something more readable
        
        trigrams = [[("%s "*len(x)%x).strip() for x in y] for y in trigrams]
        
        # put trigrams in their own column
        
        dfx['trigrams'] = trigrams
        
        # place into each into their own columns
        
        dfx = pd.concat([dfx['conversations_status'],pd.DataFrame(dfx.trigrams.tolist())],1)
        
        # isolate column names without conversion status
        
        col_names = dfx.columns[1:]
        
        # melt dataframe to just words and statuses
        
        dfx = pd.melt(dfx, id_vars = 'conversations_status', value_name = 'trigrams', value_vars = col_names).reset_index()
        
        # keep just what we want and remove None values
        
        dfx = dfx[['trigrams','conversations_status']].dropna().reset_index(drop=True)
            
        # group by unigrams, get average conversion status and total count
        
        dfx = dfx.groupby('trigrams')['conversations_status'].agg(['mean', 'count']).reset_index()
        
        dfx.columns = ['trigrams','value','count']
        
        # add business column names
        
        dfx['business_name'] = business_names[i]
        
        # Filter to phrases that occur 5 times
        
        dfx = dfx[dfx['count'] >= 5]
        
        # Add weight column to order by
        
        dfx['weight'] = dfx['count'] * dfx['value'] 
                
        # Clean up output a little
        
        dfx = dfx.loc[:,['business_name','trigrams','value','count','weight']].sort_values(by= 'weight',ascending = False).reset_index(drop=True)
                    
        print(str(business_names[i]) + " is completed")
        
        df_final = df_final.append(dfx)
        
        #print(dfx.head())
        
    return df_final

    
                
                