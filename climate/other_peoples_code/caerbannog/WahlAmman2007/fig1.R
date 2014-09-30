`fig1` <-
function(){

par( mfrow=c(3,1), oma=c(6,0,0,0))
par( mar=c(0,5,2,2))

PCs.3<- princomp(tree)$scores[,1:5]

PCs.2<- princomp( tree, cor=TRUE)$scores[,1:5]

plot( tt,  scale(PCs[,1]), type="l", lty=1, xaxt="n", ylab="Scaled PC1")
abline(h=0,col="blue")
title("MBH centering and scaling in instrumental period",adj=0)

plot( tt,  -1*scale(PCs.3[,1]), type="l", lty=1,xaxt="n", ylab="Scaled PC1" )
abline(h=0,col="blue")
title("First PC using covariance",adj=0)


plot( tt,  scale(PCs.2[,1]), 

type="l", lty=1, xaxt="n", ylab="Scaled PC1")
abline( h=0, col="blue")
title("First PC using correlations",adj=0)


par( oma=c(0,0,0,0), mar=c(5,5,2,2))
axis( 1)
mtext( side=1, line=3, text="Years")

}

