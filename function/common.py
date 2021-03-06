#!/usr/bin/python
# -*- coding: UTF-8 -*-
#基础包：接口测试的封装

import core.tezExcel as excel
import core.tezLog as log
import core.tezRequest as request 
from prettytable import PrettyTable
import gl 
from matplotlib.delaunay.testfuncs import TestData
from core.tezRequest import logging
import sys
import time
import json

filename = gl.FILE_NAME

def writeTxt(fileName, inputText):
    fileName = fileName
    file_obj = open(fileName, 'a+')
    file_obj.write(inputText)
    
    file_obj.close()

def get_excel_sheet(path, module):
    #依据模块名称获取sheet
    excel.open_excel(path)
    return excel.get_sheet(module)

def data_conversion(params):
    data_param = {}
    if params:
        for param in params.split('&'):
            index_tmp = param.find('=')
            data_param[param[:index_tmp]] = param[index_tmp + 1:]
    return data_param

def run_test(sheet):
    rows = excel.get_rows(sheet)
    fail = 0 
    for i in range(2, rows):
        testNumber      = str(int(excel.get_content(sheet, i, gl.CASE_NUMBER)))
        testData        = data_conversion(excel.get_content(sheet, i, gl.CASE_DATA)) 
        testName        = excel.get_content(sheet, i, gl.CASE_NAME)
        testUrl         = excel.get_content(sheet, i, gl.CASE_URL)
        testMethod      = excel.get_content(sheet, i, gl.CASE_METHOD)
        testHeaders     = data_conversion(excel.get_content(sheet, i, gl.CASE_HEADERS))
        testCode        = excel.get_content(sheet, i, gl.CASE_CODE)
        testExcept      = data_conversion(excel.get_content(sheet, i, gl.CASE_EXCEPT))
        actualCode      = str(request.api_test(testMethod, testUrl, testData, testHeaders)[0])
        expectCode      = str(int(testCode))
        testActual      = request.api_test(testMethod, testUrl, testData, testHeaders)[1]
        
        failResults     = PrettyTable(["Number", "Method", "Url", "Data", "ExpectCode", "ActualCode", "testExcept", "testAcual"])
        failResults.align["Number"] = "1"
        failResults.padding_width = 1
        failResults.add_row([testNumber, testMethod, testUrl, json.dumps(testData), expectCode, actualCode, json.dumps(testExcept), json.dumps(testActual)]) 
        if actualCode != expectCode:
            logging.info("Number %s", testNumber)
            logging.info("FailCase %s", testName)
            logging.info("FailureInfo")
            logging.info("\n" + str(failResults))
            print "FailureInfo"
            print failResults
            fail += 1    
        else:
            for key_tmp in testExcept:
                if not testActual.has_key(key_tmp) and testActual[key_tmp] == testExcept[key_tmp]:
                    logging.info("Number %s", testNumber)
                    logging.info("FailCase %s", testName)
                    logging.info("FailureInfo")
                    logging.info("\n" + str(failResults))
                    print "FailureInfo"
                    print failResults
                    fail += 1  
    if fail > 0:
        return False
    return True

def excel_release(path):
    excel.release(path)