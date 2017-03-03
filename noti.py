#!/usr/bin/python
# coding=utf-8

import pandas as pd
import pandas_datareader.data as web
from datetime import datetime, timedelta, date
import time
import sys
import traceback
import re
from pprint import pprint
import sqlite3
import telepot

ROOT = '/root/git/stock-analyzer/'

# 주식 정보를 위한 루틴
THRESHOLD_RATIO = 10

kospi = pd.read_csv( ROOT+'kospi_201702.csv' )
kospi_codes = kospi.iloc[:,1]

#kosdaq = pd.read_csv( ROOT+'kosdaq_201702.csv')
#kosdaq_codes = kosdaq.iloc[:,1]

codes = []
for c in kospi_codes:
	c = str(c)
	c = '0'*(6-len(c))+c+'.KS'
	codes.append(c)
#for c in kosdaq_codes:
#	codes.append(c+'.KQ')

m2 = timedelta( days = 60 )
end = datetime.now()
start = end - m2

cands = []
for c in codes:
	try:
	    data = web.DataReader( c, 'yahoo', start, end )
	except:
	    print 'error in', c
	    traceback.print_exc()
	else:
	    v = data['Volume']

	    lastDay = v.index[-1]
	    print "last data:", lastDay.date()
	    # 원래는 날자 체크를 하려고 했는데, yahoo가 정보가 느려서 패스
	    # if lastDay.date() != end.date():
	    # 	# 마지막날이 오늘이 아니면 오늘장은 쉬는 날임.
	    # 	print "today is off. because last date:", lastDay.date(), 'today:', end.date(), c
	    # 	sys.exit(0)
	    # 	#pass

	    last = v[-1]
	    mean = v[:-1].mean() #워킹데이 기준 59일치 평균
	    ratio = last / mean

	    # 마지막날 올랐는지 체크
	    lastCloseDiff = data['Adj Close'].diff()[-1]

	    print c, ratio, lastCloseDiff
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


# 등록한 유저들에게 메시지를 보내주기 위한 루틴
TOKEN = sys.argv[1]

bot = telepot.Bot(TOKEN)
pprint( bot.getMe() )

conn2 = sqlite3.connect(ROOT+'logs.db')
c2 = conn2.cursor()
c2.execute('CREATE TABLE IF NOT EXISTS logs( url TEXT, PRIMARY KEY(url) )')
conn2.commit()

conn = sqlite3.connect(ROOT+'subscribe.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS subscribe( user TEXT, name TEXT, PRIMARY KEY(user) )')
conn.commit()

def sendMessage(user,msg):
	try:
		bot.sendMessage(user,msg)
	except:
		traceback.print_exc(file=sys.stdout)

users = []
c.execute('SELECT user FROM subscribe') # get subscribed users
for data in c.fetchall():
	users.append( data[0] )

for cand in cands:
	#print stocks.ix[ cand['index'] ]
	print cand
	msg = 'http://finance.naver.com/item/main.nhn?code='+cand['code'].split('.')[0]

	for user in users:
		sendMessage( user, msg )
