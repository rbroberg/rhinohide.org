import gzip
import os
import fnmatch
import subprocess

# =============================================================================
# !!! This script will unpack to approximately 81GB of uncompressed data    !!!
# =============================================================================
#       this should start the data decompress in the directory "../data"
#           it is intended to be run from the scripts directory
# =============================================================================
p="../data"
os.chdir(p)

# =============================================================================
# gunzip files
# =============================================================================
gzfiles = []
for root, dirnames, filenames in os.walk('.'):
	for filename in fnmatch.filter(filenames, '*.gz'):
		gzfiles.append(os.path.join(root, filename))

# these are large files, use native tools
gunzipexe = 'gunzip'
for fn in gzfiles:
	print(fn)
	try:
		dummy=subprocess.check_call([gunzipexe, fn])
	except:
		print('unpackIdevalData: could not gunzip('+fn+')')

# =============================================================================
# untar files
# =============================================================================
tarfiles = []
for root, dirnames, filenames in os.walk('.'):
	for filename in fnmatch.filter(filenames, '*.tar'):
		tarfiles.append(os.path.join(root, filename))

# these are large files, use native tools
tarexe = 'tar'
for fn in tarfiles:
	fn = fn.replace('\\','/')
	p='/'.join(fn.split('/')[0:-1])
	print(fn)
	try:
		dummy=subprocess.check_call([tarexe, '-xkf', fn, '-C', p])
	except:
		print('unpackIdevalData: could not untar('+fn+')')

# =============================================================================
# untar #2: explicit recursion might be better
# =============================================================================
tarfiles = []
for root, dirnames, filenames in os.walk('.'):
	for filename in fnmatch.filter(filenames, '*.tar'):
		tarfiles.append(os.path.join(root, filename))

# these are large files, use native tools
tarexe = 'tar'
for fn in tarfiles:
	fn = fn.replace('\\','/')
	p='/'.join(fn.split('/')[0:-1])
	print(fn)
	try:
		dummy=subprocess.check_call([tarexe, '-xkf', fn, '-C', p])
	except:
		print('unpackIdevalData: could not untar('+fn+')')

# =============================================================================
# gunzip #2: explicit recursion might be better
# =============================================================================
gzfiles = []
for root, dirnames, filenames in os.walk('.'):
	for filename in fnmatch.filter(filenames, '*.gz'):
		gzfiles.append(os.path.join(root, filename))

# these are large files, use native tools
gunzipexe = 'gunzip'
for fn in gzfiles:
	print(fn)
	try:
		dummy=subprocess.check_call([gunzipexe, fn])
	except:
		print('unpackIdevalData: could not gunzip('+fn+')')

