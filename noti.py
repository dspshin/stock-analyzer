#!/usr/bin/python
# coding=utf-8

import pandas as pd
import pandas_datareader.data as web
from datetime import datetime, timedelta
import time

stocks = pd.read_csv('stocks_201612.csv', encoding='utf-8')
codes = stocks.iloc[:,1]

m2 = timedelta( days = 60 )
end = datetime.now()
start = end - m2

for code in codes:
    c = str(code)+'.KS'
    try:
        data = web.DataReader( c, 'yahoo', start, end )
    except:
        print c, 'is kosdaq'
    else:
        print c, 'is success!!'
    time.sleep(1)
