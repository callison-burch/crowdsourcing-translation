def f(x):
    return 0.02*x**2 - 3.63*x+166.41
if __name__ == "__main__":
    inFile = open("./cost2.txt",'r')
    outFile = open("./pricebleu2.txt",'w')
    avgsenlength = 20.1
    wordprice = 0.3
    #print >> outFile, str(0.0)+" "+str(29.56)
    
    avgentenceprice = avgsenlength*wordprice
    l = [i for i in range(90,101)]
    count = 0
    for line in inFile:
        costs = [float(item) for item in line.split()]
        price = 1.0*0.2*1792*avgentenceprice + 1.0*0.8*1792*(costs[1])*0.1
        predictprice = 1.0*0.2*1792*avgentenceprice + 1.0*0.8*1792*(f(l[count]))*0.1
        #price =1.0*0.8*1792*(costs[1])*0.1
        #predictprice = 1.0*0.8*1792*(f(l[count]))*0.1
        print costs
        print (price,predictprice,costs[0])
        print >> outFile, str(price)+" "+str(predictprice) +" "+str(costs[0])
        count = count + 1
    outFile.close()
        

