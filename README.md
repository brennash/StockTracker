# StockTracker

This repository contains the basic Python code to implement an 
basic stock tracker library on a number of daily stock market adjusted 
closing values. Note that this is a tracker only, the predictive part
will be updated later. 

The code is written in Python 2.7.3 on a Mac OS X and tested under
Ubuntu 14.04 LTS. No ports are being considered at this time for Windows
Frankly if you're too dumb to be still using Windows I don't think this 
repo is for you at all. If you're stuck using Windows in work, I'm sure
you'll figure out a way around the issue.

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
directory. Basically library requires a JSON file as input listing one or
more shares which form a fund. There are a number of settings which control
how much of each share can be bought, the total spend and the interval 
between repeat purchases. The output is the performance of this portfolio
on a named ```sell_date```.

```
{
    "name": "Test Fund",
    "sell_date": 20160112,
    "total_buy_limit":10000.00,
    "fund": [
        {
            "ticker": "RANDOM",
            "buy_date": 20150101,
            "buy_limit": 600.00,
            "repeat": "monthly"
        },
        {
            "ticker": "AMZN",
            "buy_date": 20150101,
            "buy_limit": 500.00,
            "repeat": "weekly"
        },
        {
            "ticker": "V",
            "buy_date": 20150601,
            "unit_limit": 10,
            "buy_limit": 300.00
        }
    ]
}
```

Note the 'RANDOM' ticker name in the above JSON. This allows the 
application to randomly select an S&P500 stock at each purchase interval 
and see how it performs over the given time period.

## Running the application
To run the application you need a valid JSON file describing the stocks to be checked, 
as well as Python 2.7.3 or greater installed on your system. I don't think there's many 
required libraries, but anything extra you need should be available on a 'pip install'. 

To run the application type, 

```
python runStockTracker [-v|--verbose] <filname.json>
```

The ```verbose``` option is mostly there for debugging, there's no need to use 
it when you're running as per normal, since most of the output will be duplicated. 
In case of problems, there's a test script which can be run from the main directory 
either, again, this should be largely unnecessary. 

## The Output
The output of the application is as follows, giving an example of 
purchased Amazon (AMZN) stock, purchased monthly between the 2nd Jan
and the 18th Dec 2015. This is one of the impressive S&P500 stocks in 
that for an investment of 9650.15 you end up with a profit of 4960.94 
or (51%) over 12 months. Nice!! The end of the output shows the repeat
stock purchases according to whatever schedule you select, here they're
set to 'monthly' which is every four weeks. 

```
AMZN
Units:22.0, Total:9650.15
Opening Price per Unit:308.52, Opening Date:02/01/2015
Closing Price per Unit:664.14, Closing Date:18/12/2015
Closing Total:14611.08
Profit:4960.93, Percentage:51.4 %

Stock,Date,Units,Amount
AMZN,02/01/2015,3,925.56
AMZN,30/01/2015,2,709.06
AMZN,27/02/2015,2,760.32
AMZN,27/03/2015,2,741.12
AMZN,24/04/2015,2,890.20
AMZN,22/05/2015,2,855.26
AMZN,19/06/2015,2,869.84
AMZN,17/07/2015,2,966.02
AMZN,14/08/2015,1,531.52
AMZN,11/09/2015,1,529.44
AMZN,09/10/2015,1,539.80
AMZN,06/11/2015,1,659.37
AMZN,04/12/2015,1,672.64
Total,18/12/2015,22,9650.15
```

