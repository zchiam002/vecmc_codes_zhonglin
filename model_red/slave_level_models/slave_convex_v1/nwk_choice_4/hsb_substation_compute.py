#This is the compute file 

def hsb_substation_compute (hsb_ss_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##hsb_ss_dc = np.zeros((3,1))
    ##hsb_ss_dc[0,0] = hsb_substation['hsb_ss_demand']['value']
    ##hsb_ss_dc[1,0] = hsb_substation['hsb_ss_totalflownwk']['value']
    ##hsb_ss_dc[2,0] = hsb_substation['hsb_ss_cp']['value']
    ##hsb_ss_dc[3,0] = hsb_substation['hsb_ss_tinmax']['value']
    ##hsb_ss_dc[4,0] = hsb_substation['hsb_ss_deltmax']['value']
    
    ##Calculating the constant value for the exting stream 
    if hsb_ss_dc[1,0] == 0:
        exit_cst_value = 0
    else:
        exit_cst_value = hsb_ss_dc[0,0] / (hsb_ss_dc[1,0] * hsb_ss_dc[2,0])
    
    ##Calculating the constraint equation coefficient 
    if hsb_ss_dc[0,0] == 0:
        constraint_eqn_coeff = 0
    else:
        constraint_eqn_coeff = (hsb_ss_dc[1,0] * hsb_ss_dc[2,0]) /  hsb_ss_dc[0,0] 
        
    ##Initiate a matrix to hold the return values 
    hsb_ss_calc = np.zeros((2,1))
    
    hsb_ss_calc[0,0] = exit_cst_value
    hsb_ss_calc[1,0] = constraint_eqn_coeff

    return hsb_ss_calc  

    