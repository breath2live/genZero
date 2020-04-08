import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sloth import sloth
import indicator
import genZeroRun
import sys


# define and start ups
sns.set()
maxsloths = 10
stack = []
stock = None
stockiv = None
option = {}

# helpers
def showMe(text):
	print('[{}] {}'.format(sys._getframe(1).f_code.co_name, text))
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
	loadOptionData = 0

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

	# impporting option data
	if loadOptionData == 1:
		for i in range(2005,2021):
			option[i] = pd.read_csv('~/mktData/{}/RAW_IV.csv'.format(i), index_col='date', parse_dates=True)
			showMe(i, 'Option data imported.')
def addIndicator():
	# Moving Average
	indicator.addMA(stock, 'close', 20)
	indicator.addMA(stock, 'close', 90)
	indicator.addMA(stock, 'close', 200)
	# Bollinger Band
	indicator.addBB(stock, 'close', 200, 2)
	# Ranking
	indicator.addRank(stock, 'iv-close', 10)
	indicator.addRank(stock, 'iv-close', 20)
	indicator.addRank(stock, 'iv-close', 252)

# depreciated
def rundata():
	# init run
	showMe('init')
	cnt = 1
	cntmax = len(stock)
	startdate = stock.index[0]
	enddate = stock.index[cntmax-1]
	showMe(cntmax)

	# run
	for date in stock.index:
		showMe('{} / {}  | {} % | {} -> {}'.format(cnt, cntmax, round(cnt/cntmax*100, 2), date, enddate))
		#showMe(stock.loc[date])

		cnt +=1
	# END run

# run
def run():
	showMe('setup...')
	showMe('ready for inputs')
	while True:
		inp = input()

		if inp == 'exit' or 'q':
			return
		else:
			showMe('Invalid Input. Type "exit" | "q" esc to quit')


# main
def main():
	# setup
	showMe('setup...')
	getdata()

	# add indicators and others
	showMe('add Indicators')
	addIndicator()

	# run input loop
	run()

	# clean up and exit
	showMe('clean up and exit')
	###



if __name__ == '__main__' :
	main()
