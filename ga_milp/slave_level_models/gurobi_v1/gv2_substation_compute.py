#This is the compute file 

def gv2_substation_compute (ch1_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##gv2_ss_dc = np.zeros((3,1))
    ##gv2_ss_dc[0,0] = gv2_substation['gv2_ss_demand']['value']
    ##gv2_ss_dc[1,0] = gv2_substation['gv2_ss_totalflownwk']['value']
    ##gv2_ss_dc[2,0] = gv2_substation['gv2_ss_cp']['value']
    
    ##Calculating the constant value for the exting stream 
    exit_cst_value = gv2_ss_dc[0,0] / (gv2_ss_dc[1,0] * gv2_ss_dc[2,0])
    
    ##Initiate a matrix to hold the return values 
    gv2_ss_calc = np.zeros((1,1))
    
    gv2_ss_calc[0,0] = exit_cst_value

    return gv2_ss_calc  

    

