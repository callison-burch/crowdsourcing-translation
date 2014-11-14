pdf("curve1.pdf",width=7,height=4,encoding = 'default')
library('scales')
library(gplots)
#palette( rev(rich.colors(32)))
palette(rev(rich.colors(32)))
newWords <- read.table("./firstksentence.txt", header = FALSE)

x <- as.vector(t(newWords[1]))
y <- as.vector(t(newWords[2]))
z <- as.vector(t(newWords[3]))
w <- as.vector(t(newWords[4]))
y1 <- as.vector(t(newWords[8]))
z1 <- as.vector(t(newWords[9]))
w1 <- as.vector(t(newWords[10]))
#u <- as.vector(t(newWords[:,5]))

plot(NULL,NULL, main=NULL, sub=NULL,
xlab="First K-Sentences ", ylab="BLEU",
xlim=c(0, 60)
,ylim=c(15,40),xaxt = 'n',yaxt='n'
)
axis(1,at = seq(0, 60, by = 10), las=1,tck = 0.01,cex.axis = 1)
axis(2,at = seq(15, 40, by = 5), las=1,tck = 0.01,cex.axis = 1)
grid(nx = NA,ny = NULL,lty = 1)



    print (length(y))
lines(x, z1, type=c('o'),col = 18,cex = 2,pch = '*')
lines(x, y1, type=c('o'),col = 1,cex = 2,pch = '*')
lines(x, w1, type=c('o'),col = 29,cex = 2,pch = '*')
#lines(x, z1, type=c('o'),col = 18,cex = 2,pch = 'o')
#lines(x, y1, type=c('o'),col = 1,cex = 2,pch = 'o')
#lines(x, w1, type=c('o'),col = 29,cex = 2,pch = 'o')
legend("bottomright",
c("First K Ranking", "Gold Ranking",
"Random Selection"),col = c(1, 18,29),lty= (1),pch = '*',bg = 'white')
dev.off()
