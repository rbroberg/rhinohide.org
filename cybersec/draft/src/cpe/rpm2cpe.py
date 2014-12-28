#!/usr/bin/python
# Useage: python rpm2cpe.py

import rpm
import commands

# match format used in Red Hat CPE/CVE mapping
# https://www.redhat.com/security/data/metrics/rhsamapcpe.txt
# only tested in Amazon EC2 free RHEL 7 instance
status, output = commands.getstatusoutput("hostnamectl")
osstr=output.split('CPE OS Name: ')[1].split('\n')[0]
#osstr=osstr.replace('cpe:/o:','cpe:/a:')
osstr=osstr.replace('.0:GA:','::') 

ts = rpm.TransactionSet()
mi = ts.dbMatch()

for h in mi:
    print "%s/%s" % (osstr, h['name'])

'''
# Sample listing from RHSA MAP CPE
# I'm still unclear when Red Hat uses cpe:/o versus cpe:/a
# openstack and  jboss, though, would be under cpe:/a
RHSA-2014:1826
CVE-2014-6051,CVE-2014-6052,CVE-2014-6053,CVE-2014-6054,CVE-2014-6055
cpe:/o:redhat:enterprise_linux:6::server/libvncserver
cpe:/o:redhat:enterprise_linux:6::client/libvncserver
cpe:/o:redhat:enterprise_linux:6::server/libvncserver
cpe:/o:redhat:enterprise_linux:6::workstation/libvncserver
cpe:/o:redhat:enterprise_linux:7::client/libvncserver
cpe:/o:redhat:enterprise_linux:7::server/libvncserver
cpe:/o:redhat:enterprise_linux:7::workstation/libvncserver
'''