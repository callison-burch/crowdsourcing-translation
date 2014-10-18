
if __name__ == "__main__":
    inFile = open("./cost.txt",'r')
    outFile = open("./pricebleu1.txt",'w')
    avgsenlength = 20.1
    wordprice = 0.3
    #print >> outFile, str(0.0)+" "+str(29.56)
    l = [30.26,33.72,33.91,34.34,37.63,37.56,37.57,34.22,37.57,37.57,37.10,37.76,37.94,37.52,37.13]
    avgentenceprice = avgsenlength*wordprice
    count = 0
    for line in inFile:
        costs = [float(item) for item in line.split()]
        price = 1.0*costs[0]/150.6*1792*4*avgentenceprice + 1.0*(1-costs[0]/150.6)*1792*0.1 
        print costs
        print (price,costs[1],l[count])
        print >> outFile, str(price)+" "+str(costs[1])+" "+str(l[count])
        count += 1
    outFile.close()
        

