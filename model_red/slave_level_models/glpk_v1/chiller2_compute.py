#This is the compute file 

def chiller2_compute (ch2_dc):
    
    import numpy as np
    
    ##ch2_dc    - list of input values
    ##ch2_dc[0,0] = chiller2['ch2_evapflow']['value']
    ##ch2_dc[1,0] = chiller2['ch2_evaptret']['value']
    ##ch2_dc[2,0] = chiller2['ch2_condflow']['value']
    ##ch2_dc[3,0] = chiller2['ch2_condtin']['value']
    ##ch2_dc[4,0] = chiller2['ch2_rated_cap']['value']
    ##ch2_dc[5,0] = chiller2['ch2_b0']['value']    
    ##ch2_dc[6,0] = chiller2['ch2_b1']['value']
    ##ch2_dc[7,0] = chiller2['ch2_b2']['value']
    ##ch2_dc[8,0] = chiller2['ch2_qc_coeff']['value']
    ##ch2_dc[9,0] = chiller2['ch2_totalenwkflow']['value']
    ##ch2_dc[10,0] = chiller2['ch2_totalcnwkflow']['value']
    
    ch2_evaptout = 273.15 + 1                                                   ##The lowest it can go
    ch2_evapflow = (ch2_dc[0,0]/3600) * 998.2                                   ##Convert it to kg/s
    
    if (ch2_evapflow != 0) and (ch2_dc[2,0] != 0):
        ch2_dt_maxcap = ch2_dc[4,0] / (ch2_evapflow * 4.2)
        ch2_dt_lim_tevap_in = ch2_dc[1,0] - ch2_evaptout                            ##Maximum delta t due to the evaporator inlet temperature 
        ch2_dtevap_fmax = min(ch2_dt_maxcap,ch2_dt_lim_tevap_in)                    ##The capacity will be the smaller delta t of the above 2
        ch2_dtevap_step = ch2_dtevap_fmax/4                                         ##Each temperature step on the evaporator 
        
        ch2_maxqe = ch2_evapflow*4.2*ch2_dt_maxcap                                  ##The maximum cooling effect 
        
        ch2_maxqc = ch2_dc[8,0]*ch2_maxqe                                           ##The maximum heat rejection at the condenser side 
        ch2_condflow = (ch2_dc[2,0]/3600)*998.2                                     ##Convert it to kg/s
        ch2_dtcond_fmax = ch2_maxqc/(ch2_condflow*4.2)
        ch2_dtcond_step = ch2_dtcond_fmax/4                                         ##Each temperature step on the condenser
        
        ##Select COP based on percentage delta t
        
        ch2_qe1 = 0.25*(ch2_evapflow*4.2*ch2_dt_maxcap)                             ##To define the upper and lower limit of Qe at each step
        ch2_qe2 = 0.5*(ch2_evapflow*4.2*ch2_dt_maxcap)
        ch2_qe3 = 0.75*(ch2_evapflow*4.2*ch2_dt_maxcap)
        ch2_qe4 = (ch2_evapflow*4.2*ch2_dt_maxcap)
    
        ch2_t11 = ch2_dc[5,0]*(ch2_dc[1,0]/ch2_qe1)
        ch2_t21 = ch2_dc[6,0]*((ch2_dc[3,0]-ch2_dc[1,0])/(ch2_dc[3,0]*ch2_qe1))     ##Deriving the terms to calculate COP at each step
        ch2_t31 = ch2_dc[1,0]/ch2_dc[3,0]
        ch2_t41 = ch2_dc[7,0]*(ch2_qe1/ch2_dc[3,0])
    
        ch2_t12 = ch2_dc[5,0]*(ch2_dc[1,0]/ch2_qe2)
        ch2_t22 = ch2_dc[6,0]*((ch2_dc[3,0]-ch2_dc[1,0])/(ch2_dc[3,0]*ch2_qe2))
        ch2_t32 = ch2_dc[1,0]/ch2_dc[3,0]
        ch2_t42 = ch2_dc[7,0]*(ch2_qe2/ch2_dc[3,0])
    
        ch2_t13 = ch2_dc[5,0]*(ch2_dc[1,0]/ch2_qe3)
        ch2_t23 = ch2_dc[6,0]*((ch2_dc[3,0]-ch2_dc[1,0])/(ch2_dc[3,0]*ch2_qe3))
        ch2_t33 = ch2_dc[1,0]/ch2_dc[3,0]
        ch2_t43 = ch2_dc[7,0]*(ch2_qe3/ch2_dc[3,0])
    
        ch2_t14 = ch2_dc[5,0]*(ch2_dc[1,0]/ch2_qe4)
        ch2_t24 = ch2_dc[6,0]*((ch2_dc[3,0]-ch2_dc[1,0])/(ch2_dc[3,0]*ch2_qe4))
        ch2_t34 = ch2_dc[1,0]/ch2_dc[3,0]
        ch2_t44 = ch2_dc[7,0]*(ch2_qe4/ch2_dc[3,0])    
    
        ch2_cop1 = pow((((ch2_t11+ch2_t21+1)/(ch2_t31-ch2_t41))-1),-1)              ##The derived COPs at each of the steps
        ch2_cop2 = pow((((ch2_t12+ch2_t22+1)/(ch2_t32-ch2_t42))-1),-1)
        ch2_cop3 = pow((((ch2_t13+ch2_t23+1)/(ch2_t33-ch2_t43))-1),-1)
        ch2_cop4 = pow((((ch2_t14+ch2_t24+1)/(ch2_t34-ch2_t44))-1),-1)
    
        ch2_enode1 = 0.25*ch2_maxqe/ch2_cop1                                        ##The end nodes of the piecewise linear segments (electricity vs Qe)
        ch2_enode2 = 0.5*ch2_maxqe/ch2_cop2
        ch2_enode3 = 0.75*ch2_maxqe/ch2_cop3
        ch2_enode4 = ch2_maxqe/ch2_cop4
        
        ch2_grad1 = ch2_enode1/0.25                                                 ##The gradients of the piecewise linear segments 
        ch2_grad2 = (ch2_enode2-ch2_enode1)/(0.5-0.25)
        ch2_grad3 = (ch2_enode3-ch2_enode2)/(0.75-0.5)
        ch2_grad4 = (ch2_enode4-ch2_enode3)/(1-0.75)
    
        ch2_int1 = 0;                                                               ##The y-axis intercepts of the piecewise linear segments 
        ch2_int2 = ch2_enode2-(ch2_grad2*0.5) 
        ch2_int3 = ch2_enode3-(ch2_grad3*0.75)
        ch2_int4 = ch2_enode4-(ch2_grad4*1)
    
        ch2_emax1 = 1*ch2_grad1 + ch2_int1                                          ##The maximum points of each piecewise linear segments, this is needed for percentage use 
        ch2_emax2 = 1*ch2_grad2 + ch2_int2
        ch2_emax3 = 1*ch2_grad3 + ch2_int3
        ch2_emax4 = 1*ch2_grad4 + ch2_int4
        
        ch2_eratio = ch2_dc[0,0]/ch2_dc[9,0]
        ch2_cratio = ch2_dc[2,0]/ch2_dc[10,0]
        
        ##Initialize matrix to hold return values 
        
        ch2_dc_calc =np.zeros((17,1))
        
        ch2_dc_calc[0,0] = ch2_int1
        ch2_dc_calc[1,0] = ch2_int2
        ch2_dc_calc[2,0] = ch2_int3
        ch2_dc_calc[3,0] = ch2_int4
        ch2_dc_calc[4,0] = ch2_emax1-ch2_int1
        ch2_dc_calc[5,0] = ch2_emax2-ch2_int2
        ch2_dc_calc[6,0] = ch2_emax3-ch2_int3
        ch2_dc_calc[7,0] = ch2_emax4-ch2_int4
        ch2_dc_calc[8,0] = ch2_dt_maxcap
        ch2_dc_calc[9,0] = ch2_eratio
        ch2_dc_calc[10,0] = ch2_cratio
        ch2_dc_calc[11,0] = ch2_dtcond_fmax
        ch2_dc_calc[12,0] = 0
        ch2_dc_calc[13,0] = 0.25
        ch2_dc_calc[14,0] = 0.5
        ch2_dc_calc[15,0] = 0.75
        ch2_dc_calc[16,0] = 1
    
        return ch2_dc_calc
    
    else:
        ch2_dc_calc =np.zeros((17,1))
        
        return ch2_dc_calc
    
