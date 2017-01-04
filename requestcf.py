import urllib.request
from collections import defaultdict
import re
import glob, os
import numpy

xchangelist = []
testpasslist = []

print('------------------------------------------------------------------------------')
wldatalist =[]
wltickerlist=[]
filename = 'nyse52wl'
date = '10317'
print(filename+date)
with open(filename+date+'.csv') as wlfile:
	for lines in wlfile:
		wldatalist.append(lines.split(','))
for x in wldatalist:
	wltickerlist.append(x[0])
wltickerlist.pop(0)
fwltickerlist =[]

for x in wltickerlist:
	if re.search(' ',x):
		fwltickerlist.append(re.sub(' ','.',x))
	else:
		fwltickerlist.append(x)

xchange = 'XNYS'
for x in fwltickerlist:
	
	stockticker= x
	xstockticker = xchange+stockticker

	inv,ni,da,ce,ar,ap,owc,onci,pe = '0','0','0','0','0','0','0','0','0'

	cashflow= []
	years = []
	cashflowdic = {}
	cashflowdicindex = []
	try:
		with open(stockticker+'.csv') as cashflowscsv:
			for lines in cashflowscsv:
				cashflow.append(lines.split(','))
	except FileNotFoundError:		
		a_url = 'http://financials.morningstar.com/ajax/ReportProcess4CSV.html?&t='+ xstockticker + '&region=usa&culture=en-US&cur=&reportType=cf&period=12&dataType=A&order=asc&columnYear=5&rounding=3&view=raw&denominatorView=raw&number=3'
		data = urllib.request.urlopen(a_url).read()
		with open(stockticker+'.csv',mode='wb') as a_file:
			a_file.write(data)
		with open(stockticker+'.csv',mode='r',encoding='utf-8-sig') as a_file:
			data = a_file.read()
		with open(stockticker+'.csv',mode='w',encoding='utf-8') as a_file:
			a_file.write(data)			
		with open(stockticker+'.csv') as cashflowscsv:
			for lines in cashflowscsv:
				cashflow.append(lines.split(','))
	
	if len(cashflow) > 3:
		print(x)
		for lines in cashflow:
		  cashflowdic.setdefault(lines[0],lines[1:])
		keyscashflow = (list(iter(cashflowdic)))
		pattern = re.compile("Fiscal")
		for x in keyscashflow:
			if len(cashflowdic[x])== 6:
				cashflowdicindex.append(x)
			if pattern.match(x):
				years.append(cashflowdic[x])



		for x in cashflowdicindex:
			if re.search('\n',cashflowdic[x][-1]):
				cashflowdic[x][-1] = cashflowdic[x][-1][:-1]
			if re.search('Net in',x):
				ni = cashflowdic[x]
			if re.search('Accounts recei',x):
				ar = cashflowdic[x]
			if re.search('Accounts paya',x) or re.search('Payables',x):
				ap = cashflowdic[x]
			if re.search('Capital exp',x):
				ce = cashflowdic[x]
			if re.search('Other working capital',x):
				owc = cashflowdic[x]
			if re.search('Depreciation',x):
				da = cashflowdic[x]
			if re.search('Inventory',x):
				inv = cashflowdic[x]
			if re.search('Other non-cas',x):
				onci = cashflowdic[x]
			if re.search('Prepaid expe',x):
				pe = cashflowdic[x]
			if re.search('Income taxes pa',x):
				ip = cashflowdic[x]
		oep =[inv,ni,da,ce,ar,ap,owc,onci,pe]
		capex =[]
		for x in oep[3]:
			if x == '':
				x = 0
			capex.append(int(x))
		capexnp = numpy.array(capex)	
		oe = [x for x in oep if x != '0']
		oeint =[]
		z = []
		i = 0

		for x in oe:
			for i in x:
				if i == '':
					i = 0
				else:
					i = int(i)
					z.append(i)
			oeint.append(z)
			z =[]
		
		oesum=[sum(o) for o in zip(*oeint)]
		if sum(oesum[-3:])/3 > 0 and len(oesum) > 2 and sum(oesum[-3:])/3 > sum(oesum)/len(oesum):
			print(cashflow[0][0].rstrip())
			print(years[0])
			print(oesum,'Owner\'s Earnings')
			print(sum(oesum)/len(oesum),'5 year Average OE')
			print(sum(oesum[-3:])/3,'3 year Average OE')
			#print(list(zip(*oeint)))
			print('Average Capex {} years'.format(len(capex)-1),sum(capex[:-1])/len(capex)-1)
			print('Standard Deviation of Capex',numpy.std(capexnp))
			print(capexnp,'Cap Ex')
			testpasslist.append(stockticker)
print(testpasslist)