from lxml import etree

fn23="/projects/rhinohide.org/cybersec/draft/data/NIST-CPE/official-cpe-dictionary_v2.3.xml"
tree23 = etree.parse(fn23)
root23 = tree23.getroot()

fn22="/projects/rhinohide.org/cybersec/draft/data/NIST-CPE/official-cpe-dictionary_v2.2.xml"
tree22 = etree.parse(fn22)
root22 = tree22.getroot()

path="//{http://cpe.mitre.org/dictionary/2.0}cpe-item[contains(@name,'cpe:/o:microsoft')]"
findall = etree.ETXPath(path)
a=findall(tree22)
names22=[]
for c in a:
	if not c.get('deprecated') == 'true':
		names22.append(c.get('name'))
	else:
		names22.append(c.get('deprecated-by'))

names22=list(set(names22))
names22.sort()
if names22[0]==None:
	names22 = names22[1:]


# includes deprecated names
# path="//{http://cpe.mitre.org/dictionary/2.0}cpe-item[contains(@name,'cpe:/o:microsoft')]"

# collect the cpe23-items not deprecated
path="//{http://cpe.mitre.org/dictionary/2.0}cpe-item[contains(@name,'cpe:/o:microsoft') and not(contains(@deprecated,'true'))]/{http://scap.nist.gov/schema/cpe-extension/2.3}cpe23-item[contains(@name,'cpe:2.3:o:microsoft')]"
findall = etree.ETXPath(path)
a=findall(tree23)

# collect the cpe23-items deprecated
path="//{http://scap.nist.gov/schema/cpe-extension/2.3}deprecated-by[contains(@name,'cpe:2.3:o:microsoft')]"
findall = etree.ETXPath(path)
b=findall(tree23)

names23=[]
for c in a:
	names23.append(c.get('name'))

for c in b:
	names23.append(c.get('name'))

names23=list(set(names23))
names23.sort()
if names23[0]==None:
	names23 = names23[1:]


# note that names23 is a subset of names22
# set(names23).difference(set(names22))
# set(names22).difference(set(names23))

f=open("/projects/rhinohide.org/cybersec/draft/data/NIST-CPE/mscpe23.txt", 'w')
for p in names23:
    f.write(p+'\n')

f.close()

f=open("/projects/rhinohide.org/cybersec/draft/data/NIST-CPE/mscpe22.txt", 'w')
for p in names22:
    f.write(p+'\n')

f.close()
