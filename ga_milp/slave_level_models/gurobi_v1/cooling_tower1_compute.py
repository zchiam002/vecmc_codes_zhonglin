##This is the compute file 

def cooling_tower1_compute (ct1_dc):
    
    import numpy as np 
    from sklearn import linear_model 
    
    ##ct1_dc    - list of input values    
    ##ct1_dc[0,0] = cooling_tower1['ct1_totalmassflowrate']['value']
    ##ct1_dc[1,0] = cooling_tower1['ct1_massflowrateratio']['value']
    ##ct1_dc[2,0] = cooling_tower1['ct1_wetblubtemp']['value']
    ##ct1_dc[3,0] = cooling_tower1['ct1_b0']['value']
    ##ct1_dc[4,0] = cooling_tower1['ct1_b1']['value']
    ##ct1_dc[5,0] = cooling_tower1['ct1_b2']['value']
    ##ct1_dc[6,0] = cooling_tower1['ct1_b3']['value']
    ##ct1_dc[7,0] = cooling_tower1['ct1_b4']['value']
    ##ct1_dc[8,0] = cooling_tower1['ct1_b5']['value']
    ##ct1_dc[9,0] = cooling_tower1['ct1_ma_min']['value']
    ##ct1_dc[10,0] = cooling_tower1['ct1_ma_max']['value']
    ##ct1_dc[11,0] = cooling_tower1['ct1_twi_max']['value']
    ##ct1_dc[12,0] = cooling_tower1['ct1_efanmax']['value']
    
    ##Defining a function to return the delta t or range of the cooling tower as a function of Twi and ma 
    
    def delT_calc (ma, Twi, constants):
        ##Constants
        mw = constants[0]                      ##mw (m3/h)
        Twb = constants[1]                     ##Twb (K)
        
        ##Converting mw to kg/h
        mw = mw * 998.2    
    
        ##Calculated coefficients 
        b0 = 0.14029549639345207	
        b1 = 0.600266127023157	
        b2 = -0.0211475692653011	
        b3 = 0.2792094538127389	
        b4 = 9.294683422723725E-4
        b5 = 0.16052557022400754 
        
        term1 = b0 * (Twi - Twb)
        term2 = b1 * (ma / mw) * (Twi - Twb)
        term3 = b2 * pow((Twi - Twb), 2)
        term4 = b3 * pow((ma / mw), 2) * (Twi - Twb)
        term5 = b4 * pow((Twi - Twb), 3)
        term6 = b5 * (ma / mw) * pow((Twi - Twb), 2)
        
        delT_overall = term1 + term2 + term3 + term4 + term5 + term6

    return delT_overall
    
    ##To employ multi-variate regression analysis to find the relationship between variables
    
    ma_min = ct1_dc[9,0]
    ma_max = ct1_dc[10,0]
    ma_steps = 20 
    ma_interval = (ma_max - ma_min) / ma_steps  
    
    twi_min = ct1_dc[2,0]
    twi_max = ct1_dc[11,0]
    twi_steps = 20 
    twi_interval = (twi_max - twi_min) / twi_steps

    mf_water = ct1_dc[0,0] * ct1_dc[1,0]
    T_wetbulb = ct1_dc[2,0]
    constants = [mf_water, T_wetbulb]
    
    valuesX = np.zeros((ma_steps * twi_steps, 5))
    valuesY = np.zeros((ma_steps * twi_steps, 1))
    
    row = 0
    for i in range (0,ma_steps):
        for j in range (0, twi_steps):
            valuesX[row, 0] = 0 #pow(ma_min + (i * ma_interval), 2)
            valuesX[row, 1] = ma_min + (i * ma_interval)
            valuesX[row, 2] = 0 #pow(twi_min + (j * twi_interval) , 2)
            valuesX[row, 3] = twi_min + (j * twi_interval)
            valuesX[row, 4] = (ma_min + (i * ma_interval)) + (twi_min + (j * twi_interval))
            valuesY[row ,0] = delT_calc(valuesX[row, 1], valuesX[row, 3], constants)
    
    clf = linear_model.LinearRegression(fit_intercept = True)
    clf.fit(valuesX, valuesY)
    result_1 = clf.score(valuesX, valuesY, sample_weight=None)
    lin_coeff_1 = clf.coef_
    int_1 = clf.intercept_

    ##Since the idea is to express delta T as a function of Twi, ma and Twi * ma 
    ma_coeff = lin_coeff_1[0,1]
    twi_coeff = lin_coeff_1[0,3]
    matwi_coeff = lin_coeff_1[0,4]
    cst_term = int_1
    
    ##Determining the value for can coefficient 
    lin_fan_coeff = ct1_dc[12,0] / ct1_dc[10,0]
    
    ##Initiating a matrix to hold the return values 
    
    ct1_calc = np.zeros((5,1))
    
    ct1_calc[0,0] = ma_coeff
    ct1_calc[1,0] = twi_coeff
    ct1_calc[2,0] = matwi_coeff
    ct1_calc[3,0] = cst_term
    ct1_calc[4,0] = lin_fan_coeff 
    
    return ct1_calc