import unittest
import json, re
import datetime
from tswa.TimeSeries import TimeSeries

class Test(unittest.TestCase):

	def test_TimeSeries_Init_1(self):
		ts = TimeSeries('test.test')
		ts.addDataPoint(0, 'Date,Open,High,Low,Close,Volume,Adj Close')
		ts.addDataPoint(1, '2015-12-18,668.650024,676.840027,664.130005,664.140015,6765900,664.140015')
		ts.addDataPoint(2, '2015-12-17,680.00,682.50,670.650024,670.650024,3663500,670.650024')
		ts.addDataPoint(3, '2015-12-16,663.559998,677.349976,659.320007,675.77002,3926600,675.77002')
		ts.addDataPoint(4, '2015-12-15,665.030029,671.50,657.349976,658.640015,4724900,658.640015')
		ts.addDataPoint(5, '2015-12-14,641.75,658.590027,635.27002,657.909973,4329700,657.909973')
		actual = ts.size()
		expected = 5
		self.assertEquals(expected, actual)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
