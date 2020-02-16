##This is the compute file 

##Note: Some of the implementations may be more accurate than others due to the dynamic step size 

def hsb_substation_4nc_compute (hsb_ss_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##hsb_ss_dc = np.zeros((5,1))          
    
    ##hsb_ss_dc[0,0] = hsb_ss_demand
    ##hsb_ss_dc[1,0] = hsb_ss_totalflownwk
    ##hsb_ss_dc[2,0] = hsb_ss_cp
    ##hsb_ss_dc[3,0] = hsb_ss_tinmax
    ##hsb_ss_dc[4,0] = hsb_ss_deltmax
    
    ##Calculating the constant value for the exting stream
    if hsb_ss_dc[1,0] == 0:
        exit_cst_value = 0
    else:
        flow = hsb_ss_dc[1,0] * 998.2 / 3600
        exit_cst_value = hsb_ss_dc[0,0] / (flow * hsb_ss_dc[2,0])
    
    ##Calculating the constraint equation coefficient 
    if hsb_ss_dc[0,0] == 0:
        constraint_eqn_coeff = 0
    else:
        constraint_eqn_coeff = (flow * hsb_ss_dc[2,0]) /  hsb_ss_dc[0,0] 
    
    
    ##Initiate a matrix to hold the return values 
    hsb_ss_calc = np.zeros((2,1))
    
    hsb_ss_calc[0,0] = exit_cst_value
    hsb_ss_calc[1,0] = constraint_eqn_coeff

    return hsb_ss_calc  