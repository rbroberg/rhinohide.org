# http://sourceforge.net/projects/pywin32/files/
# pywin32-219.win-amd64-py2.7.exe OR pywin32-219.win32-py2.7.exe
# pip install wmi

# alterative to wmi?
# https://www.mandiant.com/blog/parsing-registry-hives-python/

# repositories
# https://oval.mitre.org/rep-data/5.10/org.mitre.oval/i/index.html

from lxml import etree

import _winreg
import wmi
import re

'''
    <registry_object id="oval:org.mitre.oval:obj:11742" version="1" comment="Registry that holds the DisplayName of the Windows Movie Maker 2.6 installed" xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows">
      <hive>HKEY_LOCAL_MACHINE</hive>
      <key>SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{B3DAF54F-DB25-4586-9EF1-96D24BB14088}</key>
      <name>DisplayName</name>
    </registry_object>
'''
# nested sets: strid="oval:org.mitre.oval:obj:7290"
def get_registry_object(tree, strid):
	l_regobj=[] # list of dictionaries
	path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}registry_object[@id='"+strid+"']"
	findall = etree.ETXPath(path)
	robj=findall(tree)[0]
	# if this is a set, recurse
	path="./{http://oval.mitre.org/XMLSchema/oval-definitions-5}set"
	rset = robj.find(path)
	if not rset is None:
		#nested sets - not recursive only goes down to level 2
		path="./{http://oval.mitre.org/XMLSchema/oval-definitions-5}set"
		rset2=rset.findall(path)
		for s in rset2:
			# objects at this level
			path="./{http://oval.mitre.org/XMLSchema/oval-definitions-5}object_reference"
			lobj=s.findall(path)
			for l in lobj:
				try: l_regobj=l_regobj+get_registry_object(tree,l.text)
				except: print "non fatal error while processing strid: "+strid
		# objects at this level
		path="./{http://oval.mitre.org/XMLSchema/oval-definitions-5}object_reference"
		lobj=rset.findall(path)
		for l in lobj:
			try: l_regobj=l_regobj+get_registry_object(tree,l.text)
			except: print "non fatal error while processing strid: "+strid
	else:
		# not a set
		try: hive=robj.find("./{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}hive").text
		except: hive=None
		
		try: key=robj.find("./{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}key").text # could include pattern match
		except: key=None
		
		try: name=robj.find("./{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}name").text
		except: name=None
		
		try: behaviors = robj.find("./{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}behaviors").get('windows_view')
		except:	behaviors = None
		
		try: keyop = robj.find("./{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}key").get('operation')
		except:	keyop = None
		
		l_regobj=[{'hive':hive, 'key':key, 'name':name, 'view':behaviors, 'keyop':keyop}]
	
	# flatten list
	return l_regobj

# simple registry object
# get_registry_object(tree, "oval:org.mitre.oval:obj:24058" )

# nested registry object
# get_registry_object(tree, "oval:org.mitre.oval:obj:23956")

'''
    <registry_state id="oval:org.mitre.oval:ste:27503" version="2" comment="State matches if the release version is equal to 378675" xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows">
      <value>378675</value>
    </registry_state>
'''
# different datatypes, operations
# also registry_state can be key instead of value
def get_registry_state(tree, strid):
    path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}registry_state[@id='"+strid+"']"
    findall = etree.ETXPath(path)
    obj=findall(tree)[0]
    value=obj.find("./{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}value")
    key=obj.find("./{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}key")
    if value is not None:
        try:
            valop=value.get('operation')
        except:
            valup=None
        valtext=value.text
        try:
            valtype=value.get('datetype')
        except:
            valtype=None
    else: 
        valop=None
        valtext=None
        valtype=None
    if key is not None:
        try:
            keyop=key.get('operation')
        except:
            keyop=None
        keytext=key.text
    else: 
        keyop=None
        keytext=None
    
    return {'value':valtext, 'valop':valop, 'datatype':valtype, 'key':keytext, 'keyop':keyop}

#get_registry_state(tree, "oval:org.mitre.oval:ste:19893")
'''
    <family_test id="oval:org.mitre.oval:tst:99" version="1" comment="the installed operating system is part of the Microsoft Windows family" check_existence="at_least_one_exists" check="only one" xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#independent">
      <object object_ref="oval:org.mitre.oval:obj:99"/>
      <state state_ref="oval:org.mitre.oval:ste:99"/>
    </family_test>
'''
import os
# TODO: many simplified assumptions here
def eval_family_state(strfam):
	if os.name == "nt" and strfam.lower() == "windows":
		return True
	elif os.name == "posix" and strfam.lower() == "unix":
		return True
	else:
		return False

# strid="oval:org.mitre.oval:ste:99"
def get_family_state(tree, strid):
	path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5#independent}family_state[@id='"+strid+"']"
	findall = etree.ETXPath(path)
	obj=findall(tree)[0]
	fam=obj.find("./{http://oval.mitre.org/XMLSchema/oval-definitions-5#independent}family")
	try: famtext=fam.text
	except: famtext=None
	try: famop=fam.get('operation')
	except: famop=None
	return {'famtext':famtext, 'famop':famop}

#strid="oval:org.mitre.oval:tst:99"
def eval_family_test(tree, strid):
	l_regtest=[]
	path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5#independent}family_test[@id='"+strid+"']"
	findall = etree.ETXPath(path)
	try:
		rtest=findall(tree)[0]
	except:
		return -1
	
	# state
	ste=rtest.findall('./{http://oval.mitre.org/XMLSchema/oval-definitions-5#independent}state')
	try: l_state = [get_family_state(tree, ste[0].get('state_ref'))]
	except: print "non fatal error in family state for strid: "+strid
	
	# logical operation
	# TODO: ops are different from family_test than registry_test
	regop='AND'
	try:
		if rtest.get('check')=='at least one': regop='OR'
	except:
		print "non fatal error in determining op for strid: "+strid
	
	try:
		return eval_family_state(l_state[0]['famtext'])
	except:
		return -1

'''
    <registry_test id="oval:org.mitre.oval:tst:100228" version="2" comment="Check if the release version of .Net framework 4.5.1 (full) is equal to 378675" check_existence="at_least_one_exists" check="all" xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows">
      <object object_ref="oval:org.mitre.oval:obj:30444"/>
      <state state_ref="oval:org.mitre.oval:ste:27503"/>
    </registry_test>
'''

# check_existence=['at_least_one_exists']
# check=['at least one', 'all']

# _winreg.HKEY_CLASSES_ROOT
# _winreg.HKEY_CURRENT_USER
# _winreg.HKEY_LOCAL_MACHINE
# _winreg.HKEY_USERS
# _winreg.HKEY_PERFORMANCE_DATA
# _winreg.HKEY_CURRENT_CONFIG
def eval_registry_value(keydict, valdict):
	c = wmi.WMI(namespace="default").StdRegProv
	if keydict['hive']=='HKEY_CLASSES_ROOT':
		winhive=_winreg.HKEY_CLASSES_ROOT
	elif keydict['hive']=='HKEY_CURRENT_USER':
		winhive=_winreg.HKEY_CURRENT_USER
	elif keydict['hive']=='USERS':
		winhive=_winreg.HKEY_USERS
	elif keydict['hive']=='HKEY_LOCAL_MACHINE':
		winhive=_winreg.HKEY_LOCAL_MACHINE
	elif keydict['hive']=='HKEY_PERFORMANCE_DATA':
		winhive=_winreg.HKEY_PERFORMANCE_DATA
	elif keydict['hive']=='HKEY_CURRENT_CONFIG':
		winhive=_winreg.HKEY_CURRENT_CONFIG
	else:
		print "eval_registry_value: no hive defined"
		return -1
	
	# need to deal with key patterns as well as value patterns
	try:
		if keydict['view']=="32_bit":
			key32 = keydict['key'].replace("SOFTWARE","SOFTWARE\\\\Wow6432Node")
			key = _winreg.OpenKey(winhive,key32, 0, _winreg.KEY_READ)
			value = _winreg.QueryValueEx(key, keydict['name'])
		else:
			key = _winreg.OpenKey(winhive,keydict['key'], 0, _winreg.KEY_READ)
			value = _winreg.QueryValueEx(key, keydict['name'])
		if valdict['valop'] is None:
			return eval_version(str(value[0]),valdict['value'],None)
		else:
			return eval_version(str(value[0]),valdict['value'],valdict['valop'])		
	except:
		# would be better to test non-existence rather than assume it on failure
		return False
	# how did I get here?
	return -1

def eval_registry_key(keydict):
	c = wmi.WMI(namespace="default").StdRegProv
	if keydict['hive']=='HKEY_CLASSES_ROOT':
		winhive=_winreg.HKEY_CLASSES_ROOT
	elif keydict['hive']=='HKEY_CURRENT_USER':
		winhive=_winreg.HKEY_CURRENT_USER
	elif keydict['hive']=='USERS':
		winhive=_winreg.HKEY_USERS
	elif keydict['hive']=='HKEY_LOCAL_MACHINE':
		winhive=_winreg.HKEY_LOCAL_MACHINE
	elif keydict['hive']=='HKEY_PERFORMANCE_DATA':
		winhive=_winreg.HKEY_PERFORMANCE_DATA
	elif keydict['hive']=='HKEY_CURRENT_CONFIG':
		winhive=_winreg.HKEY_CURRENT_CONFIG
	else:
		print "eval_registry_value: no hive defined"
		return -1
	
	# need to deal with key patterns as well as value patterns
	try:
		if keydict['view']=="32_bit":
			key32 = keydict['key'].replace("SOFTWARE","SOFTWARE\\\\Wow6432Node")
			key = _winreg.OpenKey(winhive,key32, 0, _winreg.KEY_READ)
		else:
			key = _winreg.OpenKey(winhive,keydict['key'], 0, _winreg.KEY_READ)
	except:
		# would be better to test non-existence rather than assume it on failure
		return False
	# how did I get here?
	return -1

def eval_registry_test(tree, strid):
	l_regtest=[]
	path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}registry_test[@id='"+strid+"']"
	findall = etree.ETXPath(path)
	try:
		rtest=findall(tree)[0]
	except:
		return -1
	# prototype only: this includes unacceptable assumptions
	
	# object
	obj=rtest.findall('./{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}object')
	if len(obj)>0: l_object=get_registry_object(tree, obj[0].get('object_ref'))
	else: return -1
	
	# state
	ste=rtest.findall('./{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}state')
	l_state=[]
	for i in range(len(ste)):
		try: l_state.append(get_registry_state(tree, ste[0].get('state_ref')))
		except: print "not fatal error in registry state for strid: "+strid
	
	# logical operation
	regop='AND'
	try:
		if rtest.get('check')=='at least one': regop='OR'
	except:
		print "non fatal error in determining op for strid: "+strid
	
	# if state exists and only one object, eval object against each state
	# there could be two objects [32bit & 64bit] ignored for now
	if len(l_state) > 0:
		for i in range(len(l_state)):
			l_regtest.append(eval_registry_value(l_object[0],l_state[i]))
		return eval_logicallist(l_regtest,regop)
	else:
		for i in range(len(l_object)):
			l_regtest.append(eval_registry_key(l_object[i]))
		return eval_logicallist(l_regtest,regop)
	
	return -1

#strid="oval:org.mitre.oval:tst:100228"
#get_registry_test(tree,"oval:org.mitre.oval:tst:87142") # IE 11
#get_registry_test(tree,"oval:org.mitre.oval:tst:80429") # IE 10
#get_registry_test(tree,"oval:org.mitre.oval:tst:86752") # Office 2010 with more than one state

# ops = set(['pattern match', 'greater than or equal', 'case insensitive equals', 'less than', 'greater than', None])
def eval_bit(v1, v2, op):
	if op is None: return v1 == v2
	if op == 'equals': return v1 == v2
	if op == 'case insensitive equals': return v1.lower() == v2.lower()
	if op == 'greater than': return v1 > v2
	if op == 'greater than or equal': return v1 >= v2
	if op == 'lesser than': return v1 < v2
	if op == 'lesser than or equal': return v1 <= v2
	return -1

def eval_version(v1, v2, op):
	if op == 'pattern match': return not re.match(v2,v1)==None
	else:
		s1=split(v1,'.')
		s2=split(v2,'.')
		llist = []
		for i in range(min(len(s1),len(s2))):
			llist.append(eval_bit(s1[i],s2[i],op))
		if len(s1)>len(s2):
			llist.append(eval_bit("dummy","",op))
		if len(s2)>len(s1):
			llist.append(eval_bit("","dummy",op))
		return eval_logicallist(llist,'AND')
	# how did I get here?
	return -1

# strid='oval:org.mitre.oval:tst:86752'
def eval_test(tree, strid):
    # registry_test
    path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}registry_test[@id='"+strid+"']"
    findall = etree.ETXPath(path)
    if len(findall(tree)) > 0:
        return eval_registry_test(tree, strid)
    
    # family_test
    path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5#independent}family_test[@id='"+strid+"']"
    findall = etree.ETXPath(path)
    if len(findall(tree)) > 0:
        return eval_family_test(tree, strid)
    
    # cannot evaluate
    return -1


fnxml="/projects/rhinohide.org/cybersec/draft/data/MITRE-OVAL/microsoft.windows.7.xml"
tree = etree.parse(fnxml)
root = tree.getroot()

path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5}definition"
findall = etree.ETXPath(path)
a=findall(tree)
a[0].get('class') # inventory
list(a[0]) # metadata, criteria

for aa in a[200:300]:
	e=eval_definition(tree,aa.get('id'))
	#print aa.get('id'), e)
	if e:
		get_definition_cpe(tree, aa.get('id'))


# TODO: there are a very small number of multi-cpe (2)
def get_definition_cpe(tree, strid):
	path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5}definition[@id='"+strid+"']"
	findall = etree.ETXPath(path)
	df = findall(tree)[0]
	try:
		cpath=".//{http://oval.mitre.org/XMLSchema/oval-definitions-5}reference"
		cpe = df.find(cpath)
		return cpe.get('ref_id')
	except:
		return -1

	

# all definition in microsoft.windows.7.xml have only two children, meta and criteria
# criteria can have logical 'operator' 'AND' 'OR'
# criteria can be nested
# criteria can have 'extended_definition'

# example of nested, with OR and AND operators
# id="oval:org.mitre.oval:def:22275"
path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5}definition[contains(@id,'def:22275')]"
findall = etree.ETXPath(path)
b=findall(tree)
b[0].get('id') # 'oval:org.mitre.oval:def:22275'
b[0][1][0][0].get('test_ref') # 'oval:org.mitre.oval:tst:100228'

# always one object but one or more states per registry test?
get_registry_test(tree, "oval:org.mitre.oval:tst:87142") # True
get_registry_test(tree, b[0][1][0][0].get('test_ref')) # False

# need recursive function test_criteria
# in which nested logical criteria are evalauted

# read elements of criteria at this level
# evaluate criterion
# recursion on criteria
def eval_logicallist(llist, op):
	# strip None elements
	logicallist=[item for item in llist if not item is None]
	# if any element is -1, then cannot evaluate
	if len([i for i in logicallist  if i==-1])>0:
		return -1
	# op is 'AND' or 'OR'
	if op == 'AND' and sum(logicallist)==len(logicallist):
		return True
	elif op == 'OR' and sum(logicallist)>0:
		return True
	else:
		return False

l0=[False,False,False]
l1=[True,True,True]
l2=[True, False, False]
l3=[-1,True,False]
eval_logicallist(l3,'AND')

def eval_criteria(tree, criteria):
	# get operator
	# get list of criterion
	# get list of child criteria
	
	if not criteria.get('operator') is None:
		op=criteria.get('operator') 
	else:
		op='AND'
	
	# get criterion
	dpath="./{http://oval.mitre.org/XMLSchema/oval-definitions-5}criterion"
	d=criteria.findall(dpath)

	# eval criterion
	llist1 = [eval_test(tree, cc.get('test_ref')) for cc in d]
	return eval_logicallist(llist1, op)


def eval_definition(tree, strid):
	path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5}definition[contains(@id,'"+strid+"')]"
	findall = etree.ETXPath(path)
	dobj=findall(tree)[0]
	cpath="./{http://oval.mitre.org/XMLSchema/oval-definitions-5}criteria"
	return eval_criteria(tree, dobj.find(cpath))



# nested level AND
# oval:org.mitre.oval:def:7384
path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5}definition[contains(@id,'def:22275')]"

# 1 level AND
# oval:org.mitre.oval:def:7384
path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5}definition[contains(@id,'def:7384')]"
findall = etree.ETXPath(path)
b=findall(tree)
cpath="./{http://oval.mitre.org/XMLSchema/oval-definitions-5}criteria"
c=b[0].findall(cpath)[0]

# get operator

# https://oval.mitre.org/language/version5.11/ovaldefinition/minimal/oval-definitions-schema.xsd
# https://oval.mitre.org/language/version5.11/ovaldefinition/minimal/windows-definitions-schema.xsd

# -----------------------------------------------------------------------------
# DEFINITIONS
# -----------------------------------------------------------------------------
# /oval_definitions/definitions/definition [id|version|class] # class="inventory"
# /oval_definitions/definitions/definition/metadata/title
# /oval_definitions/definitions/definition/metadata/affected/platform
# /oval_definitions/definitions/definition/metadata/reference [source|ref_id] # CPEs
# /oval_definitions/definitions/definition/metadata/criteria/criterion [comment|test_ref] # test ref maps to new object

# -----------------------------------------------------------------------------
# TESTS
# -----------------------------------------------------------------------------
# /oval_definitions/tests/registry_tests
# /oval_definitions/tests/rpminfo_test
# /oval_definitions/tests/textfilecontent54_test
# /oval_definitions/tests/file_test

# -----------------------------------------------------------------------------
# OBJECTS
# -----------------------------------------------------------------------------
# /oval_definitions/objects/registry_object
# /oval_definitions/objects/rpminfo_object
# /oval_definitions/objects/file_object

# -----------------------------------------------------------------------------
# STATES
# -----------------------------------------------------------------------------
# /oval_definitions/states/registry_state
# /oval_definitions/states/oslevel_state
# /oval_definitions/states/textfilecontent54_state
# /oval_definitions/states/file_state
# /oval_definitions/states/version_state

# -----------------------------------------------------------------------------
# VARIABLES
# -----------------------------------------------------------------------------
# /oval_definitions/variables/local_variable


'''
# How many definitions?
path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5}definition"
findall = etree.ETXPath(path)
a=findall(tree)
a[0].get('class') # inventory
list(a[0]) # meta, criteria
len(a) # 562

path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5}reference[@source='CPE']"
findall = etree.ETXPath(path)
b=findall(tree)
len(b) # 564 -> more than one CPE per definition?

# how many with less than one CPE: 0
tot=0
path="./{http://oval.mitre.org/XMLSchema/oval-definitions-5}reference[@source='CPE']"
for aa in a:
    if len(aa[0].findall(path))<1:
        tot = tot+1
        aa.get('id')

tot


#how many with more than one: 2
tot=0
path="./{http://oval.mitre.org/XMLSchema/oval-definitions-5}reference[@source='CPE']"
for aa in a:
    if len(aa[0].findall(path))>1:
        tot = tot+1
        b=aa[0].findall(path)
        for bb in b: 
            aa.get('id'), bb.get('ref_id')

tot

'''

'''
def getKeys(winhive,keyset,key):
    this=_winreg.OpenKey(winhive, key, 0, _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY)
    itr=_winreg.QueryInfoKey(this)[0]
    for i in range(itr):
        nkey=key+"\\"+_winreg.EnumKey(this,i)
        if nkey[:1]=="\\": nkey=nkey[1:]
        #print i,nkey
        keyset.add(nkey)
        try:
            getKeys(winhive,keyset,nkey)
        except:
            print "error: "+nkey
    return list(keyset)

hkcu=getKeys(_winreg.HKEY_CURRENT_USER, set(), "")
hklm=getKeys(_winreg.HKEY_LOCAL_MACHINE, set(), "")
'''