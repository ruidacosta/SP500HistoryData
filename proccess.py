import sqlite3

filename = 'SP&500.csv'
conn = sqlite3.connect(':memory:')

tickers = []

def readInstruments():
	first = True
	with open(filename,'r') as fd:
		for line in fd:
			if not first:
				tickers.append(str(line.replace('\r','').replace('\n','').split(';')[0]))
			else:
				first = False
	
def startDB():
	conn = sqlite3.connect(':memory:')
	
def readDataFiles(ticker):
	tmp = []
	with open('data\\' + ticker + '.csv','r') as fd:
		for line in fd:
			tmp.append(tuple(line.replace('\r','').replace('\n','').split(',')))
	return tmp[1:]

def createSQLiteDB():
	cur = conn.cursor()
	cur.execute('''Create table quotes
		(symbol text,date text,open text,high text, low text,close text, volume text,adj_close text, primary key (symbol,date))''')
	conn.commit()

def insertSQLiteDB(quotes_lst,ticker):
	cur = conn.cursor()
	cur.executemany('insert into quotes values ("'+ticker+'",?,?,?,?,?,?,?)', quotes_lst)
	#'insert into quotes ("symbol","date","open","high","low","close","volume","adj_close") values ( )'
	
def sendToFile():
	query = 'select date,symbol,open,high,low,close,volume,adj_close from quotes order by date'
	cur = conn.cursor()
	with open('SP500Quotes.csv','w') as fd:
		fd.write(';'.join(('date','symbol','open','high','low','close','volume','adj_close')) + '\n')
		for row in cur.execute(query):
			fd.write(';'.join(row) + '\n')

def main():
	print "Loading tickers..."
	readInstruments()
	#print tickers
	#startDB()
	print "Create database..."
	createSQLiteDB()
	for ticker in tickers:
		print "Inserting " + ticker + " data..."
		insertSQLiteDB(readDataFiles(ticker),ticker)
	conn.commit() 
	print "Creating csv file..."
	sendToFile()
	print "Done."

if __name__ == '__main__':
	main()