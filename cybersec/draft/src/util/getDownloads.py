from lxml import etree
import urllib
import os
from zipfile import ZipFile

def dlfile(url, dldir, fn):
    thisfile = urllib.URLopener()
    thisfile.retrieve(url, dldir+'/'+fn)

def uzip(source_filename, dest_dir):
    zip=ZipFile(dest_dir+'/'+source_filename) 
    zip.extractall(dest_dir)

fn = "/projects/rhinohide.org/cybersec/draft/data/NIST-CVE/download.html"
sep = os.sep
dldir = sep.join(fn.split('/')[0:-1])

# Parse the download file into xml tree
tree = etree.parse(fn)
root = tree.getroot()
path="/html/body/a"
find = etree.XPath(path)
links=find(root)

for a in links:
    af = a.get('href').split('/')[-1].replace('.zip','')
    if a.get('class') == 'manual':
        # manual download required
        print("Please download the file "+a.text+" from the following url")
        print(a.get('href'))
    elif a.get('class') == 'auto':
        # file exists
        if os.path.isfile(dldir+os.sep+af):
            print("File already exists: "+af )
        # zip file exists; unzip
        elif os.path.isfile(dldir+os.sep+af+".zip"):
            print("Unzipping "+af+'.zip')
            uzip(af+'.zip',dldir)
        else:
            # initiate download
            print("Starting download for the file "+af + " from the following url")
            print(a.get('href'))
            try:
                urllib.urlretrieve(a.get('href'), dldir+'/'+a.get('href').split('/')[-1])
                if os.path.isfile(dldir+os.sep+af+".zip"):
                    print("Unzipping "+af+'.zip')
                    try:
                        uzip(af+'.zip',dldir)
                    except:
                        print(">>>> Unzip FAILED for "+af)
            except:
                print(">>>> Download FAILED for "+af)

