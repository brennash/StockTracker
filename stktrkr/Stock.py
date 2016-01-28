import re
import csv
import urllib2
import datetime
from dateutil.relativedelta import relativedelta
from stktrkr.DataPoint import DataPoint

class Stock:
	def __init__(self, ticker, buyDate, sellDate, buyLimit, unitLimit, repeat, verbose=False):
		# The data around the stock
		self.ticker = ticker
		self.buyDate = buyDate
		self.sellDate = sellDate
		self.buyLimit = buyLimit
		self.unitLimit = unitLimit
		self.repeat = repeat
		self.verbose = verbose
		
		# The stock units bought
		self.purchased = 0.0
		self.units = 0
		self.purchasedList = []
		self.unitsList = []
		self.dateList = []
		
		# The stock data points
		self.dataPoints = []
		
		# The header of the CSV data
		self.header = []
		self.headerSize = 0
		
		# Add the data points
		self.addDataPoints(ticker, buyDate, sellDate)
		self.buy(buyDate, sellDate, buyLimit, unitLimit, repeat)
		
	def addDataPoints(self, ticker, buyDate, sellDate):
		""" Adds a set of data points, which are 
			lists of lists.
		"""
		# Gets the CSV giving the stock data
		csvList = self.getCSV(ticker, buyDate, sellDate)

		# Parse this list and add the data points
		for index, csv in enumerate(csvList):
			self.addDataPoint(index, csv)

		# Sort the data points into date order
		self.dataPoints.sort(key=lambda dp: dp.getDate(), reverse=False)		
			
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

	def getCSV(self, name, startDate, endDate):
		""" Gets the CSV for the particular stock in the specified
			timeframe. Returns this CSV as a list of strings. 
		"""
		startYear, startMonth, startDay = self.getDate(str(startDate))
		endYear, endMonth, endDay = self.getDate(str(endDate))
		url = 'http://real-chart.finance.yahoo.com/table.csv?s='+name
		url = url + '&a='+startMonth+'&b='+startDay+'&c='+startYear
		url = url + '&d='+endMonth+'&e='+endDay+'&f='+endYear+'&g=d&ignore=.csv'
		response = urllib2.urlopen(url)
		cr = csv.reader(response)
		csvList = list(cr)
		return csvList

	def getDate(self, dateValue):
		dateString = str(dateValue)
		year = dateString[0:4]
		month = str(int(dateString[4:6])-1)
		day = str(int(dateString[6:]))
		return year, month, day

	def size(self):
		return len(self.dataPoints)

	def getOpeningPrice(self):
		""" Returns the date and the adjusted price for the first value
			in the set of data points, i.e., the opening date and price.
		"""
		return self.dataPoints[0].getDate(), self.dataPoints[0].getAdjustedValue()

	def getClosingPrice(self):
		""" Returns the closing date and the adjusted price for the first value
			in the set of data points, i.e., the closing date and price.
		"""	
		return self.dataPoints[-1].getDate(), self.dataPoints[-1].getAdjustedValue()
		
	def getPrice(self, searchDate):
		for dataPoint in self.dataPoints:
			date = dataPoint.getDate()
			price = dataPoint.getAdjustedValue()
			if date == searchDate:
				return date, price
			elif date > searchDate:
				break
		return None, None
			
			
		

	def buy(self, buyDate, sellDate, buyLimit, unitLimit, repeat):
		""" Buy shares up to a purchase price limit defined 
			by buyLimit, starting at an initial date defined by
			buyDate, and repeated never/daily/monthly/quarterly.
			
			Returns nothing, just updates the stock details.
		"""
		startDate, startPrice = self.getOpeningPrice()
		maxAmount = int(buyLimit)/int(startPrice)
				
		if repeat == 'never' and maxAmount > 0:
			self.purchased = (maxAmount * startPrice)
			self.units = maxAmount
			self.purchasedList.append(maxAmount * startPrice)
			self.unitsList.append(maxAmount)
			self.dateList = [startDate]	
		else:
			currentDate = startDate
			endDate, endPrice = self.getClosingPrice()
			while currentDate <= endDate:
				date, price = self.getPrice(currentDate)
				if date is not None and price is not None:
					maxAmount = int(buyLimit)/int(price)
					if maxAmount > 0:
						self.purchased += (maxAmount * price)
						self.units += maxAmount
						self.purchasedList.append(maxAmount * price)
						self.unitsList.append(maxAmount)
						self.dateList.append(date)				
				currentDate = self.getNextDate(currentDate, repeat)
	
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

	def totalPurchased(self):
		return self.purchased
		
	def totalUnits(self):
		return self.units

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
