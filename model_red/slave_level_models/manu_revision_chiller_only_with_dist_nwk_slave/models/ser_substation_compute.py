##This is the compute file 

##Note: Some of the implementations may be more accurate than others due to the dynamic step size 

def ser_substation_compute (ser_ss_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##ser_ss_dc = np.zeros((5,1))          
    
    ##ser_ss_dc[0,0] = ser_ss_demand
    ##ser_ss_dc[1,0] = ser_ss_totalflownwk
    ##ser_ss_dc[2,0] = ser_ss_cp
    ##ser_ss_dc[3,0] = ser_ss_tinmax
    ##ser_ss_dc[4,0] = ser_ss_deltmax
    
    ##Calculating the constant value for the exting stream
    if ser_ss_dc[1,0] == 0:
        exit_cst_value = 0
    else:
        flow = ser_ss_dc[1,0] * 998.2 / 3600
        exit_cst_value = ser_ss_dc[0,0] / (flow * ser_ss_dc[2,0])
    
    ##Calculating the constraint equation coefficient 
    if ser_ss_dc[0,0] == 0:
        constraint_eqn_coeff = 0
    else:
        constraint_eqn_coeff = (flow * ser_ss_dc[2,0]) /  ser_ss_dc[0,0] 
    
    
    ##Initiate a matrix to hold the return values 
    ser_ss_calc = np.zeros((2,1))
    
    ser_ss_calc[0,0] = exit_cst_value
    ser_ss_calc[1,0] = constraint_eqn_coeff

    return ser_ss_calc  