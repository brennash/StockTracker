import re
import datetime

class DataPoint:
	def __init__(self, tokens, header):
		self.data = []
		self.header = header
		self.dateIndex = self.getIndex('Date')

		for index, token in enumerate(tokens):
			if index == self.dateIndex:
				date = datetime.datetime.strptime(token, '%Y-%m-%d')
				self.data.append(date)
			else:
				self.data.append(float(token))

	def getAdjustedValue(self):
		index = self.getIndex('Adj Close')
		return self.data[index]		

	def getDate(self):
		index = self.getIndex('Date')
		return self.data[index]

	def getIndex(self, key):
		try:
			dateIndex = self.header.index(key)
			return dateIndex
		except ValueError:
			print "No Key Values found in Header for",key
			return -1
			
	def printData(self):
		print self.data