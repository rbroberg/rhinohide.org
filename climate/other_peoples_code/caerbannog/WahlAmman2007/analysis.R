# read in data

T<-scan("2004GL021750-NOAMER.1400.txt",skip=1)
T<-matrix(T,nrow=581,ncol=72,byrow=TRUE)
tree<-T[1:581,3:72]

tt<- c(1400:1980)


# MBH- uncentered PCs  GRL Data, Caspar Ammann's code
# =======
m.tree<-apply(tree[503:581,],2,mean)
s.tree<-apply(tree[503:581,],2,sd)
xstd<-scale(tree,center=m.tree,scale=s.tree)
fm<-lm(xstd[503:581,]~c(1:nrow(xstd[503:581,]))) #fit linear model to calibrati$
sdprox<-sd(fm$residuals)                         #get residuals

## RWM errors out: mxstd<-scale(xstd,center=FALSE,scale=sdprox)     #standardize by residual stddev
mxstd=xstd/sdprox

w<-svd(mxstd)                                    #SVD
PCs<-w$u[,1:5]                                   #Retain only first 5 PCs for c$
m.pc<-apply(PCs[503:581,],2,mean)
s.pc<-apply(PCs[503:581,],2,sd)
PCs<-scale(PCs,center=m.pc,scale=s.pc)


source("fig1.R") # only need to source these fucntion once if they
source("fig2.R") # are saved in your work space. 

pdf("fig1.pdf", width=9, height=8)
fig1()
dev.off()

pdf("fig2.pdf", width=9, height=6)
fig2()
dev.off()

