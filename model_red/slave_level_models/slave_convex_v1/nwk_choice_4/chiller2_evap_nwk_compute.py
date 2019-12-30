##This is the compute file 

def chiller2_evap_nwk_compute (ch2_e_nwk_dc):
    
    import numpy as np
    
    ##ch2_e_nwk_dc    - list of input values
    ##ch2_e_nwk_dc[0,0] = chiller2_evap_nwk['ch2_e_nwk_totalflow']['value']
    ##ch2_e_nwk_dc[1,0] = chiller2_evap_nwk['ch2_e_nwk_evap_delp_coeff']['value']
    ##ch2_e_nwk_dc[2,0] = chiller2_evap_nwk['ch2_e_nwk_common_nwk_delp_coeff']['value']
    ##ch2_e_nwk_dc[3,0] = chiller2_evap_nwk['ch2_e_nwk_max_flow']['value']   
    
    ##Performing piecewise linearization of the system curve, into 4 parts  
    sys_flow1 = 0
    sys_flow2 = 0.25 * ch2_e_nwk_dc[3,0]
    sys_flow3 = 0.5 * ch2_e_nwk_dc[3,0]
    sys_flow4 = 0.75 * ch2_e_nwk_dc[3,0]
    sys_flow5 = 1 * ch2_e_nwk_dc[3,0]

    sys_delp1 = ch2_e_nwk_dc[1,0]*pow(sys_flow1 ,1.852) + ch2_e_nwk_dc[2,0]*pow(ch2_e_nwk_dc[0,0] ,1.852)
    sys_delp2 = ch2_e_nwk_dc[1,0]*pow(sys_flow2 ,1.852) + ch2_e_nwk_dc[2,0]*pow(ch2_e_nwk_dc[0,0] ,1.852)
    sys_delp3 = ch2_e_nwk_dc[1,0]*pow(sys_flow3 ,1.852) + ch2_e_nwk_dc[2,0]*pow(ch2_e_nwk_dc[0,0] ,1.852)
    sys_delp4 = ch2_e_nwk_dc[1,0]*pow(sys_flow4 ,1.852) + ch2_e_nwk_dc[2,0]*pow(ch2_e_nwk_dc[0,0] ,1.852)
    sys_delp5 = ch2_e_nwk_dc[1,0]*pow(sys_flow5 ,1.852) + ch2_e_nwk_dc[2,0]*pow(ch2_e_nwk_dc[0,0] ,1.852)
    
    sys_grad1 = (sys_delp2 - sys_delp1) / (sys_flow2 - sys_flow1)
    sys_grad2 = (sys_delp3 - sys_delp2) / (sys_flow3 - sys_flow2)
    sys_grad3 = (sys_delp4 - sys_delp3) / (sys_flow4 - sys_flow3)
    sys_grad4 = (sys_delp5 - sys_delp4) / (sys_flow5 - sys_flow4)
    
    sys_int1 = sys_delp2 - sys_grad1*sys_flow2
    sys_int2 = sys_delp3 - sys_grad2*sys_flow3
    sys_int3 = sys_delp4 - sys_grad3*sys_flow4
    sys_int4 = sys_delp5 - sys_grad4*sys_flow5

    ##Initiate a matrix to hold the return values 
    
    ch2_e_nwk_calc = np.zeros((13 ,1))
    
    ch2_e_nwk_calc[0,0] = sys_grad1
    ch2_e_nwk_calc[1,0] = sys_grad2
    ch2_e_nwk_calc[2,0] = sys_grad3
    ch2_e_nwk_calc[3,0] = sys_grad4
    ch2_e_nwk_calc[4,0] = sys_int1
    ch2_e_nwk_calc[5,0] = sys_int2
    ch2_e_nwk_calc[6,0] = sys_int3
    ch2_e_nwk_calc[7,0] = sys_int4
    ch2_e_nwk_calc[8,0] = 0
    ch2_e_nwk_calc[9,0] = 0.25
    ch2_e_nwk_calc[10,0] = 0.5
    ch2_e_nwk_calc[11,0] = 0.75
    ch2_e_nwk_calc[12,0] = 1
    
    return ch2_e_nwk_calc