import urllib
import os

# =============================================================================
#   !!! This script will download approximately 18GB of compressed data !!!
# =============================================================================
#       this should start the data download in the directory "../data"
#           it is intended to be run from the scripts directory
# =============================================================================
p=".."
os.chdir("..")
p="data"
if not os.path.exists(p):
	os.makedirs(p)

os.chdir(p)

# =============================================================================
# some global definintions and functions
# =============================================================================
miturl=urllib.URLopener()
urldata='http://www.ll.mit.edu/mission/communications/cyber/CSTcorpora/ideval/data/'

def myMakedirs(plist):
	for p in plist:
		if not os.path.exists(p):
			os.makedirs(p)

def myFetchData(years, modes, weeks, days, files):
	for year in years:
		p=year
		myMakedirs([p])
		for mode in modes:
			p = year+'/'+mode
			myMakedirs([p])
			for week in weeks:
				p=year+'/'+mode+'/'+week
				myMakedirs([p])
				for day in days:
					p=year+'/'+mode+'/'+week+'/'+day
					myMakedirs([p])
					for fn in files:
						p=year+'/'+mode+'/'+week+'/'+day+'/'+fn
						if not os.path.isfile(p):
							try:
								print('myFetchData: fetching('+p+')')
								miturl.retrieve(urldata+p,p)
							except:
								print('myFetchData:     failed to retreive('+p+')')

# =============================================================================
# 1998
# =============================================================================

paths1998=['1998',
	'1998/testing',
	'1998/training',
	'1998/training/four_hours',
	'1998/training/sample',]

myMakedirs(paths1998)

files1998=[
	"pascal.bsm.gz",
	"pascal.praudit.gz",
	"pascal.psmonitor.gz",
	"bsm.list.gz",
	"tcpdump.list.gz",
	"tcpdump.gz",]

# -----------------------------------------------------------------------------
# 1998: training: weeks 1-2
# -----------------------------------------------------------------------------
weeks=['week1','week2']
for week in weeks:
	p = '1998/training/'+week
	myMakedirs([p])

miscfiles=[
	'1998/training/week1/README',
	'1998/training/week1/monday.tar',
	'1998/training/week1/tuesday.tar',
	'1998/training/week1/wednesday.tar',
	'1998/training/week1/thursday.tar',
	'1998/training/week1/friday.tar',
	'1998/training/week2/README',
	'1998/training/week2/monday.tar',
	'1998/training/week2/tuesday.tar',
	'1998/training/week2/wednesday.tar',
	'1998/training/week2/thursday.tar',
	'1998/training/week2/friday.tar',]

for p in miscfiles:
	if not os.path.isfile(p):
		miturl.retrieve(urldata+p,p)

# -----------------------------------------------------------------------------
# 1998: training: weeks 3-7
# -----------------------------------------------------------------------------
days=['monday','tuesday','wednesday','thursday','friday']
weeks=["week3","week4","week5","week6","week7"]
modes=["training"]
years=["1998"]
myFetchData(years, modes, weeks, days, files1998)

# -----------------------------------------------------------------------------
# 1998: training: four_hours; truth files
# -----------------------------------------------------------------------------
miscfiles=[
	'1998/training/four_hours/README',
	'1998/training/four_hours/bsm.gz',
	'1998/training/four_hours/tcpdump.gz',
	'1998/training/four_hours/pascal.praudit.gz',
	'1998/training/four_hours/root.dump.gz',
	'1998/training/four_hours/home.dump.gz',
	'1998/training/four_hours/usr.dump.gz',
	'1998/training/four_hours/opt.dump.gz',
	'1998/training/sample/DARPA_eval_b.readme',
	'1998/training/sample/DARPA_eval_b.tar.gz',
	'1998/Truth_Week_2.llist.tar.gz',
	'1998/Truth_Week_1.llist.tar.gz']

for p in miscfiles:
	if not os.path.isfile(p):
		miturl.retrieve(urldata+p,p)

# -----------------------------------------------------------------------------
# 1998: testing: weeks 1-2
# -----------------------------------------------------------------------------
days=['monday','tuesday','wednesday','thursday','friday']
weeks=['week1','week2']
modes=["testing"]
years=["1998"]
myFetchData(years, modes, weeks, days, files1998)

# =============================================================================
# 1999
# =============================================================================

paths1999=['1999',
'1999/testing',
'1999/training',]

myMakedirs(paths1999)

files1999=[
	'outside.tcpdump.gz',
	'fs_listing.tar.gz',
	'directory_dumps.tar.gz',
	'hume_evt.tar.gz',
	'pascal.bsm.gz',
	'inside.tcpdump.gz']

# -----------------------------------------------------------------------------
# 1999: training: weeks 1-3
# -----------------------------------------------------------------------------
days=['monday','tuesday','wednesday','thursday','friday']
weeks=['week1','week2','week3']
modes=["training"]
years=["1999"]
myFetchData(years, modes, weeks, days, files1999)

# -----------------------------------------------------------------------------
# 1999: testing: weeks 4-5
# -----------------------------------------------------------------------------
days=['monday','tuesday','wednesday','thursday','friday']
weeks=['week4','week5']
modes=["testing"]
years=["1999"]
myFetchData(years, modes, weeks, days, files1999)

# -----------------------------------------------------------------------------
# 1999: miscellaneus files
# -----------------------------------------------------------------------------
miscfiles=[	
	'1999/pascal_config.tar.gz',
	'1999/testing/week5/monday/51hume_evt.tar.gz',
	'1999/testing/week4/tuesday/42hume_evt.tar.gz',
	'1999/testing/week4/wednesday/43hume_evt.tar.gz',
	'1999/testing/week4/thursday/44hume_evt.tar.gz',
	'1999/testing/week5/monday/pascal.bsm.tar.gz',
	'1999/testing/week5/tuesday/pascal.bsm.tar.gz',
	'1999/testing/week5/wednesday/pascal.bsm.tar.gz',
	'1999/testing/week5/thursday/pascal.bsm.tar.gz']

for p in miscfiles:
	if not os.path.isfile(p):
		miturl.retrieve(urldata+p,p)

# -----------------------------------------------------------------------------
# extras in week3
# -----------------------------------------------------------------------------
extras=['extra_monday','extra_tuesday','extra_wednesday']
weeks=['week3']
modes=["training"]
years=["1999"]
myFetchData(years, modes, weeks, extras, files1999)
