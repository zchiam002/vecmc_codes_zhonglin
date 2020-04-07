##This function converts the system curve into the standard quadratic form with no intercept 

def convert_to_quadratic(single_coeff, limit):
    from sklearn import linear_model 
    import numpy as np
    
    x = np.zeros((1000,2))
    y = np.zeros((1000,1))
    flow = 0
    step = limit / 1000
    
    for i in range (0,1000):
        x[i,0] = flow 
        x[i,1] = pow(flow,2)
        y[i,0] = single_coeff*pow(flow, 1.852)
        flow = flow + step
    clf = linear_model.LinearRegression(fit_intercept = False)
    clf.fit(x,y)
    
    quad_coeff = clf.coef_
    ##quad_coeff[0,0] refers to the x coefficient 
    ##quad_coeff[0,1] refers to the x^2 coefficient  
    
    return quad_coeff[0,1], quad_coeff[0,0] 