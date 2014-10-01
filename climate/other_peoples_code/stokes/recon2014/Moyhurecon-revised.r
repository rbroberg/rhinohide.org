
# Code written by Nick Stokes, 26 Sept 2014, adapted from NAS report, diagrams for post at
# http://www.moyhu.blogspot.com.au/2014/09/theres-more-to-life-than-pc1.html

# 20141001rb: multiple revisions for model exploration

# This part from NAS
n <- 600;
#baseline <- n - 0:99;	# NAS original
baseline <- 250:349;
#baseline <- 1:600
phi <- 0.9;

npc=4		# number of pcs to retain
nrecon=300	# number of recons to run

HSIndex <- function(x) # hacked to provide rescaling for recons.
{
	(mean(x[baseline]) - mean(x)) / sqrt(var(x)); # orig NAS

	# stoke scaling
	#v = (mean(x[baseline]) - mean(x))# / sqrt(var(x));
	#sign(v)/sqrt(var(x))

	# mean(x) # upside down hockey sticks
	# mean(x[baseline]) # near zero no hockey sticks
	# (mean(x[baseline]) - mean(x)) # upside up hockey sticks
	# mean(x) / sqrt(var(x)) # upside down hockey sticks
}

CreateSimProxies <- function(p=50)
{
	a <- matrix(NA, n, p); 
	for (j in 1:p) {
		b <- arima.sim(model = list(ar = phi), n);
		a[ , j] <- b - mean(b[baseline]); # centers model on recent
	}
	return(a)
}

SimulatePC <- function(proxies)  # Does recon as well
{
	w=recon(proxies)
	invisible(w);
	#invisible(svd(proxies)$u[,1:npc])
}

SimulatePC1NAS <- function(p = 50)
{
	a <- matrix(NA, n, p);
	for (j in 1:p) {
		b <- arima.sim(model = list(ar = phi), n);
		a[ , j] <- b - mean(b[baseline]);
	}
	invisible(svd(a)$u[,1]);
}

recon=function(a){  #L=svu$u$vec
	str(a)
	L=cbind(svd(a)$u[,1:npc])  # Here's where you set number of PCs
	m=(t(L)%*%a)
	s=rowMeans(L%*%m);  # The recon
	s
}

M=NULL

a <- matrix(NA, n, nrecon);

for (j in 1:ncol(a)) {
	proxies=CreateSimProxies();
	a[ , j] <- SimulatePC(proxies);
}

b <- apply(a, 2, HSIndex);  # rescales
c <- t(t(a)*b);
cav=rowMeans(c) # take average of all runs

#}###
#graphics.off()
#png("recon3.png",width=700)  # Change name as needed

matplot(c, type = "l", xlim=c(0,600),ylim=range(c), xlab = "years", ylab = "", lty = 2,main=paste(nrecon," recon with ",npc," PC, rescaled. AR1(",phi,")",sep=''));
#matplot(c, type = "l", xlim=c(0,600),ylim=c(-0.1,0.1), xlab = "years", ylab = "", lty = 2,main=paste("Recon with ",npc," PC, rescaled. AR1(",phi,")",sep=''));
lines(cav,type='l',col="black",lwd=3) # 
abline(h=mean(c),col="white",lwd=1.5)
if (nrecon<10) {legend("topleft",paste(nrecon,"recon",1:nrecon),text.col=1:nrecon)}


# make AR1 model eivecs
PopulationCov <- function(n)  # NAS routine
{
	a <- matrix(NA, n, n);
	a[] <- phi^abs(row(a) - col(a));
	for (i in 1:n)
		a[i, ] <- a[i, ] - mean(a[i, baseline]);
	for (j in 1:n)
		a[ , j] <- a[ , j] - mean(a[baseline, j]);
	invisible(a);
}
e <- eigen(PopulationCov(n));
for(i in 1:npc)
	lines(e$vectors[,i], col = i, lwd = 2);

	
#lines(e$vectors[,2], col = 2, lwd = 2);
#lines(c(0,600),c(0,0))
#if (nrecon<10) {legend("topleft",paste("Eivec",1:nrecon),text.col=1:nrecon)"

