#!/usr/bin/python
# coding=utf-8

import pandas as pd
import pandas_datareader.data as web
from datetime import datetime, timedelta
import time

stocks = pd.read_csv('kospi_201702.csv')
codes = stocks.iloc[:,1]

m2 = timedelta( days = 60 )
end = datetime.now()
start = end - m2

for code in codes:
	c = str(code)
	c = '0'*(6-len(c))+c+'.KS'
	try:
	    data = web.DataReader( c, 'yahoo', start, end )
	except:
	    print 'error:', c
	else:
	    v = data['Volume']
	    last = v[-1]
	    mean = v[:-1].mean()
	    print c, mean, last
	    if last > mean*20:
	    	print 'Found !!!!'
	
	time.sleep(1)
