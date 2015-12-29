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
