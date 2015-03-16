from sklearn import linear_model
from numpy import *
import numpy as np

if __name__ == "__main__":
    l = range(90,101)
    trainset = np.array([l]).T
    (m,n) = trainset.shape
    print (m,n)
    X_1 = ones (shape = (m,3))
    X_1[:,1:2] = trainset
    tsqu = [x**2 for x in trainset]
    X_1 [:,2:3] = tsqu
    Y = [1.67,1.75,1.77,1.87,2.00,2.12,2.31,2.43,2.79,3.05,3.58]
    lr = linear_model.LinearRegression(fit_intercept=False, normalize=False, copy_X=True)
    lr.fit(X_1, Y)
    lr.coef_ = np.array([166.41, -3.63, 0.02])
    label=  lr.predict(X_1)
    print label
    sum = 0.0
    for (x,y) in zip(Y,label):
        sum += (x-y)**2
    print sum
    print 1.0*sum/11
    print lr.coef_
    print lr.score(X_1,Y)
    
