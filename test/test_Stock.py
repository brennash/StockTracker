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

	def test_Stock_GetPrice_1(self):
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
		
		expected = 10.6
		buyDate = datetime.datetime(2015, 1, 2)
		actualDate, actualPrice = stock.getPrice(buyDate)
		self.assertEquals(expected, actualPrice)

	def test_Stock_GetPrice_2(self):
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
		
		expected = 10.5
		buyDate = datetime.datetime(2015, 1, 1)
		actualDate, actualPrice = stock.getPrice(buyDate)
		self.assertEquals(expected, actualPrice)

	def test_Stock_GetPrice_3(self):
		header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
		line1 = ['2015-01-01', '10.1', '10.2', '10.3', '10.4', '12345', '10.5']
		line3 = ['2015-01-04', '10.1', '10.2', '10.3', '10.4', '12345', '10.7']
		line2 = ['2015-01-03', '10.1', '10.2', '10.3', '10.4', '12345', '10.6']
		csv = []
		csv.append(header)
		csv.append(line1)
		csv.append(line2)
		csv.append(line3)

		stock = Stock('TEST')
		stock.addDataPoints(csv)
		stock.sort()
		
		expected = 10.7
		buyDate = datetime.datetime(2015, 1, 4)
		actualDate, actualPrice = stock.getPrice(buyDate)
		self.assertEquals(expected, actualPrice)

	def test_Stock_Repeat_1(self):
		header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
		line1 = ['2015-01-01', '10.1', '10.2', '10.3', '10.4', '12345', '10.5']
		line3 = ['2015-01-04', '10.1', '10.2', '10.3', '10.4', '12345', '10.7']
		line2 = ['2015-01-03', '10.1', '10.2', '10.3', '10.4', '12345', '10.6']
		csv = []
		csv.append(header)
		csv.append(line1)
		csv.append(line2)
		csv.append(line3)

		stock = Stock('TEST')
		stock.addDataPoints(csv)
		stock.sort()
		
		startDate = datetime.datetime(2015, 1, 1)
		nextDate = datetime.datetime(2015, 1, 2)
		expected = stock.getNextDate(startDate, 'daily')
		self.assertEquals(expected, nextDate)
		
	def test_Stock_Repeat_2(self):
		header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
		line1 = ['2015-01-01', '10.1', '10.2', '10.3', '10.4', '12345', '10.5']
		line3 = ['2015-01-04', '10.1', '10.2', '10.3', '10.4', '12345', '10.7']
		line2 = ['2015-01-03', '10.1', '10.2', '10.3', '10.4', '12345', '10.6']
		csv = []
		csv.append(header)
		csv.append(line1)
		csv.append(line2)
		csv.append(line3)

		stock = Stock('TEST')
		stock.addDataPoints(csv)
		stock.sort()
		
		startDate = datetime.datetime(2015, 1, 1)
		nextDate = datetime.datetime(2015, 1, 8)
		expected = stock.getNextDate(startDate, 'weekly')
		self.assertEquals(expected, nextDate)

	def test_Stock_Repeat_3(self):
		header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
		line1 = ['2015-01-01', '10.1', '10.2', '10.3', '10.4', '12345', '10.5']
		line3 = ['2015-01-04', '10.1', '10.2', '10.3', '10.4', '12345', '10.7']
		line2 = ['2015-01-03', '10.1', '10.2', '10.3', '10.4', '12345', '10.6']
		csv = []
		csv.append(header)
		csv.append(line1)
		csv.append(line2)
		csv.append(line3)

		stock = Stock('TEST')
		stock.addDataPoints(csv)
		stock.sort()
		
		startDate = datetime.datetime(2014, 11, 1)
		nextDate = datetime.datetime(2015, 1, 24)
		expected = stock.getNextDate(startDate, 'quarterly')
		self.assertEquals(expected, nextDate)

	def test_Stock_Repeat_4(self):
		header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
		line1 = ['2015-01-01', '10.1', '10.2', '10.3', '10.4', '12345', '10.5']
		line3 = ['2015-01-04', '10.1', '10.2', '10.3', '10.4', '12345', '10.7']
		line2 = ['2015-01-03', '10.1', '10.2', '10.3', '10.4', '12345', '10.6']
		csv = []
		csv.append(header)
		csv.append(line1)
		csv.append(line2)
		csv.append(line3)

		stock = Stock('TEST')
		stock.addDataPoints(csv)
		stock.sort()
		
		startDate = datetime.datetime(2015, 1, 31)
		nextDate = datetime.datetime(2015, 2, 28)
		expected = stock.getNextDate(startDate, 'monthly')
		self.assertEquals(expected, nextDate)

	def test_Stock_Repeat_5(self):
		header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
		line1 = ['2015-01-01', '10.1', '10.2', '10.3', '10.4', '12345', '10.5']
		line3 = ['2015-01-04', '10.1', '10.2', '10.3', '10.4', '12345', '10.7']
		line2 = ['2015-01-03', '10.1', '10.2', '10.3', '10.4', '12345', '10.6']
		csv = []
		csv.append(header)
		csv.append(line1)
		csv.append(line2)
		csv.append(line3)

		stock = Stock('TEST')
		stock.addDataPoints(csv)
		stock.sort()
		
		startDate = datetime.datetime(2015, 2, 28)
		nextDate = datetime.datetime(2015, 3, 28)
		expected = stock.getNextDate(startDate, 'monthly')
		self.assertEquals(expected, nextDate)
		
	def test_Stock_Daily_1(self):
		""" Tests the weekly repeated purchases...
		"""
		header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
		line1 = ['2015-01-01', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line3 = ['2015-01-02', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line2 = ['2015-01-03', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line3 = ['2015-01-04', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line4 = ['2015-01-05', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line5 = ['2015-01-06', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line6 = ['2015-01-07', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line7 = ['2015-01-08', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line8 = ['2015-01-09', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line9 = ['2015-01-10', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line10 = ['2015-01-11', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line11 = ['2015-01-12', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line12 = ['2015-01-13', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line13 = ['2015-01-14', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line14 = ['2015-01-15', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line15 = ['2015-01-16', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']

		csv = []
		csv.append(header)
		csv.append(line1)
		csv.append(line2)
		csv.append(line3)
		csv.append(line4)
		csv.append(line5)
		csv.append(line6)
		csv.append(line7)
		csv.append(line8)
		csv.append(line9)
		csv.append(line10)
		csv.append(line11)
		csv.append(line12)
		csv.append(line13)
		csv.append(line14)
		csv.append(line15)

		stock = Stock('TEST')
		stock.addDataPoints(csv)
		stock.sort()
		
		expected = 160.0
		buyDate = datetime.datetime(2015, 1, 1)
		
		stock.buyShares(11.0, buyDate, 'daily')
		actualPrice = stock.getTotalStockPurchased()
		self.assertEquals(expected, actualPrice)
		
	def test_Stock_Daily_2(self):
		""" Tests the weekly repeated purchases...
		"""
		header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
		line1 = ['2015-01-01', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line3 = ['2015-01-02', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line2 = ['2015-01-03', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line3 = ['2015-01-04', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line4 = ['2015-01-05', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line5 = ['2015-01-06', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line6 = ['2015-01-07', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line7 = ['2015-01-08', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line8 = ['2015-01-09', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line9 = ['2015-01-10', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line10 = ['2015-01-11', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line11 = ['2015-01-12', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line12 = ['2015-01-13', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line13 = ['2015-01-14', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line14 = ['2015-01-15', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line15 = ['2015-01-16', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']

		csv = []
		csv.append(header)
		csv.append(line1)
		csv.append(line2)
		csv.append(line3)
		csv.append(line4)
		csv.append(line5)
		csv.append(line6)
		csv.append(line7)
		csv.append(line8)
		csv.append(line9)
		csv.append(line10)
		csv.append(line11)
		csv.append(line12)
		csv.append(line13)
		csv.append(line14)
		csv.append(line15)

		stock = Stock('TEST')
		stock.addDataPoints(csv)
		stock.sort()
		
		buyDate = datetime.datetime(2015, 1, 1)		
		stock.buyShares(11.0, buyDate, 'daily')
		unitsList = stock.getListStockUnits()
		testList = True
		for unit in unitsList:
			if unit != 1:
				testList = False
				break
		self.assertTrue(testList)


	def test_Stock_BuyUnits_1(self):
		""" Tests the weekly repeated unit-only purchases...
		"""
		header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
		line1 = ['2015-01-01', '10.1', '10.2', '10.3', '10.4', '12345', '50.0']
		line3 = ['2015-01-02', '10.1', '10.2', '10.3', '10.4', '12345', '20.0']
		line2 = ['2015-01-03', '10.1', '10.2', '10.3', '10.4', '12345', '60.0']
		csv = []
		csv.append(header)
		csv.append(line1)
		csv.append(line2)
		csv.append(line3)

		stock = Stock('TEST')
		stock.addDataPoints(csv)
		stock.sort()
		
		buyDate = datetime.datetime(2015, 1, 2)		
		stock.buyUnitShares(2, 20.0, buyDate, 'never')
		actual = stock.getTotalStockPurchased()
		expected = 20.0
		self.assertEquals(expected, actual)

	def test_Stock_BuyUnits_2(self):
		""" Tests the date select for the buyUnitShares() function
		"""
		header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
		line1 = ['2015-01-01', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line3 = ['2015-01-02', '10.1', '10.2', '10.3', '10.4', '12345', '20.0']
		line2 = ['2015-01-03', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		csv = []
		csv.append(header)
		csv.append(line1)
		csv.append(line2)
		csv.append(line3)

		stock = Stock('TEST')
		stock.addDataPoints(csv)
		stock.sort()
		
		buyDate = datetime.datetime(2015, 1, 1)		
		stock.buyUnitShares(2, 11.0, buyDate, 'daily')
		actual = stock.getTotalStockPurchased()
		expected = 40.0
		self.assertEquals(expected, actual)
		
	def test_Stock_BuyUnits_3(self):
		""" Tests when maxUnits <<< maxBuyLimit, so that only 
			maxUnits is used to determine the stock purchase
		"""
		header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
		line1 = ['2015-01-01', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line3 = ['2015-01-02', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		line2 = ['2015-01-03', '10.1', '10.2', '10.3', '10.4', '12345', '10.0']
		csv = []
		csv.append(header)
		csv.append(line1)
		csv.append(line2)
		csv.append(line3)

		stock = Stock('TEST')
		stock.addDataPoints(csv)
		stock.sort()
		
		buyDate = datetime.datetime(2015, 1, 1)		
		stock.buyUnitShares(1, 1000.0, buyDate, 'daily')
		actual = stock.getTotalStockPurchased()
		expected = 30.0
		self.assertEquals(expected, actual)
		
	def test_Stock_BuyUnits_4(self):
		""" Tests when maxBuyLimit >> share price, so that no
			shares should be purchased
		"""
		header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
		line1 = ['2015-01-01', '10.1', '10.2', '10.3', '10.4', '12345', '1000.0']
		line3 = ['2015-01-02', '10.1', '10.2', '10.3', '10.4', '12345', '1000.0']
		line2 = ['2015-01-03', '10.1', '10.2', '10.3', '10.4', '12345', '1000.0']
		csv = []
		csv.append(header)
		csv.append(line1)
		csv.append(line2)
		csv.append(line3)

		stock = Stock('TEST')
		stock.addDataPoints(csv)
		stock.sort()
		
		buyDate = datetime.datetime(2015, 1, 1)		
		stock.buyUnitShares(10, 100.0, buyDate, 'daily')
		actual = stock.getTotalStockPurchased()
		expected = 0.0
		self.assertEquals(expected, actual)
		
def main():
    unittest.main()

if __name__ == '__main__':
    main()
