pdf("curve1.pdf",width=7,height=7,encoding = 'default')
library('scales')
library(gplots)
#palette( rev(rich.colors(32)))
palette(rev(rich.colors(32)))
newWords <- read.table("./firstksentence.txt", header = FALSE)

x <- as.vector(t(newWords[1]))
y <- as.vector(t(newWords[2]))
z <- as.vector(t(newWords[3]))
w <- as.vector(t(newWords[4]))
#u <- as.vector(t(newWords[:,5]))

plot(NULL,NULL, main=NULL, sub=NULL,
xlab="First K-Sentences ", ylab="BLEU",
xlim=c(0, 60)
,ylim=c(0,40),xaxt = 'n',yaxt='n'
)
axis(1,at = seq(0, 60, by = 10), las=1,tck = 0.01,cex.axis = 1)
axis(2,at = seq(0, 40, by = 5), las=1,tck = 0.01,cex.axis = 1)
grid(nx = NA,ny = NULL,lty = 1)



    print (length(y))
lines(x, z, type=c('o'),col = 18,cex = 2,pch = '*')
lines(x, y, type=c('o'),col = 1,cex = 2,pch = '*')
lines(x, w, type=c('o'),col = 29,cex = 2,pch = '*')
legend("bottomright",
c("Partial Ranking BLEU", "Gold Ranking BLEU",
"Random Selection BLEU"),col = c(1, 18,29),lty= (1),pch = '*')
dev.off()
