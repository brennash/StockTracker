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
{"name":"test1",
    "sell_date":20151221,
    "stocks":[
        {"ticker":"SP500-RANDOM","buy_date":20150101,"buy_limit":1000.00,"repeat":"monthly"},
        {"ticker":"SP500-RANDOM","buy_date":20150101,"buy_limit":1000.00,"repeat":"monthly"},
        {"ticker":"AMZN","buy_date":20150101,"buy_limit":1000.00},
        {"ticker":"TSLA","buy_date":20150201,"unit_limit":10,"buy_limit":1500.00},
        {"ticker":"NVDA","buy_date":20150201,"unit_limit":10,"buy_limit":1500.00}
    ]
}
```

## Running the application
To run the application you need a valid JSON file describing the stocks to be checked, 
as well as Python 2.7.3 or greater installed on your system. I don't think there's many 
required libraries, but anything extra you need should be available on a 'pip install'. 

To run the application type, 

python runStockTracker [-v|--verbose] <filname.json>

## The Output
The output of the application is as follows, giving an example of 
purchased Amazon (AMZN) stock, purchased monthly between the 2nd Jan
and the 18th Dec 2015. This is one of the impressive S&P500 stocks in 
that for an investment of 9650.15 you end up with a profit of 4960.94 
or (51%) over 12 months. Nice!!

```
AMZN
Units:22.0, Total:9650.15
Opening Price per Unit:308.52, Opening Date:02/01/2015
Closing Price per Unit:664.14, Closing Date:18/12/2015
Closing Total:14611.08
Profit:4960.93, Percentage:51.4 %
```

