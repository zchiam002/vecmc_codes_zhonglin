#This is the compute file 

def chiller2_compute (ch2_dc):
    
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
    
    ##ch2_dc    - list of input values
    ##ch2_dc[0,0] = chiller2['ch2_evaptret']['value']
    ##ch2_dc[1,0] = chiller2['ch2_condtin']['value']
    ##ch2_dc[2,0] = chiller2['ch2_rated_cap']['value']
    ##ch2_dc[3,0] = chiller2['ch2_b0']['value']    
    ##ch2_dc[4,0] = chiller2['ch2_b1']['value']
    ##ch2_dc[5,0] = chiller2['ch2_b2']['value']
    ##ch2_dc[6,0] = chiller2['ch2_qc_coeff']['value']
    ##ch2_dc[7,0] = chiller2['ch2_totalenwkflow']['value']
    ##ch2_dc[8,0] = chiller2['ch2_totalcnwkflow']['value']
    
    ch2_qe1 = 0.001
    ch2_qe2 = 0.25 * ch2_dc[2,0]
    ch2_qe3 = 0.5 * ch2_dc[2,0]
    ch2_qe4 = 0.75 * ch2_dc[2,0]
    ch2_qe5 = 1 * ch2_dc[2,0]

    ch2_cop1, ch2_qc1 = gnu_chiller(ch2_dc[3,0], ch2_dc[4,0], ch2_dc[5,0], ch2_dc[6,0], ch2_dc[0,0], ch2_dc[1,0], ch2_qe1)
    ch2_cop2, ch2_qc2 = gnu_chiller(ch2_dc[3,0], ch2_dc[4,0], ch2_dc[5,0], ch2_dc[6,0], ch2_dc[0,0], ch2_dc[1,0], ch2_qe2)
    ch2_cop3, ch2_qc3 = gnu_chiller(ch2_dc[3,0], ch2_dc[4,0], ch2_dc[5,0], ch2_dc[6,0], ch2_dc[0,0], ch2_dc[1,0], ch2_qe3)
    ch2_cop4, ch2_qc4 = gnu_chiller(ch2_dc[3,0], ch2_dc[4,0], ch2_dc[5,0], ch2_dc[6,0], ch2_dc[0,0], ch2_dc[1,0], ch2_qe4)
    ch2_cop5, ch2_qc5 = gnu_chiller(ch2_dc[3,0], ch2_dc[4,0], ch2_dc[5,0], ch2_dc[6,0], ch2_dc[0,0], ch2_dc[1,0], ch2_qe5)
    
    ch2_e1 = ch2_qe1 / ch2_cop1
    ch2_e2 = ch2_qe2 / ch2_cop2
    ch2_e3 = ch2_qe3 / ch2_cop3
    ch2_e4 = ch2_qe4 / ch2_cop4
    ch2_e5 = ch2_qe5 / ch2_cop5

    ##Determining the gradients for the E vs Qe graph
    
    ch2_egrad1 = (ch2_e2 - ch2_e1) / (ch2_qe2 - ch2_qe1)
    ch2_egrad2 = (ch2_e3 - ch2_e2) / (ch2_qe3 - ch2_qe2)
    ch2_egrad3 = (ch2_e4 - ch2_e3) / (ch2_qe4 - ch2_qe3)
    ch2_egrad4 = (ch2_e5 - ch2_e4) / (ch2_qe5 - ch2_qe4)
    
    ch2_int1 = ch2_e2 - (0.25*ch2_dc[2,0])*ch2_egrad1    
    ch2_int2 = ch2_e3 - (0.5*ch2_dc[2,0])*ch2_egrad2               
    ch2_int3 = ch2_e4 - (0.75*ch2_dc[2,0])*ch2_egrad3               
    ch2_int4 = ch2_e5 - (1*ch2_dc[2,0])*ch2_egrad4
    
    ##Initiate a matrix to hold the return values 
    ch2_dc_calc =np.zeros((13,1))
    
    ch2_dc_calc[0,0] = ch2_int1
    ch2_dc_calc[1,0] = ch2_int2
    ch2_dc_calc[2,0] = ch2_int3
    ch2_dc_calc[3,0] = ch2_int4
    ch2_dc_calc[4,0] = ch2_egrad1
    ch2_dc_calc[5,0] = ch2_egrad2
    ch2_dc_calc[6,0] = ch2_egrad3
    ch2_dc_calc[7,0] = ch2_egrad4
    ch2_dc_calc[8,0] = 0
    ch2_dc_calc[9,0] = 0.25
    ch2_dc_calc[10,0] = 0.5
    ch2_dc_calc[11,0] = 0.75
    ch2_dc_calc[12,0] = 1
    
    return ch2_dc_calc   

    

