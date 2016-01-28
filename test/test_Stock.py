import unittest
import json, re
import datetime
from stktrkr.Stock import Stock

class Test(unittest.TestCase):

	def test_Stock_Init_1(self):
		stock = Stock('AMZN', 20150111, 20160115, 1000.0, 10.0, 'never', False)
		date, price = stock.getOpeningPrice()
		self.assertTrue(price > 0.0 and price < 1000.0)
		
	def test_Stock_Init_2(self):
		stock = Stock('AMZN', 20160111, 20160115, 1000.0, 10.0, 'never', False)
		date, price = stock.getOpeningPrice()
		self.assertTrue(price > 500.0 and price < 750.0)
		
	def test_Stock_Init_3(self):
		stock = Stock('AAPL', 20160127, 20160127, 100.0, 2.0, 'never', False)
		date, price = stock.getOpeningPrice()
		self.assertTrue(price > 93.0 and price < 97.0)

	def test_Stock_Init_4(self):
		stock = Stock('AAPL', 20160126, 20160127, 100.0, 2.0, 'daily', False)
		price = stock.totalPurchased()
		self.assertTrue(price > 185.0 and price < 200.0)

	def test_Stock_Init_5(self):
		stock = Stock('AAPL', 20160125, 20160127, 100.0, 2.0, 'daily', False)
		price = stock.totalPurchased()
		self.assertTrue(price > 250.0 and price < 300.0)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
