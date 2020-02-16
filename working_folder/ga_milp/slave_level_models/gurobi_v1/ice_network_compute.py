##This is the compute file 

def ice_network_compute (ice_nwk_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##ice_nwk_dc = np.zeros((6,1))                                                
    ##ice_nwk_dc[0,0] = ice_network['ice_nwk_icecoeff']['value']
    ##ice_nwk_dc[1,0] = ice_network['ice_nwk_icemaxflow']['value']


    ##Calculating the intervals for the ice network 
    ice_flow1 = 0
    ice_flow2 = 0.25 * ice_nwk_dc[1,0]
    ice_flow3 = 0.5 * ice_nwk_dc[1,0]
    ice_flow4 = 0.75 * ice_nwk_dc[1,0]
    ice_flow5 = 1 * ice_nwk_dc[1,0]

    ice_delp1 = 0
    ice_delp2 = ice_nwk_dc[0,0]*pow(ice_flow2,1.852)
    ice_delp3 = ice_nwk_dc[0,0]*pow(ice_flow3,1.852)
    ice_delp4 = ice_nwk_dc[0,0]*pow(ice_flow4,1.852)
    ice_delp5 = ice_nwk_dc[0,0]*pow(ice_flow5,1.852)
    
    ice_grad1 = (ice_delp2 - ice_delp1) / (ice_flow2 - ice_flow1)
    ice_grad2 = (ice_delp3 - ice_delp2) / (ice_flow3 - ice_flow2)
    ice_grad3 = (ice_delp4 - ice_delp3) / (ice_flow4 - ice_flow3)
    ice_grad4 = (ice_delp5 - ice_delp4) / (ice_flow5 - ice_flow4)
    
    ice_int1 = 0
    ice_int2 = ice_delp3 - (ice_grad2 * ice_flow3)
    ice_int3 = ice_delp4 - (ice_grad3 * ice_flow4)
    ice_int4 = ice_delp5 - (ice_grad4 * ice_flow5)
    
    ##Initiate a matrix to hold the return values 
    ice_nwk_calc = np.zeros((13,1))
    
    ice_nwk_calc[0,0] = ice_grad1
    ice_nwk_calc[1,0] = ice_grad2
    ice_nwk_calc[2,0] = ice_grad3
    ice_nwk_calc[3,0] = ice_grad4
    ice_nwk_calc[4,0] = ice_int1
    ice_nwk_calc[5,0] = ice_int2
    ice_nwk_calc[6,0] = ice_int3
    ice_nwk_calc[7,0] = ice_int4
    ice_nwk_calc[8,0] = 0
    ice_nwk_calc[9,0] = 0.25
    ice_nwk_calc[10,0] = 0.5
    ice_nwk_calc[11,0] = 0.75
    ice_nwk_calc[12,0] = 1

    return ice_nwk_calc