#This is the compute file 

def fir_substation_compute (fir_ss_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##fir_ss_dc = np.zeros((3,1))
    ##fir_ss_dc[0,0] = fir_substation['fir_ss_demand']['value']
    ##fir_ss_dc[1,0] = fir_substation['fir_ss_totalflownwk']['value']
    ##fir_ss_dc[2,0] = fir_substation['fir_ss_cp']['value']
    ##fir_ss_dc[3,0] = fir_substation['fir_ss_tinmax']['value']
    ##fir_ss_dc[4,0] = fir_substation['fir_ss_deltmax']['value']  
    
    ##Calculating the constant value for the exting stream
    if fir_ss_dc[0,0] == 0:
        exit_cst_value = 0
    else:
        exit_cst_value = fir_ss_dc[0,0] / (fir_ss_dc[1,0] * fir_ss_dc[2,0])
        
    ##Calculating the constraint equation coefficient 
    if fir_ss_dc[0,0] == 0:
        constraint_eqn_coeff = 0
    else:
        constraint_eqn_coeff = (fir_ss_dc[1,0] * fir_ss_dc[2,0]) /  fir_ss_dc[0,0] 
    
    ##Initiate a matrix to hold the return values 
    fir_ss_calc = np.zeros((2,1))
    
    fir_ss_calc[0,0] = exit_cst_value
    fir_ss_calc[1,0] = constraint_eqn_coeff

    return fir_ss_calc  
