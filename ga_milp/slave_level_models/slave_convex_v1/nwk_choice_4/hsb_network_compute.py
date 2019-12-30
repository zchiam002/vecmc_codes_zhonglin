##This is the compute file 

def hsb_network_compute (hsb_nwk_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##hsb_nwk_dc = np.zeros((6,1))                                                
    ##hsb_nwk_dc[0,0] = hsb_network['hsb_nwk_hsbcoeff']['value']
    ##hsb_nwk_dc[1,0] = hsb_network['hsb_nwk_hsbmaxflow']['value']


    ##Calculating the intervals for the hsb network 
    hsb_flow1 = 0
    hsb_flow2 = 0.25 * hsb_nwk_dc[1,0]
    hsb_flow3 = 0.5 * hsb_nwk_dc[1,0]
    hsb_flow4 = 0.75 * hsb_nwk_dc[1,0]
    hsb_flow5 = 1 * hsb_nwk_dc[1,0]

    hsb_delp1 = 0
    hsb_delp2 = hsb_nwk_dc[0,0]*pow(hsb_flow2,1.852)
    hsb_delp3 = hsb_nwk_dc[0,0]*pow(hsb_flow3,1.852)
    hsb_delp4 = hsb_nwk_dc[0,0]*pow(hsb_flow4,1.852)
    hsb_delp5 = hsb_nwk_dc[0,0]*pow(hsb_flow5,1.852)
    
    hsb_grad1 = (hsb_delp2 - hsb_delp1) / (hsb_flow2 - hsb_flow1)
    hsb_grad2 = (hsb_delp3 - hsb_delp2) / (hsb_flow3 - hsb_flow2)
    hsb_grad3 = (hsb_delp4 - hsb_delp3) / (hsb_flow4 - hsb_flow3)
    hsb_grad4 = (hsb_delp5 - hsb_delp4) / (hsb_flow5 - hsb_flow4)
    
    hsb_int1 = 0
    hsb_int2 = hsb_delp3 - (hsb_grad2 * hsb_flow3)
    hsb_int3 = hsb_delp4 - (hsb_grad3 * hsb_flow4)
    hsb_int4 = hsb_delp5 - (hsb_grad4 * hsb_flow5)
    
    ##Initiate a matrix to hold the return values 
    hsb_nwk_calc = np.zeros((13,1))
    
    hsb_nwk_calc[0,0] = hsb_grad1
    hsb_nwk_calc[1,0] = hsb_grad2
    hsb_nwk_calc[2,0] = hsb_grad3
    hsb_nwk_calc[3,0] = hsb_grad4
    hsb_nwk_calc[4,0] = hsb_int1
    hsb_nwk_calc[5,0] = hsb_int2
    hsb_nwk_calc[6,0] = hsb_int3
    hsb_nwk_calc[7,0] = hsb_int4
    hsb_nwk_calc[8,0] = 0
    hsb_nwk_calc[9,0] = 0.25
    hsb_nwk_calc[10,0] = 0.5
    hsb_nwk_calc[11,0] = 0.75
    hsb_nwk_calc[12,0] = 1

    return hsb_nwk_calc
