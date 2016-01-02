import re
import csv
import datetime
from dateutil.relativedelta import relativedelta
from stktrkr.DataPoint import DataPoint

class Stock:
	def __init__(self, stockName, verbose=False):
		# The data around the stock
		self.stockName = stockName
		self.dataPoints = []
		
		self.purchaseUnits = 0
		self.purchaseTotal = 0.0
		self.purchaseUnitsList = []
		self.purchaseTotalList = []
		self.purchaseDateList = []
		
		self.verbose = verbose
		
		# The header of the CSV data
		self.header = []
		self.headerSize = 0
						
	def addDataPoints(self, csvList):
		""" Adds a set of data points, which are 
			lists of lists.
		"""
		for index, csv in enumerate(csvList):
			self.addDataPoint(index, csv)
			
	def addDataPoint(self, index, row):
		""" Adds a data point given the index and 
			row, which are a list of lists.
		"""
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
	
	def getPrice(self, dateValue):
		""" Returns the date and value for a stock for a given date.
		"""
		prevDate = self.dataPoints[0].getDate()
		for index, dataPoint in enumerate(self.dataPoints):
			if dataPoint.getDate() == dateValue:
				return dataPoint.getDate(), dataPoint.getAdjustedValue()
			elif prevDate < dateValue and dateValue < dataPoint.getDate():
				return dataPoint.getDate(), dataPoint.getAdjustedValue()
			prevDate = dataPoint.getDate()
		return None, None
	
	def getPriceDiff(self):
		startDate, startPrice = self.getOpeningPrice()
		endDate, endPrice = self.getClosingPrice()
		delta = endDate-startDate
		return delta.days, (endPrice-startPrice)
	
	def buy(self, buyDateInt, buyLimit, unitLimit, repeat):
		startDate, startPrice = self.getOpeningPrice()
		buyDate = datetime.datetime.strptime(str(buyDateInt), '%Y%m%d')
					
		# If there's not share unit limit and the stock price
		# is less than the purchase limit
		if unitLimit == -1 and startPrice < buyLimit:
			self.buyShares(buyLimit, buyDate, repeat)

		# Else if there's a stock unit limit and you 
		# can afford 
		elif unitLimit > 0 and (unitLimit*startPrice) < buyLimit:
			self.buyUnitShares(unitLimit, buyLimit, buyDate, repeat)

	
	def buyShares(self, buyLimit, buyDate, repeat):
		""" Buy shares up to a purchase price limit defined 
			by buyLimit, starting at an initial date defined by
			buyDate, and repeated never/daily/monthly/quarterly.
			
			Returns nothing, just updates the stock details.
		"""
		startDate, startPrice = self.getOpeningPrice()
		maxAmount = int(buyLimit)/int(startPrice)
		
		if self.verbose:
			dateString = startDate.strftime('%d/%m/%Y')
			print 'StartDate:{0},StartPrice:{1:.1f}'.format(startDate, startPrice)
			print 'MaxUnits:{0}'.format(maxAmount)
		
		if repeat == 'never' and maxAmount > 0:
			self.purchaseTotal = (maxAmount * startPrice)
			self.purchaseUnits = maxAmount
			self.purchaseTotalList.append(maxAmount * startPrice)
			self.purchaseUnitsList.append(maxAmount)
			self.purchaseDateList = [startDate]	
		else:
			currentDate = startDate
			endDate, endPrice = self.getClosingPrice()
			while currentDate <= endDate:
				date, price = self.getPrice(currentDate)
				maxAmount = int(buyLimit)/int(price)
				if maxAmount > 0:
					self.purchaseTotal += (maxAmount * price)
					self.purchaseUnits += maxAmount
					self.purchaseTotalList.append(maxAmount * price)
					self.purchaseUnitsList.append(maxAmount)
					self.purchaseDateList.append(date)				
				currentDate = self.getNextDate(currentDate, repeat)

	def buyUnitShares(self, unitLimit, buyLimit, buyDate, repeat):
		""" Buy a number of shares up to a unit limit defined 
			by unitLimit, starting at an initial date defined by
			buyDate, and repeated never/daily/monthly/quarterly.
			The buyLimit rather than the unitLimit is the more 
			important limiting factor. 
			
			Returns nothing, just updates the stock details.
		"""
		startDate, startPrice = self.getOpeningPrice()
		maxUnits = int(buyLimit) / int(startPrice)
		if maxUnits > unitLimit:
			maxUnits = unitLimit
			
		if repeat.lower() == 'never' and maxUnits > 0:
			self.purchaseTotal = (maxUnits * startPrice)
			self.purchaseUnits = maxUnits
			self.purchaseTotalList.append(maxUnits * startPrice)
			self.purchaseUnitsList.append(maxUnits)
			self.purchaseDateList = [startDate]	
		elif repeat.lower() != 'never':
			currentDate = startDate
			endDate, endPrice = self.getClosingPrice()
			while currentDate <= endDate:
				date, price = self.getPrice(currentDate)
				maxUnits = int(buyLimit) / int(startPrice)
				if maxUnits > unitLimit:
					maxUnits = unitLimit
				if maxUnits > 0:
					self.purchaseTotal += (maxUnits * price)
					self.purchaseUnits += maxUnits
					self.purchaseTotalList.append(maxUnits * price)
					self.purchaseUnitsList.append(maxUnits)
					self.purchaseDateList.append(date)				
				currentDate = self.getNextDate(currentDate, repeat)	
		else:
			print 'ERROR',unitLimit,buyLimit,buyDate,repeat
			print 'MaxUnits',maxUnits
			print 'startPrice',startPrice
	
	def getNextDate(self, currentDate, repeat):
		""" Gets the next date, depending on the input, i.e., 
			quartely, monthly, weekly or daily.
		"""
		if repeat.lower() == 'quarterly':
			updatedDate = currentDate + relativedelta(weeks=12)
		elif repeat.lower() == 'monthly':
			updatedDate = currentDate + relativedelta(weeks=4)
		elif repeat.lower() == 'weekly':
			updatedDate = currentDate + relativedelta(weeks=1)
		elif repeat.lower() == 'daily':
			updatedDate = currentDate + relativedelta(days=1)
		else:
			updatedDate = currentDate
		return updatedDate

	def getTotalStockPurchased(self):
		return self.purchaseTotal
		
	def getListStockUnits(self):
		return self.purchaseUnitsList

	def printDetails(self):
		openingDate, openingPrice = self.getOpeningPrice()
		closingDate, closingPrice = self.getClosingPrice()

		openingDateStr = openingDate.strftime('%d/%m/%Y')
		closingDateStr = closingDate.strftime('%d/%m/%Y')
		closingTotal = self.purchaseUnits * closingPrice
		
		if self.purchaseTotal > 0.0:
			profit = closingTotal - self.purchaseTotal
			percentage = (profit * 100.0) / self.purchaseTotal
		else:
			profit = 0.0
			percentage = 0.0

		print '\n{0}'.format(self.stockName)
		print 'Units:{0:.1f}, Total:{1:.2f}'.format(self.purchaseUnits, self.purchaseTotal)

		print 'Opening Price per Unit:{0:.2f}, Opening Date:{1}'.format(openingPrice, openingDateStr)
		print 'Closing Price per Unit:{0:.2f}, Closing Date:{1}'.format(closingPrice, closingDateStr)

		print 'Closing Total:{0:.2f}'.format(closingTotal)
		print 'Profit:{0:.2f}, Percentage:{1:.1f} %'.format(profit, percentage)
		
		if len(self.purchaseDateList) > 1:
			print '\nStock,Date,Units,Amount'
			for index, date in enumerate(self.purchaseDateList):
				dateStr = date.strftime('%d/%m/%Y')
				amount = self.purchaseTotalList[index]
				units = self.purchaseUnitsList[index]
				print '{0},{1},{2},{3:.2f}'.format(self.stockName,dateStr,units,amount)
			print '{0},{1},{2},{3:.2f}'.format('Total',closingDateStr,self.purchaseUnits,self.purchaseTotal) 
