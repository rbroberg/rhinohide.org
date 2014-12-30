import glob
from lxml import etree

# get product id / product name map from cvrf
datdir="/projects/rhinohide.org/cybersec/draft/data/MSRC-CVRF/"
xmldir=datdir+"*xml"
fxml=glob.glob(xmldir)
fxml.sort()

'''
# fixed on Dec 30 by email communication with secure@microsoft.com

cvrfhead='<?xml version="1.0" encoding="UTF-8"?> ' \
	+ '<cvrf:cvrfdoc ' \
	+ 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
	+ 'xmlns:dc="http://purl.org/dc/elements/1.1/"  ' \
	+ 'xmlns:cvrf-common="http://www.icasi.org/CVRF/schema/common/1.1" ' \
	+ 'xmlns:prod="http://www.icasi.org/CVRF/schema/prod/1.1"  ' \
	+ 'xmlns:vuln="http://www.icasi.org/CVRF/schema/vuln/1.1"  ' \
	+ 'xmlns:cvrf="http://www.icasi.org/CVRF/schema/cvrf/1.1"  ' \
	+ 'xmlns:wbld="http://schemas.microsoft.com/office/word/2004/5/build" ' \
	+ 'xmlns:scap-core="http://scap.nist.gov/schema/scap-core/1.0" ' \
	+ 'xmlns:cvssv2="http://scap.nist.gov/schema/cvss-v2/1.0"  ' \
	+ 'xmlns:cpe-lang="http://cpe.mitre.org/language/2.0"  ' \
	+ 'xmlns:sch="http://purl.oclc.org/dsdl/schematron"  ' \
	+ 'xmlns:my="http://schemas.microsoft.com/office/infopath/2003/myXSD/2012-04-25T17:42:50" ' \
	+ 'xmlns:xd="http://schemas.microsoft.com/office/infopath/2003">'

cvrftail=' </cvrf:cvrfdoc>'
'''

# Microsoft had inconsistent publications of its CVRF
# some are complete and some are partial
# Repaired as of 20141230
d_name2id={}
d_id2name={}
for fn in fxml:
	f=open(fn)
	xml=f.readlines()
	f.close()
	
	#if xml[0].find('cvrf:cvrfdoc') == -1 and xml[1].find('cvrf:cvrfdoc') == -1 :
	#	xml[0]=cvrfhead+xml[0]
	
	#if xml[-1].find('cvrf:cvrfdoc') == -1 and xml[-2].find('cvrf:cvrfdoc') == -1 :
	#	xml[-1]=xml[-1]+cvrftail
	
	try:
		strxml=' '.join(xml)
		root=etree.fromstring(strxml)
		#root = tree.getroot()
	except:
		xml[1]=xml[1]+'>'
		try:
			strxml=' '.join(xml)
			root=etree.fromstring(strxml)
		except:
			print('Parsing failed on '+fn+'\n')
	
	path="//{http://www.icasi.org/CVRF/schema/prod/1.1}FullProductName"
	find = etree.ETXPath(path)
	prods=find(root)
		
	for p in find(root):
		ppid=str(p.get('ProductID')).replace(' ','').split('-')
		# when installed on in MS12-038 
		pptxt=str(p.text).replace(' when installed','').split(' on ')
		# only want the first half; several typos in second half
		#for i in range(len(ppid)):
		for i in range(1):
			try:
				# append if entry exists
				d_id2name[ppid[i]]=d_id2name[ppid[i]]+pptxt[i]
				d_name2id[pptxt[i]]=d_name2id[pptxt[i]]+ppid[i]
			except:
				try:
					# create new list for value if entry doesn't already exist
					d_id2name[ppid[i]]=[pptxt[i]]
					d_name2id[pptxt[i]]=[ppid[i]]
				except:
					# this will happen if " on " is not in dual product name
					# also '???' used as product id in some instances
					pass

# -----------------------------------------------------------------
'''
pp=d_id2name.keys()
pp.sort()
f = open(datdir+'msprodid.txt', 'w')
for p in pp:
	n = d_id2name[p]
	for i in range(len(n)):
		f.write('\t'.join([p, n[i]])+'\n')
		print('\t'.join([p, n[i]]))

f.close()
'''
# -----------------------------------------------------------------

# <vuln:CVE>
# {http://www.icasi.org/CVRF/schema/vuln/1.1}CVE
path="//{http://www.icasi.org/CVRF/schema/vuln/1.1}CVE"
find = etree.ETXPath(path)
cves=find(root)
cve=cves[0].text

url="http://web.nvd.nist.gov/view/vuln/detail?vulnId="+cve
from bs4 import BeautifulSoup
import urllib
soup = BeautifulSoup(urllib.urlopen(url),["lxml","xml"])
a=soup.find_all(text=re.compile("cpe:/"))

cpe:/o:microsoft:windows_server_2008:r2:sp1 | Windows Server 2008 R2 * Service Pack 1
cpe:2.3:o:microsoft:windows_server_2008:r2:sp1:*:*:*:*:*:* |  
cpe:2.3:o:microsoft:windows_server_2008:r2:sp1:x64:*:*:*:*:* | Windows Server 2008 R2 for x64-based Systems Service Pack 1
cpe:2.3:o:microsoft:windows_server_2008:r2:sp1:itanium:*:*:*:*:* | Windows Server 2008 R2 for Itanium-Based Systems Service Pack 1

b=soup.find_all(text=re.compile("cpe:2.3"))
