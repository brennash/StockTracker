import unittest
import json, re
import datetime
from stktrkr.StockTracker import StockTracker

class Test(unittest.TestCase):

	def test_StockTracker_Init_1(self):
		jsonInput = '{name:\'myIndex\','
		jsonInput = jsonInput + 'sellDate:20151221,'
		jsonInput = jsonInput + 'stocks:['
		jsonInput = jsonInput + '{ticker:\'AMZN\',buyDate:20140101,buyLimit:1000.00}'
		jsonInput = jsonInput + ']}'
		self.assertTrue(True)
		tracker = StockTracker()
		csv = tracker.getCSV('V',20151001,20151031)
		self.assertEquals(23,len(csv))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
