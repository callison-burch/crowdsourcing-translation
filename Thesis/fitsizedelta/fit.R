Yfunc <- function(x ){
    #  return(2.00466200e-02*x^2 -3.63394872e+00 *x + 1.66407552e+02)
    return(0.02*x^2 -3.63 *x + 166.41)
}

pdf("fit.pdf",width=7,height=7,encoding = 'default')
library('scales')
library(gplots)
#palette( rev(rich.colors(32)))
palette(rev(rich.colors(32)))

#curve(Yfunc, -2*pi, 2*pi, xname = "t")
x <- vector(mode="numeric", length=11)
y <- vector(mode="numeric", length=11)
print (1:5)
x <- c(90,91,92,93,94,95,96,97,98,99,100)
y <- c(1.67,1.75,1.77,1.87,2.00,2.12,2.31,2.43,2.79,3.05,3.58)

plot(NULL,NULL, main=NULL, sub=NULL,
xlab="Delta(%)", ylab="Averaged Size of Translation Set",
xlim=c(90, 100)
,ylim=c(0,4),xaxt = 'n',yaxt='n'
)
axis(1,at = seq(90, 100, by = 1), las=1,tck = 0.01,cex.axis = 1)
axis(2,at = seq(0, 4, by = 1), las=1,tck = 0.01,cex.axis = 1)
for (i in 1:11){
   points(x[i],y[i],pch = 1,cex= 2, col = "red")
}
plot(Yfunc,y = 0, to = 101,add = TRUE,col = "blue",lwd = 2)


dev.off()
