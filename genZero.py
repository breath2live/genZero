import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys, os
import datetime as dt

# project
from portfolio import portfolio
from helper import showMe
import indicator
import bigdataOption


# define and start ups
sns.set()
stock = None
stockiv = None
option = None





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


# main
def main():
	global stock, option
	# setup
	showMe('setup...')
	stock = bigdataOption.loadStock('~/mktData', 'spy-trd.csv', 'spy-iv.csv')
	option = bigdataOption.loadOption('~/mktData', start=2007, end=2020)
	# add indicators and others
	showMe('add Indicators')
	addIndicator()
	###########







	###########
	# clean up and exit
	showMe('clean up and exit')
	###

if __name__ == '__main__' :
	main()
