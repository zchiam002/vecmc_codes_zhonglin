#This is the compute file

def substation_ser_compute (ssser_dc):
    import numpy as np
    
    ##ssser_dc[0,0] = substation_ser['ssser_demand']['value']
    ##ssser_dc[1,0] = substation_ser['ssser_flowrate']['value']
    ##ssser_dc[2,0] = substation_ser['ssser_totalnwkflow']['value']
    
    if ssser_dc[1,0] == 0:
        ssser_delt = 0
    
        if ssser_dc[2,0] == 0:    
            ssser_fratio = 0
        else:
            ssser_fratio = ssser_dc[1,0]/ssser_dc[2,0]
        
    else:        
        ssser_delt = ssser_dc[0,0]/(((ssser_dc[1,0]*998.2)/3600)*4.2)               ##The required delta t of the substation
    
        ssser_fratio = ssser_dc[1,0]/ssser_dc[2,0]                                  ##The flowrate ratio of the substation 
    
    ssser_dc_calc = np.zeros((2,1))
    
    ssser_dc_calc[0,0] = ssser_delt
    ssser_dc_calc[1,0] = ssser_fratio

    return ssser_dc_calc