#############################################################
# Rui Duarte Costa                                          #
# (ruidacosta@gmail.com)                                    #
#############################################################
# Download 4 years historical data for tickers in csv       #
#############################################################

import requests
import random
import time
import os.path

filename = 'SP&500.csv'
startDate = 'Jun+19,2011'
endDate = 'Jun+18,2012'

tickers = []

def loadTickers():
	first = True
	with open(filename,'r') as fd:
		for line in fd:
			if not first:
				tickers.append(str(line.replace('\r','').replace('\n','').split(';')[0]))
			else:
				first = False
	
def getDataByTicker(ticker):
	#requestURL = 'http://www.google.com/finance/historical?q='+ ticker + '&startdate=' + startDate + '&enddate=' + endDate + '&output=csv'
	# a => Month-1, b => day, c => year, d => Month-1 e => day, f => year
	if (os.path.isfile('data\\' + ticker + '.csv')):
		print ticker + " ticker file already exists."
		return False
	a = '5'
	b = '19'
	c = '2011'
	d = '5'
	e = '18'
	f = '2015'
	requestURL = 'http://ichart.yahoo.com/table.csv?s=' + ticker + '&a=' + a + '&b=' + b + '&c=' + c + '&d=' + d + '&e=' + e + '&f=' + f + '&g=d&ignore=.csv'
	r = requests.get(requestURL)
	if (r.status_code == 200):
		with open('data\\' + ticker + '.csv','w') as fd:
			fd.write((u'%s' % r.text).encode('utf8'))
			fd.close()
	else:
		print "ERROR: can not get data for " + ticker + "."
		return False
	return True
	
def writeData():
	pass

def main():
	print "Loading Tickers..."
	loadTickers()
	print "Get data By Ticker..."
	for ticker in tickers:
		print ticker
		if (getDataByTicker(ticker)):
			rnd = random.randint(1,30)
			print "Wait " + str(rnd) + " seconds..."
			time.sleep(rnd)
	print "Processing data..."
	writeData()
	print "Done."

if __name__ == '__main__':
	main()