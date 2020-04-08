
# extern function of genZero

# run
def run():
	showMe('setup...')
	showMe('ready for inputs')
	while True:
		inp = input()

		if inp == 'exit' or 'q':
			return
		else:
			showMe('Invalid Input. Type "exit" | "q" esc to quit')
