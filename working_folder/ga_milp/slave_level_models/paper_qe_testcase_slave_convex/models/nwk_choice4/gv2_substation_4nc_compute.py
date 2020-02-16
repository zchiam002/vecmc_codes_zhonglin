#This is the compute file 

def gv2_substation_4nc_compute (gv2_ss_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##gv2_ss_dc = np.zeros((5,1))          
    
    ##gv2_ss_dc[0,0] = gv2_ss_demand
    ##gv2_ss_dc[1,0] = gv2_ss_totalflownwk
    ##gv2_ss_dc[2,0] = gv2_ss_cp
    ##gv2_ss_dc[3,0] = gv2_ss_tinmax
    ##gv2_ss_dc[4,0] = gv2_ss_deltmax
    
    ##Calculating the constant value for the exting stream
    if gv2_ss_dc[1,0] == 0:
        exit_cst_value = 0
    else:
        flow = gv2_ss_dc[1,0] * 998.2 / 3600
        exit_cst_value = gv2_ss_dc[0,0] / (flow * gv2_ss_dc[2,0])
    
    ##Calculating the constraint equation coefficient 
    if gv2_ss_dc[0,0] == 0:
        constraint_eqn_coeff = 0
    else:
        constraint_eqn_coeff = (flow * gv2_ss_dc[2,0]) /  gv2_ss_dc[0,0] 
    
    
    ##Initiate a matrix to hold the return values 
    gv2_ss_calc = np.zeros((2,1))
    
    gv2_ss_calc[0,0] = exit_cst_value
    gv2_ss_calc[1,0] = constraint_eqn_coeff

    return gv2_ss_calc  

    

