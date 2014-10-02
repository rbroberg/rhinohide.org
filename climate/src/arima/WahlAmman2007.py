import pandas as pd
import numpy as np
#from sklearn import linear_model
from scipy import stats
#import statsmodels.formula.api as sm
#import scikits.statsmodels.api as sm
import statsmodels.api as sm

datadir = "/projects/rhinohide.org/climate/other_peoples_code/caerbannog/WahlAmman2007/"
# original file is missing column header for idx column
datafile = datadir+"2004GL021750-NOAMER.1400-rb-lastcolhdr.txt"

D=pd.read_csv(datafile,sep="\t")
T=D.as_matrix()
T.shape # (581,72)

# drop tree rings
tree=D.iloc[:,2:72].as_matrix()
tree.shape # (581,70)

# get year
tt=D.iloc[:,1].as_matrix()
tt.shape # (581,)

# MBH- uncentered PCs  GRL Data, Caspar Ammann's code (rb: refactored)
# =======
m_tree = np.mean(tree[502:,:],axis=0) # these line up at least 7 places
s_tree = np.std(tree[502:,:],axis=0) # curious that these vary from R ... n -v- (n-1) ?
xstd = (tree-m_tree)/s_tree

#lm=linear_model.LinearRegression()
#lm.fit(xstd[502:,:],[i for i in range(xstd[502:,:].shape[0])])

x=np.array([[i for i in range(xstd[502:,:].shape[0])]for j in range(xstd[502:,:].shape[1])]).transpose()
sm.OLS( x[:,0], xstd[502:,:]).fit().summary()

#x=[i for i in range(xstd[502:,:].shape[0])]
# slope, intercept, r_value, p_value, std_err
#params=[stats.linregress(xstd[502:,i],x) for i in range(xstd[502:,].shape[1])]



from statsmodels.formula.api import ols
mod = ols(xstd[502:,i]~x)
res = mod.fit()
print(res.summary())

mod = ols(formula='Lottery ~ Literacy + Wealth + Region', data=df)
res = mod.fit()



m.tree<-apply(tree[503:581,],2,mean)
s.tree<-apply(tree[503:581,],2,sd)
xstd<-scale(tree,center=m.tree,scale=s.tree)
fm<-lm(xstd[503:581,]~c(1:nrow(xstd[503:581,]))) #fit linear model to calibrati$
sdprox<-sd(fm$residuals) 