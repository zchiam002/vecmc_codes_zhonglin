#This is the compute file

def substation_gv2_compute (ssgv2_dc):
    import numpy as np
    
    ##ssgv2_dc[0,0] = substation_gv2['ssgv2_demand']['value']
    ##ssgv2_dc[1,0] = substation_gv2['ssgv2_flowrate']['value']
    ##ssgv2_dc[2,0] = substation_gv2['ssgv2_totalnwkflow']['value']
    
    if ssgv2_dc[1,0] == 0:
        ssgv2_delt = 0
    
        if ssgv2_dc[2,0] == 0:    
            ssgv2_fratio = 0
        else:
            ssgv2_fratio = ssgv2_dc[1,0]/ssgv2_dc[2,0]
        
    else:
        ssgv2_delt = ssgv2_dc[0,0]/(((ssgv2_dc[1,0]*998.2)/3600)*4.2)               ##The required delta t of the substation
    
        ssgv2_fratio = ssgv2_dc[1,0]/ssgv2_dc[2,0]                                  ##The flowrate ratio of the substation 
    
    ssgv2_dc_calc = np.zeros((2,1))
    
    ssgv2_dc_calc[0,0] = ssgv2_delt
    ssgv2_dc_calc[1,0] = ssgv2_fratio

    return ssgv2_dc_calc