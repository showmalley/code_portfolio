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

# Unigrams

unigram_vals = unigram_vals(tweet_df)

unigram_vals.to_csv('unigram_vals.csv')

# Bigrams

bigram_vals = bigram_vals(tweet_df)

bigram_vals.to_csv('bigram_vals.csv')

# Trigrams 

trigram_vals = trigram_vals(tweet_df)

trigram_vals.to_csv('trigram_vals.csv')