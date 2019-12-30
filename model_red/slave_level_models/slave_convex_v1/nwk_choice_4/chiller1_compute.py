#This is the compute file 

def chiller1_compute (ch1_dc):
    
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
    
    ##ch1_dc    - list of input values
    ##ch1_dc[0,0] = chiller1['ch1_evaptret']['value']
    ##ch1_dc[1,0] = chiller1['ch1_condtin']['value']
    ##ch1_dc[2,0] = chiller1['ch1_rated_cap']['value']
    ##ch1_dc[3,0] = chiller1['ch1_b0']['value']    
    ##ch1_dc[4,0] = chiller1['ch1_b1']['value']
    ##ch1_dc[5,0] = chiller1['ch1_b2']['value']
    ##ch1_dc[6,0] = chiller1['ch1_qc_coeff']['value']
    ##ch1_dc[7,0] = chiller1['ch1_totalenwkflow']['value']
    ##ch1_dc[8,0] = chiller1['ch1_totalcnwkflow']['value']
    
    ch1_qe1 = 0.001
    ch1_qe2 = 0.25 * ch1_dc[2,0]
    ch1_qe3 = 0.5 * ch1_dc[2,0]
    ch1_qe4 = 0.75 * ch1_dc[2,0]
    ch1_qe5 = 1 * ch1_dc[2,0]

    ch1_cop1, ch1_qc1 = gnu_chiller(ch1_dc[3,0], ch1_dc[4,0], ch1_dc[5,0], ch1_dc[6,0], ch1_dc[0,0], ch1_dc[1,0], ch1_qe1)
    ch1_cop2, ch1_qc2 = gnu_chiller(ch1_dc[3,0], ch1_dc[4,0], ch1_dc[5,0], ch1_dc[6,0], ch1_dc[0,0], ch1_dc[1,0], ch1_qe2)
    ch1_cop3, ch1_qc3 = gnu_chiller(ch1_dc[3,0], ch1_dc[4,0], ch1_dc[5,0], ch1_dc[6,0], ch1_dc[0,0], ch1_dc[1,0], ch1_qe3)
    ch1_cop4, ch1_qc4 = gnu_chiller(ch1_dc[3,0], ch1_dc[4,0], ch1_dc[5,0], ch1_dc[6,0], ch1_dc[0,0], ch1_dc[1,0], ch1_qe4)
    ch1_cop5, ch1_qc5 = gnu_chiller(ch1_dc[3,0], ch1_dc[4,0], ch1_dc[5,0], ch1_dc[6,0], ch1_dc[0,0], ch1_dc[1,0], ch1_qe5)
    
    ch1_e1 = ch1_qe1 / ch1_cop1
    ch1_e2 = ch1_qe2 / ch1_cop2
    ch1_e3 = ch1_qe3 / ch1_cop3
    ch1_e4 = ch1_qe4 / ch1_cop4
    ch1_e5 = ch1_qe5 / ch1_cop5

    ##Determining the gradients for the E vs Qe graph
    
    ch1_egrad1 = (ch1_e2 - ch1_e1) / (ch1_qe2 - ch1_qe1)
    ch1_egrad2 = (ch1_e3 - ch1_e2) / (ch1_qe3 - ch1_qe2)
    ch1_egrad3 = (ch1_e4 - ch1_e3) / (ch1_qe4 - ch1_qe3)
    ch1_egrad4 = (ch1_e5 - ch1_e4) / (ch1_qe5 - ch1_qe4)
    
    ch1_int1 = ch1_e2 - (0.25*ch1_dc[2,0])*ch1_egrad1   
    ch1_int2 = ch1_e3 - (0.5*ch1_dc[2,0])*ch1_egrad2               
    ch1_int3 = ch1_e4 - (0.75*ch1_dc[2,0])*ch1_egrad3               
    ch1_int4 = ch1_e5 - (1*ch1_dc[2,0])*ch1_egrad4
    
    ##Initiate a matrix to hold the return values 
    ch1_dc_calc =np.zeros((13,1))
    
    ch1_dc_calc[0,0] = ch1_int1
    ch1_dc_calc[1,0] = ch1_int2
    ch1_dc_calc[2,0] = ch1_int3
    ch1_dc_calc[3,0] = ch1_int4
    ch1_dc_calc[4,0] = ch1_egrad1
    ch1_dc_calc[5,0] = ch1_egrad2
    ch1_dc_calc[6,0] = ch1_egrad3
    ch1_dc_calc[7,0] = ch1_egrad4
    ch1_dc_calc[8,0] = 0
    ch1_dc_calc[9,0] = 0.25
    ch1_dc_calc[10,0] = 0.5
    ch1_dc_calc[11,0] = 0.75
    ch1_dc_calc[12,0] = 1
    
    return ch1_dc_calc   

    
