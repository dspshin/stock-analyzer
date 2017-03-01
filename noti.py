#!/usr/bin/python
# coding=utf-8

import pandas as pd
import pandas_datareader.data as web
from datetime import datetime, timedelta
import time
import sys
import traceback

THRESHOLD_RATIO = 10

stocks = pd.read_csv('kospi_201702.csv')
codes = stocks.iloc[:,1]

m2 = timedelta( days = 60 )
end = datetime.now()
start = end - m2

cands = []
for i, code in enumerate(codes):
	c = str(code)
	c = '0'*(6-len(c))+c+'.KS'
	try:
	    data = web.DataReader( c, 'yahoo', start, end )
	except:
	    print 'error in', c
	    traceback.print_exc()
	else:
	    v = data['Volume']

	    lastDay = v.index[-1]
	    if lastDay.date() != end.date():
	    	# 마지막날이 오늘이 아니면 오늘장은 쉬는 날임.
	    	#print "today is off. because last date:", lastDay.date(), 'today:', end.date()
	    	#sys.exit(0)
	    	pass

	    last = v[-1]
	    mean = v[:-1].mean() #워킹데이 기준 59일치 평균
	    ratio = last / mean

	    # 마지막날 올랐는지 체크
	    lastCloseDiff = data['Adj Close'].diff()[-1]

	    print i, c, ratio, lastCloseDiff
	    if ratio > THRESHOLD_RATIO and lastCloseDiff > 0:
	    	# ratio가 기준을 넘고, 마지막날 주가가 오른 경우
	    	print 'Found !'
	    	cands.append({
	    		'code':c,
	    		'ratio':ratio,
	    		'lastCloseDiff':lastCloseDiff
	    		})
	
	# 슬립은 필요없어 보임.
	#time.sleep(1) 

print cands
