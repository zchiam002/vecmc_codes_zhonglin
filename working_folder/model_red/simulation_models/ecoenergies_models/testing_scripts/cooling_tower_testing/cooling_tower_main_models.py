##This script contains the main models of the cooling tower 

def ct_uem_original (twb, m_ct, m_air, t_in, delt_max):
    
    import pandas as pd     
    
    ##twb --- the wetbulb temperature 
    ##m_ct --- flowrate through the cooling tower
    ##m_air --- air-flow through the cooling tower 
    ##t_in --- temperature of fluid entering the cooling tower 
    
    ##Cooling tower regression derived coefficients 
    
    b0 = 0.14029549639345207	
    b1 = 0.600266127023157	
    b2 = -0.0211475692653011	
    b3 = 0.2792094538127389	
    b4 = 9.294683422723725*pow(10, -4)
    b5 = 0.16052557022400754
#    b0 = 0.23382397 	
#    b1 = -0.03876029 	
#    b2 = -0.03298896 	
#    b3 = 0.00113387	
#    b4 = -0.00416801
#    b5 = 0.42846231
    
    ##Calculating the delta-T of the cooling tower 
    import sys 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
    from cooling_tower_models import delT_calc
    
    delT_ct = delT_calc ([b0, b1, b2, b3, b4, b5], m_air, t_in, [m_ct, twb])
    if delT_ct > delt_max :
        delT_ct = delt_max
    elif delT_ct < 0:
        delT_ct = 0
    
    return delT_ct

def cooling_tower_uem_reg_lprelax (m_air, m_ct, tw_in, twb, bilinear_pieces, del_t_coeff_temp, ma_table, twi_table):
    
    import pandas as pd 
        
    ##Searching the bilinear pieces 
    import sys 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
    from cooling_tower_models import search_bilin_table_for_values
    bilin_est = search_bilin_table_for_values (ma_table, twi_table, m_air, tw_in)
    
    del_t_temp = (del_t_coeff_temp[0,0] * m_air) + (del_t_coeff_temp[1,0] * tw_in) + (del_t_coeff_temp[2,0] * bilin_est) + del_t_coeff_temp[3,0]

    return del_t_temp

def cooling_tower_uem_reg_lprelax_pwl_twi (m_air, m_ct, tw_in, twb, bilinear_pieces, del_t_coeff_temp_dict, ma_table, twi_table, pwl, twi_min, twi_max):
    
    import pandas as pd
    
    ##Searching the bilinear pieces
    import sys 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
    from cooling_tower_models import search_bilin_table_for_values
    bilin_est = search_bilin_table_for_values (ma_table, twi_table, m_air, tw_in)
    
    ##Identifying the right set of pwl coefficients to use for tw_in
    pwl_range = twi_max - twi_min
    
    for i in range (0, pwl):
        lower_limit = (i * pwl_range) + twi_min
        upper_limit = ((i + 1) * pwl_range) + twi_min
        
        if (tw_in >= lower_limit) and (tw_in <= upper_limit):
            ma_coeff = del_t_coeff_temp_dict['ma_coeff_' + str(i)]
            twi_coeff = del_t_coeff_temp_dict['twi_coeff_' + str(i)]
            matwi_coeff = del_t_coeff_temp_dict['matwi_coeff_' + str(i)]
            cst_term = del_t_coeff_temp_dict['cst_term_' + str(i)]
            break
                   
    del_t_temp = (ma_coeff * m_air) + (twi_coeff * tw_in) + (matwi_coeff * bilin_est) + cst_term      
    
    return del_t_temp
    
    
    
    
    
    

#################################################################################################################################################################################
##Additional functions

##A function which returns the regression coefficients for a single tower
def ct_reg_coeff_calc_new (ct_reg_coeff, twb, twi_min, twi_max, ma_min, ma_max, flow_mw_unit):

    import numpy as np 
    from sklearn import linear_model 
    import sys 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
    from cooling_tower_models import delT_calc
    
    ##To employ multi-variate regression analysis to find the relationship between variables
    ma_steps = 200 
    ma_interval = (ma_max - ma_min) / ma_steps  

    twi_steps = 200
    twi_interval = (twi_max - twi_min) / twi_steps
    
    T_wetbulb = twb
    constants = [flow_mw_unit, T_wetbulb]
    
    valuesX = np.zeros((ma_steps * twi_steps, 3))
    valuesY = np.zeros((ma_steps * twi_steps, 1))
    
    row = 0
    for i in range (0,ma_steps):
        for j in range (0, twi_steps):
            valuesX[row, 0] = ma_min + (i * ma_interval)
            valuesX[row, 1] = twi_min + (j * twi_interval)
            valuesX[row, 2] = (ma_min + (i * ma_interval)) * (twi_min + (j * twi_interval))
            valuesY[row ,0] = delT_calc(ct_reg_coeff, valuesX[row, 0], valuesX[row, 1], constants)
            row = row + 1
            
    clf = linear_model.LinearRegression(fit_intercept = True)
    clf.fit(valuesX, valuesY)
    result_1 = clf.score(valuesX, valuesY, sample_weight=None)
    lin_coeff_1 = clf.coef_
    int_1 = clf.intercept_

    ##Since the idea is to express delta T as a function of Twi, ma and Twi * ma 
    ma_coeff = lin_coeff_1[0,0]
    twi_coeff = lin_coeff_1[0,1]
    matwi_coeff = lin_coeff_1[0,2]
    cst_term = int_1
    
    ##Initiating a matrix to hold the return values 
    
    ct_calc = np.zeros((5,1))
    
    ct_calc[0,0] = ma_coeff
    ct_calc[1,0] = twi_coeff
    ct_calc[2,0] = matwi_coeff
    ct_calc[3,0] = cst_term
    
    return ct_calc

##A function which returns the regression coefficients for a single tower for piecewise linearized tin 
def ct_reg_coeff_calc_new_pwl (ct_reg_coeff, twb, twi_min_O, twi_max_O, ma_min, ma_max, flow_mw_unit, pwl):

    import numpy as np 
    from sklearn import linear_model 
    import sys 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
    from cooling_tower_models import delT_calc
    
    ##To employ multi-variate regression analysis to find the relationship between variables
    ma_steps = 200 
    ma_interval = (ma_max - ma_min) / ma_steps  
    
    ##Initiating the pwl process
        ##Initiating a dictionary to store the derived coefficients 
    ret_coeff_dict = {}
    
    twi_steps = 200
    twi_pwl_range = (twi_max_O - twi_min_O) / pwl
    twi_interval =  twi_pwl_range / twi_steps 
    
    T_wetbulb = twb
    constants = [flow_mw_unit, T_wetbulb]    
    
    for ii in range (0, pwl):
        twi_min = (ii * twi_pwl_range) + twi_min_O
        valuesX = np.zeros((ma_steps * twi_steps, 3))
        valuesY = np.zeros((ma_steps * twi_steps, 1))
        
        row = 0
        for i in range (0, ma_steps):
            for j in range (0, twi_steps):
                valuesX[row, 0] = ma_min + (i * ma_interval)
                valuesX[row, 1] = twi_min + (j * twi_interval)
                valuesX[row, 2] = (ma_min + (i * ma_interval)) * (twi_min + (j * twi_interval))
                valuesY[row ,0] = delT_calc(ct_reg_coeff, valuesX[row, 0], valuesX[row, 1], constants)
                row = row + 1
                
        clf = linear_model.LinearRegression(fit_intercept = True)
        clf.fit(valuesX, valuesY)
        result_1 = clf.score(valuesX, valuesY, sample_weight=None)
        lin_coeff_1 = clf.coef_
        int_1 = clf.intercept_
    
        ##Since the idea is to express delta T as a function of Twi, ma and Twi * ma 
        ret_coeff_dict['ma_coeff_' + str(ii)] = lin_coeff_1[0,0]
        ret_coeff_dict['twi_coeff_' + str(ii)] = lin_coeff_1[0,1]
        ret_coeff_dict['matwi_coeff_' + str(ii)] = lin_coeff_1[0,2]
        ret_coeff_dict['cst_term_' + str(ii)] = int_1
        
    
    return ret_coeff_dict

