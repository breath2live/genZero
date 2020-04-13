import pandas as pd
import numpy as np

"""
trigger:
	newWeek
	newMonth
	newYear

"""

class strategy():
	# shared
	ids = []

	# unshared
	trigger = pd.DataFrame([], index=[], columns=['condition', 'trade'])


	class metadata():
		def __init__(self, id):
			self.id = id
			self.name = 'strategy-' + str(id)
			self.portfolio = None

	def __init__(self):
		self.metadata = self.metadata(self._newid())

	def _newid(self):
		new = len(self.ids)
		self.ids.append(new)
		return new

	def linkpf(self, pf):
		self.portfolio = pf

	def addTrigger(self, name):
		self.triggers = self.triggers.append(pd.DataFrame( [], index=[], columns=self.triggers.columns))
