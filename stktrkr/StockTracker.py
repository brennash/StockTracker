# !/usr/bin/env python
#title           :Time Series Wave Analyzer
#description     :Figures out the points of inflection in time series
#author          :Shane Brennan
#date            :20151224
#version         :0.1
#notes           :
#python_version  :2.7.3
#==============================================================================

import json
import sys
import os
import csv
import urllib2
import datetime
from random import randint
from stktrkr.Stock import Stock
from stktrkr.DataPoint import DataPoint

class StockTracker:
	def __init__(self, verbose=False):
		# Initialize the various SP lists
		self.initSP500()
		self.stockDict = []
		self.verbose = verbose
	
	def readFile(self, filename):
		if self.verbose:
			print 'Opening file',filename
			
		file = open(filename, 'r')
		stringValue = ''
		length = 0
		for line in file:
			stringValue = stringValue + line.rstrip() + ' '
			length += 1
		
		if self.verbose:
			print 'Read',length,'lines from file...'
		return stringValue.rstrip()
	
	
	def process(self, jsonString):
		jsonDict = json.loads(jsonString)
		stocks = jsonDict['stocks']
		sellDate = jsonDict['sell_date']
		
		for stock in stocks:
			name = stock['ticker'].upper()
			buyDate = stock['buy_date']
			if name == 'SP500-RANDOM':
				name = self.getRandomSP500()		

			# Printing verbose output stock name		
			if self.verbose:
				print 'Processing',name		
		
			buyLimit = stock['buy_limit']

			try:
				unitLimit = stock['unit_limit']		
			except KeyError:
				unitLimit = -1
				
			try:
				repeat = stock['repeat']		
			except KeyError:
				repeat = 'never'
			
			# Print the details for each purchase plan
			if self.verbose:
				print 'BuyLimit:{0},UnitLimit:{1},Repeat:{2}'.format(buyLimit,unitLimit,repeat)
			
			# Read the raw stock data
			csvList = self.getCSV(name, buyDate, sellDate)
			
			# Initialise the Stock and add data
			stock = Stock(name, self.verbose)
			stock.addDataPoints(csvList)
			
			# Sort them into date order oldest to newest
			stock.sort()
			
			# Buy the stock and print the details
			stock.buy(buyDate, buyLimit, unitLimit, repeat)
			stock.printDetails()

	def getCSV(self, name, startDate, endDate):
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
	
	def getRandomSP500(self):
		index = randint(0,len(self.sp500))
		return self.sp500[index]	
		
	def initSP500(self):
		self.sp500 =['ABT', 'ABBV', 'ACN', 'ACE', 'ATVI', 'ADBE', \
		'ADT', 'AAP', 'AES', 'AET', 'AFL', 'AMG', 'A', 'GAS', 'APD', \
		'ARG', 'AKAM', 'AA', 'AGN', 'ALXN', 'ALLE', 'ADS', 'ALL', \
		'GOOGL', 'GOOG', 'ALTR', 'MO', 'AMZN', 'AEE', 'AAL', 'AEP' \
		'AXP', 'AIG', 'AMT', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'APC', \
		'ADI', 'AON', 'APA', 'AIV', 'AAPL', 'AMAT', 'ADM', 'AIZ', 'T', \
		'ADSK', 'ADP', 'AN', 'AZO', 'AVGO', 'AVB', 'AVY', 'BHI', 'BLL', \
		'BAC', 'BK', 'BCR', 'BXLT', 'BAX', 'BBT', 'BDX', 'BBBY', 'BRK-B', \
		'BBY', 'BIIB', 'BLK', 'HRB', 'BA', 'BWA', 'BXP', 'BSX', 'BMY', \
		'BRCM', 'BF-B', 'CHRW', 'CA', 'CVC', 'COG', 'CAM', 'CPB', 'COF', \
		'CAH', 'HSIC', 'KMX', 'CCL', 'CAT', 'CBG', 'CBS', 'CELG', 'CNP', \
		'CTL', 'CERN', 'CF', 'SCHW', 'CHK', 'CVX', 'CMG', 'CB', 'CI', \
		'XEC', 'CINF', 'CTAS', 'CSCO', 'C', 'CTXS', 'CLX', 'CME', 'CMS', \
		'COH', 'KO', 'CCE', 'CTSH', 'CL', 'CPGX', 'CMCSA', 'CMA', 'CAG', \
		'COP', 'CNX', 'ED', 'STZ', 'GLW', 'COST', 'CCI', 'CSRA', 'CSX', \
		'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DLPH', 'DAL', \
		'XRAY', 'DVN', 'DO', 'DFS', 'DISCA', 'DISCK', 'DG', 'DLTR', \
		'D', 'DOV', 'DOW', 'DPS', 'DTE', 'DD', 'DUK', 'DNB', 'ETFC', \
		'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMC', 'EMR', \
		'ENDP', 'ESV', 'ETR', 'EOG', 'EQT', 'EFX', 'EQIX', 'EQR', \
		'ESS', 'EL', 'ES', 'EXC', 'EXPE', 'EXPD', 'ESRX', 'XOM', \
		'FFIV', 'FB', 'FAST', 'FDX', 'FIS', 'FITB', 'FSLR', 'FE', \
		'FISV', 'FLIR', 'FLS', 'FLR', 'FMC', 'FTI', 'F', 'FOSL', 'BEN', \
		'FCX', 'FTR', 'GME', 'GPS', 'GRMN', 'GD', 'GE', 'GGP', 'GIS', \
		'GM', 'GPC', 'GILD', 'GS', 'GT', 'GWW', 'HAL', 'HBI', 'HOG', \
		'HAR', 'HRS', 'HIG', 'HAS', 'HCA', 'HCP', 'HP', 'HES', 'HPE', \
		'HD', 'HON', 'HRL', 'HST', 'HPQ', 'HUM', 'HBAN', 'ITW', 'ILMN', \
		'IR', 'INTC', 'ICE', 'IBM', 'IP', 'IPG', 'IFF', 'INTU', 'ISRG', \
		'IVZ', 'IRM', 'JEC', 'JBHT', 'JNJ', 'JCI', 'JPM', 'JNPR', 'KSU', \
		'K', 'KEY', 'GMCR', 'KMB', 'KIM', 'KMI', 'KLAC', 'KSS', 'KHC', \
		'KR', 'LB', 'LLL', 'LH', 'LRCX', 'LM', 'LEG', 'LEN', 'LVLT', \
		'LUK', 'LLY', 'LNC', 'LLTC', 'LMT', 'L', 'LOW', 'LYB', 'MTB', \
		'MAC', 'M', 'MNK', 'MRO', 'MPC', 'MAR', 'MMM', 'MMC', 'MLM', \
		'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MHFI', 'MCK', 'MJN', 'WRK', \
		'MDT', 'MRK', 'MET', 'KORS', 'MCHP', 'MU', 'MSFT', 'MHK', \
		'TAP', 'MDLZ', 'MON', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MUR', \
		'MYL', 'NDAQ', 'NOV', 'NAVI', 'NTAP', 'NFLX', 'NWL', 'NFX', 'NEM', \
		'NWSA', 'NWS', 'NEE', 'NLSN', 'NKE', 'NI', 'NBL', 'JWN', 'NSC', 'NTRS', \
		'NOC', 'NRG', 'NUE', 'NVDA', 'ORLY', 'OXY', 'OMC', 'OKE', 'ORCL', \
		'OI', 'PCAR', 'PH', 'PDCO', 'PAYX', 'PYPL', 'PNR', 'PBCT', 'POM', 'PEP', \
		'PKI', 'PRGO', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PXD', 'PBI', \
		'PCL', 'PNC', 'RL', 'PPG', 'PPL', 'PX', 'PCP', 'PCLN', 'PFG', 'PG', \
		'PGR', 'PLD', 'PRU', 'PEG', 'PSA', 'PHM', 'PVH', 'QRVO', 'PWR', 'QCOM', \
		'DGX', 'RRC', 'RTN', 'O', 'RHT', 'REGN', 'RF', 'RSG', 'RAI', \
		'RHI', 'ROK', 'COL', 'ROP', 'ROST', 'RCL', 'R', 'CRM', 'SNDK', 'SCG', \
		'SLB', 'SNI', 'STX', 'SEE', 'SRE', 'SHW', 'SIG', 'SPG', 'SWKS', 'SLG', \
		'SJM', 'SNA', 'SO', 'LUV', 'SWN', 'SE', 'STJ', 'SWK', 'SPLS', 'SBUX', \
		'HOT', 'STT', 'SRCL', 'SYK', 'STI', 'SYMC', 'SYF', 'SYY', 'TROW', \
		'TGT', 'TEL', 'TE', 'TGNA', 'THC', 'TDC', 'TSO', 'TXN', 'TXT', 'HSY', \
		'TRV', 'TMO', 'TIF', 'TWX', 'TWC', 'TJX', 'TMK', 'TSS', 'TSCO', 'RIG', \
		'TRIP', 'FOXA', 'FOX', 'TSN', 'TYC', 'USB', 'UA', 'UNP', 'UAL', 'UNH', \
		'UPS', 'URI', 'UTX', 'UHS', 'UNM', 'URBN', 'VFC', 'VLO', 'VAR', 'VTR', \
		'VRSN', 'VRSK', 'VZ', 'VRTX', 'VIAB', 'V', 'VNO', 'VMC', 'WMT', 'WBA', \
		'DIS', 'WM', 'WAT', 'ANTM', 'WFC', 'HCN', 'WDC', 'WU', 'WY', 'WHR', \
		'WFM', 'WMB', 'WEC', 'WYN', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XL', \
		'XYL', 'YHOO', 'YUM', 'ZBH', 'ZION', 'ZTS']	
	
