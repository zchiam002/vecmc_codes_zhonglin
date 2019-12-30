#This is the compute file 

def substation_cp_compute (sscp_dc):
    
    import numpy as np
    
    ##sscp_dc[0,0] = substation_cp['sscp_demand']['value']
    ##sscp_dc[1,0] = substation_cp['sscp_flowrate']['value']
    ##sscp_dc[2,0] = substation_cp['sscp_totalnwkflow']['value']

    if sscp_dc[1,0] == 0:
        sscp_delt = 0
        
        if sscp_dc[2,0] == 0:    
            sscp_fratio = 0
        else:
            sscp_fratio = sscp_dc[1,0]/sscp_dc[2,0]
        
    else:
        sscp_delt = sscp_dc[0,0]/(((sscp_dc[1,0]*998.2)/3600)*4.2)              ##The required delta t of the substatio
        sscp_fratio = sscp_dc[1,0]/sscp_dc[2,0]                                 ##The flowrate ratio of the substation 
    
    sscp_dc_calc = np.zeros((2,1))
    
    sscp_dc_calc[0,0] = sscp_delt
    sscp_dc_calc[1,0] = sscp_fratio
    
    return sscp_dc_calc