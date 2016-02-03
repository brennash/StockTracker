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
import datetime
import re
from random import randint
from stktrkr.Stock import Stock
from stktrkr.DataPoint import DataPoint

class StockTracker:
	def __init__(self, verbose=False):
		# Initialize the various SP lists
		self.stockList = []
		self.verbose = verbose
	
	def readFile(self, filename):
		""" Read in the input JSON string specifying the fund 
			to be generated. Each input file must containing only
			one valid JSON string. 
		"""
		if self.verbose:
			print 'Opening file',filename
			
		file = open(filename, 'r')
		jsonString = ''
		
		num = 0
		for line in file:
			jsonString = jsonString + ' ' + line.rstrip()
		
		return jsonString
	
	
	def process(self, jsonString):
		""" This function takes as input the a single file 
			containing one valid JSON string, spread over 
			one or more lines. 
		"""		
		
		# Load the JSON string for the fund
		try:
			jsonDict = json.loads(jsonString)
		except ValueError:
			print 'ERROR - Invalid JSON...'
			print jsonString
			exit(1)
	
		# Parse the JSON data
		jsonDict = json.loads(jsonString)
		name = jsonDict['name']
		sellDate = jsonDict['sell_date']
		stocks = jsonDict['stocks']

		# Output the name of the fund
		if self.verbose:
			print 'Processing {0}...'.format(name)
		
		for stock in stocks:
			ticker = stock['ticker'].upper()
			
			if ticker == 'RANDOM':
				ticker = self.getRandomTicker()	
			
			buyDate = stock['buy_date']
			buyLimit = stock['buy_limit']
			
			# Get the optional parameters, unit limit
			try:
				unitLimit = stock['unit_limit']		
			except KeyError:
				unitLimit = -1
			
			# And the optional parameter, repeat interval
			try:
				repeat = stock['repeat']		
			except KeyError:
				repeat = 'never'
			
			# Output the stock details if verbose is enabled
			if self.verbose:
				print '{0}, BuyDate:{1}, BuyLimit:{2}, UnitLimit{3}, Repeat:{4}'.format(ticker, \
						buyDate, buyLimit, unitLimit, repeat)
					
			# Initialize the stock and save it to list
			stock = Stock(ticker, buyDate, sellDate, buyLimit, unitLimit, repeat, self.verbose)
			self.stockList.append(stock)
			
		# Now figure out your winnings
		for stock in self.stockList:
			total = stock.printDetails()
			
	def getRandomTicker(self):
		sp500 =['ABT', 'ABBV', 'ACN', 'ACE', 'ATVI', 'ADBE', \
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
		index = randint(0,len(sp500))
		return sp500[index]	
