# http://sourceforge.net/projects/pywin32/files/
# pywin32-219.win-amd64-py2.7.exe OR pywin32-219.win32-py2.7.exe
# pip install wmi

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
    path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}registry_object[@id='"+strid+"']"
    findall = etree.ETXPath(path)
    obj=findall(tree)
    hive=obj[0][0].text
    key=obj[0][1].text
    name=obj[0][2].text
    return {'hive':hive, 'key':key, 'name':name}

'''
    <registry_state id="oval:org.mitre.oval:ste:27503" version="2" comment="State matches if the release version is equal to 378675" xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows">
      <value>378675</value>
    </registry_state>
'''
def get_registry_state(tree, strid):
    path="//{http://oval.mitre.org/XMLSchema/oval-definitions-5#windows}registry_state[@id='"+strid+"']"
    findall = etree.ETXPath(path)
    obj=findall(tree)
    value=obj[0][0].text
    return {'value':value}

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
    obj=findall(tree)
    # prototype only: this includes unacceptable assumptions
    d_object=get_registry_object(tree, obj[0][0].get('object_ref'))
    d_state=get_registry_state(tree, obj[0][1].get('state_ref'))
    p=re.compile(d['value'])
    c = wmi.WMI(namespace="default").StdRegProv
    if d_object['hive']=='HKEY_LOCAL_MACHINE':
        winhive=_winreg.HKEY_LOCAL_MACHINE
    key = _winreg.OpenKey(winhive,d_object['key'], 0, _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY)
    value = _winreg.QueryValueEx(key, d_object['name'])
    return not re.match(d['value'],str(value[0]))==None

    
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


