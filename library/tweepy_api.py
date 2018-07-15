# coding: utf-8
#! /usr/bin/python

import tweepy

class TweepyAPI:
    def __init__(self):
        #Information of Twitter API account "horiishu"
        CONSUMER_KEY = 
        CONSUMER_SECRET = 
        ACCESS_TOKEN = 
        ACCESS_SECRET = 
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

        #Make instance of API
        api = tweepy.API(auth, wait_on_rate_limit = True)

        self.followers_data = []

    def get_followers(self, account_name):
        print(" ========== Start to get followers data ==========")
        try:
            followers_ids = tweepy.Cursor(api.followers_ids, id = account_name, cursor = -1).items()
        except tweepy.error.TweepError:
            print("Error: Failed to get followers!")
        followers_ids = set(followers_ids)
        print(account_name + " followers value = " + str(len(followers_ids)))

        return followers_ids