#This is the compute file 

def gv2_substation_compute_nwk_choice_4 (gv2_ss_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##gv2_ss_dc = np.zeros((3,1))
    ##gv2_ss_dc[0,0] = gv2_substation['gv2_ss_demand']['value']
    ##gv2_ss_dc[1,0] = gv2_substation['gv2_ss_totalflownwk']['value']
    ##gv2_ss_dc[2,0] = gv2_substation['gv2_ss_cp']['value']
    ##gv2_ss_dc[3,0] = gv2_substation['gv2_ss_tinmax']['value']
    ##gv2_ss_dc[4,0] = gv2_substation['gv2_ss_deltmax']['value']
    
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
        constraint_eqn_coeff = (gv2_ss_dc[1,0] * gv2_ss_dc[2,0]) /  gv2_ss_dc[0,0] 
    
    
    ##Initiate a matrix to hold the return values 
    gv2_ss_calc = np.zeros((2,1))
    
    gv2_ss_calc[0,0] = exit_cst_value
    gv2_ss_calc[1,0] = constraint_eqn_coeff

    return gv2_ss_calc  

    

