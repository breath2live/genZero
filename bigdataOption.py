import datetime as dt
import pandas as pd
import sys
from helper import showMe




# load data
def loadStock(path, stockfile, ivfile):
	# stock and IV datas
	stock = pd.read_csv('{}/{}'.format(path, stockfile), index_col='date', parse_dates=True)
	showMe('{} imported'.format(stockfile))
	stockiv = pd.read_csv('{}/{}'.format(path, ivfile), index_col='date', parse_dates=True)
	showMe('{} imported'.format(ivfile))

	# overlay data
	stock['iv-open'] = stockiv['open']
	stock['iv-high'] = stockiv['high']
	stock['iv-low'] = stockiv['low']
	stock['iv-close'] = stockiv['close']
	#showMe(stock[stock.isnull()['iv-open'] == True])

	# fix data
	fixdata(stock['iv-open'])
	fixdata(stock['iv-high'])
	fixdata(stock['iv-low'])
	fixdata(stock['iv-close'])
	#showMe(stock[stock.isnull()['iv-open'] == True])

	# cut stock data
	return stock
def fixdata(df):
	missingData = len(df[df.isna()].index)
	if missingData == 0: return
	for item in df[df.isna()].index:
		tmp = df.shift(-df.index.get_loc(item))
		df[item] = tmp.dropna()[:10].rolling(10).mean()[-1:][0]
	showMe('Remaining Missing Data in <{}> | {} of {}:'.format(df.name, len(df[df.isna()].index), missingData))
	return df
def loadOption(path, start=2007, end=2009, symbol='SPY'):
	option = pd.read_csv('{}/{}/RAW_IV.csv'.format(path, start), index_col='date', parse_dates=True)
	showMe(str(start), 'Option data imported.')
	for i in range(start+1,end+1):
		option = pd.concat([option, pd.read_csv('{}/{}/RAW_IV.csv'.format(path, i), index_col='date', parse_dates=True)])
		showMe(str(i), 'Option data imported.')
	option['option_expiration'] = pd.to_datetime(option['option_expiration'])
	return option[option['symbol'] == symbol]




# analyse function
def nextContract(df, date, duration):
	"""
	df = DataFrame
	date = index by Date
	duration = closest to this duration
	"""
	date = pd.to_datetime(date)
	if type(duration) != dt.timedelta : duration = dt.timedelta(days=duration)

	allexp = df.loc[date]['option_expiration'].unique()

	record = float('inf')
	expContract = None
	for exp in allexp:
		diff = abs(float(str(pd.to_datetime(exp)-date-duration).split()[0]))
		if diff < record:
			record = diff
			expContract = pd.to_datetime(exp)
	return expContract
def getContractByDelta(df, date, delta, call_put='C', option_expiration=None, duration=45):
	date = pd.to_datetime(date)
	if type(duration) != dt.timedelta : duration = dt.timedelta(days=duration)
	if option_expiration == None: option_expiration = nextContract(df, date, duration)
	if call_put != 'C' and call_put != 'P': return (1, 'Invalid type:', call_put)

	#print('date:{}, call_put:{}, exp:{}'.format(date,call_put, option_expiration))

	tmp = df.loc[date]
	tmp = tmp[(tmp['option_expiration'] == option_expiration) & (tmp['call_put'] == call_put) & (tmp['delta'] != 0)]

	if call_put == 'C':
		diff = tmp['delta']-delta
		record = diff.abs().min()
		if record+delta in tmp['delta'].values:
			return tmp[tmp['delta'] == record+delta ]
		elif -record+delta in tmp['delta'].values:
			return tmp[tmp['delta'] == -record+delta ]
	elif call_put == 'P':
		diff = tmp['delta']+delta
		record = diff.abs().min()
		if record-delta in tmp['delta'].values:
			return tmp[tmp['delta'] == record-delta ]
		elif -record-delta in tmp['delta'].values:
			return tmp[tmp['delta'] == -record-delta ]
	else:
		return (1, 'Invalid type:', call_put)
def getDetailsOnExpiration(df, contract):
	exp = contract['option_expiration'][0]
	tmp = tmp[tmp['option_expiration'] == exp].loc[exp].copy()
	return tmp[ (tmp['strike'] == contract['strike'][0]) & (tmp['call_put'] == contract['call_put'][0]) ]
def getDetailsOnExpirationBySimple(df, exp='', call_put='', strike='', contract=None):
	if contract != None:
		contract = contract.split()
		exp = contract[0]
		call_put = contract[1]
		strike = contract[2]
	exp = pd.to_datetime(exp)
	strike = float(strike)
	tmp = df[df['option_expiration'] == exp].loc[exp]
	return tmp[ (tmp['call_put'] == call_put) & (tmp['strike'] == strike) ].copy()
def getContractBySimple(df, date, exp='', call_put='', strike='', contract=None):
	if contract != None:
		contract = contract.split()
		exp = contract[0]
		call_put = contract[1]
		strike = contract[2]
	date = pd.to_datetime(date)
	exp = pd.to_datetime(exp)
	strike = float(strike)
	tmp = df[df['option_expiration'] == exp].loc[date]
	return tmp[ (tmp['call_put'] == call_put) & (tmp['strike'] == strike) ].copy()
def getContractFullBySimple(df, date, exp='', call_put='', strike='', contract=None):
	if contract != None:
		contract = contract.split()
		exp = contract[0]
		call_put = contract[1]
		strike = contract[2]
	date = pd.to_datetime(date)
	exp = pd.to_datetime(exp)
	strike = float(strike)
	tmp = df[ (df['option_expiration'] == exp) & (df['call_put'] == call_put) & (df['strike'] == strike) ]
	return tmp.loc[tmp.index >= date].copy()
