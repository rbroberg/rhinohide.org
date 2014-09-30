`fig2` <-
function(){

par( mfrow=c(2,1), oma=c(5,0,0,0))
par( mar=c(0,5,3,2))


PCs.3<- princomp(tree)$scores[,1:5]

PCs.2<- princomp( tree, cor=TRUE)$scores[,1:5]

plot( tt,  scale(PCs[,1]), 

type="l", lty=1, xaxt="n", ylab="Scaled PC1")
abline( h=0, col="blue")
title("First five covariance PCs projected (green)
  onto MBH centered and scaled PC (black)",adj=0)

lm( scale(PCs[,1]) ~ PCs.3[,1:5] ) -> out
lines( tt, predict(out), col="green", lwd=2)
lines( tt, scale(PCs[,1]))

plot( tt,  scale(PCs[,1]), 

type="l", lty=1, xaxt="n", ylab="Scaled PC1")
abline( h=0, col="blue")
title("First five correlation PCs projected (green)
  onto MBH centered and scaled PC (black)",adj=0)

lm( scale(PCs[,1]) ~ PCs.2[,1:5] ) -> out
lines( tt, predict(out), col="green", lwd=2)
lines( tt, scale(PCs[,1]))

par( oma=c(0,0,0,0), mar=c(5,5,2,2))
axis( 1)
mtext(side=1, line=3, text="Years")

}

