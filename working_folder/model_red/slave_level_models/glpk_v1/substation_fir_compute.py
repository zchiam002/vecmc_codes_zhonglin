#This is the compute file

def substation_fir_compute (ssfir_dc):
    import numpy as np
    
    ##ssfir_dc[0,0] = substation_fir['ssfir_demand']['value']
    ##ssfir_dc[1,0] = substation_fir['ssfir_flowrate']['value']
    ##ssfir_dc[2,0] = substation_fir['ssfir_totalnwkflow']['value']
    
    if ssfir_dc[1,0] == 0:
        ssfir_delt = 0
        
        if ssfir_dc[2,0] == 0:    
            ssfir_fratio = 0
        else:
            ssfir_fratio = ssfir_dc[1,0]/ssfir_dc[2,0]
        
    else:        
        ssfir_delt = ssfir_dc[0,0]/(((ssfir_dc[1,0]*998.2)/3600)*4.2)               ##The required delta t of the substation
    
        ssfir_fratio = ssfir_dc[1,0]/ssfir_dc[2,0]                                  ##The flowrate ratio of the substation 
    
    ssfir_dc_calc = np.zeros((2,1))
    
    ssfir_dc_calc[0,0] = ssfir_delt
    ssfir_dc_calc[1,0] = ssfir_fratio

    return ssfir_dc_calc