# coding: utf-8
#! /usr/bin/python

import tweepy
import sys

CONSUMER_KEY = '9OMN7bmOmIgVMBcVqpZFEUFDn'
CONSUMER_SECRET ='bbTmJA1EPyuFj3XPpiTAqLgIpKf4VbeStyEowWrKzdXtcbDKRy'
ACCESS_TOKEN = '243028271-hNYIWiCNhS5UzdnPLzAF5UkmRnVZAx8N8alZUcrz'
ACCESS_SECRET = 'T33eCZuJsPn4PWIYPeYkyXl8gagACN1eETCXrWGIXICLK'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

#Make instance of API

api = tweepy.API(auth, wait_on_rate_limit = True)

class Followers_data:
    """Output followers data"""
    def make_followers_set(self, args):
        #Get followers ids list
        cnt = 1
        all_followers_list = []
        for all_followers in args[1:len(args)]:
            print("!!!start get followers data of account " + str(cnt) + " !!!")
            followers_ids = tweepy.Cursor(api.followers_ids, id = args[cnt], cursor = -1).items()
            set_ids = set(followers_ids)
            all_followers_list.append(set_ids)
            cnt += 1

        intersection = []
        for followers_cnt in range(len(all_followers_list)):
            intersection.append(all_followers_list[0].intersection(all_followers_list[followers_cnt]))
            print(len(intersection[followers_cnt]))

if __name__ == "__main__":
    args = sys.argv
    #args[0]:Main account, args[1]~:account for compare
    if len(args) < 3:
        print("!!!INPUT more than 2 account!!!")
        sys.exit()
    f_data = Followers_data()
    f_data.make_followers_set(args)
