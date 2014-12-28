#On Windows Server 2003, Windows Vista, and newer operating systems, querying Win32_Product will trigger Windows Installer to perform a consistency check to verify the health of the application. This consistency check could cause a repair installation to occur. You can confirm this by checking the Windows Application Event log. You will see the following events each time the class is queried and for each product installed:
#Event ID: 1035 

Get-WmiObject -Class Win32_Product