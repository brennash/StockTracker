# StockTracker

This repository contains the basic Python code to implement an 
basic stock tracker library on a number of daily stock market adjusted 
closing values. 

The code is written in Python on an Ubuntu 14.04 LTS environment. 
No ports are being considered at this time for either Windows or 
MacOS for any specific parts of the repository. Frankly if you're
too dumb to be still using Windows I don't think this repo is 
for you at all. 

# Development notes
Was going to use the Python library for yahoo-finance, however, the 
speed of it's response was shockingly poor, so instead this app uses
UrlLib2 to get the raw data in CSV format. 

## Installation
* sudo apt-get update
* sudo apt-get install git python-pip
* sudo pip install urllib2 (where appropriate)

## Usage
The StockTracker library can be kicked off using the script in the bin
directory. Basically library requires a JSON file as input listing when 
and how many shares are to be bought on a certain day. The output is the 
performance of this portfolio on a specified day, also highlighted in the
JSON input. 

```
{
	name:'test1',
	startDate:20150101,
	endDate:20151221,
	stocks:[
		{ticker:'AMZN',buyDate:20150101,buyLimit:1000.00},
		{ticker:'TSLA',buyDate:20150201,unitLimit:10,buyLimit:1500.00}
	]
}
