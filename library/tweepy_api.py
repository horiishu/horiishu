# coding: utf-8
#! /usr/bin/python

import tweepy
import re

f = open(r'/home/tweepy_keys.txt')
KEYS = f.read().split("\n")

class TweepyAPI:
    def __init__(self):
        # Information of Twitter API account horiishu
        CONSUMER_KEY = KEYS[0]
        CONSUMER_SECRET = KEYS[1]
        ACCESS_TOKEN = KEYS[2]
        ACCESS_SECRET = KEYS[3]
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

        #Make instance of API
        self.api = tweepy.API(auth, wait_on_rate_limit = True)

    def get_followers(self, account_name):
        print(" ========== Start to get followers data ==========")
        try:
            followers_ids = tweepy.Cursor(self.api.followers_ids, id = account_name, cursor = -1).items()
        except:
            print("Error: Failed to get followers!")
        followers_ids = set(followers_ids)
        print(account_name + " followers value : " + str(len(followers_ids)))

        return followers_ids

if __name__ == '__main__':
    t = TweepyAPI()
    t.get_followers("yaritaiji0324")