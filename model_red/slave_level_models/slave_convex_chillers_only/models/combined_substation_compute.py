#This is the compute file 

def combined_substation_compute (cb_ss_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##cb_ss_dc[0,0] = cbss_demand
    ##cb_ss_dc[1,0] = cbss_totalflownwk
    ##cb_ss_dc[2,0] = cb_ss_cp
    ##cb_ss_dc[3,0] = cb_ss_tinmax
    ##cb_ss_dc[4,0] = cb_ss_deltmax
    
    ##Calculating the constant value for the exting stream
    if cb_ss_dc[1,0] == 0:
        exit_cst_value = 0
    else:
        flow = cb_ss_dc[1,0] * 998.2 / 3600
        exit_cst_value = cb_ss_dc[0,0] / (flow * cb_ss_dc[2,0])
    
    ##Calculating the constraint equation coefficient 
    if cb_ss_dc[0,0] == 0:
        constraint_eqn_coeff = 0
    else:
        constraint_eqn_coeff = (cb_ss_dc[1,0] * cb_ss_dc[2,0]) /  cb_ss_dc[0,0] 
    
    
    ##Initiate a matrix to hold the return values 
    cb_ss_calc = np.zeros((2,1))
    
    cb_ss_calc[0,0] = exit_cst_value
    cb_ss_calc[1,0] = constraint_eqn_coeff

    return cb_ss_calc  

    

