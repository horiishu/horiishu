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
CONSUMER_SECRET = args[1]
ACCESS_TOKEN = '243028271-hNYIWiCNhS5UzdnPLzAF5UkmRnVZAx8N8alZUcrz'
ACCESS_SECRET = args[2]
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

#Make instance of API
api = tweepy.API(auth, wait_on_rate_limit = True)

#Obtain date
date = datetime.date.today()

class Followers_data:
    """Output followers data"""

    def make_followers_set(self, args):
        """Get followers ids list"""
        cnt = 3
        all_followers_list = []

        #Make followers ID data
        for all_followers in args[3:len(args)]:
            print("!!!start get followers data of %s !!!"%all_followers)
            followers_ids = tweepy.Cursor(api.followers_ids, id = args[cnt], cursor = -1).items()
            set_ids = set(followers_ids)
            print(args[cnt] + "'s follwer is " + str(len(set_ids)) + " !!!!!")
            all_followers_list.append(set_ids)
            cnt += 1

        return all_followers_list

    def calc_intersection(self, all_followers_list):
        """Calcration count of both followers"""
        cnt = 2
        intersection = []
        for followers_cnt in range(len(all_followers_list)):
            intersection.append(all_followers_list[0].intersection(all_followers_list[followers_cnt]))
            print(str(date) + " "  + args[3] + " & " + args[followers_cnt + 3] +
                    " = " + str(len(intersection[followers_cnt])))
            cnt += 1

    def write_csv(self, all_followers_list):
        """Write followers count & date"""
        csvfile_writer = open(str(date) + '_followersData_' + args[3] + '.csv', 'a', newline='')
        writer = csv.writer(csvfile_writer)
        cnt = 3
        for write_data in all_followers_list:
            writer.writerow([str(date) + args[cnt] + str(len(write_data))])
            cnt += 1

    def read_csv_data(self):
        """Read hisory of followers count & date"""
        csv_data_list = []
        csv_data_element = []
        csvfile_reader = open(str(date) + '_followersData_' + args[3] + '.csv')
        for row in csv.reader(csvfile_reader):
            csv_data_list.append(row)
        for csv_element in csv_data_list:
            csv_data_element.append(csv_element[0])

        return csv_data_element

    def make_graph(self, csv_data_element):
        """Output data to graph"""
        args1_list = []
        date_list = []
        follower_list = []
        
        #correct args[3] data
        for csv_list in csv_data_element:
            if args[3] in csv_list:
                args1_list.append(csv_list)

        #x axis date
        date_ptn = r"\d{4}-\d{2}-\d{2}"
        for search_date in args1_list:
            date = re.findall(date_ptn, search_date)
            date_list.extend(date)
        
        #y axis account value
        remove_str = date_ptn + args[3]
        remove_int = 10 + len(args[3])
        for search_follower_cnt in args1_list:
            follower_cnt = re.sub(remove_str, '', search_follower_cnt)
            follower_list.append(int(follower_cnt))

        #make graph
        plt.plot(date_list, follower_list, marker="o")
        plt.title("follower value")
        plt.xlabel("date")
        plt.ylabel("value")
        plt.grid(True)
        plt.savefig(args[3] +"_account_value.png")

    def output_html(self):
        """output result html"""

        print('Content-type: text/html\n')
        html = ("""
        <!DOCTYPE html>
        <html>
        <head><title>result_%s</title></head>
        <body>
        <img src='./%s_account_value.png'>
        </body></html>
        """%(str(date),args[3]))
        with open(str(date) + '_followersData_' + args[3] + '.html', 'wb') as file:
            file.write(html.encode('utf-8'))

    def start(self, args):
        """Start"""
        all_follwers_list = self.make_followers_set(args)
        self.calc_intersection(all_follwers_list)
        self.write_csv(all_follwers_list)
        csv_data_element = self.read_csv_data()
        self.make_graph(csv_data_element)
        self.output_html()

if __name__ == "__main__":
    #args = sys.argv
    #args[1]:cosumer_key , args[2]:access_key
    if len(args) < 5:
        print("!!!INPUT more than 2 account!!!")
        sys.exit()
    f_data = Followers_data()
    f_data.start(args)
