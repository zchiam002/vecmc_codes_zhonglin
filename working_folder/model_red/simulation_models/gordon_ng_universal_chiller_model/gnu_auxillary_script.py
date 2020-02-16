##This script contains the auxillary functions required to create and run the model 

##This function calibrates the model based on raw data and returns the coefficients and  
def gnu_calibrate_model ():
    
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__))[:-51] + '\\'
    import pandas as pd
    import numpy as np
    from sklearn import linear_model
    
    ##Determining the input data directory 
    input_data_dir = current_path + 'simulation_models\\gordon_ng_universal_chiller_model\\input_data\\chiller_input_data.csv'
    
    ##Importing the data 
    input_data = pd.read_csv(input_data_dir)
    
    ##Determining the dimensions of the input data 
    dim_input_data = input_data.shape 
    rows = dim_input_data[0]
    
    ##Organizing the data for the use of multivariate linear regession
        ##Initializing a placeholder for the reorganized data 
    org_data_X = np.zeros((rows, 3))
    org_data_Y = np.zeros((rows, 1))
    
    ##The equation is:
        ##(tin_evap/tin_cond) * (1 + (1/COP)) - 1   =   (b0 * (tin_evap/Qe)) + (b1 * ((tin_cond - tin_evap)/(tin_cond * Qe))) + (b2 * (Qe / tin_cond) * (1 + (1/COP)))
    
    ##Hence it can be expressed in the form of 
        ## y = (b0 * x0) + (b1 * x1) + (b2 * x2)
    ##Where
        ##y     =   (tin_evap/tin_cond) * (1 + (1/COP)) - 1
        ##x0    =   tin_evap/Qe
        ##x1    =   (tin_cond - tin_evap)/(tin_cond * Qe)     
        ##x2    =   (Qe / tin_cond) * (1 + (1/COP))
        
    for i in range (0, rows):
        
        ##Extracting the key variable values 
        tin_evap = input_data['tin_evap_(K)'][i]
        tin_cond = input_data['tin_cond_(K)'][i]
        COP = input_data['load_(kW)'][i] / input_data['elect_(kW)'][i]
        Qe = input_data['load_(kW)'][i]
        
        ##Filling the numpy array 
        org_data_X[i, 0] = tin_evap/Qe
        org_data_X[i, 1] = (tin_cond - tin_evap)/(tin_cond * Qe) 
        org_data_X[i, 2] = (Qe / tin_cond) * (1 + (1/COP))
        org_data_Y[i, 0] = (tin_evap/tin_cond) * (1 + (1/COP)) - 1
        
    ##Running the regession 
    clf = linear_model.LinearRegression(fit_intercept = False)
    clf.fit(org_data_X, org_data_Y)
    result_1 = clf.score(org_data_X, org_data_Y, sample_weight=None)
    lin_coeff_1 = clf.coef_
    int_1 = clf.intercept_    
    
    r2_value = result_1
    b0 = lin_coeff_1[0,0]
    b1 = lin_coeff_1[0,1]
    b2 = lin_coeff_1[0,2]
    intercept = int_1
    
    return r2_value, b0, b1, b2, intercept