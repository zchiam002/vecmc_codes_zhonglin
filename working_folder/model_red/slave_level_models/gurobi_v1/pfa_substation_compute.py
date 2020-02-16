#This is the compute file 

def pfa_substation_compute (ch1_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##pfa_ss_dc = np.zeros((3,1))
    ##pfa_ss_dc[0,0] = pfa_substation['pfa_ss_demand']['value']
    ##pfa_ss_dc[1,0] = pfa_substation['pfa_ss_totalflownwk']['value']
    ##pfa_ss_dc[2,0] = pfa_substation['pfa_ss_cp']['value']
    
    ##Calculating the constant value for the exting stream 
    exit_cst_value = pfa_ss_dc[0,0] / (pfa_ss_dc[1,0] * pfa_ss_dc[2,0])
    
    ##Initiate a matrix to hold the return values 
    pfa_ss_calc = np.zeros((1,1))
    
    pfa_ss_calc[0,0] = exit_cst_value

    return pfa_ss_calc  

    