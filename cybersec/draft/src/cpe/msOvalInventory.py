# http://sourceforge.net/projects/pywin32/files/
# pywin32-219.win-amd64-py2.7.exe OR pywin32-219.win32-py2.7.exe
# pip install wmi

# https://www.mandiant.com/blog/parsing-registry-hives-python/

from lxml import etree

import _winreg
import wmi
import re
# _winreg.HKEY_CLASSES_ROOT
# _winreg.HKEY_CURRENT_USER
# _winreg.HKEY_LOCAL_MACHINE
# _winreg.HKEY_USERS
# _winreg.HKEY_PERFORMANCE_DATA
# _winreg.HKEY_CURRENT_CONFIG
# 

'''
    <registry_object id="oval:org.mitre.oval:obj:11742" version="1" comment="Registry that holds the DisplayName of the Windows Movie Maker 2.6 installed" xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows">
      <hive>HKEY_LOCAL_MACHINE</hive>
      <key>SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{B3DAF54F-DB25-4586-9EF1-96D24BB14088}</key>
      <name>DisplayName</name>
    </registry_object>
'''
def get_registry_object(tree, strid):
    # this does not deal with nested sets
    path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}registry_object[@id='"+strid+"']"
    findall = etree.ETXPath(path)
    robj=findall(tree)[0]
    hive=robj.find("./{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}hive").text
    key=robj.find("./{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}key").text # could include pattern match
    name=robj.find("./{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}name").text
    try:
        behaviors = robj.find("./{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}behaviors").get('windows_view')
    except:
        behaviors = None
    try:
        keyop = robj.find("./{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}key").get('operation')
    except:
        keyop = None
    return {'hive':hive, 'key':key, 'name':name, 'view':behaviors, 'keyop':keyop}

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

get_registry_state(tree, "oval:org.mitre.oval:ste:19893")

'''
    <registry_test id="oval:org.mitre.oval:tst:100228" version="2" comment="Check if the release version of .Net framework 4.5.1 (full) is equal to 378675" check_existence="at_least_one_exists" check="all" xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows">
      <object object_ref="oval:org.mitre.oval:obj:30444"/>
      <state state_ref="oval:org.mitre.oval:ste:27503"/>
    </registry_test>
'''
strid="oval:org.mitre.oval:tst:100228"
def get_registry_test(tree, strid):
    path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}registry_test[@id='"+strid+"']"
    findall = etree.ETXPath(path)
    rtest=findall(tree)[0]
    # prototype only: this includes unacceptable assumptions
    # object
    obj=rtest.findall('./{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}object')
    if len(obj)>0: d_object=get_registry_object(tree, obj[0].get('object_ref'))
    else: return -1
    # state
    ste=rtest.findall('./{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}state')
    if len(ste)>0: d_state=get_registry_state(tree, ste[0].get('state_ref'))
    else: d_state={value:''}
    #p=re.compile(d_state['value'])
    c = wmi.WMI(namespace="default").StdRegProv
    if d_object['hive']=='HKEY_LOCAL_MACHINE':
        winhive=_winreg.HKEY_LOCAL_MACHINE
    key = _winreg.OpenKey(winhive,d_object['key'], 0, _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY)
    value = _winreg.QueryValueEx(key, d_object['name'])
    return not re.match(d_state['value'],str(value[0]))==None


def eval_winreg_key_patternmatch(hive,key)
        c = wmi.WMI(namespace="default").StdRegProv
fnxml="/projects/rhinohide.org/cybersec/draft/data/MITRE-OVAL/microsoft.windows.7.xml"
tree = etree.parse(fnxml)
root = tree.getroot()

path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5}definition"
findall = etree.ETXPath(path)
a=findall(tree)
a[0].get('class') # inventory
list(a[0]) # meta, criteria

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
get_registry_test(tree, "oval:org.mitre.oval:tst:87142")
get_registry_test(tree, b[0][1][0][0].get('test_ref'))

strid='oval:org.mitre.oval:tst:21126'
def eval_test(tree, strid):
    # registry_test
    path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}registry_test[@id='"+strid+"']"
    findall = etree.ETXPath(path)
    if len(findall(tree)) > 0:
        return get_registry_test(tree, strid)
    
    # cannot evaluate
    return -1
   
# need recursive function test_criteria
# in which nested logical criteria are evalauted

# read elements of criteria at this level
# evaluate criterion
# recursion on criteria
def eval_logicallist(logicallist, op):
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

def eval_criteria(criteria)
    # get operator
    # get list of criterion
    # get list of child criteria


# get operator
if c.get('operator'):
    op=c.get('operator') 
else:
    op='AND'

# get criterion
dpath="./{http://oval.mitre.org/XMLSchema/oval-definitions-5}criterion"
d=c.findall(dpath)
# eval criterion
llist1 = [eval_test(tree, cc.get('test_ref')) for cc in d]

# 1 level AND
# oval:org.mitre.oval:def:7384
path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5}definition[contains(@id,'def:7384')]"
findall = etree.ETXPath(path)
b=findall(tree)
cpath="./{http://oval.mitre.org/XMLSchema/oval-definitions-5}criteria"
c=b[0].findall(cpath)[0]


# nested level AND
# oval:org.mitre.oval:def:7384
path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5}definition[contains(@id,'def:22275')]"

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