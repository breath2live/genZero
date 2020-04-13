import sys

def showMe(*text):
	id = str(sys._getframe(1).f_code).split(',')[0]+'>'
	msg = id + '   ' + ' '.join([str(elem) for elem in text])
	print(msg)
