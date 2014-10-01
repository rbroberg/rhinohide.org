import numpy as np
from statsmodels.tsa.arima_process import arma_generate_sample
import matplotlib.pyplot as plt
from scipy.linalg import svd
numpy.linalg.lstsq

npc = 1
nproxies = 50
nyears = 600
nrecon = 5


ar = [1, -0.9]
ma = [1, 1]

def HSIndex(x):
	return (np.mean(x[500:600])-np.mean(x)) / np.std(x)

def SimulatePC1(p=50):
	m = np.zeros((nyears,p))
	for j in range(p):
		b = arma_generate_sample(ar, ma, nyears)
		m[:,j] = b - np.mean(b[500:600])
	u,s,v = svd(m,full_matrices=False)
	return(u[:,0])

a = np.zeros((nyears, nrecon))
for j in range(nrecon):
	a[:,j] = SimulatePC1()

b = [HSIndex(a[:,j]) for j in range(nrecon)]

c=np.sign(b)*a
cave=np.mean(c,axis=1)

plt.plot(c)
plt.plot(cave,color="black",lw=2)
plt.show()

