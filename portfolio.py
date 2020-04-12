import pandas as pd
import numpy as np
import datetime as dt
import bigdataOption

# project related
from helper import showMe


class portfolio():
	# class
	class metadata():
		def __init__(self, id):
			self.id = id
			self.name = 'pf-' + id
			self.maxcushion = 0.8


	# method
	def __init__(self, value=100000, startdate='2007-01-01', enddate='2020-04-01'):
		self.metadata = self.metadata()
		self.startdate = pd.to_datetime(startdate)
		self.enddate = pd.to_datetime(enddate)
		self.prevdate = self.startdate
		self.name = 'pf-{}'.format(np.random.randint(10**10,10**11))
		self.addPortfolio(startdate, value, value, 0, 0, 0)
