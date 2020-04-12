import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import indicator
import bigdataOption
import sys, os
import datetime as dt


# define and start ups
sns.set()
maxsloths = 10
stack = []
stock = None
stockiv = None
option = {}
f = open('logging.log', 'w')
f.write('')
f.close()


def fixdata(df):
	missingData = len(df[df.isna()].index)
	if missingData == 0: return
	for item in df[df.isna()].index:
		tmp = df.shift(-df.index.get_loc(item))
		df[item] = tmp.dropna()[:10].rolling(10).mean()[-1:][0]
	showMe('Missing Data in <{}> | {} of {}:'.format(df.name, len(df[df.isna()].index), missingData))
	return df
def getdata():
	global stock, stockiv, option
	loadOptionData = 1

	# stock and IV datas
	stock = pd.read_csv('~/mktData/spy-trd.csv', index_col='date', parse_dates=True)
	showMe('Stock data imported')
	stockiv = pd.read_csv('~/mktData/spy-iv.csv', index_col='date', parse_dates=True)
	showMe('Stock IV data imported')

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
	stock = stock.loc[stock.index >= '2007-01-01']

	# impporting option data
	if loadOptionData == 1: loadOption()
def loadOption():
	for i in range(2007,2009):
		option[i] = pd.read_csv('~/mktData/{}/RAW_IV.csv'.format(i), index_col='date', parse_dates=True)
		option[i]['option_expiration'] = pd.to_datetime(option[i]['option_expiration'])
		showMe(str(i), 'Option data imported.')
def addIndicator():
	# Moving Average
	indicator.addMA(stock, 'close', 20)
	indicator.addMA(stock, 'close', 90)
	indicator.addMA(stock, 'close', 200)
	# Bollinger Band
	indicator.addBB(stock, 'close', 200, 2)
	# Ranking
	indicator.addRank(stock, 'iv-close', 20)
	indicator.addRank(stock, 'iv-close', 50)
	indicator.addRank(stock, 'iv-close', 252)


# depreciated
def rundata():
	# init run
	showMe('init')
	cnt = 0
	cntmax = len(stock)-1
	startdate = stock.index[0]
	enddate = stock.index[cntmax]


	# trades and portfolio
	portfolio = pd.DataFrame([], index=pd.DatetimeIndex([], name='date'), columns=[['NLV', 'margin', 'unreal', 'real']])
	position = pd.DataFrame([], index=pd.DatetimeIndex([], name='date'), columns=[['contract', 'side', 'quantity', 'value', 'avgPrive']])
	trades = pd.DataFrame([], index=pd.DatetimeIndex([], name='date'), columns=option[2007].columns)
	tradescnt = 0
	openpos = []

	# dna
	opencnt = 0
	opencntmax = 10

	duration = 45
	delta = 0.20


	# run
	for date in stock.loc[(stock.index >= '2007-01-01') & (stock.index < '2008-01-01')].index:
		#showMe('{} / {}  | {} % | {}'.format(cnt, cntmax, round((cnt+1)/(cntmax+1)*100, 2), date))
		rank = stock.loc[date]['iv-close-Rank50']
		if rank > 70 and opencnt < opencntmax:
			tradescnt += 1
			showMe('###################################################################')
			showMe('##### Date:', date)
			showMe('##### Stock Price (close):', stock.loc[date]['close'], 'iv-close:', stock.loc[date]['iv-close'])
			showMe('##### Open Trade. Trigger: iv-close-Rank50 value:', rank)

			# get Contract
			# Put
			contract_put = bigdataOption.getContractByDelta(option, date, delta, call_put='P', duration=duration).copy()
			trades = trades.append(contract_put)
			openpos.append(contract_put[['option_expiration', 'call_put', 'strike']])
			disp = contract_put

			# expired Contract
			# put
			contract_put = bigdataOption.getDetailsOnExpiration(option, contract_put).copy()
			contract_put['exchange'] = 'EXPIRED'
			contract_put['mean_price'] = -contract_put['mean_price']
			trades = trades.append(contract_put)
			disp = disp.append(contract_put)

			showMe('Contract(s):\n', disp[['exchange', 'option_expiration', 'call_put', 'strike', 'mean_price', 'delta']], '\n\n')

		# for each openPos -> track position, if expired: remove from list
		position = position.append(pd.DataFrame([['', 'SELL', 1, price, 1*price]], index=[date]))




		cnt +=1
	# END run
	print(trades)
	print(tradescnt)
	print(trades['mean_price'].sum())

	trades.to_csv('trades.csv')


# run
def run():
	showMe('setup...')
	showMe('ready for inputs')
	while True:
		inp = input().split()


		help = 'Invalid Input. Type "exit" | "q" esc to quit'
		if len(inp) > 0:
			# <exit> | <q>
			if inp[0] in ['exit', 'q']:
				return
			# <strategy>
			elif inp[0] in ['strategy', 'strat']:
				help = '\n<strategy | strat>\n->  <ls>\n->  <add>\n->  <del>\n'
				if len(inp) > 1:
					if inp[1] == 'ls':
						pass
					elif inp[1] == 'add':
						pass
					elif inp[1] == 'del':
						pass
					else:
						showMe(help)
				else:
					showMe(help)
			elif inp[0] in ['load']:
				help = '\n<load>\n->  <option>\n'
				if len(inp) > 1:
					if inp[1] == 'option':
						loadOption()
					else:
						showMe(help)
				else:
					showMe(help)
			else:
				showMe(help)




# main
def main():
	# setup
	showMe('setup...')
	getdata()

	# add indicators and others
	showMe('add Indicators')
	addIndicator()

	# run input loop
	rundata()

	# clean up and exit
	showMe('clean up and exit')
	###



if __name__ == '__main__' :
	main()
