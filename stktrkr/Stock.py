import re
import csv
from tswa.DataPoint import DataPoint

class TimeSeries:
	def __init__(self, stockName):
		self.stockName = stockName
		self.dataPoints = []
		self.header = []
		self.headerSize = 0
		
	def buyShares(self, totalShares):
		shares = totalShares
		totalInvested = shares*self.dataPoints[0].getAdjustedValue()
		totalAtEnd = shares*self.dataPoints[-1].getAdjustedValue()
		profit = totalAtEnd-totalInvested
		print 'Start:{0:.2f} End:{1:.2f}'.format(totalInvested, totalAtEnd)
		print 'Total Profit:{0:.2f}'.format(profit)
		print 'Tax:{0:.2f}'.format(profit*0.2)
		print 'Net Profit:{0:.2f}'.format(profit*0.8)
		
		
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

	def getElement(self, index):
		if index >= 0 and index < len(self.dataPoints):
			return self.dataPoints[index]
		else:
			print "Error - no element at index",index
			return None
			
	def getMinimum(self, startDate, endDate):
		""" Gets the minimum adjusted closing value between 
		    two specified dates. The presumption is the self.dataPoints
		    array is sorted from earliest to latest dates
		"""
		startIndex = self.getFirstIndex(startDate)
		endIndex = self.getLastIndex(endDate)
		
		minValue = self.dataPoints[startIndex].getAdjustedValue()
		minDate = self.dataPoints[startIndex].getDate()
		
		for x in xrange(startIndex, endIndex+1):
			if self.dataPoints[x].getAdjustedValue() < minValue:
				minValue = self.dataPoints[x].getAdjustedValue()
				minDate = self.dataPoints[x].getDate()

		return minDate, minValue
		
	def getMaximum(self, startDate, endDate):
		""" Gets the maximum adjusted closing value between 
		    two specified dates. The presumption is the self.dataPoints
		    array is sorted from earliest to latest dates
		"""
		startIndex = self.getFirstIndex(startDate)
		endIndex = self.getLastIndex(endDate)
		
		maxValue = self.dataPoints[startIndex].getAdjustedValue()
		maxDate = self.dataPoints[startIndex].getDate()
		
		for x in xrange(startIndex, endIndex+1):
			if self.dataPoints[x].getAdjustedValue() > maxValue:
				maxValue = self.dataPoints[x].getAdjustedValue()
				maxDate = self.dataPoints[x].getDate()
		return maxDate, maxValue
	
		
	def getNextMaximum(self, startDate):
		""" Gets the next maximum adjusted closing value after 
		    a specified date. If the next maximum isn't found it
		    returns a zero and the startDate.
		"""
		startIndex = self.getFirstIndex(startDate)
		endIndex = len(self.dataPoints) - 1
		
		maxValue = 0
		maxDate = startDate

		lastValue1 = self.dataPoints[startIndex].getAdjustedValue()
		lastValue2 = self.dataPoints[startIndex].getAdjustedValue()
		lastValue3 = self.dataPoints[startIndex].getAdjustedValue()
		
		for x in xrange(startIndex, endIndex+1):
			currentValue = self.dataPoints[x].getAdjustedValue()
			if self.dataPoints[x].getAdjustedValue() > maxValue:
				maxValue = self.dataPoints[x].getAdjustedValue()
				maxDate = self.dataPoints[x].getDate()
		return maxDate, maxValue	
			
	def getNextMinimum(self, startDate):
		""" Gets the next maximum adjusted closing value after 
		    a specified date. If the next maximum isn't found it
		    returns a zero and the startDate.
		"""
		startIndex = self.getFirstIndex(startDate)
		endIndex = len(self.dataPoints) - 1
		
		value = 0
		date = startDate
		
		for x in xrange(startIndex, endIndex+1):
			if self.dataPoints[x].getAdjustedValue() > maxValue:
				value = self.dataPoints[x].getAdjustedValue()
				date = self.dataPoints[x].getDate()
		return date, value	


	def getFirstIndex(self, searchDate):
		if searchDate < self.dataPoints[0].getDate():
			return 0
		else:
			for index, dataPoint in enumerate(self.dataPoints):
				if searchDate == dataPoint.getDate():
					return index
		return -1

	def getLastIndex(self, searchDate):
		if searchDate > self.dataPoints[-1].getDate():
			return (len(self.dataPoints)-1)
		else:	
			index = (len(self.dataPoints)-1)
			for dataPoint in reversed(self.dataPoints):
				if searchDate == dataPoint.getDate():
					return index
				index -= 1
		return -1
	
	def getFirstDate(self):
		return self.dataPoints[0].getDate()
		
	def getLastDate(self):
		return self.dataPoints[-1].getDate()
	
	def printAllDates(self):
		""" Helper function to print all the dates in the order 
			they are currently stored. 
		"""
		for index, dataPoint in enumerate(self.dataPoints):
			print index, dataPoint.getDate()
