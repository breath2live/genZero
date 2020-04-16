import pandas as pd
import numpy as np
from helper import showMe, getnextid

"""
trigger:
	newWeek
	newMonth
	newYear

"""

class strategy():
	# shared
	#ids = []

	# unshared
	trigger = pd.DataFrame([], index=[], columns=['condition'])


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
		self.openposition = []

	def setStock(self, stock):
		self.stock = stock
	def setOption(self, option):
		self.option = option
	def setIndicator(self, indicator):
		self.indicator = indicator
	def setPortfolio(self, pf):
		self.metadata.portfolio = pf

	def addTrigger(self, name, condition):
		self.trigger = self.trigger.append(pd.DataFrame( [[condition]], index=[name], columns=self.trigger.columns))

	def checkTriggers(self):
		res = []
		for cmd in self.trigger['condition']: exec('res.append({})'.format(cmd))
		return False not in res

	def execStrategy(self):
		# add trades, legs
		showMe(self.metadata.name, self.date)


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

	def indicatorData(self, column):
		if self.indicator is not None:
			if column in self.indicator.columns:
				return self.indicator.loc[self.date][column]



	def runDates(self, startdate='2007-01-01', enddate='2020-01-01'):
		self.prevdate = startdate
		for date in self.stock.loc[(self.stock.index >= startdate) & (self.stock.index < enddate)].index:
			self.runDate(date)
	def runDate(self, date):
		self.date = date
		if self.checkTriggers(): self.execStrategy()
