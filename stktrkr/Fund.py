import re
import csv
import datetime
from dateutil.relativedelta import relativedelta
from stktrkr.Stock import Stock

class Fund:
	def __init__(self, fundName, verbose=False):