#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 验证包：接口测试脚本

import sys
import core.tezLog as log
import function.common as common
import core.tezExcel as excel

reload(sys)
sys.setdefaultencoding('utf8')

logging = log.getLogger()


#1。外部输入参数
path = sys.path[0]


#2.根据module获取Sheet
if len(sys.argv) == 2:
	module = sys.argv[1]
	print 'sheet名称:%s' %module
	logging.info('sheet名称:%s' %module)
	logging.info("-------------- Execute TestCases ---------------")
	sheet = common.get_excel_sheet(path + "\\" + common.filename, module)
	#3.执行测试用例
	res = common.run_test(sheet)
	logging.info("-------------- Get the result ------------ %s\n", res)
else:
	modules = excel.get_sheetNames(path + "\\" + common.filename)
	#print modules
	for module in modules:
		print 'sheet名称:%s' %module
		logging.info('sheet名称:%s' %module)
		logging.info("-------------- Execute TestCases ---------------")
		sheet = common.get_excel_sheet(path + "\\" + common.filename, module)
		#3.执行测试用例
		res = common.run_test(sheet)
		logging.info("-------------- Get the result ------------ %s\n", res)
common.excel_release(path)