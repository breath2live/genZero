import pandas as pd
import numpy as np
from helper import showMe, getnextid

class position():
	class metadata():
		def __init__(self, id):
			self.id = id
			self.name = 'position-' + str(id)

	def __init__(self):
		self.metadata = self.metadata(getnextid('position'))
		self.opendate = None
		self.closedate = None
		self.closetype = None
