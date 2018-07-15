# coding: utf-8
#! /usr/bin/python

import logging

class Logging:
    def __init__(self):
        logger = logging.getLogger('LoggingTest')
        logger.setLevel(10)
        fh = logging.FileHandler('test.log')
        logger.addHandler(fh)
        sh = logging.StreamHandler()
        logger.addHandler(sh)
        formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)

if __name__ == '__main__':
    Logging()
    logger.info('info')
    logger.warning('warning')