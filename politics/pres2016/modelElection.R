getPredictedFit <- function(x,y,z){
  thisfit=lm(y~x)
  b=thisfit$coef[1]
  m=thisfit$coef[2]
  p=m*z+b
  s=summary(thisfit)$sigma
  return(c(p,s))
}

#getModelVote <- function(n,vals){
#  return(rnorm(n,vals[1],vals[2]))
#}

x=c(1980,1984,1988,1992,1996,2000,2004,2008,2012)
y=c(5.4,4.2,3.6,2.2,1.1,0.8,-1.2,-2.4,-1.1)

#getModelVote(getPredictedFit(x,y,2016))


# face list of 50 preds, 50 sds
p=rnorm(50, 0, 5)
s=abs(rnorm(50, 0, 5))
ps=cbind(p,s)

# fake vector of evs
evs=sample(1:20, 50, replace=T)

# set up the monte carlo matrix
nrun=100000
mc = matrix(, nrow = nrun, ncol = 50)

for (i in 1:50){
  mc[,i]=getModelVote(1000,ps[i,])
}

mc <- (mc>0)*1

towin=sum(evs)/2
evsums=mc %*% evs
evmax=sum(evs)
rng = max(evsums)+1

# manual exam of hist pdf
breaks = seq (as.integer(min(evsums)),as.integer(max(evsums+1)),by=1)
nmb.cuts = cut(evmax-evsums, breaks, right=FALSE)
nmb.freq = table(nmb.cuts)
nmb.freq = nmb.freq/length(nmb.cuts)
ymax=max(nmb.freq) # use this for text placement
xmax=breaks[length(breaks)]
xmin=breaks[1]
windex=as.integer(towin)-xmin

pD=100*sum(evsums>towin)/nrun
pR=100*sum(evsums<towin)/nrun

hist(evsums,breaks=breaks, main="", xlab="Democratic Electoral Votes", ylab="", freq=F, col=c(rep("red",windex),"green",rep("blue",xmax-windex)))
  abline(v=towin,lwd=2,col="black")
  datestamp = format(Sys.time(), "%B %d %Y")
  title(main="Projected 2016 Electoral Vote Distribution\nMonte Carlo Based on State Trends 1980-2012")
  text(xmin+50,0.95*ymax,pos=2,paste("P(R win) = ",pR,"%",sep=""))
  text(xmin+50,0.85*ymax,pos=2,paste("P(D win) = ",pD,"%",sep=""))
  text(xmax-50,0.95*ymax,pos=4,paste("number of runs = ",nrun,sep=""))
  #text(220,0.75*ymax,pos=4,paste("includes",bias,"polling bias adj"))
  mtext(paste("http://rhinohide.wordpress.com",format(Sys.time(), "%Y%m%d %H%M")), 4, side=1, adj=1, cex=0.7, col="dark gray")
  mtext("data US States", 4, side=1, adj=0, cex=0.7, col="dark gray")



