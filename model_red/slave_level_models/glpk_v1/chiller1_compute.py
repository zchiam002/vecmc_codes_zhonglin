#This is the compute file 

def chiller1_compute (ch1_dc):
    
    import numpy as np
    
    ##ch1_dc    - list of input values
    ##ch1_dc[0,0] = chiller1['ch1_evapflow']['value']
    ##ch1_dc[1,0] = chiller1['ch1_evaptret']['value']
    ##ch1_dc[2,0] = chiller1['ch1_condflow']['value']
    ##ch1_dc[3,0] = chiller1['ch1_condtin']['value']
    ##ch1_dc[4,0] = chiller1['ch1_rated_cap']['value']
    ##ch1_dc[5,0] = chiller1['ch1_b0']['value']    
    ##ch1_dc[6,0] = chiller1['ch1_b1']['value']
    ##ch1_dc[7,0] = chiller1['ch1_b2']['value']
    ##ch1_dc[8,0] = chiller1['ch1_qc_coeff']['value']
    ##ch1_dc[9,0] = chiller1['ch1_totalenwkflow']['value']
    ##ch1_dc[10,0] = chiller1['ch1_totalcnwkflow']['value']
    
    ch1_evaptout = 273.15 + 1                                                   ##The lowest it can go
    ch1_evapflow = (ch1_dc[0,0]/3600) * 998.2                                   ##Convert it to kg/s
    
    if (ch1_evapflow != 0) and (ch1_dc[2,0] != 0):
        ch1_dt_maxcap = ch1_dc[4,0] / (ch1_evapflow * 4.2)
        ch1_dt_lim_tevap_in = ch1_dc[1,0] - ch1_evaptout                            ##Maximum delta t due to the evaportaor inlet temperature 
        ch1_dtevap_fmax = min(ch1_dt_maxcap,ch1_dt_lim_tevap_in)                    ##The capacity will be the smaller delta t of the above 2
        ch1_dtevap_step = ch1_dtevap_fmax/4                                         ##Each temperature step on the evaporator 
        
        ch1_maxqe = ch1_evapflow*4.2*ch1_dt_maxcap                                  ##The maximum cooling effect 
        
        ch1_maxqc = ch1_dc[8,0]*ch1_maxqe                                           ##The maximum heat rejection at the condenser side 
        ch1_condflow = (ch1_dc[2,0]/3600)*998.2                                     ##Convert it to kg/s
        ch1_dtcond_fmax = ch1_maxqc/(ch1_condflow*4.2)
        ch1_dtcond_step = ch1_dtcond_fmax/4                                         ##Each temperature step on the condenser
        
        ##Select COP based on percentage delta t
        
        ch1_qe1 = 0.25*(ch1_evapflow*4.2*ch1_dt_maxcap)                             ##To define the upper and lower limit of Qe at each step
        ch1_qe2 = 0.5*(ch1_evapflow*4.2*ch1_dt_maxcap)
        ch1_qe3 = 0.75*(ch1_evapflow*4.2*ch1_dt_maxcap)
        ch1_qe4 = (ch1_evapflow*4.2*ch1_dt_maxcap)
    
        ch1_t11 = ch1_dc[5,0]*(ch1_dc[1,0]/ch1_qe1)
        ch1_t21 = ch1_dc[6,0]*((ch1_dc[3,0]-ch1_dc[1,0])/(ch1_dc[3,0]*ch1_qe1))     ##Deriving the terms to calculate COP at each step
        ch1_t31 = ch1_dc[1,0]/ch1_dc[3,0]
        ch1_t41 = ch1_dc[7,0]*(ch1_qe1/ch1_dc[3,0])
    
        ch1_t12 = ch1_dc[5,0]*(ch1_dc[1,0]/ch1_qe2)
        ch1_t22 = ch1_dc[6,0]*((ch1_dc[3,0]-ch1_dc[1,0])/(ch1_dc[3,0]*ch1_qe2))
        ch1_t32 = ch1_dc[1,0]/ch1_dc[3,0]
        ch1_t42 = ch1_dc[7,0]*(ch1_qe2/ch1_dc[3,0])
    
        ch1_t13 = ch1_dc[5,0]*(ch1_dc[1,0]/ch1_qe3)
        ch1_t23 = ch1_dc[6,0]*((ch1_dc[3,0]-ch1_dc[1,0])/(ch1_dc[3,0]*ch1_qe3))
        ch1_t33 = ch1_dc[1,0]/ch1_dc[3,0]
        ch1_t43 = ch1_dc[7,0]*(ch1_qe3/ch1_dc[3,0])
    
        ch1_t14 = ch1_dc[5,0]*(ch1_dc[1,0]/ch1_qe4)
        ch1_t24 = ch1_dc[6,0]*((ch1_dc[3,0]-ch1_dc[1,0])/(ch1_dc[3,0]*ch1_qe4))
        ch1_t34 = ch1_dc[1,0]/ch1_dc[3,0]
        ch1_t44 = ch1_dc[7,0]*(ch1_qe4/ch1_dc[3,0])    
    
        ch1_cop1 = pow((((ch1_t11+ch1_t21+1)/(ch1_t31-ch1_t41))-1),-1)              ##The derived COPs at each of the steps
        ch1_cop2 = pow((((ch1_t12+ch1_t22+1)/(ch1_t32-ch1_t42))-1),-1)
        ch1_cop3 = pow((((ch1_t13+ch1_t23+1)/(ch1_t33-ch1_t43))-1),-1)
        ch1_cop4 = pow((((ch1_t14+ch1_t24+1)/(ch1_t34-ch1_t44))-1),-1)
    
        ch1_enode1 = 0.25*ch1_maxqe/ch1_cop1                                        ##The end nodes of the piecewise linear segments (electricity vs Qe)
        ch1_enode2 = 0.5*ch1_maxqe/ch1_cop2
        ch1_enode3 = 0.75*ch1_maxqe/ch1_cop3
        ch1_enode4 = ch1_maxqe/ch1_cop4
        
        ch1_grad1 = ch1_enode1/0.25                                                 ##The gradients of the piecewise linear segments 
        ch1_grad2 = (ch1_enode2-ch1_enode1)/(0.5-0.25)
        ch1_grad3 = (ch1_enode3-ch1_enode2)/(0.75-0.5)
        ch1_grad4 = (ch1_enode4-ch1_enode3)/(1-0.75)
    
        ch1_int1 = 0                                                                ##The y-axis intercepts of the piecewise linear segments 
        ch1_int2 = ch1_enode2-(ch1_grad2*0.5)
        ch1_int3 = ch1_enode3-(ch1_grad3*0.75)
        ch1_int4 = ch1_enode4-(ch1_grad4*1)
    
        ch1_emax1 = 1*ch1_grad1 + ch1_int1                                          ##The maximum points of each piecewise linear segments, this is needed for percentage use 
        ch1_emax2 = 1*ch1_grad2 + ch1_int2
        ch1_emax3 = 1*ch1_grad3 + ch1_int3
        ch1_emax4 = 1*ch1_grad4 + ch1_int4
        
        ch1_eratio = ch1_dc[0,0]/ch1_dc[9,0]
        ch1_cratio = ch1_dc[2,0]/ch1_dc[10,0]
        
        ##Initialize matrix to hold return values 
        
        ch1_dc_calc =np.zeros((17,1))
        
        ch1_dc_calc[0,0] = ch1_int1
        ch1_dc_calc[1,0] = ch1_int2
        ch1_dc_calc[2,0] = ch1_int3
        ch1_dc_calc[3,0] = ch1_int4
        ch1_dc_calc[4,0] = ch1_emax1-ch1_int1
        ch1_dc_calc[5,0] = ch1_emax2-ch1_int2
        ch1_dc_calc[6,0] = ch1_emax3-ch1_int3
        ch1_dc_calc[7,0] = ch1_emax4-ch1_int4
        ch1_dc_calc[8,0] = ch1_dt_maxcap
        ch1_dc_calc[9,0] = ch1_eratio
        ch1_dc_calc[10,0] = ch1_cratio
        ch1_dc_calc[11,0] = ch1_dtcond_fmax
        ch1_dc_calc[12,0] = 0
        ch1_dc_calc[13,0] = 0.25
        ch1_dc_calc[14,0] = 0.5
        ch1_dc_calc[15,0] = 0.75
        ch1_dc_calc[16,0] = 1
        
        return ch1_dc_calc
    
    else:
        ch1_dc_calc =np.zeros((17,1))
        
        return ch1_dc_calc
