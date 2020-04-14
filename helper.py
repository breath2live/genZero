import sys
import yaml

def showMe(*text):
	id = str(sys._getframe(1).f_code).split(',')[0]+'>'
	msg = id + '   ' + ' '.join([str(elem) for elem in text])
	print(msg)
def readyaml():
	try:
		with open(r'genZero.yaml') as file:
			return yaml.load(file, Loader=yaml.FullLoader)
	except OSError as err:
		showMe(err)
		showMe('creating new yaml')
		return createyaml()
def writeyaml(value):
	try:
		with open(r'genZero.yaml', 'w') as file:
			return yaml.dump(value, file)
	except OSError as err:
		showMe(err)
		return 1
def createyaml():
	yaml = { 'id': {'script':0, 'portfolio':0, 'strategy':0, 'trade':0} }
	writeyaml(yaml)
	return yaml
def getnextscriptid():
	doc = readyaml()
	doc['id']['script'] +=1
	writeyaml(doc)
	return doc['id']['script']
def getnextid(kind):
	doc = readyaml()
	v = kind.lower()
	if v == 'script':
		doc['id']['script'] +=1
		res = doc['id']['script']
	elif v == 'portfolio':
		doc['id']['portfolio'] +=1
		res = doc['id']['portfolio']
	elif v == 'strategy':
		doc['id']['strategy'] +=1
		res = doc['id']['strategy']
	else:
		res = None
	writeyaml(doc)
	return res
