# includes
from manager.process import process
from threading import Timer

import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import bigdataOption
from helper import showMe, getnextid
import sys

# define and start ups
stock = None
stockiv = None
option = None
configfile = None
runningFile = []
sns.set()


# Function
def loadfile(path, id):
	global idcnt
	try:
		with open(path) as f:
			exec('id={}\n'.format(id) + f.read())
	except OSError as err:
		showMe(err)
def loadstock():
	global stock
	stock = bigdataOption.loadStock('~/mktData', 'spy-trd.csv', 'spy-iv.csv')
def loadoption():
	global option
	option = bigdataOption.loadOption('~/mktData', start=2007, end=2020)
def run():
	global idcnt
	showMe('setup...')
	### DEV
	runningFile.append(process(loadfile, 'script.py', getnextid('script')).start())
	Timer(20, sys.exit(1)).start()
	###
	showMe('ready for inputs')
	while True:
		inp = input('').split()

		help = 'Invalid Input. Type "exit" | "q" esc to quit'
		if len(inp) > 0:
			# <exit> | <q>
			if inp[0] in ['exit', 'q']:
				return
			elif inp[0] in ['file', 'f']:
				help = '\nfile\n->  <path/file.py>\n'
				if len(inp) > 1:
					runningFile.append(process(loadfile, inp[1], getnextid('script')).start())
				else:
					showMe(help)
			elif inp[0] in ['option', 'o']:
				loadoption()
			elif inp[0] in ['stock', 's']:
				loadstock()
			elif inp[0] in ['all', 'a']:
				loadstock()
				loadoption()
			else:
				showMe(help)
def workflow():
	# setup
	showMe('setup...')

	# run
	run()

	# clean up and exit
	showMe('clean up and exit')
	###



if __name__ == '__main__' :
	workflow()
