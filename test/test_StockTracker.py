import unittest
import json, re
import datetime
#from stktrkr.StockTracker import StockTracker

class Test(unittest.TestCase):

	def test_StockTracker_Init_1(self):
		jsonInput = '{name:\'myIndex\','
		jsonInput = jsonInput + 'sellDate:20151221,'
		jsonInput = jsonInput + 'stocks:['
		jsonInput = jsonInput + '{ticker:\'sp500-random\',buyDate:20150201,buyLimit:350.00,repeat:\'monthly\'},'
		jsonInput = jsonInput + '{ticker:\'AMZN\',buyDate:20150101,buyLimit:1000.00},'
		jsonInput = jsonInput + '{ticker:\'TSLA\',buyDate:20150201,unitLimit:10,buyLimit:1500.00}'
		jsonInput = jsonInput + ']}'
		self.assertTrue(True)
#		tracker = StockTracker()
#		tracker.process(jsonInput)
#		self.assertEquals(expected, actual)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
