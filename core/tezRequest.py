#!/usr/bin/python#
#-*- coding: UTF-8 -*-
#基础包：接口测试的封装װ

import requests
import tezLog as log 

logging = log.getLogger()

def api_test(method, url, data, headers):
    '''
            定义一个请求接口的方法和需要的参数
    method  -   请求方法    str
    url     -   请求地址   str
    data    -   请求参数    str
    headers -   请求头信息 str
    '''
    try:
        if method == 'post':
            results = requests.post(url=url, params=data, headers=headers)
        if method == 'get':
            results = requests.get(url=url, params=data, headers=headers)
        response = results.json()
        #code = response.get('code')
        code = results.status_code
        return code
    except Exception, e:
        logging.error('service is error', e)