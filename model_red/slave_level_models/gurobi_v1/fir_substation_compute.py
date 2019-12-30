#This is the compute file 

def fir_substation_compute (ch1_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##fir_ss_dc = np.zeros((3,1))
    ##fir_ss_dc[0,0] = fir_substation['fir_ss_demand']['value']
    ##fir_ss_dc[1,0] = fir_substation['fir_ss_totalflownwk']['value']
    ##fir_ss_dc[2,0] = fir_substation['fir_ss_cp']['value']
    
    ##Calculating the constant value for the exting stream 
    exit_cst_value = fir_ss_dc[0,0] / (fir_ss_dc[1,0] * fir_ss_dc[2,0])
    
    ##Initiate a matrix to hold the return values 
    fir_ss_calc = np.zeros((1,1))
    
    fir_ss_calc[0,0] = exit_cst_value

    return fir_ss_calc  