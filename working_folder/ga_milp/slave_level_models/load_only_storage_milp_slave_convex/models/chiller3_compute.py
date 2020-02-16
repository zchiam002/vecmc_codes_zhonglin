#This is the compute file 

def chiller3_compute (ch3_dc):
     
    import pandas as pd
    
    ##ch3_dc  - list of input values
    ##ch3_dc[0,0] = ch3_twb
    ##ch3_dc[1,0] = ch3_rated_cap
    ##ch3_dc[2,0] = ch3_b0
    ##ch3_dc[3,0] = ch3_b1
    ##ch3_dc[4,0] = ch3_b2
    ##ch3_dc[5,0] = ch3_qc_coeff
    ##ch3_dc[6,0] = ch3_steps
    ##ch3_dc[7,0] = ch3_tevap_out
    ##ch3_dc[8,0] = ch3_delt_evap
    ##ch3_dc[9,0] = ch3_delt_cond
    ##ch3_dc[10,0] = ch3_evap_nwk_coeff
    ##ch3_dc[11,0] = ch3_cp
    ##ch3_dc[12,0] = ch3_cond_nwk_coeff    
    
    ##Initialize a return value for the 
    ret_vals = pd.DataFrame(columns = ['lb', 'ub', 'grad', 'int'])
    
    for i in range (0, int(ch3_dc[6,0])):
        
        ##Determining the upper and lower bounds of the capacity 
        if i == 0:
            qe_lb = 0.0001
            qe_ub = (1 / ch3_dc[6,0]) * ch3_dc[1,0]
        else:
            qe_lb = i * (1 / ch3_dc[6,0]) * ch3_dc[1,0]
            qe_ub = (i + 1) * (1 / ch3_dc[6,0]) * ch3_dc[1,0]
            
        lb_frac = i * (1/ch3_dc[6,0])
        ub_frac = (i + 1) * (1 / ch3_dc[6,0])
        
        ##Computing the return temperature of the chiller on the evaporator side
        ret_temp_chiller = ch3_dc[7,0] + ch3_dc[8,0]
        ##Computing the inlet temperature of the chiller on the condenser side 
        tcond_in_chiller = ch3_dc[0,0] + 273.15 + 5
        
        cop1, qc1 = gnu_chiller3_4nc (ch3_dc[2,0], ch3_dc[3,0], ch3_dc[4,0], ch3_dc[5,0], ret_temp_chiller, tcond_in_chiller, qe_lb)
        cop2, qc2 = gnu_chiller3_4nc (ch3_dc[2,0], ch3_dc[3,0], ch3_dc[4,0], ch3_dc[5,0], ret_temp_chiller, tcond_in_chiller, qe_ub)
        
        ##Determining the gradient and the intercepts for the E vs Qe graph 
        elect_cons_lb = qe_lb / cop1
        elect_cons_ub = qe_ub / cop2
        
        grad = (elect_cons_ub - elect_cons_lb) / (qe_ub - qe_lb)
        intercept = elect_cons_ub - (qe_ub * grad)
        
        temp = [lb_frac, ub_frac, grad, intercept]
        temp_df = pd.DataFrame(data = [temp], columns = ['lb', 'ub', 'grad', 'int'])
        ret_vals = ret_vals.append(temp_df, ignore_index = True)
        
    ###################################################################################################################################
    ##Initialize a return dataframe for evaporator network constants    
    evap_nwk_ret_vals = pd.DataFrame(columns = ['lb', 'ub', 'grad', 'int'])

    ##Determining the maximum flowrate for the evaporator network (excluding the shared area)
    enwk_max_flow = (3600 * ch3_dc[1,0]) / (ch3_dc[11,0] * ch3_dc[8,0] * 998.2)
    
    ##Determining the step size 
    enwk_step_size = 1 / ch3_dc[6,0]
    
    for i in range (0, int(ch3_dc[6,0])):
        enwk_lb = i * enwk_step_size
        enwk_ub = (i + 1) * enwk_step_size 
        
        enwk_flow_lb = enwk_lb * enwk_max_flow
        enwk_flow_ub = enwk_ub * enwk_max_flow
        
        enwk_delp_lb = (ch3_dc[10,0] * pow(enwk_flow_lb, 1.852))
        enwk_delp_ub = (ch3_dc[10,0] * pow(enwk_flow_ub, 1.852))
        
        enwk_grad_temp = (enwk_delp_ub - enwk_delp_lb) / (enwk_flow_ub - enwk_flow_lb)
        enwk_int_temp = enwk_delp_ub - (enwk_grad_temp * enwk_flow_ub)
        
        temp_data = [enwk_grad_temp, enwk_int_temp, enwk_lb, enwk_ub]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['grad', 'int' ,'lb' ,'ub'])
        
        evap_nwk_ret_vals = evap_nwk_ret_vals.append(temp_df, ignore_index = True)    
    
    ###################################################################################################################################
    ##Initialize a return dataframe for the condenser network constants 
    cond_nwk_ret_vals = pd.DataFrame(columns = ['lb', 'ub', 'grad', 'int'])
    
    ##Determining the maximum flowrate for the evaporator network (excluding the shared area)
    cnwk_e_at_max_qe = (ch3_dc[1,0] * ret_vals['grad'][ch3_dc[6,0] - 1]) + ret_vals['int'][ch3_dc[6,0] - 1]
    cnwk_max_qc = ch3_dc[5,0] * (cnwk_e_at_max_qe + ch3_dc[1,0])
    cnwk_max_flow = (3600 * cnwk_max_qc) / (ch3_dc[11,0] * ch3_dc[9,0] * 998.2)    
    
    ##Determining the step size 
    cnwk_step_size = 1 / ch3_dc[6,0]

    for i in range (0, int(ch3_dc[6,0])):
        cnwk_lb = i * cnwk_step_size 
        cnwk_ub = (i + 1) * cnwk_step_size  
        
        cnwk_flow_lb = cnwk_lb * cnwk_max_flow
        cnwk_flow_ub = cnwk_ub * cnwk_max_flow
        
        cnwk_delp_lb = (ch3_dc[12,0] * pow(cnwk_flow_lb, 1.852)) 
        cnwk_delp_ub = (ch3_dc[12,0] * pow(cnwk_flow_ub, 1.852))
        
        cnwk_grad_temp = (cnwk_delp_ub - cnwk_delp_lb) / (cnwk_flow_ub - cnwk_flow_lb)
        cnwk_int_temp = cnwk_delp_ub - (cnwk_grad_temp * cnwk_flow_ub)
        
        temp_data = [cnwk_grad_temp, cnwk_int_temp, cnwk_lb, cnwk_ub]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['grad', 'int' ,'lb' ,'ub'])
        
        cond_nwk_ret_vals = cond_nwk_ret_vals.append(temp_df, ignore_index = True)    
        
    return ret_vals, evap_nwk_ret_vals, cond_nwk_ret_vals  

##Function to calculate the COP of the chiller using GNU method 
def gnu_chiller3_4nc (b0, b1, b2, qc_coeff, Tin_evap, Tin_cond, Qe):

    ##b0, b1, b2    --- regression derived coefficients 
    ##qc_coeff      --- not condenser heat rejection coefficient 
    ##Tin_evap      --- the chilled water return temperature to the chiller (K)
    ##Tin_cond      --- water temperature of the water entering the condenser (K)
    ##Qe            --- the cooling load which the chiller is subjected to (kWh)
  
    a_1 = (b0 * Tin_evap) / Qe
    a_2 = b1 * ((Tin_cond - Tin_evap) / (Tin_cond * Qe))
    a_3 = Tin_evap / Tin_cond
    a_4 = (b2 * Qe) / Tin_cond

    temp = (((a_1 + a_2 + 1) / (a_3 - a_4)) - 1)
    COP = pow(temp, -1)
    
    Qc = qc_coeff * ((Qe/COP) + Qe)

    return COP, Qc

    
