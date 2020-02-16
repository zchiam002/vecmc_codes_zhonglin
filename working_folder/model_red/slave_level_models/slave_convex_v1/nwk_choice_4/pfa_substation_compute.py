#This is the compute file 

def pfa_substation_compute (pfa_ss_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##pfa_ss_dc = np.zeros((3,1))
    ##pfa_ss_dc[0,0] = pfa_substation['pfa_ss_demand']['value']
    ##pfa_ss_dc[1,0] = pfa_substation['pfa_ss_totalflownwk']['value']
    ##pfa_ss_dc[2,0] = pfa_substation['pfa_ss_cp']['value']
    ##pfa_ss_dc[3,0] = pfa_substation['pfa_ss_tinmax']['value']
    ##pfa_ss_dc[4,0] = pfa_substation['pfa_ss_deltmax']['value']
    
    ##Calculating the constant value for the exting stream 
    if pfa_ss_dc[1,0] == 0:
        exit_cst_value = 0
    else:
        exit_cst_value = pfa_ss_dc[0,0] / (pfa_ss_dc[1,0] * pfa_ss_dc[2,0])
    
    ##Calculating the constraint equation coefficient 
    if pfa_ss_dc[0,0] == 0:
        constraint_eqn_coeff = 0
    else:
        constraint_eqn_coeff = (pfa_ss_dc[1,0] * pfa_ss_dc[2,0]) /  pfa_ss_dc[0,0]    
        
    ##Initiate a matrix to hold the return values 
    pfa_ss_calc = np.zeros((2,1))
    
    pfa_ss_calc[0,0] = exit_cst_value
    pfa_ss_calc[1,0] = constraint_eqn_coeff    

    return pfa_ss_calc  
