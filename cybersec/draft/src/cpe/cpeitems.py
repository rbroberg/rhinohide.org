import lxml
from urllib import urlopen

# http://pythonhackers.com/python-packages/cpe
# https://cpe.readthedocs.org/en/latest/

# 25MB as of Dec 27, 2014
#fn="http://static.nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.2.xml"
fn="test-cpe-dictionary_v2.3.xml"

>>> a[0].get('name')
'cpe:/a:7-zip:7-zip:3.13'
>>> a[-1].get('name')
'cpe:/a:7-zip:p7zip:4.14.01'import xml.etree.ElementTree as ET
tree = ET.parse(urlopen(fn))
root = tree.getroot()


a=root.findall(".//{http://cpe.mitre.org/dictionary/2.0}cpe-item")
b=()
for aa in a:
    b.
a[0].find("{http://cpe.mitre.org/dictionary/2.0}title")

root[1].attrib['name']
a[2].get('name')
root.findall(".//{http://cpe.mitre.org/dictionary/2.0}cpe-item[@name='cpe:/a:1024cms:1024_cms:1.2.5']")

path="//{http://cpe.mitre.org/dictionary/2.0}cpe-item[contains(@name,'7-zip')]"
findall = etree.ETXPath(path)
a=findall(tree)
a[0].get('name')
#'cpe:/a:7-zip:7-zip:3.13'
# a[-1].get('name')
'cpe:/a:7-zip:p7zip:4.14.01'

result=tree.xpath(path)
print(result)

[contains(@name,'7-zip')]")

#for event, elem in iterparse(urlopen("http://online.effbot.org/rss.xml")):
#    if elem.tag == "item":
#        print elem.findtext("link"), "-", elem.findtext("title")
#        elem.clear() # won't need the children any more
