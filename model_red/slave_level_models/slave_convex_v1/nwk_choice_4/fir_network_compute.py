##This is the compute file 

def fir_network_compute (fir_nwk_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##fir_nwk_dc = np.zeros((6,1))                                                
    ##fir_nwk_dc[0,0] = fir_network['fir_nwk_fircoeff']['value']
    ##fir_nwk_dc[1,0] = fir_network['fir_nwk_firmaxflow']['value']


    ##Calculating the intervals for the fir network 
    fir_flow1 = 0
    fir_flow2 = 0.25 * fir_nwk_dc[1,0]
    fir_flow3 = 0.5 * fir_nwk_dc[1,0]
    fir_flow4 = 0.75 * fir_nwk_dc[1,0]
    fir_flow5 = 1 * fir_nwk_dc[1,0]

    fir_delp1 = 0
    fir_delp2 = fir_nwk_dc[0,0]*pow(fir_flow2,1.852)
    fir_delp3 = fir_nwk_dc[0,0]*pow(fir_flow3,1.852)
    fir_delp4 = fir_nwk_dc[0,0]*pow(fir_flow4,1.852)
    fir_delp5 = fir_nwk_dc[0,0]*pow(fir_flow5,1.852)
    
    fir_grad1 = (fir_delp2 - fir_delp1) / (fir_flow2 - fir_flow1)
    fir_grad2 = (fir_delp3 - fir_delp2) / (fir_flow3 - fir_flow2)
    fir_grad3 = (fir_delp4 - fir_delp3) / (fir_flow4 - fir_flow3)
    fir_grad4 = (fir_delp5 - fir_delp4) / (fir_flow5 - fir_flow4)
    
    fir_int1 = 0
    fir_int2 = fir_delp3 - (fir_grad2 * fir_flow3)
    fir_int3 = fir_delp4 - (fir_grad3 * fir_flow4)
    fir_int4 = fir_delp5 - (fir_grad4 * fir_flow5)
    
    ##Initiate a matrix to hold the return values 
    fir_nwk_calc = np.zeros((13,1))
    
    fir_nwk_calc[0,0] = fir_grad1
    fir_nwk_calc[1,0] = fir_grad2
    fir_nwk_calc[2,0] = fir_grad3
    fir_nwk_calc[3,0] = fir_grad4
    fir_nwk_calc[4,0] = fir_int1
    fir_nwk_calc[5,0] = fir_int2
    fir_nwk_calc[6,0] = fir_int3
    fir_nwk_calc[7,0] = fir_int4
    fir_nwk_calc[8,0] = 0
    fir_nwk_calc[9,0] = 0.25
    fir_nwk_calc[10,0] = 0.5
    fir_nwk_calc[11,0] = 0.75
    fir_nwk_calc[12,0] = 1

    return fir_nwk_calc