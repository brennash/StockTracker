import re
import csv
import datetime
from stktrkr.DataPoint import DataPoint

class Stock:
	def __init__(self, stockName):
		self.stockName = stockName
		self.dataPoints = []
		self.header = []
		self.headerSize = 0
		
		self.stockUnits = 0
		self.stockPurchaseTotal = 0.0
		self.stockPurchaseAmounts = []
		self.stockPurchaseDates = []
				
	def addDataPoints(self, csvList):
		for index, csv in enumerate(csvList):
			self.addDataPoint(index, csv)
			
	def addDataPoint(self, index, row):
		regex = re.compile('^[a-zA-Z]+')

		# If there's a header
		if regex.match(row[0]) and self.headerSize > 0:
			print "Error reading line",lineIndex
		elif regex.match(row[0]) and self.headerSize == 0:
			self.header = row
			self.headerSize = len(self.header)
		else:
			dp = DataPoint(row, self.header)
			self.dataPoints.append(dp)

	def size(self):
		return len(self.dataPoints)

	def sort(self):
		self.dataPoints.sort(key=lambda dp: dp.getDate(), reverse=False)

	def getOpeningPrice(self):
		return self.dataPoints[0].getDate(), self.dataPoints[0].getAdjustedValue()
	
	def getClosingPrice(self):
		return self.dataPoints[-1].getDate(), self.dataPoints[-1].getAdjustedValue()
	
	def getPriceDiff(self):
		startDate, startPrice = self.getOpeningPrice()
		endDate, endPrice = self.getClosingPrice()
		delta = endDate-startDate
		return delta.days, (endPrice-startPrice)
	
	def buy(self, buyDateInt, buyLimit, unitLimit, repeat):
		startDate, startPrice = self.getOpeningPrice()
		buyDate = datetime.datetime.strptime(str(buyDateInt), '%Y%m%d')
		
		# Make sure the official buyDate is within 5 days of the 
		# starting data for the stock (i.e., weekends etc.)
		if startDate + datetime.timedelta(days = 4) > buyDate:
			openDate, openPrice = self.getOpeningPrice()
		else:
			print self.stockName,"the buyDate (",buyDate,") is removed from the startDate (",startDate,")"
			exit(1)
	
	def buyShares(self, upperLimit):
		startDate, startPrice = self.getOpeningPrice()
		total = int(upperLimit)/int(startPrice)
		return total, (total*startPrice)
		
	def buyUnitShares(self, units, upperLimit):
		startDate, startPrice = self.getOpeningPrice()
		total = int(upperLimit)/int(startPrice)
		if total > units:
			return units, (units*startPrice)
		else:
			return total, (total*startPrice)	