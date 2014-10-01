import numpy as np
from statsmodels.tsa.arima_process import arma_generate_sample
import matplotlib.pyplot as plt
from scipy.linalg import svd
numpy.linalg.lstsq

npc = 1
nproxies = 50
nyears = 200
nrecon = 5

ar = [.9, 0]
ma = [1., 0.4]

def HSIndex(x):
	return (np.mean(x[50:150])-np.mean(x)) / np.std(x)

def SimulatePC1(p=50):
	m = np.zeros((nyears,p))
	for j in range(p):
		b = arma_generate_sample(ar, ma, nyears)
		m[:,j] = b - np.mean(b[50:150])
	u,_,_ = svd(m)
	return(u[0:npc])

a = np.zeros((nyears, nrecon))
for j in range(nrecon):
	a[:,j] = SimulatePC1()

b = [HSIndex(a[:,j]) for j in range(nrecon)]

c=np.sign(b)*a

plt.plot(c)
plt.show()











# create proxy array
proxies = np.zeros((nrecon, nproxies, nyears))

# generate ar random proxies
svds=np.zeros((nrecon,nyears))
for i in range(nrecon):
	for j in range(nproxies):
		proxies[i,j,:] = arma_generate_sample(ar, ma, nyears)
	svds[i,:]=svd(proxies[i,:,:].transpose())[0][0]

# scaling factor per proxy
scaler = (np.mean(proxies[:,:,50:150],axis=(1,2))-np.mean(proxies,axis=(1,2))) / np.std(proxies,axis=(1,2))**0.5

U=[]
for i in range(nrecon):
	u,w,v = svd(proxies[i,:,:])
	U.append(u)
uarr = np.array(U) # 3,50,50

c=uarr[:,:,0]*scaler


# scaled proxies
prox = proxies
for i in range(nrecon):
	for j in range(nproxies):
		prox[i,j,:] = proxies[i,j,:]*scaler[i,j]

plt.plot(prox)
plt.show()


# dim(a) # [1] 200   5
# length(b) # [1] 5
# dim(c) # [1] 200   5
