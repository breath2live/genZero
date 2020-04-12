
def showMe(*text):
	msg = '[{}] '.format(sys._getframe(1).f_code.co_name) + ' '.join([str(elem) for elem in text])
	print(msg)
