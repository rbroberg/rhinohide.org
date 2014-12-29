from lxml import etree

# https://nvd.nist.gov/schema/nvd-cve-feed_2.0.xsd
# nvd.nist.gov/schema/vulnerability_0.4.xsd

#    <vuln:vulnerable-software-list>
#      <vuln:product>cpe:/o:linux:linux_kernel:2.6.20.1</vuln:product>
#    </vuln:vulnerable-software-list>

fn="/projects/rhinohide.org/cybersec/draft/data/NIST-CVE/nvdcve-2.0-2004.xml"

tree = etree.parse(fn)
root = tree.getroot()

path="//{http://scap.nist.gov/schema/feed/vulnerability/2.0}entry')]"
findall = etree.ETXPath(path)
a=findall(tree)

f=open("/projects/rhinohide.org/cybersec/draft/data/NIST-CPE/mscpe.txt", 'w')
for p in a:
    f.write(p.get('name')+'\n')

f.close()

    