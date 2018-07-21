# coding: utf-8
#! /usr/bin/python

import tweepy
import sys
import csv
import datetime
import subprocess
import re

#matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

#configure of pandas
#plt.style.use('ggplot') 
#font = {'family' : 'meiryo'}
#matplotlib.rc('font', **font)

args = sys.argv

#Information of Twitter API account "horiishu"
CONSUMER_KEY = '9OMN7bmOmIgVMBcVqpZFEUFDn'
CONSUMER_SECRET = 'bbTmJA1EPyuFj3XPpiTAqLgIpKf4VbeStyEowWrKzdXtcbDKRy'
ACCESS_TOKEN = '243028271-hNYIWiCNhS5UzdnPLzAF5UkmRnVZAx8N8alZUcrz'
ACCESS_SECRET = 'T33eCZuJsPn4PWIYPeYkyXl8gagACN1eETCXrWGIXICLK'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

#Make instance of API
api = tweepy.API(auth, wait_on_rate_limit = True)

#Obtain date
date = datetime.date.today()

class Followers_data:
    """Output followers data"""

    def make_followers_set(self):
        """Get followers ids list"""
        #Make followers D data
        print("!!!start get followers data !!!")
        try:
            followers_ids = tweepy.Cursor(api.followers_ids, id = 'yaritaiji0324', cursor = -1).items()
        except tweepy.error.TweepError:
            print("Error detected")
        set_ids = set(followers_ids)            
        print("follwer is " + str(len(set_ids)) + " !!!!!")

if __name__ == "__main__":
    print(CONSUMER_KEY)
    print(CONSUMER_SECRET)
    print(ACCESS_TOKEN)
    print(ACCESS_SECRET)