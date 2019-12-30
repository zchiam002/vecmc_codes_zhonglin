#This is the compute file

def substation_hsb_compute (sshsb_dc):
    import numpy as np
    
    ##sshsb_dc[0,0] = substation_hsb['sshsb_demand']['value']
    ##sshsb_dc[1,0] = substation_hsb['sshsb_flowrate']['value']
    ##sshsb_dc[2,0] = substation_hsb['sshsb_totalnwkflow']['value']
    
    if sshsb_dc[1,0] == 0:
        sshsb_delt = 0
        
        if sshsb_dc[2,0] == 0:    
            sshsb_fratio = 0
        else:
            sshsb_fratio = sshsb_dc[1,0]/sshsb_dc[2,0]
        
    else:        
        sshsb_delt = sshsb_dc[0,0]/(((sshsb_dc[1,0]*998.2)/3600)*4.2)               ##The required delta t of the substation
    
        sshsb_fratio = sshsb_dc[1,0]/sshsb_dc[2,0]                                  ##The flowrate ratio of the substation 
    
    sshsb_dc_calc = np.zeros((2,1))
    
    sshsb_dc_calc[0,0] = sshsb_delt
    sshsb_dc_calc[1,0] = sshsb_fratio

    return sshsb_dc_calc