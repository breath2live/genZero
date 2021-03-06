
def exists(df, column):
	if column in df.columns: return 1
	return 0

def addMA(df, column, window=50):
	name = '{}-MA{}'.format(column, window)
	if not exists(df, name): df[name] = df[column].rolling(window).mean()

def addBB(df, column, window=50, std=2):
	name = '{}-BB{}/{}-U'.format(column, window, std)
	if not exists(df, name): df[name] = df[column].rolling(window).mean() + std*df[column].rolling(window).std()
	name = '{}-BB{}/{}-L'.format(column, window, std)
	if not exists(df, name): df[name] = df[column].rolling(window).mean() - std*df[column].rolling(window).std()

def addRank(df, column, window=50, acc=0):
	name = '{}-Rank{}'.format(column, window)
	if not exists(df, name): df['{}-Rank{}'.format(column, window)] = round((df[column] - df[column].rolling(window).min()) / (df[column].rolling(window).max() - df[column].rolling(window).min())*100,acc)


def getMA(df, window=50):
	return df.rolling(window).mean()
def getBBupper(df, window=50, std=2):
	return df.rolling(window).mean() + std*df.rolling(window).std()
def getBBlower(df, window=50, std=2):
	return df.rolling(window).mean() - std*df.rolling(window).std()
def getRank(df, window=50, acc=0):
	return round((df - df.rolling(window).min()) / (df.rolling(window).max() - df.rolling(window).min())*100,acc)
