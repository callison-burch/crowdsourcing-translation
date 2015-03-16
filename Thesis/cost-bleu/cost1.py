
if __name__ == "__main__":
    inFile = open("./cost.txt",'r')
    outFile = open("./pricebleu1.txt",'w')
    avgsenlength = 20.1
    wordprice = 0.3
    #print >> outFile, str(0.0)+" "+str(29.56)
    l = [34.36,29.27,33.67,34.99,33.61,38.14,34.82,37.91,37.83,37.92,37.14,37.68,37.94,37.52,37.13]
    avgentenceprice = avgsenlength*wordprice
    count = 0
    for line in inFile:
        costs = [float(item) for item in line.split()]
        price = 1.0*costs[0]/150.6*1792*avgentenceprice + 1.0*(1-costs[0]/150.6)*1792*0.1 
        print costs
        print (price,costs[1],l[count])
        print >> outFile, str(price)+" "+str(costs[1])+" "+str(l[count])
        count += 1
    outFile.close()
        

