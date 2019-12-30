#This is the compute file 

def ser_substation_compute (ch1_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##ser_ss_dc = np.zeros((3,1))
    ##ser_ss_dc[0,0] = ser_substation['ser_ss_demand']['value']
    ##ser_ss_dc[1,0] = ser_substation['ser_ss_totalflownwk']['value']
    ##ser_ss_dc[2,0] = ser_substation['ser_ss_cp']['value']
    
    ##Calculating the constant value for the exting stream 
    exit_cst_value = ser_ss_dc[0,0] / (ser_ss_dc[1,0] * ser_ss_dc[2,0])
    
    ##Initiate a matrix to hold the return values 
    ser_ss_calc = np.zeros((1,1))
    
    ser_ss_calc[0,0] = exit_cst_value

    return ser_ss_calc  