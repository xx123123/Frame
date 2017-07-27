#!/usr/bin/python
# -*- coding: UTF-8 -*-
#基础包：日志服务
import logging
import time
import sys

def getLogger():
    global tezLogPath 
    tezLogPath = sys.path[0]
    try:
        tezLogPath
    except NameError:
        tezLogPath = '/data/log/apiTest'

    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    file = tezLogPath + time.strftime("%Y-%m-%d", time.localtime()) + ".log"
    f = open(file, 'w')
    f.close()
    logging.basicConfig(filename=file, level=logging.INFO, format=FORMAT)
    #logging.basicConfig(level=logging.INFO, format=FORMAT)
    return logging