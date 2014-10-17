
if __name__ == "__main__":
    inFile = open("./cost.txt",'r')
    outFile = open("./pricebleu1.txt",'w')
    avgsenlength = 20.1
    wordprice = 0.3
    #print >> outFile, str(0.0)+" "+str(29.56)
    avgentenceprice = avgsenlength*wordprice
    for line in inFile:
        costs = [float(item) for item in line.split()]
        price = 1.0*costs[0]/150.6*1792*4*avgentenceprice + 1.0*(1-costs[0]/150.6)*1792*0.1 
        print costs
        print (price,costs[1])
        print >> outFile, str(price)+" "+str(costs[1])
    outFile.close()
        

