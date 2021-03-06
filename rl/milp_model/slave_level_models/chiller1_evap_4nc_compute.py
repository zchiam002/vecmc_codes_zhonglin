#This is the compute file 

def chiller1_evap_4nc_compute (ch1_4nc_dc):
     
    import pandas as pd
    
    ##ch1_4nc_dc    - list of input values
    ##ch1_4nc_dc[0,0] = ch1_4nc_evaptret
    ##ch1_4nc_dc[1,0] = ch1_4nc_condtin
    ##ch1_4nc_dc[2,0] = ch1_4nc_rated_cap
    ##ch1_4nc_dc[3,0] = ch1_4nc_b0    
    ##ch1_4nc_dc[4,0] = ch1_4nc_b1
    ##ch1_4nc_dc[5,0] = ch1_4nc_b2
    ##ch1_4nc_dc[6,0] = ch1_4nc_qc_coeff
    ##ch1_4nc_dc[7,0] = ch1_4nc_totalenwkflow
    ##ch1_4nc_dc[8,0] = ch1_4nc_steps
    
    ##Initialize a return value for the 
    ret_vals = pd.DataFrame(columns = ['lb', 'ub', 'grad', 'int'])
    
    for i in range (0, int(ch1_4nc_dc[8,0])):
        
        ##Determining the upper and lower bounds of the capacity 
        if i == 0:
            qe_lb = 0.0001
            qe_ub = (1 / ch1_4nc_dc[8,0]) * ch1_4nc_dc[2,0]
        else:
            qe_lb = i * (1 / ch1_4nc_dc[8,0]) * ch1_4nc_dc[2,0]
            qe_ub = (i + 1) * (1 / ch1_4nc_dc[8,0]) * ch1_4nc_dc[2,0]
            
        lb_frac = i * (1/ch1_4nc_dc[8,0])
        ub_frac = (i + 1) * (1 / ch1_4nc_dc[8,0])
            
        cop1, qc1 = gnu_chiller1_4nc (ch1_4nc_dc[3,0], ch1_4nc_dc[4,0], ch1_4nc_dc[5,0], ch1_4nc_dc[6,0], ch1_4nc_dc[0,0], ch1_4nc_dc[1,0], qe_lb)
        cop2, qc2 = gnu_chiller1_4nc (ch1_4nc_dc[3,0], ch1_4nc_dc[4,0], ch1_4nc_dc[5,0], ch1_4nc_dc[6,0], ch1_4nc_dc[0,0], ch1_4nc_dc[1,0], qe_ub)
        
        ##Determining the gradient and the intercepts for the E vs Qe graph 
        elect_cons_lb = qe_lb / cop1
        elect_cons_ub = qe_ub / cop2
        
        grad = (elect_cons_ub - elect_cons_lb) / (qe_ub - qe_lb)
        intercept = elect_cons_ub - (qe_ub * grad)
        
        temp = [lb_frac, ub_frac, grad, intercept]
        temp_df = pd.DataFrame(data = [temp], columns = ['lb', 'ub', 'grad', 'int'])
        ret_vals = ret_vals.append(temp_df, ignore_index = True)
        
    return ret_vals   

##Function to calculate the COP of the chiller using GNU method 
def gnu_chiller1_4nc (b0, b1, b2, qc_coeff, Tin_evap, Tin_cond, Qe):

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

    
