fn="data/gini-regulation-ranking.txt"
gini <- read.table(fn,header=T,sep="\t")
gini <- gini[,1:5]

# not much cor in pisa or church
fn2="../pisa/data/pisa-math-2012_statechurch.txt"
pisa <- read.table(fn2,header=T,sep="\t")

# not much cor in pisa or church
fn3="data/gini-population.txt"
pop <- read.table(fn3,header=T,sep="\t")

# adj r=.54
fit <- lm(gini[,2] ~ gini[,3] + gini[,4] + pop[,5] + pisa[,2])
summary(fit) 
cor(cbind(gini[,2:4],pop[,5],pisa[2]))

# adj r=.52
fit <- lm(gini[,2] ~ gini[,3] + gini[,4] + pop[,5])
summary(fit) 
cor(cbind(gini[,2:4],pop[,5]))

# adj r=.51
fit <- lm(gini[,2] ~ pop[,5]+gini[,3])
summary(fit) 
cor(cbind(gini[,2:4],pop[,5]))

fn="data/gini-real-multivar.txt"
gini <- read.table(fn,header=T,sep="\t")
cor(cbind(gini[,2],gini[,3],log(gini[,4]),log(gini[,5]),log(gini[,6]),gini[,7]))
fit <- lm(gini[,2] ~ gini[,3]+log(gini[,4])+log(gini[,5])+log(gini[,6]))
summary(fit) 

fit <- lm(gini[,2] ~ log(gini[,4])+log(gini[,5])+gini[,7])
summary(fit) 

# switch
fit <- lm(log(gini[,4]) ~ log(gini[,6])+gini[,2]+gini[,7])
summary(fit)

