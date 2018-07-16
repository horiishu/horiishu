# coding: utf-8
#! /usr/bin/python

import sys
import csv
import subprocess
import re
import os

#matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

ACCOUNT_DATA_PATH = r"/home/pi/archive/tweepy_data/"

class Followers_data(BaseModule):
    """Output followers data"""

    def __init__(self, account_list):
         # Use base_module construster
        super(Followers_data, self).__init__()

        self.account_list = account_list
        self.followers_set = []
        self.intersection_followers = []
        self.summary_data = []
        self.csv_data_list

    def get_followers_set(self):
        """ Get followers ids list """
        for account in self.account_list:
            followers_set_data = self.tweepy.get_followers(account)
            self.followers_set.append(followers_set_data)
        self.summary_data.append(self.account_list[0], "N/A", str(len(self.followers_set[0])))

    def calc_intersection(self):
        """ get mutual followers data """
        cnt = 0
        for followers_set in self.followers_set:
            if cnt == 0:
                cnt += 1
                continue
            else:
                intersection_data = self.followers_set[0].intersection(followers_set)
                self.intersection_followers.append(intersection_data)
                self.summary_data.append(self.account_list[cnt], str(len(intersection_data)), \
                                            str(len(self.account_list)))
            cnt += 1
    
    def save_csv(self):
        csvfile_writer = open(ACCOUNT_DATA_PATH + 'followersData_' \
                        + self.account_list[0] + '.csv', 'a', newline='')
        writer = csv.writer(csvfile_writer)
        for write_data, account_name in zip(self.followers_set, self.account_list):
            writer.writerow([str(self.date) + account_name + str(len(write_data))])
    
    def read_csv(self):
        """Read hisory of followers count & date"""
        csv_data_list = []
        csvfile_reader = open(ACCOUNT_DATA_PATH + 'followersData_' + self.account_list[0] + '.csv')
        for row in csv.reader(csvfile_reader):
            self.csv_data_list.append(row)

    def make_graph(self):
        """Output data to graph"""
        main_account_data = []
        date_list = []
        follower_list = []
        
        #correct args[3] data
        for csv_list in self.csv_data_list:
            if self.account_list[0] in csv_list:
                main_account_data.append(csv_list)

        #x axis date
        date_ptn = r"\d{4}-\d{2}-\d{2}"
        for search_date in main_account_data:
            date = re.findall(date_ptn, search_date)
            date_list.extend(date)
        
        #y axis account value
        remove_str = date_ptn + self.account_list[0]
        remove_int = 10 + len(self.account_list[0])
        for search_follower_cnt in main_account_data:
            follower_cnt = re.sub(remove_str, '', search_follower_cnt)
            follower_list.append(int(follower_cnt))

        #make graph
        plt.plot(date_list, follower_list, marker="o")
        plt.title("follower value")
        plt.xlabel("date")
        plt.ylabel("value")
        plt.grid(True)
        file_name = ACCOUNT_DATA_PATH + self.account_list[0] + "_account_value.png"
        plt.savefig(file_name)
        self.img = [file_name]

    def start(self):
        """ main roop """
        self.summary_data = ["", "Mutual num", "Total num"]
        self.get_followers_set()
        self.calc_intersection()
        self.save_csv()
        self.read_csv()
        self.make_graph()

    def get_sumarry(self):
        """ get result """
        return self.summary_data

if __name__ == "__main__":
    #args[1]: main account , args[2]~: sub account
    ARGS = sys.argv
    
    if ARGS < 1:
        print("Error: Define main account!!!")
    
    ACCOUNTS = ARGS[1:]

    data = Followers_data(ACCOUNTS)
    data.run()