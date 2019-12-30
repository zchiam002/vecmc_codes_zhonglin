##This is the compute file 

def tro_network_compute (tro_nwk_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##tro_nwk_dc = np.zeros((6,1))                                                
    ##tro_nwk_dc[0,0] = tro_network['tro_nwk_trocoeff']['value']
    ##tro_nwk_dc[1,0] = tro_network['tro_nwk_tromaxflow']['value']


    ##Calculating the intervals for the tro network 
    tro_flow1 = 0
    tro_flow2 = 0.25 * tro_nwk_dc[1,0]
    tro_flow3 = 0.5 * tro_nwk_dc[1,0]
    tro_flow4 = 0.75 * tro_nwk_dc[1,0]
    tro_flow5 = 1 * tro_nwk_dc[1,0]

    tro_delp1 = 0
    tro_delp2 = tro_nwk_dc[0,0]*pow(tro_flow2,1.852)
    tro_delp3 = tro_nwk_dc[0,0]*pow(tro_flow3,1.852)
    tro_delp4 = tro_nwk_dc[0,0]*pow(tro_flow4,1.852)
    tro_delp5 = tro_nwk_dc[0,0]*pow(tro_flow5,1.852)
    
    tro_grad1 = (tro_delp2 - tro_delp1) / (tro_flow2 - tro_flow1)
    tro_grad2 = (tro_delp3 - tro_delp2) / (tro_flow3 - tro_flow2)
    tro_grad3 = (tro_delp4 - tro_delp3) / (tro_flow4 - tro_flow3)
    tro_grad4 = (tro_delp5 - tro_delp4) / (tro_flow5 - tro_flow4)
    
    tro_int1 = 0
    tro_int2 = tro_delp3 - (tro_grad2 * tro_flow3)
    tro_int3 = tro_delp4 - (tro_grad3 * tro_flow4)
    tro_int4 = tro_delp5 - (tro_grad4 * tro_flow5)
    
    ##Initiate a matrix to hold the return values 
    tro_nwk_calc = np.zeros((13,1))
    
    tro_nwk_calc[0,0] = tro_grad1
    tro_nwk_calc[1,0] = tro_grad2
    tro_nwk_calc[2,0] = tro_grad3
    tro_nwk_calc[3,0] = tro_grad4
    tro_nwk_calc[4,0] = tro_int1
    tro_nwk_calc[5,0] = tro_int2
    tro_nwk_calc[6,0] = tro_int3
    tro_nwk_calc[7,0] = tro_int4
    tro_nwk_calc[8,0] = 0
    tro_nwk_calc[9,0] = 0.25
    tro_nwk_calc[10,0] = 0.5
    tro_nwk_calc[11,0] = 0.75
    tro_nwk_calc[12,0] = 1

    return tro_nwk_calc