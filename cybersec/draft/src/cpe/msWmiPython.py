# http://sourceforge.net/projects/pywin32/files/
# pywin32-219.win-amd64-py2.7.exe
# pip install wmi

import _winreg
import wmi

# "HKLM/SOFTWARE/Wow6432Node/Microsoft/Windows/CurrentVersion/Uninstall/Adobe Flash Player Plugin"
# DisplayName
# DisplayVersion
# VersionMajor
# VersionMinor

# cpe:/a:microsoft:ie:11

# ----------------
'''
    <definition id="oval:org.mitre.oval:def:18343" version="7" class="inventory">
      <metadata>
        <title>Microsoft Internet Explorer 11 is installed</title>
        <affected family="windows">
          <platform>Microsoft Windows 7</platform>
          <platform>Microsoft Windows 8</platform>
          <platform>Microsoft Windows Server 2012</platform>
          <platform>Microsoft Windows 8.1</platform>
          <platform>Microsoft Windows Server 2008 R2</platform>
          <platform>Microsoft Windows Server 2012 R2</platform>
          <product>Microsoft Internet Explorer 11</product>
        </affected>
        <reference source="CPE" ref_id="cpe:/a:microsoft:ie:11"/>
        <description>Microsoft Internet Explorer 11 is installed</description>
        <oval_repository>
          <dates>
            <submitted date="2013-11-15T11:11:35">
              <contributor organization="SecPod Technologies">SecPod Team</contributor>
            </submitted>
            <status_change date="2013-11-18T19:08:25.972-05:00">DRAFT</status_change>
            <status_change date="2013-12-09T04:00:08.269-05:00">INTERIM</status_change>
            <status_change date="2013-12-30T04:00:14.534-05:00">ACCEPTED</status_change>
            <modified comment="EDITED oval:org.mitre.oval:def:18343 - Updating platforms for Internet Explorer 11." date="2013-12-30T09:03:00.322-05:00">
              <contributor organization="ALTX-SOFT">Maria Kedovskaya</contributor>
            </modified>
            <status_change date="2013-12-30T09:07:45.958-05:00">INTERIM</status_change>
            <status_change date="2014-01-20T04:00:17.922-05:00">ACCEPTED</status_change>
            <modified comment="EDITED oval:org.mitre.oval:obj:23453 - Updated comment to include IE 11 given that this object is referenced by IE 11 inventory definitions." date="2014-12-05T18:57:00.896-05:00">
              <contributor organization="CIS">Blake Frantz</contributor>
            </modified>
            <status_change date="2014-12-05T18:59:51.501-05:00">INTERIM</status_change>
            <status_change date="2014-12-22T04:00:06.360-05:00">ACCEPTED</status_change>
          </dates>
          <status>ACCEPTED</status>
        </oval_repository>
      </metadata>
      <criteria operator="AND">
        <criterion comment="Check if Microsoft Internet Explorer 11 is installed" test_ref="oval:org.mitre.oval:tst:87142"/>
      </criteria>
    </definition>
'''
# ----------------
'''
   <registry_test id="oval:org.mitre.oval:tst:87142" version="2" comment="Check if Microsoft Internet Explorer 11 is installed" check_existence="at_least_one_exists" check="all" xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows">
      <object object_ref="oval:org.mitre.oval:obj:23453"/>
      <state state_ref="oval:org.mitre.oval:ste:24230"/>
    </registry_test>
'''
# ----------------
'''
    <registry_object id="oval:org.mitre.oval:obj:23453" version="2" comment="Object holds the version of IE 10 or IE 11" xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows">
      <hive>HKEY_LOCAL_MACHINE</hive>
      <key>SOFTWARE\Microsoft\Internet Explorer</key>
      <name>svcVersion</name>
    </registry_object>
'''
'''
    <registry_state id="oval:org.mitre.oval:ste:24230" version="1" comment="State matches if Microsoft Internet Explorer 11 is installed" xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows">
      <value operation="pattern match">^11\..*$</value>
    </registry_state>
'''

c = wmi.WMI(namespace="default").StdRegProv
key = _winreg.OpenKey(
    _winreg.HKEY_LOCAL_MACHINE,
    "SOFTWARE\Microsoft\Internet Explorer",
    0, _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY)

name = _winreg.QueryValueEx(key, "svcVersion")
print name[0]
# 11.0.9600.17498
























'''
    <registry_test id="oval:org.mitre.oval:tst:125493" version="1" comment="Adobe Flash Player 15.x is installed on the system" check_existence="at_least_one_exists" check="at least one" xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows">
      <object object_ref="oval:org.mitre.oval:obj:7290"/>
      <state state_ref="oval:org.mitre.oval:ste:34567"/>
    </registry_test>
'''
'''
    <registry_object id="oval:org.mitre.oval:obj:7290" version="4" comment="Registry that holds the versions of all Flash Player instances" xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows">
      <set xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5">
        <set>
          <object_reference>oval:org.mitre.oval:obj:27479</object_reference>
          <object_reference>oval:org.mitre.oval:obj:27174</object_reference>
        </set>
        <set>
          <object_reference>oval:org.mitre.oval:obj:27426</object_reference>
        </set>
      </set>
    </registry_object>
'''
'''
    <registry_object id="oval:org.mitre.oval:obj:27174" version="1" comment="Registry that holds the version of Flash Player from HKLM\SOFTWARE\Macromedia\FlashPlayerPlugin!Version" xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows">
      <set xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5">
        <object_reference>oval:org.mitre.oval:obj:27254</object_reference>
        <object_reference>oval:org.mitre.oval:obj:27358</object_reference>
      </set>
    </registry_object>

'''
'''
    <registry_object id="oval:org.mitre.oval:obj:27254" version="1" comment="Registry that holds the version of Flash Player from HKLM\SOFTWARE\Macromedia\FlashPlayerPlugin!Version" xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows">
      <hive>HKEY_LOCAL_MACHINE</hive>
      <key>SOFTWARE\Macromedia\FlashPlayerPlugin</key>
      <name>Version</name>
    </registry_object>
'''
'''
    <registry_state id="oval:org.mitre.oval:ste:34567" version="1" comment="Regex matching the Adobe Flash Player 15.x installed" xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows">
      <value operation="pattern match">^15\..*$</value>
    </registry_state>
'''
