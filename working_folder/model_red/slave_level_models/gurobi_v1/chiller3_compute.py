#This is the compute file 

def chiller3_compute (ch3_dc):
    
    ##Function to calculate the COP of the chiller using GNU method 
    
    def gnu_chiller (b0, b1, b2, qc_coeff, Tin_evap, Tin_cond, Qe):
    
        ##b0, b1, b2    --- regression derived coefficients 
        ##qc_coeff      --- not condenser heat rejection coefficient 
        ##Tin_evap      --- the chilled water return temperature to the chiller (K)
        ##Tin_cond      --- water temperature of the water entering the condenser (K)
        ##Qe            --- the cooling load which the chiller is subjected to (kWh)
  
        a_1 = (b0 * Tin_evap) / Qe
        a_2 = b1 * ((Tin_cond - Tin_evap) / (Tin_cond * Qe))
        a_3 = Tin_evap / Tin_cond
        a_4 = (b2 * Qe) / Tin_cond
    
        temp = (((a_1 + a_2 + 1) / (a_3 - a_4)) - 1)
        COP = pow(temp, -1)
    
        Qc = qc_coeff * Qe
    
        return COP, Qc
     
    import numpy as np
    
    ##ch3_dc    - list of input values
    ##ch3_dc[0,0] = chiller3['ch3_evaptret']['value']
    ##ch3_dc[1,0] = chiller3['ch3_condtin']['value']
    ##ch3_dc[2,0] = chiller3['ch3_rated_cap']['value']
    ##ch3_dc[3,0] = chiller3['ch3_b0']['value']    
    ##ch3_dc[4,0] = chiller3['ch3_b1']['value']
    ##ch3_dc[5,0] = chiller3['ch3_b2']['value']
    ##ch3_dc[6,0] = chiller3['ch3_qc_coeff']['value']
    ##ch3_dc[7,0] = chiller3['ch3_totalenwkflow']['value']
    ##ch3_dc[8,0] = chiller3['ch3_totalcnwkflow']['value']
    
    ch3_qe1 = 0.001
    ch3_qe2 = 0.25 * ch3_dc[2,0]
    ch3_qe3 = 0.5 * ch3_dc[2,0]
    ch3_qe4 = 0.75 * ch3_dc[2,0]
    ch3_qe5 = 1 * ch3_dc[2,0]

    ch3_cop1, ch3_qc1 = gnu_chiller(ch3_dc[3,0], ch3_dc[4,0], ch3_dc[5,0], ch3_dc[6,0], ch3_dc[0,0], ch3_dc[1,0], ch3_qe1)
    ch3_cop2, ch3_qc2 = gnu_chiller(ch3_dc[3,0], ch3_dc[4,0], ch3_dc[5,0], ch3_dc[6,0], ch3_dc[0,0], ch3_dc[1,0], ch3_qe2)
    ch3_cop3, ch3_qc3 = gnu_chiller(ch3_dc[3,0], ch3_dc[4,0], ch3_dc[5,0], ch3_dc[6,0], ch3_dc[0,0], ch3_dc[1,0], ch3_qe3)
    ch3_cop4, ch3_qc4 = gnu_chiller(ch3_dc[3,0], ch3_dc[4,0], ch3_dc[5,0], ch3_dc[6,0], ch3_dc[0,0], ch3_dc[1,0], ch3_qe4)
    ch3_cop5, ch3_qc5 = gnu_chiller(ch3_dc[3,0], ch3_dc[4,0], ch3_dc[5,0], ch3_dc[6,0], ch3_dc[0,0], ch3_dc[1,0], ch3_qe5)
    
    ch3_e1 = ch3_qe1 / ch3_cop1
    ch3_e2 = ch3_qe2 / ch3_cop2
    ch3_e3 = ch3_qe3 / ch3_cop3
    ch3_e4 = ch3_qe4 / ch3_cop4
    ch3_e5 = ch3_qe5 / ch3_cop5

    ##Determining the gradients for the E vs Qe graph
    
    ch3_egrad1 = (ch3_e2 - ch3_e1) / (ch3_qe2 - ch3_qe1)
    ch3_egrad2 = (ch3_e3 - ch3_e2) / (ch3_qe3 - ch3_qe2)
    ch3_egrad3 = (ch3_e4 - ch3_e3) / (ch3_qe4 - ch3_qe3)
    ch3_egrad4 = (ch3_e5 - ch3_e4) / (ch3_qe5 - ch3_qe4)
    
    ch3_int1 = ch3_e3 - (0.25*ch3_dc[2,0])*ch3_egrad1  
    ch3_int2 = ch3_e3 - (0.5*ch3_dc[2,0])*ch3_egrad2               
    ch3_int3 = ch3_e4 - (0.75*ch3_dc[2,0])*ch3_egrad3               
    ch3_int4 = ch3_e5 - (1*ch3_dc[2,0])*ch3_egrad4
    
    ##Initiate a matrix to hold the return values 
    ch3_dc_calc =np.zeros((13,1))
    
    ch3_dc_calc[0,0] = ch3_int1
    ch3_dc_calc[1,0] = ch3_int2
    ch3_dc_calc[2,0] = ch3_int3
    ch3_dc_calc[3,0] = ch3_int4
    ch3_dc_calc[4,0] = ch3_egrad1
    ch3_dc_calc[5,0] = ch3_egrad2
    ch3_dc_calc[6,0] = ch3_egrad3
    ch3_dc_calc[7,0] = ch3_egrad4
    ch3_dc_calc[8,0] = 0
    ch3_dc_calc[9,0] = 0.25
    ch3_dc_calc[10,0] = 0.5
    ch3_dc_calc[11,0] = 0.75
    ch3_dc_calc[12,0] = 1
    
    return ch3_dc_calc   

    

