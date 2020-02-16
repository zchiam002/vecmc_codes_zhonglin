##This is the compute file 

def cooling_tower4_compute (ct4_dc):
    
    import numpy as np 
    from sklearn import linear_model    
    ##ct4_dc    - list of input values
    ##ct4_dc[0,0] = cooling_tower4['ct4_ct_total_towers']['value']
    ##ct4_dc[1,0] = cooling_tower4['ct4_tempin']['value']
    ##ct4_dc[2,0] = cooling_tower4['ct4_totalcflow']['value']
    ##ct4_dc[3,0] = cooling_tower4['ct4_t_wetbulb']['value']
    ##ct4_dc[4,0] = cooling_tower4['ct4_c0']['value']
    ##ct4_dc[5,0] = cooling_tower4['ct4_c1']['value']
    ##ct4_dc[6,0] = cooling_tower4['ct4_c2']['value']
    ##ct4_dc[7,0] = cooling_tower4['ct4_c3']['value']
    ##ct4_dc[8,0] = cooling_tower4['ct4_c4']['value']
    ##ct4_dc[9,0] = cooling_tower4['ct4_c5']['value']  
    ##ct4_dc[10,0] = cooling_tower4['ct4_lin_fan_coeff']['value']
    ##ct4_dc[11,0] =  cooling_tower4['ct4_max_fan_power']['value']
    ##ct4_dc[12,0] = cooling_tower4['ct4_drift_perc']['value']
    ##ct4_dc[13,0] = cooling_tower4['ct4_evap_perc']['value']
    ##ct4_dc[14,0] = cooling_tower4['ct4_water_adj_coeff']['value']
    
    ct4_ind_flow = ct4_dc[2,0] / ct4_dc[0,0]                                    ##To calculate the flowrate to each individual cooling tower (m3/h)
    
    ##Establishing the relationship between delta-T of the cooling tower and the electricity consumption 
    
    iterations = 20
    
    T_wi = ct4_dc[1,0]
    T_wb = ct4_dc[3,0]
    m_w = ct4_ind_flow * 998.2
    lin_fan_coeff = ct4_dc[10,0]
    delta_t = 0
    delta_t_step_size = 0.5
    rec_delt = np.zeros((iterations,1))
    rec_elec = np.zeros((iterations,1))
    
    for i in range (0,iterations):
        T_wo = T_wi - delta_t
        X2 = ct4_dc[7,0]
        X = ct4_dc[5,0] + (ct4_dc[9,0]*(T_wi - T_wb))
        C = ct4_dc[4,0] + (ct4_dc[6,0]*(T_wi - T_wb)) + (ct4_dc[8,0]*(pow((T_wi - T_wb),2))) - ((T_wi - T_wo)/(T_wi - T_wb))
        
        discriminant = pow(X,2) - (4*X2*C)
        discriminant = pow(discriminant,0.5)
        ma_mw_ratio = (-X + discriminant) / (2*X2)
        ma = ma_mw_ratio * m_w
        rec_delt[i,0] = delta_t
        rec_elec[i,0] = lin_fan_coeff * ma

        delta_t = delta_t + delta_t_step_size
        
    clf = linear_model.LinearRegression()
    clf.fit(rec_elec,rec_delt)
    
    lin_coeff = clf.coef_
    intercept = clf.intercept_                                                                          ##This is the minimum delta t
    
    no_flow_delta_t = intercept                                                                         ##The delta_t when the fan is not turn on 
    max_delta_t = ct4_dc[11,0]*lin_coeff + intercept                                                    ##This is the maximum delta t based on max fan power
    max_delta_t_based_on_twb = T_wi - T_wb                                                              ##This is the maximum delta t based on Twb limit
    
    max_power_at_max_delta_t_based_on_twb = (max_delta_t_based_on_twb * lin_coeff) + intercept          ##This is the maximum power consumed at maximum delta t based on Twb limit
    
    if max_power_at_max_delta_t_based_on_twb < ct4_dc[11,0]:
        fmax = max_power_at_max_delta_t_based_on_twb / ct4_dc[11,0]
    else:
        fmax = 1

    ##Dealing with water related issues 
    min_water_cons = ct4_dc[12,0] * ct4_ind_flow * ct4_dc[14,0]                                                     ##This should function as the interceptat 0 utilization level 
    water_cons_grad_coeff = ct4_dc[13,0] * ct4_ind_flow * ct4_dc[14,0] * min(max_delta_t, max_delta_t_based_on_twb) ##This is the multiplicative factor to the delta t

    ##Initialize a new matrix to hold the return values 

    ct4_dc_calc =np.zeros((6,1))
    
    ct4_dc_calc[0,0] = no_flow_delta_t 
    ct4_dc_calc[1,0] = min(max_delta_t, max_delta_t_based_on_twb)
    ct4_dc_calc[2,0] = min(ct4_dc[11,0], max_power_at_max_delta_t_based_on_twb)
    ct4_dc_calc[3,0] = fmax
    ct4_dc_calc[4,0] = min_water_cons
    ct4_dc_calc[5,0] = water_cons_grad_coeff
    

    return ct4_dc_calc 

