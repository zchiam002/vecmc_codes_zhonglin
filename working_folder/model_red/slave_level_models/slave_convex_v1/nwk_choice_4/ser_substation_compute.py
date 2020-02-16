#This is the compute file 

def ser_substation_compute (ser_ss_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##ser_ss_dc = np.zeros((3,1))
    ##ser_ss_dc[0,0] = ser_substation['ser_ss_demand']['value']
    ##ser_ss_dc[1,0] = ser_substation['ser_ss_totalflownwk']['value']
    ##ser_ss_dc[2,0] = ser_substation['ser_ss_cp']['value']
    ##ser_ss_dc[3,0] = ser_substation['ser_ss_tinmax']['value']
    ##ser_ss_dc[4,0] = ser_substation['ser_ss_deltmax']['value']
    
    ##Calculating the constant value for the exting stream 
    if ser_ss_dc[1,0] == 0:
        exit_cst_value = 0
    else:
        exit_cst_value = ser_ss_dc[0,0] / (ser_ss_dc[1,0] * ser_ss_dc[2,0])
        
    ##Calculating the constraint equation coefficient 
    if ser_ss_dc[0,0] == 0:
        constraint_eqn_coeff = 0
    else:
        constraint_eqn_coeff = (ser_ss_dc[1,0] * ser_ss_dc[2,0]) /  ser_ss_dc[0,0] 
    
    ##Initiate a matrix to hold the return values 
    ser_ss_calc = np.zeros((2,1))
    
    ser_ss_calc[0,0] = exit_cst_value
    ser_ss_calc[1,0] = constraint_eqn_coeff

    return ser_ss_calc  
