import unittest
import json, re
import datetime
from stktrkr.Stock import Stock

class Test(unittest.TestCase):

	def test_Stock_Init_1(self):
		header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
		line1 = ['2015-01-01', '10.1', '10.2', '10.3', '10.4', '12345', '10.5']
		line2 = ['2015-01-03', '10.1', '10.2', '10.3', '10.4', '12345', '10.6']
		line3 = ['2015-01-04', '10.1', '10.2', '10.3', '10.4', '12345', '10.7']
		csv = []
		csv.append(header)
		csv.append(line1)
		csv.append(line2)
		csv.append(line3)

		stock = Stock('TEST')
		stock.addDataPoints(csv)
		stock.sort()
		
		expected = 3
		actual = stock.size()
		self.assertEquals(expected, actual)
		
def main():
    unittest.main()

if __name__ == '__main__':
    main()
