#This is the compute file 

def hsb_substation_compute (ch1_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##hsb_ss_dc = np.zeros((3,1))
    ##hsb_ss_dc[0,0] = hsb_substation['hsb_ss_demand']['value']
    ##hsb_ss_dc[1,0] = hsb_substation['hsb_ss_totalflownwk']['value']
    ##hsb_ss_dc[2,0] = hsb_substation['hsb_ss_cp']['value']
    
    ##Calculating the constant value for the exting stream 
    exit_cst_value = hsb_ss_dc[0,0] / (hsb_ss_dc[1,0] * hsb_ss_dc[2,0])
    
    ##Initiate a matrix to hold the return values 
    hsb_ss_calc = np.zeros((1,1))
    
    hsb_ss_calc[0,0] = exit_cst_value

    return hsb_ss_calc  

    