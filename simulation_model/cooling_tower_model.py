##This is the cooling tower model 

def ct_uem_original (twb, m_ct, m_air, t_in):    
    
    ##twb --- the wetbulb temperature 
    ##m_ct --- flowrate through the cooling tower
    ##m_air --- air-flow through the cooling tower 
    ##t_in --- temperature of fluid entering the cooling tower 
    
    ##Max_airflow 
    max_air_flow = 369117
    
    ##Computing delt max 
    approach = 5                            ##Approach temperature of the cooling tower
    absolute_delt_max = 5
    
    ##In the case all the chillers are turn off
    if t_in == 'Undefined':
        delT_ct = 0
        e_cons = 0        
    else:
        relative_delt_max = t_in - twb - approach
        
        if relative_delt_max > absolute_delt_max:
            delt_max = absolute_delt_max
        else:
            delt_max = relative_delt_max        
    
        ##Cooling tower regression derived coefficients 
        
        b0 = 0.14029549639345207	
        b1 = 0.600266127023157	
        b2 = -0.0211475692653011	
        b3 = 0.2792094538127389	
        b4 = 9.294683422723725*pow(10, -4)
        b5 = 0.16052557022400754
        
        ##Calculating the delta-T of the cooling tower     
        delT_ct = delT_calc ([b0, b1, b2, b3, b4, b5], m_air, t_in, [m_ct, twb])
        if delT_ct > delt_max :
            delT_ct = delt_max
        elif delT_ct < 0:
            delT_ct = 0
        
        ##Calculating electricity 
        e_cons = (m_air / max_air_flow) * 22
    
    
    return delT_ct, e_cons
####################################################################################################################################################################################################
##Helper functions

##A function to calculate the delta t of a tower unit using the universal engineering model 
def delT_calc (ct_reg_coeff, ma, Twi, constants):
    ##Constants
    mw = constants[0]                      ##mw (m3/h)
    Twb = constants[1]                     ##Twb (K)
    
    ##Converting mw to kg/h
    mw = mw * 998.2    

    ##Calculated coefficients 
    b0 = ct_reg_coeff[0]	
    b1 = ct_reg_coeff[1]	
    b2 = ct_reg_coeff[2]	
    b3 = ct_reg_coeff[3]		
    b4 = ct_reg_coeff[4]	
    b5 = ct_reg_coeff[5]	 
    
    term1 = b0 * (Twi - Twb)
    if mw == 0:
        term2 = 0
        term4 = 0
        term6 = 0
    else:
        term2 = b1 * (ma / mw) * (Twi - Twb)
        term4 = b3 * pow((ma / mw), 2) * (Twi - Twb)
        term6 = b5 * (ma / mw) * pow((Twi - Twb), 2)
        
    term3 = b2 * pow((Twi - Twb), 2)
    term5 = b4 * pow((Twi - Twb), 3)
    
    delT_overall = term1 + term2 + term3 + term4 + term5 + term6

    return delT_overall

