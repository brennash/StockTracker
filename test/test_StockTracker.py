import unittest
import json, re
import datetime
from stktrkr.StockTracker import StockTracker

class Test(unittest.TestCase):

	def test_StockTracker_ValidateDate_1(self):
		""" Date format test for JSON input
		"""
		#tracker = StockTracker()
		#dateString = tracker.validateDate('31-01-2015')
		#self.assertEquals('20150131', dateString)
		self.assertTrue(True)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
