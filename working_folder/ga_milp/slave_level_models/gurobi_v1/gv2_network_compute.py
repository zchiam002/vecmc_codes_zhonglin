##This is the compute file 

def gv2_network_compute (gv2_nwk_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##gv2_nwk_dc = np.zeros((6,1))                                                
    ##gv2_nwk_dc[0,0] = gv2_network['gv2_nwk_gv2coeff']['value']
    ##gv2_nwk_dc[1,0] = gv2_network['gv2_nwk_gv2maxflow']['value']


    ##Calculating the intervals for the gv2 network 
    gv2_flow1 = 0
    gv2_flow2 = 0.25 * gv2_nwk_dc[1,0]
    gv2_flow3 = 0.5 * gv2_nwk_dc[1,0]
    gv2_flow4 = 0.75 * gv2_nwk_dc[1,0]
    gv2_flow5 = 1 * gv2_nwk_dc[1,0]

    gv2_delp1 = 0
    gv2_delp2 = gv2_nwk_dc[0,0]*pow(gv2_flow2,1.852)
    gv2_delp3 = gv2_nwk_dc[0,0]*pow(gv2_flow3,1.852)
    gv2_delp4 = gv2_nwk_dc[0,0]*pow(gv2_flow4,1.852)
    gv2_delp5 = gv2_nwk_dc[0,0]*pow(gv2_flow5,1.852)
    
    gv2_grad1 = (gv2_delp2 - gv2_delp1) / (gv2_flow2 - gv2_flow1)
    gv2_grad2 = (gv2_delp3 - gv2_delp2) / (gv2_flow3 - gv2_flow2)
    gv2_grad3 = (gv2_delp4 - gv2_delp3) / (gv2_flow4 - gv2_flow3)
    gv2_grad4 = (gv2_delp5 - gv2_delp4) / (gv2_flow5 - gv2_flow4)
    
    gv2_int1 = 0
    gv2_int2 = gv2_delp3 - (gv2_grad2 * gv2_flow3)
    gv2_int3 = gv2_delp4 - (gv2_grad3 * gv2_flow4)
    gv2_int4 = gv2_delp5 - (gv2_grad4 * gv2_flow5)
    
    ##Initiate a matrix to hold the return values 
    gv2_nwk_calc = np.zeros((13,1))
    
    gv2_nwk_calc[0,0] = gv2_grad1
    gv2_nwk_calc[1,0] = gv2_grad2
    gv2_nwk_calc[2,0] = gv2_grad3
    gv2_nwk_calc[3,0] = gv2_grad4
    gv2_nwk_calc[4,0] = gv2_int1
    gv2_nwk_calc[5,0] = gv2_int2
    gv2_nwk_calc[6,0] = gv2_int3
    gv2_nwk_calc[7,0] = gv2_int4
    gv2_nwk_calc[8,0] = 0
    gv2_nwk_calc[9,0] = 0.25
    gv2_nwk_calc[10,0] = 0.5
    gv2_nwk_calc[11,0] = 0.75
    gv2_nwk_calc[12,0] = 1

    return gv2_nwk_calc
