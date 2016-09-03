key = 'abcdefghijklmnopqrstuvwxyz'

def decrypt(n, ciphertext):
    """Decrypt the string and return the plaintext"""
    result = ''

    for l in ciphertext.lower():
        try:
            i = (key.index(l) - n) % 26
            result += key[i]
        except ValueError:
            result += l

    return result


def show_result(plaintext, n):
    """Generate a resulting cipher with elements shown"""
    encrypted = encrypt(n, plaintext)
    decrypted = decrypt(n, encrypted)

    print 'Rotation: %s' % n
    print 'Plaintext: %s' % plaintext
    print 'Encrytped: %s' % encrypted
    print 'Decrytped: %s' % decrypted


import sys

if (len(sys.argv) == 2):
	fname = sys.argv[1]
else:
	print "caesars-auto.py filename"
	quit()

thisfile=open(fname, 'r')
thisstr=thisfile.read()
#print thisstr

dictfile=open("words.txt",'r')
wordlist=dictfile.readlines()
wordlist=[w.strip('\n') for w in wordlist]

def score_text(textlist,words):
	score=0
	for w in textlist:
		if w in words:
			score=score+1
	return score

scores=[]
for rota in range(26):
	teststr=decrypt(rota, thisstr)
	scores.append(score_text(teststr.split(),wordlist))
	#print rota, score


val,idx = max([(v,i) for i,v in enumerate(scores)])
str1=decrypt(idx,thisstr)
str2=""
for i in range(len(thisstr)):
	if thisstr[i].isupper():
		str2=str2+str1[i].upper()
	else:
		str2=str2+str1[i]

print str2
print val, idx




