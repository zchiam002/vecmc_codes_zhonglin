#This is the compute file

def substation_pfa_compute (sspfa_dc):
    import numpy as np
    
    ##sspfa_dc[0,0] = substation_pfa['sspfa_demand']['value']
    ##sspfa_dc[1,0] = substation_pfa['sspfa_flowrate']['value']
    ##sspfa_dc[2,0] = substation_pfa['sspfa_totalnwkflow']['value']
    
    if sspfa_dc[1,0] == 0:
        sspfa_delt = 0
        
        if sspfa_dc[2,0] == 0:    
            sspfa_fratio = 0
        else:
            sspfa_fratio = sspfa_dc[1,0]/sspfa_dc[2,0]
        
    else:    
        sspfa_delt = sspfa_dc[0,0]/(((sspfa_dc[1,0]*998.2)/3600)*4.2)              ##The required delta t of the substation
    
        sspfa_fratio = sspfa_dc[1,0]/sspfa_dc[2,0]                                 ##The flowrate ratio of the substation 
    
    sspfa_dc_calc = np.zeros((2,1))
    
    sspfa_dc_calc[0,0] = sspfa_delt
    sspfa_dc_calc[1,0] = sspfa_fratio

    return sspfa_dc_calc