import glob
from lxml import etree

# assumes a valid set of cvrf files
datdir="/opt/projects/django-cyberxml/static/data/microsoft.com/MSRC-CVRF/"
xmldir=datdir+"*xml"
fxml=glob.glob(xmldir)
fxml.sort()

d_name2id={}
d_id2name={}
for fn in fxml:
	f=open(fn)
	xml=f.readlines()
	f.close()
	
	try:
		strxml=' '.join(xml)
		root=etree.fromstring(strxml)
		#root = tree.getroot()
	except:
		print('Parsing failed on '+fn+'\n')
	
	path="//{http://www.icasi.org/CVRF/schema/prod/1.1}FullProductName"
	find = etree.ETXPath(path)
	prods=find(root)
	
	for p in find(root):
		ppid=str(p.get('ProductID')).replace(' ','').split('-')
		# when installed on in MS12-038 
		#pptxt=str(p.text).replace(' when installed','').split(' on ')
		pptxt=str(p.text).split(' on ')
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
import csv
writer = csv.writer(open('d_id2name.csv', 'wb'))
for key, value in d_id2name.items():
   writer.writerow([key, value])

writer = csv.writer(open('d_name2id.csv', 'wb'))
for key, value in d_name2id.items():
   writer.writerow([key, value])



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
