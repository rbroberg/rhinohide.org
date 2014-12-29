from lxml import etree

fn="/projects/rhinohide.org/cybersec/draft/data/NIST-CPE/official-cpe-dictionary_v2.3.xml"

tree = etree.parse(fn)
root = tree.getroot()

path="//{http://cpe.mitre.org/dictionary/2.0}cpe-item[contains(@name,'cpe:/o:microsoft')]"
findall = etree.ETXPath(path)
a=findall(tree)

f=open("/projects/rhinohide.org/cybersec/draft/data/NIST-CPE/mscpe.txt", 'w')
for p in a:
    f.write(p.get('name')+'\n')

f.close()

    