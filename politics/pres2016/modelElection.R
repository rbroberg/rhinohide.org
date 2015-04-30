library(nlme)

# granular functions since I'm having trouble with the group applies
getBestFitM <- function(vals){
  thisfit=lm(as.matrix(vals[2])~as.matrix(vals[1]))
  m=as.numeric(thisfit$coef[2])
  return(m)
}
getBestFitB <- function(vals){
  thisfit=lm(as.matrix(vals[2])~as.matrix(vals[1]))
  b=as.numeric(thisfit$coef[1])
  return(b)
}

getBestFitS <- function(vals){
  thisfit=lm(as.matrix(vals[2])~as.matrix(vals[1]))
  s=as.numeric(summary(thisfit)$sigma)
  return(s)
}

getModelVote <- function(vals){
  return(rnorm(vals[1],vals[2],vals[3]))
}

# read data
tdat = read.table("data/history.dat.clean.txt", sep="\t", header=TRUE)
evdat =  read.table("data/ev.state.fips.txt", sep="\t", header=TRUE)

# just git (D) votes, reduce redundacy
t=tdat[tdat$party=="Democratic",]

# use for "predicting" past elections
pyear=2016
t=t[t$year<pyear,]

df = t[,c(1,3,10)]
df[df$fips==1,]

# I HATE R DATA TYPING!!!!!!!

# find slope, intercept, and standard err for linear regression
b=gapply(df,FUN="getBestFitB",form=~fips, which=c("year","split"))
m=gapply(df,FUN="getBestFitM",form=~fips, which=c("year","split"))
s=gapply(df,FUN="getBestFitS",form=~fips, which=c("year","split"))
bm=cbind(b,m)

# make 2016 prediction
#x=c(1980,1988,1992,1996,2000,2004,2008,2012,2016)
#yhat=x
#i=0
#for (pyear in x) {
#  i=i+1
  preds=pyear*bm[,2]+bm[,1]
  
  # shape data for montecarlo
  nruns=1000000
  nps=cbind(rep(nruns,length(s)),preds,s) # number of runs, means and errs on each state
  
  # run monte carlo
  mc=apply(nps,FUN="getModelVote",1)
  # shape mc = nruns x 51 ev
  
  # fake vector of evs
  #evs=sample(1:20, 50, replace=T)
  evs = evdat[,3]
  
  # pick winners and losers
  mc <- (mc>0)*1
  
  towin=sum(evs)/2
  evsums=mc %*% evs
  evmax=sum(evs)
  rng = max(evsums)+1
  #print(pyear)
  #print(mean(evsums))
  #yhat[i]=mean(evsums)
#}

#lm(yhat~x)

#sum(colSums(mc)>nruns/2)
#max(rowSums(mc))
#min(rowSums(mc))

# manual exam of hist pdf
breaks = seq (as.integer(min(evsums)),as.integer(max(evsums+1)),by=1)
nmb.cuts = cut(evmax-evsums, breaks, right=FALSE)
nmb.freq = table(nmb.cuts)
nmb.freq = nmb.freq/length(nmb.cuts)
ymax=max(nmb.freq) # use this for text placement
xmax=breaks[length(breaks)]
xmin=breaks[1]
windex=as.integer(towin)-xmin

pD=100*sum(evsums>towin)/nruns
pR=100*sum(evsums<towin)/nruns

hist(evsums,breaks=breaks, main="", xlab="Democratic Electoral Votes", ylab="", freq=F, col=c(rep("red",windex),"green",rep("blue",max(xmax-windex,0))))
  abline(v=towin,lwd=2,col="black")
  datestamp = format(Sys.time(), "%B %d %Y")
  title(main=paste("Projected",pyear,"Electoral Vote Distribution\nMonte Carlo Based on State Trends 1952 -",pyear-4))
  text(xmin+120,0.95*ymax,pos=2,paste("P(R win) = ",pR,"%",sep=""))
  text(xmin+120,0.85*ymax,pos=2,paste("P(D win) = ",pD,"%",sep=""))
  text(xmax-120,0.95*ymax,pos=4,paste("number of runs = ",nruns,sep=""))
  #text(220,0.75*ymax,pos=4,paste("includes",bias,"polling bias adj"))
  mtext(paste("http://rhinohide.wordpress.com",format(Sys.time(), "%Y%m%d %H%M")), 4, side=1, adj=1, cex=0.7, col="dark gray")
  mtext("Data: US Elections Atlas", 4, side=1, adj=0, cex=0.7, col="dark gray")

mean(evsums)

