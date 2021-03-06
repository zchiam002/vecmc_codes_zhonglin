##This is the compute file 

##Note: Some of the implementations may be more accurate than others due to the dynamic step size 

def pfa_substation_4nc_compute (pfa_ss_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##pfa_ss_dc = np.zeros((5,1))          
    
    ##pfa_ss_dc[0,0] = pfa_ss_demand
    ##pfa_ss_dc[1,0] = pfa_ss_totalflownwk
    ##pfa_ss_dc[2,0] = pfa_ss_cp
    ##pfa_ss_dc[3,0] = pfa_ss_tinmax
    ##pfa_ss_dc[4,0] = pfa_ss_deltmax
    
    ##Calculating the constant value for the exting stream
    if pfa_ss_dc[1,0] == 0:
        exit_cst_value = 0
    else:
        flow = pfa_ss_dc[1,0] * 998.2 / 3600
        exit_cst_value = pfa_ss_dc[0,0] / (flow * pfa_ss_dc[2,0])
    
    ##Calculating the constraint equation coefficient 
    if pfa_ss_dc[0,0] == 0:
        constraint_eqn_coeff = 0
    else:
        constraint_eqn_coeff = (flow * pfa_ss_dc[2,0]) /  pfa_ss_dc[0,0] 
    
    
    ##Initiate a matrix to hold the return values 
    pfa_ss_calc = np.zeros((2,1))
    
    pfa_ss_calc[0,0] = exit_cst_value
    pfa_ss_calc[1,0] = constraint_eqn_coeff

    return pfa_ss_calc  