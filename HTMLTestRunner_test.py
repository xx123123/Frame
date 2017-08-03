#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import core.tezLog as log
import function.common as common
import core.tezExcel as excel
import core.tezRequest as request 
import gl
import unittest
import HTMLTestRunner,sys,StringIO

reload(sys)
sys.setdefaultencoding('utf8')

class FramedTestCase(unittest.TestCase):
	def __init__(self, methodName='runTest', param=None, actualCode=None, expectCode=None, info=None):
		super(FramedTestCase, self).__init__(methodName)
		self.param = param
		self.actualCode = actualCode
		self.expectCode = expectCode
		self.info		= info
	@staticmethod
	def Frame(testcase_klass, param=None, actualCode=None, expectCode=None, info=None):
		testloader 	= unittest.TestLoader()
		testnames	= testloader.getTestCaseNames(testcase_klass)
		suite 		= unittest.TestSuite()
		for name in testnames:
			#suite.addTest(testcase_klass(name, param=param))
			sheet = common.get_excel_sheet(path + "\\" + common.filename, param)
			rows = excel.get_rows(sheet)
			for i in range(2, rows):
				testNumber      = str(int(excel.get_content(sheet, i, gl.CASE_NUMBER)))
				testData        = common.data_conversion(excel.get_content(sheet, i, gl.CASE_DATA)) 
				testName        = excel.get_content(sheet, i, gl.CASE_NAME)
				testUrl         = excel.get_content(sheet, i, gl.CASE_URL)
				testMethod      = excel.get_content(sheet, i, gl.CASE_METHOD)
				testHeaders     = common.data_conversion(excel.get_content(sheet, i, gl.CASE_HEADERS))
				testCode        = excel.get_content(sheet, i, gl.CASE_CODE)
				actualCode      = str(request.api_test(testMethod, testUrl, testData, testHeaders)[0])
				expectCode      = str(int(testCode))
				info			= testName
				suite.addTest(testcase_klass(name, param=param, actualCode=actualCode, expectCode=expectCode, info=info))
				#print info
		return suite
	
	def setUp(self):
		#print 'setUp'
		
		pass

	def tearDown(self):
		#print 'tearDown'
		#excel.release(path)
		pass
	

class TestOne(FramedTestCase):
	def test_Frame(self):
		print 'actual-->' + str(self.actualCode)
		print 'except-->' + str(self.expectCode)
		self.assertEqual(self.actualCode, self.expectCode, str(self.info))

#添加Suite

def Suite():
	global path
	path = sys.path[0]
	global modules
	modules = excel.get_sheetNames(path + "\\" + common.filename)
	suiteTest = unittest.TestSuite()
	for module in modules:
		suiteTest.addTest(FramedTestCase.Frame(TestOne, param=module))
	excel.release(path)
	return suiteTest

if __name__ == '__main__':
    #确定生成报告的路径
    filePath = "pyResult.html"
    fp = file(filePath,'wb')

    #生成报告的Title,描述
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='Python Test Report',description='This  is Python  Report')
    runner.run(Suite())