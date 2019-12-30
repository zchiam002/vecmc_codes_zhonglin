#This is the compute file 

def chiller3_compute (ch3_dc):
    
    import numpy as np
    
    ##ch3_dc    - list of input values
    ##ch3_dc[0,0] = chiller3['ch3_evapflow']['value']
    ##ch3_dc[1,0] = chiller3['ch3_evaptret']['value']
    ##ch3_dc[2,0] = chiller3['ch3_condflow']['value']
    ##ch3_dc[3,0] = chiller3['ch3_condtin']['value']
    ##ch3_dc[4,0] = chiller3['ch3_rated_cap']['value']
    ##ch3_dc[5,0] = chiller3['ch3_b0']['value']    
    ##ch3_dc[6,0] = chiller3['ch3_b1']['value']
    ##ch3_dc[7,0] = chiller3['ch3_b2']['value']
    ##ch3_dc[8,0] = chiller3['ch3_qc_coeff']['value']
    ##ch3_dc[9,0] = chiller3['ch3_totalenwkflow']['value']
    ##ch3_dc[10,0] = chiller3['ch3_totalcnwkflow']['value']
    
    ch3_evaptout = 273.15 + 1                                                   ##The lowest it can go
    ch3_evapflow = (ch3_dc[0,0]/3600) * 998.2                                   ##Convert it to kg/s
    
    if (ch3_evapflow != 0) and (ch3_dc[2,0] != 0):
        ch3_dt_maxcap = ch3_dc[4,0] / (ch3_evapflow * 4.2)
        ch3_dt_lim_tevap_in = ch3_dc[1,0] - ch3_evaptout                            ##Maximum delta t due to the evaporator inlet temperature 
        ch3_dtevap_fmax = min(ch3_dt_maxcap,ch3_dt_lim_tevap_in)                    ##The capacity will be the smaller delta t of the above 2
        ch3_dtevap_step = ch3_dtevap_fmax/4                                         ##Each temperature step on the evaporator 
        
        ch3_maxqe = ch3_evapflow*4.2*ch3_dt_maxcap                                  ##The maximum cooling effect 
        
        ch3_maxqc = ch3_dc[8,0]*ch3_maxqe                                           ##The maximum heat rejection at the condenser side 
        ch3_condflow = (ch3_dc[2,0]/3600)*998.2                                     ##Convert it to kg/s
        ch3_dtcond_fmax = ch3_maxqc/(ch3_condflow*4.2)
        ch3_dtcond_step = ch3_dtcond_fmax/4                                         ##Each temperature step on the condenser
        
        ##Select COP based on percentage delta t
        
        ch3_qe1 = 0.25*(ch3_evapflow*4.2*ch3_dt_maxcap)                           ##To define the upper and lower limit of Qe at each step
        ch3_qe2 = 0.5*(ch3_evapflow*4.2*ch3_dt_maxcap)
        ch3_qe3 = 0.75*(ch3_evapflow*4.2*ch3_dt_maxcap)
        ch3_qe4 = (ch3_evapflow*4.2*ch3_dt_maxcap)
    
        ch3_t11 = ch3_dc[5,0]*(ch3_dc[1,0]/ch3_qe1)
        ch3_t21 = ch3_dc[6,0]*((ch3_dc[3,0]-ch3_dc[1,0])/(ch3_dc[3,0]*ch3_qe1))     ##Deriving the terms to calculate COP at each step
        ch3_t31 = ch3_dc[1,0]/ch3_dc[3,0]
        ch3_t41 = ch3_dc[7,0]*(ch3_qe1/ch3_dc[3,0])
    
        ch3_t12 = ch3_dc[5,0]*(ch3_dc[1,0]/ch3_qe2)
        ch3_t22 = ch3_dc[6,0]*((ch3_dc[3,0]-ch3_dc[1,0])/(ch3_dc[3,0]*ch3_qe2))
        ch3_t32 = ch3_dc[1,0]/ch3_dc[3,0]
        ch3_t42 = ch3_dc[7,0]*(ch3_qe2/ch3_dc[3,0])
    
        ch3_t13 = ch3_dc[5,0]*(ch3_dc[1,0]/ch3_qe3)
        ch3_t23 = ch3_dc[6,0]*((ch3_dc[3,0]-ch3_dc[1,0])/(ch3_dc[3,0]*ch3_qe3))
        ch3_t33 = ch3_dc[1,0]/ch3_dc[3,0]
        ch3_t43 = ch3_dc[7,0]*(ch3_qe3/ch3_dc[3,0])
    
        ch3_t14 = ch3_dc[5,0]*(ch3_dc[1,0]/ch3_qe4)
        ch3_t24 = ch3_dc[6,0]*((ch3_dc[3,0]-ch3_dc[1,0])/(ch3_dc[3,0]*ch3_qe4))
        ch3_t34 = ch3_dc[1,0]/ch3_dc[3,0]
        ch3_t44 = ch3_dc[7,0]*(ch3_qe4/ch3_dc[3,0])    
    
        ch3_cop1 = pow((((ch3_t11+ch3_t21+1)/(ch3_t31-ch3_t41))-1),-1)              ##The derived COPs at each of the steps
        ch3_cop2 = pow((((ch3_t12+ch3_t22+1)/(ch3_t32-ch3_t42))-1),-1)
        ch3_cop3 = pow((((ch3_t13+ch3_t23+1)/(ch3_t33-ch3_t43))-1),-1)
        ch3_cop4 = pow((((ch3_t14+ch3_t24+1)/(ch3_t34-ch3_t44))-1),-1)
    
        ch3_enode1 = 0.25*ch3_maxqe/ch3_cop1                                        ##The end nodes of the piecewise linear segments (electricity vs Qe)
        ch3_enode2 = 0.5*ch3_maxqe/ch3_cop2
        ch3_enode3 = 0.75*ch3_maxqe/ch3_cop3
        ch3_enode4 = ch3_maxqe/ch3_cop4
        
        ch3_grad1 = ch3_enode1/0.25                                                 ##The gradients of the piecewise linear segments 
        ch3_grad2 = (ch3_enode2-ch3_enode1)/(0.5-0.25)
        ch3_grad3 = (ch3_enode3-ch3_enode2)/(0.75-0.5)
        ch3_grad4 = (ch3_enode4-ch3_enode3)/(1-0.75)
    
        ch3_int1 = 0;                                                               ##The y-axis intercepts of the piecewise linear segments 
        ch3_int2 = ch3_enode2-(ch3_grad2*0.5) 
        ch3_int3 = ch3_enode3-(ch3_grad3*0.75)
        ch3_int4 = ch3_enode4-(ch3_grad4*1)
    
        ch3_emax1 = 1*ch3_grad1 + ch3_int1                                          ##The maximum points of each piecewise linear segments, this is needed for percentage use 
        ch3_emax2 = 1*ch3_grad2 + ch3_int2
        ch3_emax3 = 1*ch3_grad3 + ch3_int3
        ch3_emax4 = 1*ch3_grad4 + ch3_int4
        
        ch3_eratio = ch3_dc[0,0]/ch3_dc[9,0]
        ch3_cratio = ch3_dc[2,0]/ch3_dc[10,0]
        
        ##Initialize matrix to hold return values 
        
        ch3_dc_calc =np.zeros((17,1))
        
        ch3_dc_calc[0,0] = ch3_int1
        ch3_dc_calc[1,0] = ch3_int2
        ch3_dc_calc[2,0] = ch3_int3
        ch3_dc_calc[3,0] = ch3_int4
        ch3_dc_calc[4,0] = ch3_emax1-ch3_int1
        ch3_dc_calc[5,0] = ch3_emax2-ch3_int2
        ch3_dc_calc[6,0] = ch3_emax3-ch3_int3
        ch3_dc_calc[7,0] = ch3_emax4-ch3_int4
        ch3_dc_calc[8,0] = ch3_dt_maxcap
        ch3_dc_calc[9,0] = ch3_eratio
        ch3_dc_calc[10,0] = ch3_cratio
        ch3_dc_calc[11,0] = ch3_dt_maxcap
        ch3_dc_calc[12,0] = 0
        ch3_dc_calc[13,0] = 0.25
        ch3_dc_calc[14,0] = 0.5
        ch3_dc_calc[15,0] = 0.75
        ch3_dc_calc[16,0] = 1
    
        return ch3_dc_calc
    
    else:
        ch3_dc_calc =np.zeros((17,1))
        
        return ch3_dc_calc
