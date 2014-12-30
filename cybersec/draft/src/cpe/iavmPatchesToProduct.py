import re

'''
select distinct title from iavm_patches
where title like 'Windows %'
order by id desc
'''

fn="/projects/rhinohide.org/cybersec/draft/data/MSRC-CVRF/iavmxml-patches-windows.txt"
f = open(fn, 'r')
dat=f.readlines()
f.close()

#dat = dat[0:20]

for i in range(len(dat)):
	dat[i] = dat[i].replace('\n',' ').strip()

for x in range(5):
	for i in range(len(dat)):
		if dat[i].count('('):
			par=dat[i].split('(')[-1].split(')')[0]
			if par.lower()[0:2] == 'kb' :
				#dat[i]=''.join(dat[i].split('(')[0:-1]).strip()
				dat[i]=dat[i].replace('('+par+')','').strip()
			else:
				try:
					x=int(par) # KB number without KB prefix
					#dat[i]=''.join(dat[i].split('(')[0:-1]).strip()
					dat[i]=dat[i].replace('('+par+')','').strip()
				except:
					pass
	
	#parens=[]
	#for i in range(len(dat)):
	#	if dat[i].count('('):
	#		parens.append(dat[i].split('(')[-1].split(')')[0].strip())
	
	# if there is an 'and', split into two entries
	for d in dat:
		if d.find('and ') > -1:
			dat.remove(d)
			dd = d.split('and ')
			for m in dd:
				dat.append(m.strip())
	
	# if there is a ': ', split into two entries
	for d in dat:
		if d.find(': ') > -1:
			dat.remove(d)
			dd = d.split(': ')
			for m in dd:
				dat.append(m.strip())
	
	# if there is a '; ', split into two entries
	for d in dat:
		if d.find('; ') > -1:
			dat.remove(d)
			dd = d.split('; ')
			for m in dd:
				dat.append(m.strip())
	
	# if there is a ', ', split into two entries
	for d in dat:
		if d.find(', ') > -1:
			dat.remove(d)
			dd = d.split(', ')
			for m in dd:
				dat.append(m.strip())
	
	# if there is a '   ', split into two entries
	# not sure why I need to reiterate
	for d in dat:
		if d.find('   ') > -1:
			dat.remove(d)
			dd = d.split('   ')
			for m in dd:
				if len(m.strip()) > 0:
					dat.append(m.strip())
	
	# if there is a '   ', split into two entries
	for i in range(len(dat)):
		dat[i] = dat[i].replace('[1]','').replace('[2]','').replace('[3]','').replace('[4]','').replace('*','').strip()
		dat[i] = dat[i].replace('(SIPR)','').replace('(NIPR)','').strip()
		dat[i] = re.sub(r'KB[0-9]+','',dat[i]).strip()
		dat[i] = dat[i].replace('()','').strip()
		dat[i] = dat[i].replace('Windows XP Windows XP','Windows XP').strip()
		dat[i] = dat[i].replace('Windows VistaWindows Vista','Windows Vista').strip()
		dat[i] = dat[i].replace('Windows Server 2003Windows Server 2003','Windows Server 2003').strip()
		dat[i] = dat[i].replace('EditionWindows','Edition: Windows').strip()
		dat[i] = dat[i].replace('EditionWindws','Edition: Windows').strip()
		dat[i] = dat[i].replace('Edition Windows','Edition: Windows').strip()
		dat[i] = dat[i].replace('Explorer 6 Windows','Explorer 6: Windows').strip()
		dat[i] = dat[i].replace('Explorer 7 Windows','Explorer 7: Windows').strip()
		dat[i] = dat[i].replace('Explorer 8 Windows','Explorer 8: Windows').strip()
		dat[i] = dat[i].replace('Explorer 9 Windows','Explorer 9: Windows').strip()
		dat[i] = dat[i].replace('Explorer 10 Windows','Explorer 10: Windows').strip()
		dat[i] = dat[i].replace('Explorer 11 Windows','Explorer 11: Windows').strip()
		dat[i] = dat[i].replace(' when installed on ',' for ').strip()
		dat[i] = dat[i].replace('Windows 7Windows 7','Windows 7').strip()
		dat[i] = dat[i].replace('Windows 7 Windows 7','Windows 7').strip()
		dat[i] = dat[i].replace('Windows Vista Windows Vista','Windows Vista').strip()
		dat[i] = dat[i].replace('Windows Server 2008 R2Windows Server 2008 R2','Windows Server 2008 R2').strip()
		dat[i] = dat[i].replace('Windows Server 2008 Windows Server 2008','Windows Server 2008').strip()
		dat[i] = dat[i].replace('Windows Server 2008Windows Server 2008','Windows Server 2008').strip()
		dat[i] = dat[i].replace('Windows Server 2003 Windows Server 2003','Windows Server 2003').strip()
		dat[i] = dat[i].replace('Windows Server 2008 for x64-based Systems','Windows Server 2008 for x64-based Systems').strip()		 
		dat[i] = dat[i].replace('Service Pack 3Microsoft','Service Pack 3: Microsoft').strip()
		dat[i] = dat[i].replace('Service Pack 2Microsoft','Service Pack 2: Microsoft').strip()
		dat[i] = dat[i].replace('Service Pack 1Microsoft','Service Pack 1: Microsoft').strip()
		dat[i] = dat[i].replace('Service Pack 3Windows','Service Pack 3: Windows').strip()
		dat[i] = dat[i].replace('Service Pack 2Windows','Service Pack 2: Windows').strip()
		dat[i] = dat[i].replace('Service Pack 1Windows','Service Pack 1: Windows').strip()
		dat[i] = dat[i].replace('Service Pack 3Internet','Service Pack 3: Internet').strip()
		dat[i] = dat[i].replace('Service Pack 2Internet','Service Pack 2: internet').strip()
		dat[i] = dat[i].replace('Service Pack 1Internet','Service Pack 1: Internet').strip()
		dat[i] = dat[i].replace('Service Pack 3 Microsoft','Service Pack 3: Microsoft').strip()
		dat[i] = dat[i].replace('Service Pack 2 Microsoft','Service Pack 2: Microsoft').strip()
		dat[i] = dat[i].replace('Service Pack 1 Microsoft','Service Pack 1: Microsoft').strip()
		dat[i] = dat[i].replace('Service Pack 3 Windows','Service Pack 3: Windows').strip()
		dat[i] = dat[i].replace('Service Pack 2 Windows','Service Pack 2: Windows').strip()
		dat[i] = dat[i].replace('Service Pack 1 Windows','Service Pack 1: Windows').strip()
		dat[i] = dat[i].replace('Service Pack 3 Internet','Service Pack 3: Internet').strip()
		dat[i] = dat[i].replace('Service Pack 2 Internet','Service Pack 2: internet').strip()
		dat[i] = dat[i].replace('Service Pack 1 Internet','Service Pack 1: Internet').strip()
		dat[i] = dat[i].replace('internet Explorer','Internet Explorer').strip()
		dat[i] = dat[i].replace('20003','2003').strip()
		dat[i] = dat[i].replace('baed','based').strip()
		dat[i] = dat[i].replace('Sytem','Systems').strip()
		dat[i] = dat[i].replace('Syste ','Systems ').strip()
		dat[i] = dat[i].replace('Ssytems','Systems ').strip()
		dat[i] = dat[i].replace('Srvice ','Service ').strip()
		dat[i] = dat[i].replace('SystemsService','Systems Service').strip()
		dat[i] = dat[i].replace('SystemsWindows','Systems Windows').strip()
		dat[i] = dat[i].replace('Service 1','Service Pack 1').strip()
		dat[i] = dat[i].replace('Service 2','Service Pack 2').strip()
		dat[i] = dat[i].replace('Service 3','Service Pack 3').strip()
		dat[i] = dat[i].replace('+ Service',' Service').strip()
		dat[i] = dat[i].replace('SP1',' Service Pack 1').strip()
		dat[i] = dat[i].replace('SP2',' Service Pack 2').strip()
		dat[i] = dat[i].replace('SP3',' Service Pack 3').strip()
		dat[i] = dat[i].replace('Serivce','Service').strip()
		

	
	for d in dat:
		if d.find('Pack 2Microsoft') > -1:
			dat.remove(d)
			dd = d.split('Pack 2Microsoft')
			for m in dd:
				if len(m.strip()) > 0:
					dat.append(m.strip())
		if d.find('Pack 1Microsoft') > -1:
			dat.remove(d)
			dd = d.split('Pack 1Microsoft')
			for m in dd:
				if len(m.strip()) > 0:
					dat.append(m.strip())

for d in dat:
	dat[i] = dat[i].replace('  ',' ').strip()

len(dat)
dat=list(set(dat))
len(dat)
dat.sort()
dat[-100:]

fn="/projects/rhinohide.org/cybersec/draft/data/MSRC-CVRF/iavmxml-patches-windows-abbr.txt"
f = open(fn, 'w')
for d in dat:
	f.write(d+'\n')

f.close()

				
