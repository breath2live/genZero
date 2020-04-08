from numpy.random import rand as rdm

class dna():
	def __init__(self):
		self.bullaware = rdm()
		self.bearaware = rdm()
		self.bullagg = rdm()
		self.bearagg = rdm()

		self.duration = rdm()*100

	def __str__(self):
		return 'duration: {} bull: {}/{} bear: {}/{}'.format(self.duration, self.bullaware, self.bullagg, self.bearaware, self.bearagg)


class sloth():
	def __init__(self):
		self.health = 100
		self.dna = dna()

	def __str__(self):
		return 'health: {} dna: {}'.format(self.health, self.dna)
