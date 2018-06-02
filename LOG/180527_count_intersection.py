# coding: utf-8
#! /usr/bin/python

import tweepy
import sys
import csv
import datetime
import subprocess

#matplotlib inline
import matplotlib.pyplot as plt

CONSUMER_KEY = '9OMN7bmOmIgVMBcVqpZFEUFDn'
CONSUMER_SECRET ='bbTmJA1EPyuFj3XPpiTAqLgIpKf4VbeStyEowWrKzdXtcbDKRy'
ACCESS_TOKEN = '243028271-hNYIWiCNhS5UzdnPLzAF5UkmRnVZAx8N8alZUcrz'
ACCESS_SECRET = 'T33eCZuJsPn4PWIYPeYkyXl8gagACN1eETCXrWGIXICLK'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

#Make instance of API

api = tweepy.API(auth, wait_on_rate_limit = True)
date = datetime.date.today()

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
            print(args[cnt] + "'s follwer is " + str(len(set_ids)) + " !!!!!")
            all_followers_list.append(set_ids)
            cnt += 1

        return all_followers_list

    def calc_intersection(self, all_followers_list):
        cnt = 2
        intersection = []
        for followers_cnt in range(len(all_followers_list)):
            intersection.append(all_followers_list[0].intersection(all_followers_list[followers_cnt]))
            print(str(date) + " "  + args[1] + " & " + args[followers_cnt + 1] + " = " + str(len(intersection[followers_cnt])))
            cnt += 1

    def write_csv(self, all_followers_list):
        csvfile_writer = open(args[1] + '.csv', 'a', newline='')
        writer = csv.writer(csvfile_writer)
        cnt = 1
        for write_data in all_followers_list:
            writer.writerow([str(date) + args[cnt] + str(len(write_data))])
            cnt += 1

    def read_csv_data(self):
        csv_data_list = []
        csvfile_reader = open(args[1] + '.csv')
        for row in csv.reader(csvfile_reader):
            csv_data_list.append(row)

        return csv_data_list

    def make_graph(self, csv_data_list):
        args1_list = []
        for search_args_1 in csv_data_list:
            wao = search_args_2.find(args[1])
            if wao == True:
                rgs1_list.append(wao)
        print(args1_list)

    def start(self, args):
        all_follwers_list = self.make_followers_set(args)
        self.calc_intersection(all_follwers_list)
        self.write_csv(all_follwers_list)
        csv_data_list = self.read_csv_data()
        self.make_graph(csv_data_list)

if __name__ == "__main__":
    args = sys.argv
    #args[0]:Main account, args[1]~:account for compare
    if len(args) < 3:
        print("!!!INPUT more than 2 account!!!")
        sys.exit()
    f_data = Followers_data()
    f_data.start(args)
