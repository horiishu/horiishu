# coding: utf-8
#! /usr/bin/python

from abc import ABCMeta, abstractmethod
import datetime
import shutil

FILEPATH = r"/home/pi/archive/"

class BaseModule(metaclass=ABCMeta):

    def __init__(self):
        self.date = datetime.date.today()

    @abstractmethod
    def open(self):
        """ open"""
        pass
    
    @abstractmethod
    def close(self):
        """ close """
        pass
    
    @abstractmethod
    def start(self):
        """ main roop """
        
    def run(self):
        self.open()
        print("---------- Start Script ----------")
        self.start()
        self.close
        print("---------- Finish Script ----------")

    def __save_html(self):
        """ Make html file """
        html_filename = self.date + "result.html"
        header = self.make_header
        body = self.make_body
        footer = self.make_fooder
        data = header + body + footer

        with open(FILEPATH, 'wb') as file:
            file.write(data.encode('utf-8'))

    def make_header(self):
        header = """
                <!DOCTYPE html>
                <html>
                <head><title>result_%s</title></head>
                """%(self.date)
        return header
    
    def make_body(self):
        body = """
                <body>
                <img src='./%s_account_value.png'>
                </body>
                """%(self.summary)
        return body
    
    def make_footer(self):
        footer = """
                </html>
                """
        return footer
