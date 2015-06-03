library(ggplot2)

dat <- read.table(
  header=TRUE, text='x y
1947    21771
1948    21177
1949    20898
1950    22055
1951    22827
1952    23520
1953    25424
1954    24813
1955    26364
1956    28158
1957    28285
1958    28158
1959    29804
1960    30374
1961    30695
1962    31570
1963    32683
1964    33905
1965    35377
1966    37200
1967    38020
1968    39777
1969    41654
1970    41568
1971    41487
1972    43499
1973    44381
1974    43232
1975    42453
1976    43776
1977    44041
1978    46527
1979    47225
1980    45647
1981    44437
1982    43913
1983    44225
1984    45734
1985    46439
1986    48439
1987    49248
1988    49391
1989    50332
1990    49545
1991    48608
1992    48255
1993    47578
1994    48895
1995    49987
1996    50705
1997    52307
1998    54091
1999    55350
2000    55647
2001    54857
2002    54285
2003    54096
2004    54061')


# find length of data
l=nrow(dat)

# for range from 20-80% of the range
# calculate two linear trends
# add the squares of the residuals from both trends
# and find the point which minimizes

ressum=c()
for (i in  floor(l*.2):ceiling(l*.8)) {
	lm1=lm(dat$y[1:i]~dat$x[1:i])
	lm2=lm(dat$y[i:l]~dat$x[i:l])
	ressum=c(ressum,sum(lm1$residuals^2) + sum(lm2$residuals^2))
}

bkpt = which.min(ressum) + floor(l*.2) - 1
dat$year[bkpt]

lm1=lm(dat$y[1:bkpt]~dat$x[1:bkpt])
lm2=lm(dat$y[bkpt:l]~dat$x[bkpt:l])

lm1ext=dat$x*lm1$coef[2]+lm1$coef[1]
lm2ext=dat$x*lm2$coef[2]+lm2$coef[1]

plot(dat,ylab="income",xlab="")
title(main="Real Household Median Income 1947-2004")
abline(lm1,col="red")
abline(lm2,col="blue")
lines(lm1$fitted~dat$x[1:bkpt],col="red",lwd=3)
lines((lm1ext+2*sd(lm1$residuals))~dat$x,col="red",lwd=1)
lines((lm1ext-2*sd(lm1$residuals))~dat$x,col="red",lwd=1)
lines(lm2$fitted~dat$x[bkpt:l],col="blue",lwd=3)
lines((lm2ext+2*sd(lm2$residuals))~dat$x,col="blue",lwd=1)
lines((lm2ext-2*sd(lm2$residuals))~dat$x,col="blue",lwd=1)
points(dat)

#'''
#fast=cbind(dat[1:bkpt,],"fast")
#colnames(fast)=c("year","income","type")
#slow=cbind(dat[bkpt:l,],"slow")
#colnames(slow)=c("year","income","type")
#
#library("ggplot2")
#theme_set(theme_grey(base_size = 16))  # increase default font etc. size
#p <- ggplot(data = rbind(fast, slow), aes(year, income, colour=type, linetype=type)) +
#  geom_point()                         # "base" plot, with points only
#p + geom_smooth(method = "lm")         # fit & plot lm model + envelope
#
#'''
