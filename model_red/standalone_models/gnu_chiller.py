##This is a standalone model for the chiller 

##Built on the Gordon-Ng chiller model. This model is able to capture the effects of temperature and part load on the chiller.
##This model was chosen due to extensive references to analytically established formulae 
##The original equation is as follows 
##(Tin_evap / Tin_cond)(1 + (1 / COP)) - 1 = b0(Tin_evap / Qe) + b1((Tin_cond - Tin_evap) / (Tin_cond * Qe)) + b2((Qe / Tin_cond) * (1 + (1 / COP)))

##Built as a function 
##The coefficients need to be determined outside the model using regression based methods
##The objective of the function is to return the COP of the chiller

##It is worth noting that typically the COP of the chillers depend heavily on the average temperature of the evaporator and condenser, hence this model may
##not be able to accurately capture the impact of too large evaporator and condenser delta-ts  

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
    
##Parameters for the smaller chiller 2000kWh
max_cap_1 = 2000
b0_1 = 0.123020043325872
b1_1 = 1044.79734873891
b2_1 = 0.0204660495029597
qc_coeff_1 = 1.09866273284186

##Variables 
Qe_1 = 2000
Tin_evap_1 = 7 + 273.15
Tin_cond_1 = 25 + 273.15

COP_1 , Qc_1 = gnu_chiller(b0_1, b1_1, b2_1, qc_coeff_1, Tin_evap_1, Tin_cond_1, Qe_1)
#print(COP_1, Qc_1)



##for the larger chiller 
max_cap_2 = 7330
b0_2 = 1.35049420632748
b1_2 = -134.853705222833
b2_2 = 0.00430128306723068
qc_coeff_2 = 1.10348067074030


