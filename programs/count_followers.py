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

class Followers_data:
    """Output followers data"""

    def __init__(self, account_list):
        self.account_list = account_list
        self.followers_set = []
        self.intersection_followers = []

    def get_followers_set(self):
        """ Get followers ids list """
        for account in self.account_list:
            followers_set_data = self.get_followers(account)
            self.followers_set.append(followers_set_data)

    def calc_intersection(self):
        """ get mutual followers data """
        cnt = 0
        for followers_set in self.followers_set:
            if cnt == 0:
                continue
            else:
                self.intersection_followers.append(self.followers_set[0].intersection(followers_set))
    
    def save_csv(self):
        csvfile_writer = open(ACCOUNT_DATA_PATH + 'followersData_' + self.account_list[0] + '.csv', 'a', newline='')
         writer = csv.writer(csvfile_writer)
         for write_data, account_name in zip(self.followers_set, self.account_list):
            writer.writerow([str(self.date) + account_name + str(len(write_data))])
    
    def read_csv(self):
        """Read hisory of followers count & date"""
        csv_data_list = []
        csvfile_reader = open(ACCOUNT_DATA_PATH + 'followersData_' + self.account_list[0] + '.csv')
        for row in csv.reader(csvfile_reader):
            csv_data_list.append(row)

        print(csv_data_list)

if __name__ == "__main__":
    #args[1]: main account , args[2]~: sub account
    ARGS = sys.argv
    
    if ARGS < 1:
        print("Error: Define main account!!!")
    
    ACCOUNTS = ARGS[1:]

    data = Followers_data(ACCOUNTS)
    data.run()