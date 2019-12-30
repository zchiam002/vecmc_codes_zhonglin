##This is the compute file 

def ser_network_compute (ser_nwk_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##ser_nwk_dc = np.zeros((6,1))                                                
    ##ser_nwk_dc[0,0] = ser_network['ser_nwk_sercoeff']['value']
    ##ser_nwk_dc[1,0] = ser_network['ser_nwk_sermaxflow']['value']


    ##Calculating the intervals for the ser network 
    ser_flow1 = 0
    ser_flow2 = 0.25 * ser_nwk_dc[1,0]
    ser_flow3 = 0.5 * ser_nwk_dc[1,0]
    ser_flow4 = 0.75 * ser_nwk_dc[1,0]
    ser_flow5 = 1 * ser_nwk_dc[1,0]

    ser_delp1 = 0
    ser_delp2 = ser_nwk_dc[0,0]*pow(ser_flow2,1.852)
    ser_delp3 = ser_nwk_dc[0,0]*pow(ser_flow3,1.852)
    ser_delp4 = ser_nwk_dc[0,0]*pow(ser_flow4,1.852)
    ser_delp5 = ser_nwk_dc[0,0]*pow(ser_flow5,1.852)
    
    ser_grad1 = (ser_delp2 - ser_delp1) / (ser_flow2 - ser_flow1)
    ser_grad2 = (ser_delp3 - ser_delp2) / (ser_flow3 - ser_flow2)
    ser_grad3 = (ser_delp4 - ser_delp3) / (ser_flow4 - ser_flow3)
    ser_grad4 = (ser_delp5 - ser_delp4) / (ser_flow5 - ser_flow4)
    
    ser_int1 = 0
    ser_int2 = ser_delp3 - (ser_grad2 * ser_flow3)
    ser_int3 = ser_delp4 - (ser_grad3 * ser_flow4)
    ser_int4 = ser_delp5 - (ser_grad4 * ser_flow5)
    
    ##Initiate a matrix to hold the return values 
    ser_nwk_calc = np.zeros((13,1))
    
    ser_nwk_calc[0,0] = ser_grad1
    ser_nwk_calc[1,0] = ser_grad2
    ser_nwk_calc[2,0] = ser_grad3
    ser_nwk_calc[3,0] = ser_grad4
    ser_nwk_calc[4,0] = ser_int1
    ser_nwk_calc[5,0] = ser_int2
    ser_nwk_calc[6,0] = ser_int3
    ser_nwk_calc[7,0] = ser_int4
    ser_nwk_calc[8,0] = 0
    ser_nwk_calc[9,0] = 0.25
    ser_nwk_calc[10,0] = 0.5
    ser_nwk_calc[11,0] = 0.75
    ser_nwk_calc[12,0] = 1

    return ser_nwk_calc