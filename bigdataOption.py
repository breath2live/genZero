import datetime as dt
import pandas as pd


def nextContract(df, date, duration):
	"""
	df = DataFrame
	date = index by Date
	duration = closest to this duration
	"""
	date = pd.to_datetime(date)
	if type(duration) != dt.timedelta : duration = dt.timedelta(days=duration)

	allexp = df[date.year].loc[date]['option_expiration'].unique()

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

	tmp = df[date.year].loc[date].copy()
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
	tmp = df[exp.year]
	tmp = tmp[tmp['option_expiration'] == exp].loc[exp].copy()
	return tmp[ (tmp['strike'] == contract['strike'][0]) & (tmp['call_put'] == contract['call_put'][0]) ]

def getDetailsFull(df, contract, date=None):
	if date != None: date = pd.to_datetime(date)
	# dev
