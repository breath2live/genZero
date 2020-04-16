import pandas as pd
import numpy as np
import datetime
from helper import showMe, getnextid
import matplotlib.pyplot as plt



class strategy():
	# shared
	#ids = []

	# unshared
	condition = pd.DataFrame([], index=[], columns=['condition'])
	execute = pd.DataFrame([], index=[], columns=['command'])
	trigger = pd.DataFrame([], index=[], columns=['trigger'])

	# init and metadata
	class metadata():
		def __init__(self, id):
			self.id = id
			self.name = 'strategy-' + str(id)
			self.portfolio = None
			self.maxpositions = None
			self.maxtrades = None
	def __init__(self):
		self.metadata = self.metadata(getnextid('strategy'))
		self.date = None
		self.prevdate = None
		self.stock = None
		self.option = None
		self.indicator = None
		self.currentyear = None
		self.currentmonth = None
		self.currentweek = None
		self.starttime = None
		self.endtime = None
		self.openposition = []


	# set methods
	def setStock(self, stock):
		self.stock = stock
		self.trigger = pd.DataFrame([0 for x in range(len(self.stock.index))], index=self.stock.index, columns=['trigger'])
	def setOption(self, option):
		self.option = option
	def setIndicator(self, indicator):
		self.indicator = indicator
	def setPortfolio(self, pf):
		self.metadata.portfolio = pf

	# helpers for condition
	def newWeek(self):
		if self.date.weekofyear != self.currentweek:
			self.currentweek = self.date.weekofyear
			return True
		return False
	def newMonth(self):
		if self.date.month != self.currentmonth:
			self.currentmonth = self.date.month
			return True
		return False
	def newYear(self):
		if self.date.year != self.currentyear:
			self.currentyear = self.date.year
			return True
		return False

	# adder methods
	def addCondition(self, name, condition):
		self.condition = self.condition.append(pd.DataFrame( [condition], index=[name], columns=self.condition.columns))
	def addExecution(self, name, command):
		self.execute = self.execute.append(pd.DataFrame( [command], index=[name], columns=self.execute.columns))

	# various methos
	def checkConditions(self):
		for cmd in self.condition['condition']:
			if eval(cmd) == False: return False
		return True
	def execStrategy(self):
		for cmd in self.execute['command']: exec(cmd)
	def indicatorRow(self, column):
		if self.indicator is not None:
			if column in self.indicator.columns:
				return self.indicator.loc[self.date][column]
	def stockRow(self, column):
		if self.stock is not None:
			if column in self.stock.columns:
				return self.stock.loc[self.date][column]
	def doneStrategy(self):
		showMe('duration of strategy:', self.endtime - self.starttime)
		showMe(len(self.stock), len(self.trigger))

		fig, ax = plt.subplots(nrows=2, figsize=(18,8))
		ax[0].plot(self.stock.index, self.stock['close'], label='SPY')
		ax[0].legend()
		ax[1].plot(self.stock.index, self.trigger['trigger'], label='Trigger')
		ax[1].legend()

		plt.savefig('fig')


	# runner methods
	def runDates(self, startdate='2007-01-01', enddate='2020-01-01'):
		self.prevdate = startdate
		self.starttime = datetime.datetime.now()
		for date in self.stock.loc[(self.stock.index >= startdate) & (self.stock.index < enddate)].index:
			self.runDate(date)
		self.endtime = datetime.datetime.now()
		self.doneStrategy()
	def runDate(self, date):
		self.date = date
		if self.checkConditions():
			self.trigger.loc[date]['trigger'] = 1
			self.execStrategy()
