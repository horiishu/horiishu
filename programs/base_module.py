# coding: utf-8
#! /usr/bin/python

from abc import ABCMeta, abstractmethod
import datetime
import shutil
import re
from library.tweepy_api import TweepyAPI

FILEPATH = r"/home/araragi/archive/"

class BaseModule(metaclass=ABCMeta):

    def __init__(self):
        self.date = str(datetime.date.today())
        self.img = None
        self.tweepy = TweepyAPI()

    @abstractmethod
    def open(self):
        """ open"""
        pass
    
    @abstractmethod
    def close(self):
        """ close """
        self.save_html()
    
    @abstractmethod
    def start(self):
        """ main roop """
        pass

    @abstractmethod
    def get_sumarry(self):
        pass

    def run(self):
        self.open()
        print("---------- Start Script ----------")
        self.start()
        print("---------- Finish Script ----------")
        self.close()

    def save_html(self):
        """ Make html file """
        print("===== save html ====")
        html_filename = self.date + "result.html"
        header = self.make_header()
        body = self.make_body()
        footer = self.make_footer()
        data = header + body + footer

        with open(FILEPATH + html_filename, 'wb') as file:
            file.write(data.encode('utf-8'))

    def make_header(self):
        header = """
                <!DOCTYPE html>
                <html>
                <head><title>result_%s</title></head>
                """%(self.date)
        return header
    
    def make_body(self):
        body = "<body>" + self.data() + "</body>"
        return body

    def data(self):
        data = """
                <h1> Result </h1>
                <hr>
                <table border=”1″>
                """
        for item_list in self.get_sumarry():
            data += "<tr>"
            for item in item_list:
                data += "<td>" + item + "</td>"
            data += "</tr>"
        data += "</table>"

        if self.img:
            img_data = ""
            for img in self.img:
                img_data += "<img src='" + img + "'>"
            return data + img_data

        return data
    
    def make_footer(self):
        footer = """
                </html>
                """
        return footer
