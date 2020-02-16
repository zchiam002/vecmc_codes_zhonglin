##This is the compute file 

def pfa_network_compute (pfa_nwk_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##pfa_nwk_dc = np.zeros((6,1))                                                
    ##pfa_nwk_dc[0,0] = pfa_network['pfa_nwk_pfacoeff']['value']
    ##pfa_nwk_dc[1,0] = pfa_network['pfa_nwk_pfamaxflow']['value']


    ##Calculating the intervals for the pfa network 
    pfa_flow1 = 0
    pfa_flow2 = 0.25 * pfa_nwk_dc[1,0]
    pfa_flow3 = 0.5 * pfa_nwk_dc[1,0]
    pfa_flow4 = 0.75 * pfa_nwk_dc[1,0]
    pfa_flow5 = 1 * pfa_nwk_dc[1,0]

    pfa_delp1 = 0
    pfa_delp2 = pfa_nwk_dc[0,0]*pow(pfa_flow2,1.852)
    pfa_delp3 = pfa_nwk_dc[0,0]*pow(pfa_flow3,1.852)
    pfa_delp4 = pfa_nwk_dc[0,0]*pow(pfa_flow4,1.852)
    pfa_delp5 = pfa_nwk_dc[0,0]*pow(pfa_flow5,1.852)
    
    pfa_grad1 = (pfa_delp2 - pfa_delp1) / (pfa_flow2 - pfa_flow1)
    pfa_grad2 = (pfa_delp3 - pfa_delp2) / (pfa_flow3 - pfa_flow2)
    pfa_grad3 = (pfa_delp4 - pfa_delp3) / (pfa_flow4 - pfa_flow3)
    pfa_grad4 = (pfa_delp5 - pfa_delp4) / (pfa_flow5 - pfa_flow4)
    
    pfa_int1 = 0
    pfa_int2 = pfa_delp3 - (pfa_grad2 * pfa_flow3)
    pfa_int3 = pfa_delp4 - (pfa_grad3 * pfa_flow4)
    pfa_int4 = pfa_delp5 - (pfa_grad4 * pfa_flow5)
    
    ##Initiate a matrix to hold the return values 
    pfa_nwk_calc = np.zeros((13,1))
    
    pfa_nwk_calc[0,0] = pfa_grad1
    pfa_nwk_calc[1,0] = pfa_grad2
    pfa_nwk_calc[2,0] = pfa_grad3
    pfa_nwk_calc[3,0] = pfa_grad4
    pfa_nwk_calc[4,0] = pfa_int1
    pfa_nwk_calc[5,0] = pfa_int2
    pfa_nwk_calc[6,0] = pfa_int3
    pfa_nwk_calc[7,0] = pfa_int4
    pfa_nwk_calc[8,0] = 0
    pfa_nwk_calc[9,0] = 0.25
    pfa_nwk_calc[10,0] = 0.5
    pfa_nwk_calc[11,0] = 0.75
    pfa_nwk_calc[12,0] = 1

    return pfa_nwk_calc
