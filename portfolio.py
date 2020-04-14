import pandas as pd
import numpy as np
import datetime as dt
import bigdataOption
import copy

# project related
from helper import showMe
from strategy import strategy


class portfolio():
	# class
	class metadata():
		def __init__(self, id):
			self.id = id
			self.name = 'portfolio-' + str(id)
			self.maxcushion = 0.8

	# def DF
	_portfolio = pd.DataFrame([], index=pd.DatetimeIndex(data=[], name='date'), columns=['NLV', 'cash', 'margin', 'unreal', 'real'])
	_position = pd.DataFrame([], index=pd.DatetimeIndex(data=[], name='date'), columns=['contract', 'side', 'quantity', 'value', 'avgPrice'])
	_trades = pd.DataFrame([], index=pd.DatetimeIndex(data=[], name='date'), columns=['contract', 'side', 'quantity', 'avgPrice'])
	portfolio = _portfolio.copy()
	position = _position.copy()
	trades = _trades.copy()

	# def var
	#


	# method
	def __init__(self, id, value=100000, startdate='2007-01-01', enddate='2020-04-01'):
		self.metadata = self.metadata(id)
		self.startdate = pd.to_datetime(startdate)
		self.enddate = pd.to_datetime(enddate)
		self.prevdate = self.startdate
		#self.addPortfolio(startdate, value, value, 0, 0, 0)
		self.strategy = []

	def _newid(self):
		new = len(self.ids)
		self.ids.append(new)
		return new

	def addStrategy(self, strategy :strategy):
		strategy = copy.deepcopy(strategy)
		strategy.linkpf(self)
		self.strategy.append(strategy)
		return len(self.strategy)-1
