
'''
http://uselectionatlas.org/RESULTS/state.php?f=1&year=2012&off=0&fips=1
http://uselectionatlas.org/RESULTS/state.php?f=1&year=2012&off=0&fips=2


virginia

http://uselectionatlas.org/RESULTS/state.php?f=1&year=2012&off=0&fips=51
'''

import urllib2
#import urllib
#import os.path
#import os
#import lxml
from lxml import etree
from StringIO import StringIO


fips={1:"Alabama",
2:"Alaska",
4:"Arizona",
5:"Arkansas",
6:"California",
8:"Colorado",
9:"Connecticut",
10:"Delaware",
11:"District of Columbia",
12:"Florida",
13:"Georgia",
15:"Hawaii",
16:"Idaho",
17:"Illinois",
18:"Indiana",
19:"Iowa",
20:"Kansas",
21:"Kentucky",
22:"Louisiana",
23:"Maine",
24:"Maryland",
25:"Massachusetts",
26:"Michigan",
27:"Minnesota",
28:"Mississippi",
29:"Missouri",
30:"Montana",
31:"Nebraska",
32:"Nevada",
33:"New Hampshire",
34:"New Jersey",
35:"New Mexico",
36:"New York",
37:"North Carolina",
38:"North Dakota",
39:"Ohio",
40:"Oklahoma",
41:"Oregon",
42:"Pennsylvania",
44:"Rhode Island",
45:"South Carolina",
46:"South Dakota",
47:"Tennessee",
48:"Texas",
49:"Utah",
50:"Vermont",
51:"Virginia",
53:"Washington",
54:"West Virginia",
55:"Wisconsin",
56:"Wyoming"}

#for year in [1976,1972,1968,1964,1960,1956,1952]:
#for year in [1960,1956,1952]:
#for year in [2012,2008,2004,2000,1996,1992,1988,1984,1980]:
for year in [i*4+1952 for i in range(16)]:
	for i in fips.keys():
		try:
			u="http://uselectionatlas.org/RESULTS/state.php?f=1&year="+str(year)+"&off=0&fips="+str(i)
			headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
			   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			   'Accept-Encoding': 'none',
			   'Accept-Language': 'en-US,en;q=0.8',
			   'Connection': 'keep-alive'}
			req = urllib2.Request(u, None, headers)
			webtxt = urllib2.urlopen(req).read()
			parser = etree.HTMLParser()
			tree=etree.parse(StringIO(webtxt), parser)
			try:
				pres = tree.xpath("//tbody/tr/td")[1].text # 'Willard Mitt Romney'
				vp = tree.xpath("//tbody/tr/td")[2].text # 'Paul Ryan'
				party = tree.xpath("//tbody/tr/td")[3].text # 'AL Republican'
				vote = tree.xpath("//tbody/tr/td")[4].text # '1,255,925'
				votepc = tree.xpath("//tbody/tr/td")[5].text # '60.55%'
				ev = tree.xpath("//tbody/tr/td")[6].text # '9 '
				print '\t'.join([str(i),fips[i],str(year),pres,vp,party,vote,votepc,ev])
				pres = tree.xpath("//tbody/tr/td")[8].text # 'Barack H. Obama'
				vp = tree.xpath("//tbody/tr/td")[9].text # 'Joseph R. Biden, Jr.'
				party = tree.xpath("//tbody/tr/td")[10].text # 'AL Democratic'
				vote = tree.xpath("//tbody/tr/td")[11].text # '795,696'
				votepc = tree.xpath("//tbody/tr/td")[12].text # '38.36%'
				ev = tree.xpath("//tbody/tr/td")[13].text # '0 '
				print '\t'.join([str(i),fips[i],str(year),pres,vp,party,vote,votepc,ev])
			except:
				print("failed on: "+u)
		except urllib2.HTTPError, e:
			print e.fp.read()
	
