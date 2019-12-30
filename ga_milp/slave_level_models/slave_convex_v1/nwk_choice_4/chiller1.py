## This is a chiller model, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type


def chiller1 (ch1_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    from nwk_choice_4.chiller1_compute import chiller1_compute
    import pandas as pd
    import numpy as np
    
    
    ##Model description: 
    ##Built based on Gordon-Ng's Universal Chiller model
    ##The COP is kept constant at 4 predefined steps in equally spaced intervals 
    ##The inputs to this function are variables to the eyes of the Master optimizer 
    
    ##Legend of input variables 
    
    ##ch1_etret       - evaporator return temperature (K)
    ##ch1_ctin        - condenser inlet temperature (K)
    ##ch1_tenwkflow   - total flowrate through parallel systems (m3/h)
    ##ch1_tcnwkflow   - total flowrate through parallel systems (m3/h)
    
    ##Processing list of master decision variables as parameters
    ch1_etret = ch1_mdv['Value'][0]
    ch1_ctin = ch1_mdv['Value'][1]
    ch1_tenwkflow = ch1_mdv['Value'][2]                    ##Total flowrate through all evaporators of all chillers 
    ch1_tcnwkflow = ch1_mdv['Value'][3]                    ##Total flowrate through all condensers of all chillers 

    ##Define dictionary of values 

    chiller1 = {}
    ##Input constants 

    ##1
    ch1_evaptret = {}
    ch1_evaptret['value'] = ch1_etret
    ch1_evaptret['units'] = 'K'
    ch1_evaptret['status'] = 'cst_input'
    chiller1['ch1_evaptret'] = ch1_evaptret

    ##2
    ch1_condtin = {}
    ch1_condtin['value'] = ch1_ctin
    ch1_condtin['units'] = 'K'
    ch1_condtin['status'] = 'cst_input'
    chiller1['ch1_condtin'] = ch1_condtin

    ##3
    ch1_totalenwkflow = {}
    ch1_totalenwkflow['value'] = ch1_tenwkflow
    ch1_totalenwkflow['units'] = 'm3/h'
    ch1_totalenwkflow['status'] = 'cst_input'
    chiller1['ch1_totalenwkflow'] = ch1_totalenwkflow

    ##4
    ch1_totalcnwkflow = {}
    ch1_totalcnwkflow['value'] = ch1_tcnwkflow
    ch1_totalcnwkflow['units'] = 'm3/h'
    ch1_totalcnwkflow['status'] = 'cst_input'
    chiller1['ch1_totalcnwkflow'] = ch1_totalcnwkflow

    ##Defined constants
    
    ##5
    ch1_rated_cap = {}                              #The rated capacity of the chiller
    ch1_rated_cap['value'] = 2000
    ch1_rated_cap['units'] = 'kWh'
    ch1_rated_cap['status'] = 'cst'
    chiller1['ch1_rated_cap'] = ch1_rated_cap
    
    ##6
    ch1_b0 = {}
    ch1_b0['value'] =  0.123020043325872            #Regression-derived constants
    ch1_b0['units'] = '-'
    ch1_b0['status'] = 'cst'
    chiller1['ch1_b0'] = ch1_b0

    ##7    
    ch1_b1 = {}
    ch1_b1['value'] =  1044.79734873891            
    ch1_b1['units'] = '-'
    ch1_b1['status'] = 'cst'
    chiller1['ch1_b1'] = ch1_b1
    
    ##8
    ch1_b2 = {}
    ch1_b2['value'] =  0.0204660495029597            
    ch1_b2['units'] = '-'
    ch1_b2['status'] = 'cst'
    chiller1['ch1_b2'] = ch1_b2

    ##9
    ch1_qc_coeff = {}
    ch1_qc_coeff['value'] = 1.09866273284186        #The relationship between Qe and Qc
    ch1_qc_coeff['units'] = '-'
    ch1_qc_coeff['status'] = 'cst'
    chiller1['ch1_qc_coeff'] = ch1_qc_coeff

    ##10
    ch1_cp = {}
    ch1_cp['value'] = 4.2
    ch1_cp['units'] = 'kJ'
    ch1_cp['status'] = 'cst'
    chiller1['ch1_cp'] = ch1_cp 

    ##Dependent constants
    ch1_dc = np.zeros((9,1))                       #Initialize the list, note the number of constants
    
    ch1_dc[0,0] = chiller1['ch1_evaptret']['value']
    ch1_dc[1,0] = chiller1['ch1_condtin']['value']
    ch1_dc[2,0] = chiller1['ch1_rated_cap']['value']
    ch1_dc[3,0] = chiller1['ch1_b0']['value']    
    ch1_dc[4,0] = chiller1['ch1_b1']['value']
    ch1_dc[5,0] = chiller1['ch1_b2']['value']
    ch1_dc[6,0] = chiller1['ch1_qc_coeff']['value']
    ch1_dc[7,0] = chiller1['ch1_totalenwkflow']['value']
    ch1_dc[8,0] = chiller1['ch1_totalcnwkflow']['value']

    ch1_dc_calc = chiller1_compute(ch1_dc)
    
    ##11
    ch1_int1 = {}
    ch1_int1['value'] = ch1_dc_calc[0,0]            #Intercpets of step-wise linearity
    ch1_int1['units'] = '-'
    ch1_int1['status'] = 'calc'
    chiller1['ch1_int1'] = ch1_int1

    ##12
    ch1_int2 = {}
    ch1_int2['value'] = ch1_dc_calc[1,0]
    ch1_int2['units'] = '-'
    ch1_int2['status'] = 'calc'
    chiller1['ch1_int2'] = ch1_int2

    ##13
    ch1_int3 = {}
    ch1_int3['value'] = ch1_dc_calc[2,0]
    ch1_int3['units'] = '-'
    ch1_int3['status'] = 'calc'
    chiller1['ch1_int3'] = ch1_int3

    ##14
    ch1_int4 = {}
    ch1_int4['value'] = ch1_dc_calc[3,0]
    ch1_int4['units'] = '-'
    ch1_int4['status'] = 'calc'
    chiller1['ch1_int4'] = ch1_int4

    ##15
    ch1_egrad1 = {}
    ch1_egrad1['value'] = ch1_dc_calc[4,0]
    ch1_egrad1['units'] = '-'
    ch1_egrad1['status'] = 'calc'
    chiller1['ch1_egrad1'] = ch1_egrad1

    ##16
    ch1_egrad2 = {}
    ch1_egrad2['value'] = ch1_dc_calc[5,0]
    ch1_egrad2['units'] = '-'
    ch1_egrad2['status'] = 'calc'
    chiller1['ch1_egrad2'] = ch1_egrad2  

    ##17
    ch1_egrad3 = {}
    ch1_egrad3['value'] = ch1_dc_calc[6,0]
    ch1_egrad3['units'] = '-'
    ch1_egrad3['status'] = 'calc'
    chiller1['ch1_egrad3'] = ch1_egrad3

    ##18
    ch1_egrad4 = {}
    ch1_egrad4['value'] = ch1_dc_calc[7,0]
    ch1_egrad4['units'] = '-'
    ch1_egrad4['status'] = 'calc'
    chiller1['ch1_egrad4'] = ch1_egrad4 
    
    ##19
    ch1_f1 = {}
    ch1_f1['value'] = ch1_dc_calc[8,0]
    ch1_f1['units'] = '-'
    ch1_f1['status'] = 'calc'
    chiller1['ch1_f1'] = ch1_f1  
    
    ##20
    ch1_f2 = {}
    ch1_f2['value'] = ch1_dc_calc[9,0]
    ch1_f2['units'] = '-'
    ch1_f2['status'] = 'calc'
    chiller1['ch1_f2'] = ch1_f2  
    
    ##21
    ch1_f3 = {}
    ch1_f3['value'] = ch1_dc_calc[10,0]
    ch1_f3['units'] = '-'
    ch1_f3['status'] = 'calc'
    chiller1['ch1_f3'] = ch1_f3
    
    ##22
    ch1_f4 = {}
    ch1_f4['value'] = ch1_dc_calc[11,0]
    ch1_f4['units'] = '-'
    ch1_f4['status'] = 'calc'
    chiller1['ch1_f4'] = ch1_f4
    
    ##23
    ch1_f5 = {}
    ch1_f5['value'] = ch1_dc_calc[12,0]
    ch1_f5['units'] = '-'
    ch1_f5['status'] = 'calc'
    chiller1['ch1_f5'] = ch1_f5

    ##Unit definition 
    
    ##Unit 1
    ch1_1_e = {}
    ch1_1_e['Name'] = 'ch1_1_evap'
    ch1_1_e['Variable1'] = 'm_perc'                                                                                                           ##Percentage of flowrate from the entire evaporator network 
    ch1_1_e['Variable2'] = 't_out'                                                                                                            ##Chilled water setpoint temperature 
    ch1_1_e['Fmin_v1'] = 0 
    ch1_1_e['Fmax_v1'] = 1                                                                                                                    ##Maximum percentage is 100% 
    ch1_1_e['Fmin_v2'] = 273.15 + 1                                                                                                           ##The minimum supply temperature of the chiller is 1 deg 
    ch1_1_e['Fmax_v2'] = chiller1['ch1_evaptret']['value']                                                                                    ##The maximum supply temperature of the chiller is that of the return temperature
    ch1_1_e['Coeff_v1_2'] = 0                                                                                                                 ##This illustrates the relationship between the variables  
    ch1_1_e['Coeff_v1_1'] = chiller1['ch1_totalenwkflow']['value'] * chiller1['ch1_cp']['value'] * chiller1['ch1_evaptret']['value']          ##The relationship is Qe = m_evap_perc*m_total*Cp*Tevap_in - m_evap_perc*m_total*Cp*Tevap_out
    ch1_1_e['Coeff_v2_2'] = 0
    ch1_1_e['Coeff_v2_1'] = 0
    ch1_1_e['Coeff_v1_v2'] = -chiller1['ch1_totalenwkflow']['value'] * chiller1['ch1_cp']['value'] 
    ch1_1_e['Coeff_cst'] = 0
    ch1_1_e['Fmin'] = chiller1['ch1_f1']['value'] * chiller1['ch1_rated_cap']['value']
    ch1_1_e['Fmax'] = chiller1['ch1_f2']['value'] * chiller1['ch1_rated_cap']['value']
    ch1_1_e['Cost_v1_2'] = 0
    ch1_1_e['Cost_v1_1'] = 0
    ch1_1_e['Cost_v2_2'] = 0
    ch1_1_e['Cost_v2_1'] = 0
    ch1_1_e['Cost_v1_v2'] = 0
    ch1_1_e['Cost_cst'] = 0
    ch1_1_e['Cinv_v1_2'] = 0
    ch1_1_e['Cinv_v1_1'] = 0
    ch1_1_e['Cinv_v2_2'] = 0
    ch1_1_e['Cinv_v2_1'] = 0
    ch1_1_e['Cinv_v1_v2'] = 0
    ch1_1_e['Cinv_cst'] = 0
    ch1_1_e['Power_v1_2'] = 0
    ch1_1_e['Power_v1_1'] = 0
    ch1_1_e['Power_v2_2'] = 0
    ch1_1_e['Power_v2_1'] = 0
    ch1_1_e['Power_v1_v2'] = chiller1['ch1_egrad1']['value']
    ch1_1_e['Power_cst'] = chiller1['ch1_int1']['value']
    ch1_1_e['Impact_v1_2'] = 0
    ch1_1_e['Impact_v1_1'] = 0
    ch1_1_e['Impact_v2_2'] = 0
    ch1_1_e['Impact_v2_1'] = 0
    ch1_1_e['Impact_v1_v2'] = 0
    ch1_1_e['Impact_cst'] = 0

    unitinput = [ch1_1_e['Name'], ch1_1_e['Variable1'], ch1_1_e['Variable2'], ch1_1_e['Fmin_v1'], ch1_1_e['Fmax_v1'], ch1_1_e['Fmin_v2'], ch1_1_e['Fmax_v2'], ch1_1_e['Coeff_v1_2'], 
                ch1_1_e['Coeff_v1_1'], ch1_1_e['Coeff_v2_2'], ch1_1_e['Coeff_v2_1'], ch1_1_e['Coeff_v1_v2'], ch1_1_e['Coeff_cst'], ch1_1_e['Fmin'], ch1_1_e['Fmax'], ch1_1_e['Cost_v1_2'], 
                ch1_1_e['Cost_v1_1'], ch1_1_e['Cost_v2_2'], ch1_1_e['Cost_v2_1'], ch1_1_e['Cost_v1_v2'], ch1_1_e['Cost_cst'], ch1_1_e['Cinv_v1_2'], ch1_1_e['Cinv_v1_1'], ch1_1_e['Cinv_v2_2'], 
                ch1_1_e['Cinv_v2_1'], ch1_1_e['Cinv_v1_v2'], ch1_1_e['Cinv_cst'], ch1_1_e['Power_v1_2'], ch1_1_e['Power_v1_1'], ch1_1_e['Power_v2_2'], ch1_1_e['Power_v2_1'], 
                ch1_1_e['Power_v1_v2'], ch1_1_e['Power_cst'], ch1_1_e['Impact_v1_2'], ch1_1_e['Impact_v1_1'], ch1_1_e['Impact_v2_2'], ch1_1_e['Impact_v2_1'], ch1_1_e['Impact_v1_v2'], 
                ch1_1_e['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Unit 2
    ch1_1_c = {}
    ch1_1_c['Name'] = 'ch1_1_cond'
    ch1_1_c['Variable1'] = 'm_perc'                                                                                                           ##Percentage of flowrate from the entire condenser network 
    ch1_1_c['Variable2'] = 't_out'                                                                                                            ##Condenser water setpoint temperature 
    ch1_1_c['Fmin_v1'] = 0 
    ch1_1_c['Fmax_v1'] = 1                                                                                                                    ##Maximum percentage is 100% 
    ch1_1_c['Fmin_v2'] = chiller1['ch1_condtin']['value'] + 1                                                                                          ##The minimum condenser exit temperature is 1 deg above entry temperature 
    ch1_1_c['Fmax_v2'] = chiller1['ch1_condtin']['value'] + 10                                                                                         ##The maximum condenser exit temperature is 10 degrees above entry temperature
    ch1_1_c['Coeff_v1_2'] = 0                                                                                                                 ##This illustrates the relationship between the variables  
    ch1_1_c['Coeff_v1_1'] = -chiller1['ch1_totalcnwkflow']['value'] * chiller1['ch1_cp']['value'] * chiller1['ch1_condtin']['value']          ##The relationship is Qc = m_cond_perc*m_total*Cp*Tcond_in - m_cond_perc*m_total*Cp*Tcond_out
    ch1_1_c['Coeff_v2_2'] = 0
    ch1_1_c['Coeff_v2_1'] = 0
    ch1_1_c['Coeff_v1_v2'] = chiller1['ch1_totalcnwkflow']['value'] * chiller1['ch1_cp']['value'] 
    ch1_1_c['Coeff_cst'] = 0
    ch1_1_c['Fmin'] = chiller1['ch1_f1']['value'] * chiller1['ch1_rated_cap']['value'] * chiller1['ch1_qc_coeff']['value']
    ch1_1_c['Fmax'] = chiller1['ch1_f2']['value'] * chiller1['ch1_rated_cap']['value'] * chiller1['ch1_qc_coeff']['value']
    ch1_1_c['Cost_v1_2'] = 0
    ch1_1_c['Cost_v1_1'] = 0
    ch1_1_c['Cost_v2_2'] = 0
    ch1_1_c['Cost_v2_1'] = 0
    ch1_1_c['Cost_v1_v2'] = 0
    ch1_1_c['Cost_cst'] = 0
    ch1_1_c['Cinv_v1_2'] = 0
    ch1_1_c['Cinv_v1_1'] = 0
    ch1_1_c['Cinv_v2_2'] = 0
    ch1_1_c['Cinv_v2_1'] = 0
    ch1_1_c['Cinv_v1_v2'] = 0
    ch1_1_c['Cinv_cst'] = 0
    ch1_1_c['Power_v1_2'] = 0
    ch1_1_c['Power_v1_1'] = 0
    ch1_1_c['Power_v2_2'] = 0
    ch1_1_c['Power_v2_1'] = 0
    ch1_1_c['Power_v1_v2'] = 0                                                                                                                ##Already accounted for in the evaporator unit
    ch1_1_c['Power_cst'] = 0
    ch1_1_c['Impact_v1_2'] = 0
    ch1_1_c['Impact_v1_1'] = 0
    ch1_1_c['Impact_v2_2'] = 0
    ch1_1_c['Impact_v2_1'] = 0
    ch1_1_c['Impact_v1_v2'] = 0
    ch1_1_c['Impact_cst'] = 0

    unitinput = [ch1_1_c['Name'], ch1_1_c['Variable1'], ch1_1_c['Variable2'], ch1_1_c['Fmin_v1'], ch1_1_c['Fmax_v1'], ch1_1_c['Fmin_v2'], ch1_1_c['Fmax_v2'], ch1_1_c['Coeff_v1_2'], 
                ch1_1_c['Coeff_v1_1'], ch1_1_c['Coeff_v2_2'], ch1_1_c['Coeff_v2_1'], ch1_1_c['Coeff_v1_v2'], ch1_1_c['Coeff_cst'], ch1_1_c['Fmin'], ch1_1_c['Fmax'], ch1_1_c['Cost_v1_2'], 
                ch1_1_c['Cost_v1_1'], ch1_1_c['Cost_v2_2'], ch1_1_c['Cost_v2_1'], ch1_1_c['Cost_v1_v2'], ch1_1_c['Cost_cst'], ch1_1_c['Cinv_v1_2'], ch1_1_c['Cinv_v1_1'], ch1_1_c['Cinv_v2_2'], 
                ch1_1_c['Cinv_v2_1'], ch1_1_c['Cinv_v1_v2'], ch1_1_c['Cinv_cst'], ch1_1_c['Power_v1_2'], ch1_1_c['Power_v1_1'], ch1_1_c['Power_v2_2'], ch1_1_c['Power_v2_1'], 
                ch1_1_c['Power_v1_v2'], ch1_1_c['Power_cst'], ch1_1_c['Impact_v1_2'], ch1_1_c['Impact_v1_1'], ch1_1_c['Impact_v2_2'], ch1_1_c['Impact_v2_1'], ch1_1_c['Impact_v1_v2'], 
                ch1_1_c['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Unit 3
    ch1_2_e = {}
    ch1_2_e['Name'] = 'ch1_2_evap'
    ch1_2_e['Variable1'] = 'm_perc'                                                                                                           ##Percentage of flowrate from the entire evaporator network 
    ch1_2_e['Variable2'] = 't_out'                                                                                                            ##Chilled water setpoint temperature 
    ch1_2_e['Fmin_v1'] = 0 
    ch1_2_e['Fmax_v1'] = 1                                                                                                                    ##Maximum percentage is 100% 
    ch1_2_e['Fmin_v2'] = 273.15 + 1                                                                                                           ##The minimum supply temperature of the chiller is 1 deg 
    ch1_2_e['Fmax_v2'] = chiller1['ch1_evaptret']['value']                                                                                    ##The maximum supply temperature of the chiller is that of the return temperature
    ch1_2_e['Coeff_v1_2'] = 0                                                                                                                 ##This illustrates the relationship between the variables  
    ch1_2_e['Coeff_v1_1'] = chiller1['ch1_totalenwkflow']['value'] * chiller1['ch1_cp']['value'] * chiller1['ch1_evaptret']['value']          ##The relationship is Qe = m_evap_perc*m_total*Cp*Tevap_in - m_evap_perc*m_total*Cp*Tevap_out
    ch1_2_e['Coeff_v2_2'] = 0
    ch1_2_e['Coeff_v2_1'] = 0
    ch1_2_e['Coeff_v1_v2'] = -chiller1['ch1_totalenwkflow']['value'] * chiller1['ch1_cp']['value'] 
    ch1_2_e['Coeff_cst'] = 0
    ch1_2_e['Fmin'] = chiller1['ch1_f2']['value'] * chiller1['ch1_rated_cap']['value']
    ch1_2_e['Fmax'] = chiller1['ch1_f3']['value'] * chiller1['ch1_rated_cap']['value']
    ch1_2_e['Cost_v1_2'] = 0
    ch1_2_e['Cost_v1_1'] = 0
    ch1_2_e['Cost_v2_2'] = 0
    ch1_2_e['Cost_v2_1'] = 0
    ch1_2_e['Cost_v1_v2'] = 0
    ch1_2_e['Cost_cst'] = 0
    ch1_2_e['Cinv_v1_2'] = 0
    ch1_2_e['Cinv_v1_1'] = 0
    ch1_2_e['Cinv_v2_2'] = 0
    ch1_2_e['Cinv_v2_1'] = 0
    ch1_2_e['Cinv_v1_v2'] = 0
    ch1_2_e['Cinv_cst'] = 0
    ch1_2_e['Power_v1_2'] = 0
    ch1_2_e['Power_v1_1'] = 0
    ch1_2_e['Power_v2_2'] = 0
    ch1_2_e['Power_v2_1'] = 0
    ch1_2_e['Power_v1_v2'] = chiller1['ch1_egrad2']['value']
    ch1_2_e['Power_cst'] = chiller1['ch1_int2']['value']
    ch1_2_e['Impact_v1_2'] = 0
    ch1_2_e['Impact_v1_1'] = 0
    ch1_2_e['Impact_v2_2'] = 0
    ch1_2_e['Impact_v2_1'] = 0
    ch1_2_e['Impact_v1_v2'] = 0
    ch1_2_e['Impact_cst'] = 0

    unitinput = [ch1_2_e['Name'], ch1_2_e['Variable1'], ch1_2_e['Variable2'], ch1_2_e['Fmin_v1'], ch1_2_e['Fmax_v1'], ch1_2_e['Fmin_v2'], ch1_2_e['Fmax_v2'], ch1_2_e['Coeff_v1_2'], 
                ch1_2_e['Coeff_v1_1'], ch1_2_e['Coeff_v2_2'], ch1_2_e['Coeff_v2_1'], ch1_2_e['Coeff_v1_v2'], ch1_2_e['Coeff_cst'], ch1_2_e['Fmin'], ch1_2_e['Fmax'], ch1_2_e['Cost_v1_2'], 
                ch1_2_e['Cost_v1_1'], ch1_2_e['Cost_v2_2'], ch1_2_e['Cost_v2_1'], ch1_2_e['Cost_v1_v2'], ch1_2_e['Cost_cst'], ch1_2_e['Cinv_v1_2'], ch1_2_e['Cinv_v1_1'], ch1_2_e['Cinv_v2_2'], 
                ch1_2_e['Cinv_v2_1'], ch1_2_e['Cinv_v1_v2'], ch1_2_e['Cinv_cst'], ch1_2_e['Power_v1_2'], ch1_2_e['Power_v1_1'], ch1_2_e['Power_v2_2'], ch1_2_e['Power_v2_1'], 
                ch1_2_e['Power_v1_v2'], ch1_2_e['Power_cst'], ch1_2_e['Impact_v1_2'], ch1_2_e['Impact_v1_1'], ch1_2_e['Impact_v2_2'], ch1_2_e['Impact_v2_1'], ch1_2_e['Impact_v1_v2'], 
                ch1_2_e['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Unit 4
    ch1_2_c = {}
    ch1_2_c['Name'] = 'ch1_2_cond'
    ch1_2_c['Variable1'] = 'm_perc'                                                                                                           ##Percentage of flowrate from the entire condenser network 
    ch1_2_c['Variable2'] = 't_out'                                                                                                            ##Condenser water setpoint temperature 
    ch1_2_c['Fmin_v1'] = 0 
    ch1_2_c['Fmax_v1'] = 1                                                                                                                    ##Maximum percentage is 100% 
    ch1_2_c['Fmin_v2'] = chiller1['ch1_condtin']['value'] + 1                                                                                 ##The minimum condenser exit temperature is 1 deg above entry temperature 
    ch1_2_c['Fmax_v2'] = chiller1['ch1_condtin']['value'] + 10                                                                                ##The maximum condenser exit temperature is 10 degrees above entry temperature
    ch1_2_c['Coeff_v1_2'] = 0                                                                                                                 ##This illustrates the relationship between the variables  
    ch1_2_c['Coeff_v1_1'] = -chiller1['ch1_totalcnwkflow']['value'] * chiller1['ch1_cp']['value'] * chiller1['ch1_condtin']['value']          ##The relationship is Qc = m_cond_perc*m_total*Cp*Tcond_in - m_cond_perc*m_total*Cp*Tcond_out
    ch1_2_c['Coeff_v2_2'] = 0
    ch1_2_c['Coeff_v2_1'] = 0
    ch1_2_c['Coeff_v1_v2'] = chiller1['ch1_totalcnwkflow']['value'] * chiller1['ch1_cp']['value'] 
    ch1_2_c['Coeff_cst'] = 0
    ch1_2_c['Fmin'] = chiller1['ch1_f2']['value'] * chiller1['ch1_rated_cap']['value'] * chiller1['ch1_qc_coeff']['value']
    ch1_2_c['Fmax'] = chiller1['ch1_f3']['value'] * chiller1['ch1_rated_cap']['value'] * chiller1['ch1_qc_coeff']['value']
    ch1_2_c['Cost_v1_2'] = 0
    ch1_2_c['Cost_v1_1'] = 0
    ch1_2_c['Cost_v2_2'] = 0
    ch1_2_c['Cost_v2_1'] = 0
    ch1_2_c['Cost_v1_v2'] = 0
    ch1_2_c['Cost_cst'] = 0
    ch1_2_c['Cinv_v1_2'] = 0
    ch1_2_c['Cinv_v1_1'] = 0
    ch1_2_c['Cinv_v2_2'] = 0
    ch1_2_c['Cinv_v2_1'] = 0
    ch1_2_c['Cinv_v1_v2'] = 0
    ch1_2_c['Cinv_cst'] = 0
    ch1_2_c['Power_v1_2'] = 0
    ch1_2_c['Power_v1_1'] = 0
    ch1_2_c['Power_v2_2'] = 0
    ch1_2_c['Power_v2_1'] = 0
    ch1_2_c['Power_v1_v2'] = 0                                                                                                                ##Already accounted for in the evaporator unit
    ch1_2_c['Power_cst'] = 0
    ch1_2_c['Impact_v1_2'] = 0
    ch1_2_c['Impact_v1_1'] = 0
    ch1_2_c['Impact_v2_2'] = 0
    ch1_2_c['Impact_v2_1'] = 0
    ch1_2_c['Impact_v1_v2'] = 0
    ch1_2_c['Impact_cst'] = 0

    unitinput = [ch1_2_c['Name'], ch1_2_c['Variable1'], ch1_2_c['Variable2'], ch1_2_c['Fmin_v1'], ch1_2_c['Fmax_v1'], ch1_2_c['Fmin_v2'], ch1_2_c['Fmax_v2'], ch1_2_c['Coeff_v1_2'], 
                ch1_2_c['Coeff_v1_1'], ch1_2_c['Coeff_v2_2'], ch1_2_c['Coeff_v2_1'], ch1_2_c['Coeff_v1_v2'], ch1_2_c['Coeff_cst'], ch1_2_c['Fmin'], ch1_2_c['Fmax'], ch1_2_c['Cost_v1_2'], 
                ch1_2_c['Cost_v1_1'], ch1_2_c['Cost_v2_2'], ch1_2_c['Cost_v2_1'], ch1_2_c['Cost_v1_v2'], ch1_2_c['Cost_cst'], ch1_2_c['Cinv_v1_2'], ch1_2_c['Cinv_v1_1'], ch1_2_c['Cinv_v2_2'], 
                ch1_2_c['Cinv_v2_1'], ch1_2_c['Cinv_v1_v2'], ch1_2_c['Cinv_cst'], ch1_2_c['Power_v1_2'], ch1_2_c['Power_v1_1'], ch1_2_c['Power_v2_2'], ch1_2_c['Power_v2_1'], 
                ch1_2_c['Power_v1_v2'], ch1_2_c['Power_cst'], ch1_2_c['Impact_v1_2'], ch1_2_c['Impact_v1_1'], ch1_2_c['Impact_v2_2'], ch1_2_c['Impact_v2_1'], ch1_2_c['Impact_v1_v2'], 
                ch1_2_c['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Unit 5
    ch1_3_e = {}
    ch1_3_e['Name'] = 'ch1_3_evap'
    ch1_3_e['Variable1'] = 'm_perc'                                                                                                           ##Percentage of flowrate from the entire evaporator network 
    ch1_3_e['Variable2'] = 't_out'                                                                                                            ##Chilled water setpoint temperature 
    ch1_3_e['Fmin_v1'] = 0 
    ch1_3_e['Fmax_v1'] = 1                                                                                                                    ##Maximum percentage is 100% 
    ch1_3_e['Fmin_v2'] = 273.15 + 1                                                                                                           ##The minimum supply temperature of the chiller is 1 deg 
    ch1_3_e['Fmax_v2'] = chiller1['ch1_evaptret']['value']                                                                                    ##The maximum supply temperature of the chiller is that of the return temperature
    ch1_3_e['Coeff_v1_2'] = 0                                                                                                                 ##This illustrates the relationship between the variables  
    ch1_3_e['Coeff_v1_1'] = chiller1['ch1_totalenwkflow']['value'] * chiller1['ch1_cp']['value'] * chiller1['ch1_evaptret']['value']          ##The relationship is Qe = m_evap_perc*m_total*Cp*Tevap_in - m_evap_perc*m_total*Cp*Tevap_out
    ch1_3_e['Coeff_v2_2'] = 0
    ch1_3_e['Coeff_v2_1'] = 0
    ch1_3_e['Coeff_v1_v2'] = -chiller1['ch1_totalenwkflow']['value'] * chiller1['ch1_cp']['value'] 
    ch1_3_e['Coeff_cst'] = 0
    ch1_3_e['Fmin'] = chiller1['ch1_f3']['value'] * chiller1['ch1_rated_cap']['value']
    ch1_3_e['Fmax'] = chiller1['ch1_f4']['value'] * chiller1['ch1_rated_cap']['value']
    ch1_3_e['Cost_v1_2'] = 0
    ch1_3_e['Cost_v1_1'] = 0
    ch1_3_e['Cost_v2_2'] = 0
    ch1_3_e['Cost_v2_1'] = 0
    ch1_3_e['Cost_v1_v2'] = 0
    ch1_3_e['Cost_cst'] = 0
    ch1_3_e['Cinv_v1_2'] = 0
    ch1_3_e['Cinv_v1_1'] = 0
    ch1_3_e['Cinv_v2_2'] = 0
    ch1_3_e['Cinv_v2_1'] = 0
    ch1_3_e['Cinv_v1_v2'] = 0
    ch1_3_e['Cinv_cst'] = 0
    ch1_3_e['Power_v1_2'] = 0
    ch1_3_e['Power_v1_1'] = 0
    ch1_3_e['Power_v2_2'] = 0
    ch1_3_e['Power_v2_1'] = 0
    ch1_3_e['Power_v1_v2'] = chiller1['ch1_egrad3']['value']
    ch1_3_e['Power_cst'] = chiller1['ch1_int3']['value']
    ch1_3_e['Impact_v1_2'] = 0
    ch1_3_e['Impact_v1_1'] = 0
    ch1_3_e['Impact_v2_2'] = 0
    ch1_3_e['Impact_v2_1'] = 0
    ch1_3_e['Impact_v1_v2'] = 0
    ch1_3_e['Impact_cst'] = 0

    unitinput = [ch1_3_e['Name'], ch1_3_e['Variable1'], ch1_3_e['Variable2'], ch1_3_e['Fmin_v1'], ch1_3_e['Fmax_v1'], ch1_3_e['Fmin_v2'], ch1_3_e['Fmax_v2'], ch1_3_e['Coeff_v1_2'], 
                ch1_3_e['Coeff_v1_1'], ch1_3_e['Coeff_v2_2'], ch1_3_e['Coeff_v2_1'], ch1_3_e['Coeff_v1_v2'], ch1_3_e['Coeff_cst'], ch1_3_e['Fmin'], ch1_3_e['Fmax'], ch1_3_e['Cost_v1_2'], 
                ch1_3_e['Cost_v1_1'], ch1_3_e['Cost_v2_2'], ch1_3_e['Cost_v2_1'], ch1_3_e['Cost_v1_v2'], ch1_3_e['Cost_cst'], ch1_3_e['Cinv_v1_2'], ch1_3_e['Cinv_v1_1'], ch1_3_e['Cinv_v2_2'], 
                ch1_3_e['Cinv_v2_1'], ch1_3_e['Cinv_v1_v2'], ch1_3_e['Cinv_cst'], ch1_3_e['Power_v1_2'], ch1_3_e['Power_v1_1'], ch1_3_e['Power_v2_2'], ch1_3_e['Power_v2_1'], 
                ch1_3_e['Power_v1_v2'], ch1_3_e['Power_cst'], ch1_3_e['Impact_v1_2'], ch1_3_e['Impact_v1_1'], ch1_3_e['Impact_v2_2'], ch1_3_e['Impact_v2_1'], ch1_3_e['Impact_v1_v2'], 
                ch1_3_e['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Unit 6
    ch1_3_c = {}
    ch1_3_c['Name'] = 'ch1_3_cond'
    ch1_3_c['Variable1'] = 'm_perc'                                                                                                           ##Percentage of flowrate from the entire condenser network 
    ch1_3_c['Variable2'] = 't_out'                                                                                                            ##Condenser water setpoint temperature 
    ch1_3_c['Fmin_v1'] = 0 
    ch1_3_c['Fmax_v1'] = 1                                                                                                                    ##Maximum percentage is 100% 
    ch1_3_c['Fmin_v2'] = chiller1['ch1_condtin']['value'] + 1                                                                                 ##The minimum condenser exit temperature is 1 deg above entry temperature 
    ch1_3_c['Fmax_v2'] = chiller1['ch1_condtin']['value'] + 10                                                                                ##The maximum condenser exit temperature is 10 degrees above entry temperature
    ch1_3_c['Coeff_v1_2'] = 0                                                                                                                 ##This illustrates the relationship between the variables  
    ch1_3_c['Coeff_v1_1'] = -chiller1['ch1_totalcnwkflow']['value'] * chiller1['ch1_cp']['value'] * chiller1['ch1_condtin']['value']          ##The relationship is Qc = m_cond_perc*m_total*Cp*Tcond_in - m_cond_perc*m_total*Cp*Tcond_out
    ch1_3_c['Coeff_v2_2'] = 0
    ch1_3_c['Coeff_v2_1'] = 0
    ch1_3_c['Coeff_v1_v2'] = chiller1['ch1_totalcnwkflow']['value'] * chiller1['ch1_cp']['value'] 
    ch1_3_c['Coeff_cst'] = 0
    ch1_3_c['Fmin'] = chiller1['ch1_f3']['value'] * chiller1['ch1_rated_cap']['value'] * chiller1['ch1_qc_coeff']['value']
    ch1_3_c['Fmax'] = chiller1['ch1_f4']['value'] * chiller1['ch1_rated_cap']['value'] * chiller1['ch1_qc_coeff']['value']
    ch1_3_c['Cost_v1_2'] = 0
    ch1_3_c['Cost_v1_1'] = 0
    ch1_3_c['Cost_v2_2'] = 0
    ch1_3_c['Cost_v2_1'] = 0
    ch1_3_c['Cost_v1_v2'] = 0
    ch1_3_c['Cost_cst'] = 0
    ch1_3_c['Cinv_v1_2'] = 0
    ch1_3_c['Cinv_v1_1'] = 0
    ch1_3_c['Cinv_v2_2'] = 0
    ch1_3_c['Cinv_v2_1'] = 0
    ch1_3_c['Cinv_v1_v2'] = 0
    ch1_3_c['Cinv_cst'] = 0
    ch1_3_c['Power_v1_2'] = 0
    ch1_3_c['Power_v1_1'] = 0
    ch1_3_c['Power_v2_2'] = 0
    ch1_3_c['Power_v2_1'] = 0
    ch1_3_c['Power_v1_v2'] = 0                                                                                                                ##Already accounted for in the evaporator unit
    ch1_3_c['Power_cst'] = 0
    ch1_3_c['Impact_v1_2'] = 0
    ch1_3_c['Impact_v1_1'] = 0
    ch1_3_c['Impact_v2_2'] = 0
    ch1_3_c['Impact_v2_1'] = 0
    ch1_3_c['Impact_v1_v2'] = 0
    ch1_3_c['Impact_cst'] = 0

    unitinput = [ch1_3_c['Name'], ch1_3_c['Variable1'], ch1_3_c['Variable2'], ch1_3_c['Fmin_v1'], ch1_3_c['Fmax_v1'], ch1_3_c['Fmin_v2'], ch1_3_c['Fmax_v2'], ch1_3_c['Coeff_v1_2'], 
                ch1_3_c['Coeff_v1_1'], ch1_3_c['Coeff_v2_2'], ch1_3_c['Coeff_v2_1'], ch1_3_c['Coeff_v1_v2'], ch1_3_c['Coeff_cst'], ch1_3_c['Fmin'], ch1_3_c['Fmax'], ch1_3_c['Cost_v1_2'], 
                ch1_3_c['Cost_v1_1'], ch1_3_c['Cost_v2_2'], ch1_3_c['Cost_v2_1'], ch1_3_c['Cost_v1_v2'], ch1_3_c['Cost_cst'], ch1_3_c['Cinv_v1_2'], ch1_3_c['Cinv_v1_1'], ch1_3_c['Cinv_v2_2'], 
                ch1_3_c['Cinv_v2_1'], ch1_3_c['Cinv_v1_v2'], ch1_3_c['Cinv_cst'], ch1_3_c['Power_v1_2'], ch1_3_c['Power_v1_1'], ch1_3_c['Power_v2_2'], ch1_3_c['Power_v2_1'], 
                ch1_3_c['Power_v1_v2'], ch1_3_c['Power_cst'], ch1_3_c['Impact_v1_2'], ch1_3_c['Impact_v1_1'], ch1_3_c['Impact_v2_2'], ch1_3_c['Impact_v2_1'], ch1_3_c['Impact_v1_v2'], 
                ch1_3_c['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Unit 7
    ch1_4_e = {}
    ch1_4_e['Name'] = 'ch1_4_evap'
    ch1_4_e['Variable1'] = 'm_perc'                                                                                                           ##Percentage of flowrate from the entire evaporator network 
    ch1_4_e['Variable2'] = 't_out'                                                                                                            ##Chilled water setpoint temperature 
    ch1_4_e['Fmin_v1'] = 0 
    ch1_4_e['Fmax_v1'] = 1                                                                                                                    ##Maximum percentage is 100% 
    ch1_4_e['Fmin_v2'] = 273.15 + 1                                                                                                           ##The minimum supply temperature of the chiller is 1 deg 
    ch1_4_e['Fmax_v2'] = chiller1['ch1_evaptret']['value']                                                                                    ##The maximum supply temperature of the chiller is that of the return temperature
    ch1_4_e['Coeff_v1_2'] = 0                                                                                                                 ##This illustrates the relationship between the variables  
    ch1_4_e['Coeff_v1_1'] = chiller1['ch1_totalenwkflow']['value'] * chiller1['ch1_cp']['value'] * chiller1['ch1_evaptret']['value']          ##The relationship is Qe = m_evap_perc*m_total*Cp*Tevap_in - m_evap_perc*m_total*Cp*Tevap_out
    ch1_4_e['Coeff_v2_2'] = 0
    ch1_4_e['Coeff_v2_1'] = 0
    ch1_4_e['Coeff_v1_v2'] = -chiller1['ch1_totalenwkflow']['value'] * chiller1['ch1_cp']['value'] 
    ch1_4_e['Coeff_cst'] = 0
    ch1_4_e['Fmin'] = chiller1['ch1_f4']['value'] * chiller1['ch1_rated_cap']['value']
    ch1_4_e['Fmax'] = chiller1['ch1_f5']['value'] * chiller1['ch1_rated_cap']['value']
    ch1_4_e['Cost_v1_2'] = 0
    ch1_4_e['Cost_v1_1'] = 0
    ch1_4_e['Cost_v2_2'] = 0
    ch1_4_e['Cost_v2_1'] = 0
    ch1_4_e['Cost_v1_v2'] = 0
    ch1_4_e['Cost_cst'] = 0
    ch1_4_e['Cinv_v1_2'] = 0
    ch1_4_e['Cinv_v1_1'] = 0
    ch1_4_e['Cinv_v2_2'] = 0
    ch1_4_e['Cinv_v2_1'] = 0
    ch1_4_e['Cinv_v1_v2'] = 0
    ch1_4_e['Cinv_cst'] = 0
    ch1_4_e['Power_v1_2'] = 0
    ch1_4_e['Power_v1_1'] = 0
    ch1_4_e['Power_v2_2'] = 0
    ch1_4_e['Power_v2_1'] = 0
    ch1_4_e['Power_v1_v2'] = chiller1['ch1_egrad4']['value']
    ch1_4_e['Power_cst'] = chiller1['ch1_int4']['value']
    ch1_4_e['Impact_v1_2'] = 0
    ch1_4_e['Impact_v1_1'] = 0
    ch1_4_e['Impact_v2_2'] = 0
    ch1_4_e['Impact_v2_1'] = 0
    ch1_4_e['Impact_v1_v2'] = 0
    ch1_4_e['Impact_cst'] = 0

    unitinput = [ch1_4_e['Name'], ch1_4_e['Variable1'], ch1_4_e['Variable2'], ch1_4_e['Fmin_v1'], ch1_4_e['Fmax_v1'], ch1_4_e['Fmin_v2'], ch1_4_e['Fmax_v2'], ch1_4_e['Coeff_v1_2'], 
                ch1_4_e['Coeff_v1_1'], ch1_4_e['Coeff_v2_2'], ch1_4_e['Coeff_v2_1'], ch1_4_e['Coeff_v1_v2'], ch1_4_e['Coeff_cst'], ch1_4_e['Fmin'], ch1_4_e['Fmax'], ch1_4_e['Cost_v1_2'], 
                ch1_4_e['Cost_v1_1'], ch1_4_e['Cost_v2_2'], ch1_4_e['Cost_v2_1'], ch1_4_e['Cost_v1_v2'], ch1_4_e['Cost_cst'], ch1_4_e['Cinv_v1_2'], ch1_4_e['Cinv_v1_1'], ch1_4_e['Cinv_v2_2'], 
                ch1_4_e['Cinv_v2_1'], ch1_4_e['Cinv_v1_v2'], ch1_4_e['Cinv_cst'], ch1_4_e['Power_v1_2'], ch1_4_e['Power_v1_1'], ch1_4_e['Power_v2_2'], ch1_4_e['Power_v2_1'], 
                ch1_4_e['Power_v1_v2'], ch1_4_e['Power_cst'], ch1_4_e['Impact_v1_2'], ch1_4_e['Impact_v1_1'], ch1_4_e['Impact_v2_2'], ch1_4_e['Impact_v2_1'], ch1_4_e['Impact_v1_v2'], 
                ch1_4_e['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Unit 8
    ch1_4_c = {}
    ch1_4_c['Name'] = 'ch1_4_cond'
    ch1_4_c['Variable1'] = 'm_perc'                                                                                                           ##Percentage of flowrate from the entire condenser network 
    ch1_4_c['Variable2'] = 't_out'                                                                                                            ##Condenser water setpoint temperature 
    ch1_4_c['Fmin_v1'] = 0 
    ch1_4_c['Fmax_v1'] = 1                                                                                                                    ##Maximum percentage is 100% 
    ch1_4_c['Fmin_v2'] = chiller1['ch1_condtin']['value'] + 1                                                                                 ##The minimum condenser exit temperature is 1 deg above entry temperature 
    ch1_4_c['Fmax_v2'] = chiller1['ch1_condtin']['value'] + 10                                                                                ##The maximum condenser exit temperature is 10 degrees above entry temperature
    ch1_4_c['Coeff_v1_2'] = 0                                                                                                                 ##This illustrates the relationship between the variables  
    ch1_4_c['Coeff_v1_1'] = -chiller1['ch1_totalcnwkflow']['value'] * chiller1['ch1_cp']['value'] * chiller1['ch1_condtin']['value']          ##The relationship is Qc = m_cond_perc*m_total*Cp*Tcond_in - m_cond_perc*m_total*Cp*Tcond_out
    ch1_4_c['Coeff_v2_2'] = 0
    ch1_4_c['Coeff_v2_1'] = 0
    ch1_4_c['Coeff_v1_v2'] = chiller1['ch1_totalcnwkflow']['value'] * chiller1['ch1_cp']['value'] 
    ch1_4_c['Coeff_cst'] = 0
    ch1_4_c['Fmin'] = chiller1['ch1_f4']['value'] * chiller1['ch1_rated_cap']['value'] * chiller1['ch1_qc_coeff']['value']
    ch1_4_c['Fmax'] = chiller1['ch1_f5']['value'] * chiller1['ch1_rated_cap']['value'] * chiller1['ch1_qc_coeff']['value']
    ch1_4_c['Cost_v1_2'] = 0
    ch1_4_c['Cost_v1_1'] = 0
    ch1_4_c['Cost_v2_2'] = 0
    ch1_4_c['Cost_v2_1'] = 0
    ch1_4_c['Cost_v1_v2'] = 0
    ch1_4_c['Cost_cst'] = 0
    ch1_4_c['Cinv_v1_2'] = 0
    ch1_4_c['Cinv_v1_1'] = 0
    ch1_4_c['Cinv_v2_2'] = 0
    ch1_4_c['Cinv_v2_1'] = 0
    ch1_4_c['Cinv_v1_v2'] = 0
    ch1_4_c['Cinv_cst'] = 0
    ch1_4_c['Power_v1_2'] = 0
    ch1_4_c['Power_v1_1'] = 0
    ch1_4_c['Power_v2_2'] = 0
    ch1_4_c['Power_v2_1'] = 0
    ch1_4_c['Power_v1_v2'] = 0                                                                                                                ##Already accounted for in the evaporator unit
    ch1_4_c['Power_cst'] = 0
    ch1_4_c['Impact_v1_2'] = 0
    ch1_4_c['Impact_v1_1'] = 0
    ch1_4_c['Impact_v2_2'] = 0
    ch1_4_c['Impact_v2_1'] = 0
    ch1_4_c['Impact_v1_v2'] = 0
    ch1_4_c['Impact_cst'] = 0

    unitinput = [ch1_4_c['Name'], ch1_4_c['Variable1'], ch1_4_c['Variable2'], ch1_4_c['Fmin_v1'], ch1_4_c['Fmax_v1'], ch1_4_c['Fmin_v2'], ch1_4_c['Fmax_v2'], ch1_4_c['Coeff_v1_2'], 
                ch1_4_c['Coeff_v1_1'], ch1_4_c['Coeff_v2_2'], ch1_4_c['Coeff_v2_1'], ch1_4_c['Coeff_v1_v2'], ch1_4_c['Coeff_cst'], ch1_4_c['Fmin'], ch1_4_c['Fmax'], ch1_4_c['Cost_v1_2'], 
                ch1_4_c['Cost_v1_1'], ch1_4_c['Cost_v2_2'], ch1_4_c['Cost_v2_1'], ch1_4_c['Cost_v1_v2'], ch1_4_c['Cost_cst'], ch1_4_c['Cinv_v1_2'], ch1_4_c['Cinv_v1_1'], ch1_4_c['Cinv_v2_2'], 
                ch1_4_c['Cinv_v2_1'], ch1_4_c['Cinv_v1_v2'], ch1_4_c['Cinv_cst'], ch1_4_c['Power_v1_2'], ch1_4_c['Power_v1_1'], ch1_4_c['Power_v2_2'], ch1_4_c['Power_v2_1'], 
                ch1_4_c['Power_v1_v2'], ch1_4_c['Power_cst'], ch1_4_c['Impact_v1_2'], ch1_4_c['Impact_v1_1'], ch1_4_c['Impact_v2_2'], ch1_4_c['Impact_v2_1'], ch1_4_c['Impact_v1_v2'], 
                ch1_4_c['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Layer and stream definition 
    
    ##Unit 1 (ch1_1_evap) streams
    
    ##Stream 1
    stream1 = {}                                                                ##Chiller evaporator has 2 streams for each step_wise, one is temperature and the other is that of flowrate 
    stream1['Parent'] = 'ch1_1_evap'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'ch1_1_evap_tout'
    stream1['Layer'] = 'chil2sp1_temp'
    stream1['Stream_coeff_v1_2'] = 0
    stream1['Stream_coeff_v1_1'] = 0
    stream1['Stream_coeff_v2_2'] = 0
    stream1['Stream_coeff_v2_1'] = 0
    stream1['Stream_coeff_v1_v2'] = 1
    stream1['Stream_coeff_cst'] = 0
    stream1['InOut'] = 'out'
    
    streaminput = [stream1['Parent'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Stream_coeff_v1_2'], stream1['Stream_coeff_v1_1'], stream1['Stream_coeff_v2_2'],
                   stream1['Stream_coeff_v2_1'], stream1['Stream_coeff_v1_v2'], stream1['Stream_coeff_cst'], stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 2
    stream2 = {}                                                                ##Chiller evaporator unit has 2 streams for each step_wise, one is temperature and the other is that of flowrate 
    stream2['Parent'] = 'ch1_1_evap'
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'ch1_1_evap_mfout'
    stream2['Layer'] = 'chil2distnwk_flow'
    stream2['Stream_coeff_v1_2'] = 0
    stream2['Stream_coeff_v1_1'] = chiller1['ch1_totalenwkflow']['value']
    stream2['Stream_coeff_v2_2'] = 0
    stream2['Stream_coeff_v2_1'] = 0
    stream2['Stream_coeff_v1_v2'] = 0
    stream2['Stream_coeff_cst'] = 0
    stream2['InOut'] = 'out'
    
    streaminput = [stream2['Parent'], stream2['Type'], stream2['Name'], stream2['Layer'], stream2['Stream_coeff_v1_2'], stream2['Stream_coeff_v1_1'], stream2['Stream_coeff_v2_2'],
                   stream2['Stream_coeff_v2_1'], stream2['Stream_coeff_v1_v2'], stream2['Stream_coeff_cst'], stream2['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)  

    ##Stream 3
    stream3 = {}                                                                ##To make sure that totalflowrate tallies 
    stream3['Parent'] = 'ch1_1_evap'
    stream3['Type'] = 'balancing_only'
    stream3['Name'] = 'ch1_1_evap_mfout_chk'
    stream3['Layer'] = 'chil2distnwk_flow_check'
    stream3['Stream_coeff_v1_2'] = 0
    stream3['Stream_coeff_v1_1'] = chiller1['ch1_totalenwkflow']['value']
    stream3['Stream_coeff_v2_2'] = 0
    stream3['Stream_coeff_v2_1'] = 0
    stream3['Stream_coeff_v1_v2'] = 0
    stream3['Stream_coeff_cst'] = 0
    stream3['InOut'] = 'out'
    
    streaminput = [stream3['Parent'], stream3['Type'], stream3['Name'], stream3['Layer'], stream3['Stream_coeff_v1_2'], stream3['Stream_coeff_v1_1'], stream3['Stream_coeff_v2_2'],
                   stream3['Stream_coeff_v2_1'], stream3['Stream_coeff_v1_v2'], stream3['Stream_coeff_cst'], stream3['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True) 
    
    ##Stream 4
    stream4 = {}                                                                ##The flowrate to the evaporator network 
    stream4['Parent'] = 'ch1_1_evap'
    stream4['Type'] = 'balancing_only'
    stream4['Name'] = 'ch1_1_evap_mfout_enwk'
    stream4['Layer'] = 'ch1_2_evap_flow'
    stream4['Stream_coeff_v1_2'] = 0
    stream4['Stream_coeff_v1_1'] = chiller1['ch1_totalenwkflow']['value']
    stream4['Stream_coeff_v2_2'] = 0
    stream4['Stream_coeff_v2_1'] = 0
    stream4['Stream_coeff_v1_v2'] = 0
    stream4['Stream_coeff_cst'] = 0
    stream4['InOut'] = 'out'
    
    streaminput = [stream4['Parent'], stream4['Type'], stream4['Name'], stream4['Layer'], stream4['Stream_coeff_v1_2'], stream4['Stream_coeff_v1_1'], stream4['Stream_coeff_v2_2'],
                   stream4['Stream_coeff_v2_1'], stream4['Stream_coeff_v1_v2'], stream4['Stream_coeff_cst'], stream4['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)     
    
    ##Unit 2 (ch1_1_cond) streams
    
    ##Stream 5
    stream5 = {}                                                                ##Chiller condenser has 2 streams for each step_wise, one is temperature and the other is that of flowrate 
    stream5['Parent'] = 'ch1_1_cond'
    stream5['Type'] = 'balancing_only'
    stream5['Name'] = 'ch1_1_cond_tout'
    stream5['Layer'] = 'chil2condret_temp'
    stream5['Stream_coeff_v1_2'] = 0
    stream5['Stream_coeff_v1_1'] = 0
    stream5['Stream_coeff_v2_2'] = 0
    stream5['Stream_coeff_v2_1'] = 0
    stream5['Stream_coeff_v1_v2'] = 1
    stream5['Stream_coeff_cst'] = 0
    stream5['InOut'] = 'out'
    
    streaminput = [stream5['Parent'], stream5['Type'], stream5['Name'], stream5['Layer'], stream5['Stream_coeff_v1_2'], stream5['Stream_coeff_v1_1'], stream5['Stream_coeff_v2_2'],
                   stream5['Stream_coeff_v2_1'], stream5['Stream_coeff_v1_v2'], stream5['Stream_coeff_cst'], stream5['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 6
    stream6 = {}                                                                ##Chiller condenser has 2 streams for each step_wise, one is temperature and the other is that of flowrate 
    stream6['Parent'] = 'ch1_1_cond'
    stream6['Type'] = 'balancing_only'
    stream6['Name'] = 'ch1_1_cond_mfout'
    stream6['Layer'] = 'chil2condret_flow'
    stream6['Stream_coeff_v1_2'] = 0
    stream6['Stream_coeff_v1_1'] = chiller1['ch1_totalcnwkflow']['value']
    stream6['Stream_coeff_v2_2'] = 0
    stream6['Stream_coeff_v2_1'] = 0
    stream6['Stream_coeff_v1_v2'] = 0
    stream6['Stream_coeff_cst'] = 0
    stream6['InOut'] = 'out'
    
    streaminput = [stream6['Parent'], stream6['Type'], stream6['Name'], stream6['Layer'], stream6['Stream_coeff_v1_2'], stream6['Stream_coeff_v1_1'], stream6['Stream_coeff_v2_2'],
                   stream6['Stream_coeff_v2_1'], stream6['Stream_coeff_v1_v2'], stream6['Stream_coeff_cst'], stream6['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)    
    
    ##Stream 7
    stream7 = {}                                                                ##The flowrate to the condenser network 
    stream7['Parent'] = 'ch1_1_cond'
    stream7['Type'] = 'balancing_only'
    stream7['Name'] = 'ch1_1_cond_mfout_cnwk'
    stream7['Layer'] = 'ch1_2_cond_flow'
    stream7['Stream_coeff_v1_2'] = 0
    stream7['Stream_coeff_v1_1'] = chiller1['ch1_totalcnwkflow']['value']
    stream7['Stream_coeff_v2_2'] = 0
    stream7['Stream_coeff_v2_1'] = 0
    stream7['Stream_coeff_v1_v2'] = 0
    stream7['Stream_coeff_cst'] = 0
    stream7['InOut'] = 'out'
    
    streaminput = [stream7['Parent'], stream7['Type'], stream7['Name'], stream7['Layer'], stream7['Stream_coeff_v1_2'], stream7['Stream_coeff_v1_1'], stream7['Stream_coeff_v2_2'],
                   stream7['Stream_coeff_v2_1'], stream7['Stream_coeff_v1_v2'], stream7['Stream_coeff_cst'], stream7['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)       
    
    ##Unit 3 (ch1_2_evap) streams
    
    ##Stream 8
    stream8 = {}                                                                ##Chiller evaporator has 2 streams for each step_wise, one is temperature and the other is that of flowrate 
    stream8['Parent'] = 'ch1_2_evap'
    stream8['Type'] = 'balancing_only'
    stream8['Name'] = 'ch1_2_evap_tout'
    stream8['Layer'] = 'chil2sp1_temp'
    stream8['Stream_coeff_v1_2'] = 0
    stream8['Stream_coeff_v1_1'] = 0
    stream8['Stream_coeff_v2_2'] = 0
    stream8['Stream_coeff_v2_1'] = 0
    stream8['Stream_coeff_v1_v2'] = 1
    stream8['Stream_coeff_cst'] = 0
    stream8['InOut'] = 'out'
    
    streaminput = [stream8['Parent'], stream8['Type'], stream8['Name'], stream8['Layer'], stream8['Stream_coeff_v1_2'], stream8['Stream_coeff_v1_1'], stream8['Stream_coeff_v2_2'],
                   stream8['Stream_coeff_v2_1'], stream8['Stream_coeff_v1_v2'], stream8['Stream_coeff_cst'], stream8['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 9
    stream9 = {}                                                                ##Chiller evaporator unit has 2 streams for each step_wise, one is temperature and the other is that of flowrate 
    stream9['Parent'] = 'ch1_2_evap'
    stream9['Type'] = 'balancing_only'
    stream9['Name'] = 'ch1_2_evap_mfout'
    stream9['Layer'] = 'chil2distnwk_flow'
    stream9['Stream_coeff_v1_2'] = 0
    stream9['Stream_coeff_v1_1'] = chiller1['ch1_totalenwkflow']['value']
    stream9['Stream_coeff_v2_2'] = 0
    stream9['Stream_coeff_v2_1'] = 0
    stream9['Stream_coeff_v1_v2'] = 0
    stream9['Stream_coeff_cst'] = 0
    stream9['InOut'] = 'out'
    
    streaminput = [stream9['Parent'], stream9['Type'], stream9['Name'], stream9['Layer'], stream9['Stream_coeff_v1_2'], stream9['Stream_coeff_v1_1'], stream9['Stream_coeff_v2_2'],
                   stream9['Stream_coeff_v2_1'], stream9['Stream_coeff_v1_v2'], stream9['Stream_coeff_cst'], stream9['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)  

    ##Stream 10
    stream10 = {}                                                                ##To make sure that totalflowrate tallies
    stream10['Parent'] = 'ch1_2_evap'
    stream10['Type'] = 'balancing_only'
    stream10['Name'] = 'ch1_2_evap_mfout_chk'
    stream10['Layer'] = 'chil2distnwk_flow_check'
    stream10['Stream_coeff_v1_2'] = 0
    stream10['Stream_coeff_v1_1'] = chiller1['ch1_totalenwkflow']['value']
    stream10['Stream_coeff_v2_2'] = 0
    stream10['Stream_coeff_v2_1'] = 0
    stream10['Stream_coeff_v1_v2'] = 0
    stream10['Stream_coeff_cst'] = 0
    stream10['InOut'] = 'out'
    
    streaminput = [stream10['Parent'], stream10['Type'], stream10['Name'], stream10['Layer'], stream10['Stream_coeff_v1_2'], stream10['Stream_coeff_v1_1'], stream10['Stream_coeff_v2_2'],
                   stream10['Stream_coeff_v2_1'], stream10['Stream_coeff_v1_v2'], stream10['Stream_coeff_cst'], stream10['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True) 
    
    ##Stream 11
    stream11 = {}                                                                ##The flowrate to the evaporator network 
    stream11['Parent'] = 'ch1_2_evap'
    stream11['Type'] = 'balancing_only'
    stream11['Name'] = 'ch1_2_evap_mfout_enwk'
    stream11['Layer'] = 'ch1_2_evap_flow'
    stream11['Stream_coeff_v1_2'] = 0
    stream11['Stream_coeff_v1_1'] = chiller1['ch1_totalenwkflow']['value']
    stream11['Stream_coeff_v2_2'] = 0
    stream11['Stream_coeff_v2_1'] = 0
    stream11['Stream_coeff_v1_v2'] = 0
    stream11['Stream_coeff_cst'] = 0
    stream11['InOut'] = 'out'
    
    streaminput = [stream11['Parent'], stream11['Type'], stream11['Name'], stream11['Layer'], stream11['Stream_coeff_v1_2'], stream11['Stream_coeff_v1_1'], stream11['Stream_coeff_v2_2'],
                   stream11['Stream_coeff_v2_1'], stream11['Stream_coeff_v1_v2'], stream11['Stream_coeff_cst'], stream11['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)   
    
    ##Unit 4 (ch1_2_cond) streams
    
    ##Stream 12
    stream12 = {}                                                                ##Chiller condenser has 2 streams for each step_wise, one is temperature and the other is that of flowrate 
    stream12['Parent'] = 'ch1_2_cond'
    stream12['Type'] = 'balancing_only'
    stream12['Name'] = 'ch1_2_cond_tout'
    stream12['Layer'] = 'chil2condret_temp'
    stream12['Stream_coeff_v1_2'] = 0
    stream12['Stream_coeff_v1_1'] = 0
    stream12['Stream_coeff_v2_2'] = 0
    stream12['Stream_coeff_v2_1'] = 0
    stream12['Stream_coeff_v1_v2'] = 1
    stream12['Stream_coeff_cst'] = 0
    stream12['InOut'] = 'out'
    
    streaminput = [stream12['Parent'], stream12['Type'], stream12['Name'], stream12['Layer'], stream12['Stream_coeff_v1_2'], stream12['Stream_coeff_v1_1'], stream12['Stream_coeff_v2_2'],
                   stream12['Stream_coeff_v2_1'], stream12['Stream_coeff_v1_v2'], stream12['Stream_coeff_cst'], stream12['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 13
    stream13 = {}                                                                ##Chiller condenser has 2 streams for each step_wise, one is temperature and the other is that of flowrate 
    stream13['Parent'] = 'ch1_2_cond'
    stream13['Type'] = 'balancing_only'
    stream13['Name'] = 'ch1_2_cond_mfout'
    stream13['Layer'] = 'chil2condret_flow'
    stream13['Stream_coeff_v1_2'] = 0
    stream13['Stream_coeff_v1_1'] = chiller1['ch1_totalcnwkflow']['value']
    stream13['Stream_coeff_v2_2'] = 0
    stream13['Stream_coeff_v2_1'] = 0
    stream13['Stream_coeff_v1_v2'] = 0
    stream13['Stream_coeff_cst'] = 0
    stream13['InOut'] = 'out'
    
    streaminput = [stream13['Parent'], stream13['Type'], stream13['Name'], stream13['Layer'], stream13['Stream_coeff_v1_2'], stream13['Stream_coeff_v1_1'], stream13['Stream_coeff_v2_2'],
                   stream13['Stream_coeff_v2_1'], stream13['Stream_coeff_v1_v2'], stream13['Stream_coeff_cst'], stream13['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)    
    
    ##Stream 14
    stream14 = {}                                                                ##The flowrate to the condenser network 
    stream14['Parent'] = 'ch1_2_cond'
    stream14['Type'] = 'balancing_only'
    stream14['Name'] = 'ch1_2_cond_mfout_cnwk'
    stream14['Layer'] = 'ch1_2_cond_flow'
    stream14['Stream_coeff_v1_2'] = 0
    stream14['Stream_coeff_v1_1'] = chiller1['ch1_totalcnwkflow']['value']
    stream14['Stream_coeff_v2_2'] = 0
    stream14['Stream_coeff_v2_1'] = 0
    stream14['Stream_coeff_v1_v2'] = 0
    stream14['Stream_coeff_cst'] = 0
    stream14['InOut'] = 'out'
    
    streaminput = [stream14['Parent'], stream14['Type'], stream14['Name'], stream14['Layer'], stream14['Stream_coeff_v1_2'], stream14['Stream_coeff_v1_1'], stream14['Stream_coeff_v2_2'],
                   stream14['Stream_coeff_v2_1'], stream14['Stream_coeff_v1_v2'], stream14['Stream_coeff_cst'], stream14['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)  

    ##Unit 5 (ch1_3_evap) streams  

    ##Stream 15
    stream15 = {}                                                                ##Chiller evaporator has 2 streams for each step_wise, one is temperature and the other is that of flowrate 
    stream15['Parent'] = 'ch1_3_evap'
    stream15['Type'] = 'balancing_only'
    stream15['Name'] = 'ch1_3_evap_tout'
    stream15['Layer'] = 'chil2sp1_temp'
    stream15['Stream_coeff_v1_2'] = 0
    stream15['Stream_coeff_v1_1'] = 0
    stream15['Stream_coeff_v2_2'] = 0
    stream15['Stream_coeff_v2_1'] = 0
    stream15['Stream_coeff_v1_v2'] = 1
    stream15['Stream_coeff_cst'] = 0
    stream15['InOut'] = 'out'
    
    streaminput = [stream15['Parent'], stream15['Type'], stream15['Name'], stream15['Layer'], stream15['Stream_coeff_v1_2'], stream15['Stream_coeff_v1_1'], stream15['Stream_coeff_v2_2'],
                   stream15['Stream_coeff_v2_1'], stream15['Stream_coeff_v1_v2'], stream15['Stream_coeff_cst'], stream15['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 16
    stream16 = {}                                                                ##Chiller evaporator unit has 2 streams for each step_wise, one is temperature and the other is that of flowrate 
    stream16['Parent'] = 'ch1_3_evap'
    stream16['Type'] = 'balancing_only'
    stream16['Name'] = 'ch1_3_evap_mfout'
    stream16['Layer'] = 'chil2distnwk_flow'
    stream16['Stream_coeff_v1_2'] = 0
    stream16['Stream_coeff_v1_1'] = chiller1['ch1_totalenwkflow']['value']
    stream16['Stream_coeff_v2_2'] = 0
    stream16['Stream_coeff_v2_1'] = 0
    stream16['Stream_coeff_v1_v2'] = 0
    stream16['Stream_coeff_cst'] = 0
    stream16['InOut'] = 'out'
    
    streaminput = [stream16['Parent'], stream16['Type'], stream16['Name'], stream16['Layer'], stream16['Stream_coeff_v1_2'], stream16['Stream_coeff_v1_1'], stream16['Stream_coeff_v2_2'],
                   stream16['Stream_coeff_v2_1'], stream16['Stream_coeff_v1_v2'], stream16['Stream_coeff_cst'], stream16['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)  

    ##Stream 17
    stream17 = {}                                                               ##To make sure that totalflowrate tallies
    stream17['Parent'] = 'ch1_3_evap'
    stream17['Type'] = 'balancing_only'
    stream17['Name'] = 'ch1_3_evap_mfout_chk'
    stream17['Layer'] = 'chil2distnwk_flow_check'
    stream17['Stream_coeff_v1_2'] = 0
    stream17['Stream_coeff_v1_1'] = chiller1['ch1_totalenwkflow']['value']
    stream17['Stream_coeff_v2_2'] = 0
    stream17['Stream_coeff_v2_1'] = 0
    stream17['Stream_coeff_v1_v2'] = 0
    stream17['Stream_coeff_cst'] = 0
    stream17['InOut'] = 'out'
    
    streaminput = [stream17['Parent'], stream17['Type'], stream17['Name'], stream17['Layer'], stream17['Stream_coeff_v1_2'], stream17['Stream_coeff_v1_1'], stream17['Stream_coeff_v2_2'],
                   stream17['Stream_coeff_v2_1'], stream17['Stream_coeff_v1_v2'], stream17['Stream_coeff_cst'], stream17['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)  
    
    ##Stream 18
    stream18 = {}                                                                ##The flowrate to the evaporator network 
    stream18['Parent'] = 'ch1_3_evap'
    stream18['Type'] = 'balancing_only'
    stream18['Name'] = 'ch1_3_evap_mfout_enwk'
    stream18['Layer'] = 'ch1_2_evap_flow'
    stream18['Stream_coeff_v1_2'] = 0
    stream18['Stream_coeff_v1_1'] = chiller1['ch1_totalenwkflow']['value']
    stream18['Stream_coeff_v2_2'] = 0
    stream18['Stream_coeff_v2_1'] = 0
    stream18['Stream_coeff_v1_v2'] = 0
    stream18['Stream_coeff_cst'] = 0
    stream18['InOut'] = 'out'
    
    streaminput = [stream18['Parent'], stream18['Type'], stream18['Name'], stream18['Layer'], stream18['Stream_coeff_v1_2'], stream18['Stream_coeff_v1_1'], stream18['Stream_coeff_v2_2'],
                   stream18['Stream_coeff_v2_1'], stream18['Stream_coeff_v1_v2'], stream18['Stream_coeff_cst'], stream18['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)   
    
    ##Unit 6 (ch1_3_cond) streams
    
    ##Stream 19
    stream19 = {}                                                                ##Chiller condenser has 2 streams for each step_wise, one is temperature and the other is that of flowrate 
    stream19['Parent'] = 'ch1_3_cond'
    stream19['Type'] = 'balancing_only'
    stream19['Name'] = 'ch1_3_cond_tout'
    stream19['Layer'] = 'chil2condret_temp'
    stream19['Stream_coeff_v1_2'] = 0
    stream19['Stream_coeff_v1_1'] = 0
    stream19['Stream_coeff_v2_2'] = 0
    stream19['Stream_coeff_v2_1'] = 0
    stream19['Stream_coeff_v1_v2'] = 1
    stream19['Stream_coeff_cst'] = 0
    stream19['InOut'] = 'out'
    
    streaminput = [stream19['Parent'], stream19['Type'], stream19['Name'], stream19['Layer'], stream19['Stream_coeff_v1_2'], stream19['Stream_coeff_v1_1'], stream19['Stream_coeff_v2_2'],
                   stream19['Stream_coeff_v2_1'], stream19['Stream_coeff_v1_v2'], stream19['Stream_coeff_cst'], stream19['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 20
    stream20 = {}                                                                ##Chiller condenser has 2 streams for each step_wise, one is temperature and the other is that of flowrate 
    stream20['Parent'] = 'ch1_3_cond'
    stream20['Type'] = 'balancing_only'
    stream20['Name'] = 'ch1_3_cond_mfout'
    stream20['Layer'] = 'chil2condret_flow'
    stream20['Stream_coeff_v1_2'] = 0
    stream20['Stream_coeff_v1_1'] = chiller1['ch1_totalcnwkflow']['value']
    stream20['Stream_coeff_v2_2'] = 0
    stream20['Stream_coeff_v2_1'] = 0
    stream20['Stream_coeff_v1_v2'] = 0
    stream20['Stream_coeff_cst'] = 0
    stream20['InOut'] = 'out'
    
    streaminput = [stream20['Parent'], stream20['Type'], stream20['Name'], stream20['Layer'], stream20['Stream_coeff_v1_2'], stream20['Stream_coeff_v1_1'], stream20['Stream_coeff_v2_2'],
                   stream20['Stream_coeff_v2_1'], stream20['Stream_coeff_v1_v2'], stream20['Stream_coeff_cst'], stream20['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)    
    
    ##Stream 21
    stream21 = {}                                                                ##The flowrate to the condenser network 
    stream21['Parent'] = 'ch1_3_cond'
    stream21['Type'] = 'balancing_only'
    stream21['Name'] = 'ch1_3_cond_mfout_cnwk'
    stream21['Layer'] = 'ch1_2_cond_flow'
    stream21['Stream_coeff_v1_2'] = 0
    stream21['Stream_coeff_v1_1'] = chiller1['ch1_totalcnwkflow']['value']
    stream21['Stream_coeff_v2_2'] = 0
    stream21['Stream_coeff_v2_1'] = 0
    stream21['Stream_coeff_v1_v2'] = 0
    stream21['Stream_coeff_cst'] = 0
    stream21['InOut'] = 'out'
    
    streaminput = [stream21['Parent'], stream21['Type'], stream21['Name'], stream21['Layer'], stream21['Stream_coeff_v1_2'], stream21['Stream_coeff_v1_1'], stream21['Stream_coeff_v2_2'],
                   stream21['Stream_coeff_v2_1'], stream21['Stream_coeff_v1_v2'], stream21['Stream_coeff_cst'], stream21['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)  
    
    ##Unit 7 (ch1_4_evap) streams

    ##Stream 22
    stream22 = {}                                                                ##Chiller evaporator has 2 streams for each step_wise, one is temperature and the other is that of flowrate 
    stream22['Parent'] = 'ch1_4_evap'
    stream22['Type'] = 'balancing_only'
    stream22['Name'] = 'ch1_4_evap_tout'
    stream22['Layer'] = 'chil2sp1_temp'
    stream22['Stream_coeff_v1_2'] = 0
    stream22['Stream_coeff_v1_1'] = 0
    stream22['Stream_coeff_v2_2'] = 0
    stream22['Stream_coeff_v2_1'] = 0
    stream22['Stream_coeff_v1_v2'] = 1
    stream22['Stream_coeff_cst'] = 0
    stream22['InOut'] = 'out'
    
    streaminput = [stream22['Parent'], stream22['Type'], stream22['Name'], stream22['Layer'], stream22['Stream_coeff_v1_2'], stream22['Stream_coeff_v1_1'], stream22['Stream_coeff_v2_2'],
                   stream22['Stream_coeff_v2_1'], stream22['Stream_coeff_v1_v2'], stream22['Stream_coeff_cst'], stream22['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 23
    stream23 = {}                                                                ##Chiller evaporator unit has 2 streams for each step_wise, one is temperature and the other is that of flowrate 
    stream23['Parent'] = 'ch1_4_evap'
    stream23['Type'] = 'balancing_only'
    stream23['Name'] = 'ch1_4_evap_mfout'
    stream23['Layer'] = 'chil2distnwk_flow'
    stream23['Stream_coeff_v1_2'] = 0
    stream23['Stream_coeff_v1_1'] = chiller1['ch1_totalenwkflow']['value']
    stream23['Stream_coeff_v2_2'] = 0
    stream23['Stream_coeff_v2_1'] = 0
    stream23['Stream_coeff_v1_v2'] = 0
    stream23['Stream_coeff_cst'] = 0
    stream23['InOut'] = 'out'
    
    streaminput = [stream23['Parent'], stream23['Type'], stream23['Name'], stream23['Layer'], stream23['Stream_coeff_v1_2'], stream23['Stream_coeff_v1_1'], stream23['Stream_coeff_v2_2'],
                   stream23['Stream_coeff_v2_1'], stream23['Stream_coeff_v1_v2'], stream23['Stream_coeff_cst'], stream23['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True) 
    
    ##Stream 24
    stream24 = {}                                                                ##To make sure that totalflowrate tallies
    stream24['Parent'] = 'ch1_4_evap'
    stream24['Type'] = 'balancing_only'
    stream24['Name'] = 'ch1_4_evap_mfout_chk'
    stream24['Layer'] = 'chil2distnwk_flow_check'
    stream24['Stream_coeff_v1_2'] = 0
    stream24['Stream_coeff_v1_1'] = chiller1['ch1_totalenwkflow']['value']
    stream24['Stream_coeff_v2_2'] = 0
    stream24['Stream_coeff_v2_1'] = 0
    stream24['Stream_coeff_v1_v2'] = 0
    stream24['Stream_coeff_cst'] = 0
    stream24['InOut'] = 'out'
    
    streaminput = [stream24['Parent'], stream24['Type'], stream24['Name'], stream24['Layer'], stream24['Stream_coeff_v1_2'], stream24['Stream_coeff_v1_1'], stream24['Stream_coeff_v2_2'],
                   stream24['Stream_coeff_v2_1'], stream24['Stream_coeff_v1_v2'], stream24['Stream_coeff_cst'], stream24['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 25
    stream25 = {}                                                                ##The flowrate to the evaporator network 
    stream25['Parent'] = 'ch1_4_evap'
    stream25['Type'] = 'balancing_only'
    stream25['Name'] = 'ch1_4_evap_mfout_enwk'
    stream25['Layer'] = 'ch1_2_evap_flow'
    stream25['Stream_coeff_v1_2'] = 0
    stream25['Stream_coeff_v1_1'] = chiller1['ch1_totalenwkflow']['value']
    stream25['Stream_coeff_v2_2'] = 0
    stream25['Stream_coeff_v2_1'] = 0
    stream25['Stream_coeff_v1_v2'] = 0
    stream25['Stream_coeff_cst'] = 0
    stream25['InOut'] = 'out'
    
    streaminput = [stream25['Parent'], stream25['Type'], stream25['Name'], stream25['Layer'], stream25['Stream_coeff_v1_2'], stream25['Stream_coeff_v1_1'], stream25['Stream_coeff_v2_2'],
                   stream25['Stream_coeff_v2_1'], stream25['Stream_coeff_v1_v2'], stream25['Stream_coeff_cst'], stream25['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)     

    ##Unit 8 (ch1_4_cond) streams
    
    ##Stream 26
    stream26 = {}                                                                ##Chiller condenser has 2 streams for each step_wise, one is temperature and the other is that of flowrate 
    stream26['Parent'] = 'ch1_4_cond'
    stream26['Type'] = 'balancing_only'
    stream26['Name'] = 'ch1_4_cond_tout'
    stream26['Layer'] = 'chil2condret_temp'
    stream26['Stream_coeff_v1_2'] = 0
    stream26['Stream_coeff_v1_1'] = 0
    stream26['Stream_coeff_v2_2'] = 0
    stream26['Stream_coeff_v2_1'] = 0
    stream26['Stream_coeff_v1_v2'] = 1
    stream26['Stream_coeff_cst'] = 0
    stream26['InOut'] = 'out'
    
    streaminput = [stream26['Parent'], stream26['Type'], stream26['Name'], stream26['Layer'], stream26['Stream_coeff_v1_2'], stream26['Stream_coeff_v1_1'], stream26['Stream_coeff_v2_2'],
                   stream26['Stream_coeff_v2_1'], stream26['Stream_coeff_v1_v2'], stream26['Stream_coeff_cst'], stream26['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 27
    stream27 = {}                                                                ##Chiller condenser has 2 streams for each step_wise, one is temperature and the other is that of flowrate 
    stream27['Parent'] = 'ch1_4_cond'
    stream27['Type'] = 'balancing_only'
    stream27['Name'] = 'ch1_4_cond_mfout'
    stream27['Layer'] = 'chil2condret_flow'
    stream27['Stream_coeff_v1_2'] = 0
    stream27['Stream_coeff_v1_1'] = chiller1['ch1_totalcnwkflow']['value']
    stream27['Stream_coeff_v2_2'] = 0
    stream27['Stream_coeff_v2_1'] = 0
    stream27['Stream_coeff_v1_v2'] = 0
    stream27['Stream_coeff_cst'] = 0
    stream27['InOut'] = 'out'
    
    streaminput = [stream27['Parent'], stream27['Type'], stream27['Name'], stream27['Layer'], stream27['Stream_coeff_v1_2'], stream27['Stream_coeff_v1_1'], stream27['Stream_coeff_v2_2'],
                   stream27['Stream_coeff_v2_1'], stream27['Stream_coeff_v1_v2'], stream27['Stream_coeff_cst'], stream27['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)  
    
    ##Stream 28
    stream28 = {}                                                                ##The flowrate to the condenser network 
    stream28['Parent'] = 'ch1_4_cond'
    stream28['Type'] = 'balancing_only'
    stream28['Name'] = 'ch1_4_cond_mfout_cnwk'
    stream28['Layer'] = 'ch1_2_cond_flow'
    stream28['Stream_coeff_v1_2'] = 0
    stream28['Stream_coeff_v1_1'] = chiller1['ch1_totalcnwkflow']['value']
    stream28['Stream_coeff_v2_2'] = 0
    stream28['Stream_coeff_v2_1'] = 0
    stream28['Stream_coeff_v1_v2'] = 0
    stream28['Stream_coeff_cst'] = 0
    stream28['InOut'] = 'out'
    
    streaminput = [stream28['Parent'], stream28['Type'], stream28['Name'], stream28['Layer'], stream28['Stream_coeff_v1_2'], stream28['Stream_coeff_v1_1'], stream28['Stream_coeff_v2_2'],
                   stream28['Stream_coeff_v2_1'], stream28['Stream_coeff_v1_v2'], stream28['Stream_coeff_cst'], stream28['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)  

    
    ##Constraint definition
    
    ##Equation definitions
    
    ##Equation 1
    eqn1 = {}
    eqn1['Name'] = 'ch1_1_evap_cond_link'
    eqn1['Type'] = 'unit_link'
    eqn1['Sign'] = 'equal_to'
    eqn1['RHS_value'] = 0
    
    eqninput = [eqn1['Name'], eqn1['Type'], eqn1['Sign'], eqn1['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation 2
    eqn2 = {}
    eqn2['Name'] = 'ch1_2_evap_cond_link'
    eqn2['Type'] = 'unit_link'
    eqn2['Sign'] = 'equal_to'
    eqn2['RHS_value'] = 0
    
    eqninput = [eqn2['Name'], eqn2['Type'], eqn2['Sign'], eqn2['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation 3
    eqn3 = {}
    eqn3['Name'] = 'ch1_3_evap_cond_link'
    eqn3['Type'] = 'unit_link'
    eqn3['Sign'] = 'equal_to'
    eqn3['RHS_value'] = 0
    
    eqninput = [eqn3['Name'], eqn3['Type'], eqn3['Sign'], eqn3['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation 4
    eqn4 = {}
    eqn4['Name'] = 'ch1_4_evap_cond_link'
    eqn4['Type'] = 'unit_link'
    eqn4['Sign'] = 'equal_to'
    eqn4['RHS_value'] = 0
    
    eqninput = [eqn4['Name'], eqn4['Type'], eqn4['Sign'], eqn4['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation 5
    eqn5 = {}
    eqn5['Name'] = 'totaluse_ch1'
    eqn5['Type'] = 'unit_binary'
    eqn5['Sign'] = 'less_than_equal_to'
    eqn5['RHS_value'] = 1
    
    eqninput = [eqn5['Name'], eqn5['Type'], eqn5['Sign'], eqn5['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation terms 
    
    ##Term 1 
    term1 = {}
    term1['Parent_unit'] = 'ch1_1_evap'
    term1['Parent_eqn'] = 'ch1_1_evap_cond_link'
    term1['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types  
    term1['Coefficient'] = chiller1['ch1_qc_coeff']['value']
    term1['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
    term1['Coeff_v1_1'] = 0
    term1['Coeff_v2_2'] = 0
    term1['Coeff_v2_1'] = 0
    term1['Coeff_v1v2'] = 1
    term1['Coeff_cst'] = 0

    terminput = [term1['Parent_unit'], term1['Parent_eqn'], term1['Parent_stream'], term1['Coefficient'], term1['Coeff_v1_2'],
                 term1['Coeff_v1_1'], term1['Coeff_v2_2'], term1['Coeff_v2_1'], term1['Coeff_v1v2'], term1['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)   
    
    ##Term 2
    term2 = {}
    term2['Parent_unit'] = 'ch1_1_cond'
    term2['Parent_eqn'] = 'ch1_1_evap_cond_link'
    term2['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types  
    term2['Coefficient'] = -1
    term2['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
    term2['Coeff_v1_1'] = 0
    term2['Coeff_v2_2'] = 0
    term2['Coeff_v2_1'] = 0
    term2['Coeff_v1v2'] = 1
    term2['Coeff_cst'] = 0

    terminput = [term2['Parent_unit'], term2['Parent_eqn'], term2['Parent_stream'], term2['Coefficient'], term2['Coeff_v1_2'],
                 term2['Coeff_v1_1'], term2['Coeff_v2_2'], term2['Coeff_v2_1'], term2['Coeff_v1v2'], term2['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)   
    
    ##Term 3 
    term3 = {}
    term3['Parent_unit'] = 'ch1_2_evap'
    term3['Parent_eqn'] = 'ch1_2_evap_cond_link'
    term3['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types  
    term3['Coefficient'] = chiller1['ch1_qc_coeff']['value']
    term3['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
    term3['Coeff_v1_1'] = 0
    term3['Coeff_v2_2'] = 0
    term3['Coeff_v2_1'] = 0
    term3['Coeff_v1v2'] = 1
    term3['Coeff_cst'] = 0

    terminput = [term3['Parent_unit'], term3['Parent_eqn'], term3['Parent_stream'], term3['Coefficient'], term3['Coeff_v1_2'],
                 term3['Coeff_v1_1'], term3['Coeff_v2_2'], term3['Coeff_v2_1'], term3['Coeff_v1v2'], term3['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)   
    
    ##Term 4
    term4 = {}
    term4['Parent_unit'] = 'ch1_2_cond'
    term4['Parent_eqn'] = 'ch1_2_evap_cond_link'
    term4['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types  
    term4['Coefficient'] = -1
    term4['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
    term4['Coeff_v1_1'] = 0
    term4['Coeff_v2_2'] = 0
    term4['Coeff_v2_1'] = 0
    term4['Coeff_v1v2'] = 1
    term4['Coeff_cst'] = 0

    terminput = [term4['Parent_unit'], term4['Parent_eqn'], term4['Parent_stream'], term4['Coefficient'], term4['Coeff_v1_2'],
                 term4['Coeff_v1_1'], term4['Coeff_v2_2'], term4['Coeff_v2_1'], term4['Coeff_v1v2'], term4['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True) 
    
    ##Term 5 
    term5 = {}
    term5['Parent_unit'] = 'ch1_3_evap'
    term5['Parent_eqn'] = 'ch1_3_evap_cond_link'
    term5['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types  
    term5['Coefficient'] = chiller1['ch1_qc_coeff']['value']
    term5['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
    term5['Coeff_v1_1'] = 0
    term5['Coeff_v2_2'] = 0
    term5['Coeff_v2_1'] = 0
    term5['Coeff_v1v2'] = 1
    term5['Coeff_cst'] = 0

    terminput = [term5['Parent_unit'], term5['Parent_eqn'], term5['Parent_stream'], term5['Coefficient'], term5['Coeff_v1_2'],
                 term5['Coeff_v1_1'], term5['Coeff_v2_2'], term5['Coeff_v2_1'], term5['Coeff_v1v2'], term5['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)    
    
    ##Term 6
    term6 = {}
    term6['Parent_unit'] = 'ch1_3_cond'
    term6['Parent_eqn'] = 'ch1_3_evap_cond_link'
    term6['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types  
    term6['Coefficient'] = -1
    term6['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
    term6['Coeff_v1_1'] = 0
    term6['Coeff_v2_2'] = 0
    term6['Coeff_v2_1'] = 0
    term6['Coeff_v1v2'] = 1
    term6['Coeff_cst'] = 0

    terminput = [term6['Parent_unit'], term6['Parent_eqn'], term6['Parent_stream'], term6['Coefficient'], term6['Coeff_v1_2'],
                 term6['Coeff_v1_1'], term6['Coeff_v2_2'], term6['Coeff_v2_1'], term6['Coeff_v1v2'], term6['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True) 
    
    ##Term 7 
    term7 = {}
    term7['Parent_unit'] = 'ch1_4_evap'
    term7['Parent_eqn'] = 'ch1_4_evap_cond_link'
    term7['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types  
    term7['Coefficient'] = chiller1['ch1_qc_coeff']['value']
    term7['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
    term7['Coeff_v1_1'] = 0
    term7['Coeff_v2_2'] = 0
    term7['Coeff_v2_1'] = 0
    term7['Coeff_v1v2'] = 1
    term7['Coeff_cst'] = 0

    terminput = [term7['Parent_unit'], term7['Parent_eqn'], term7['Parent_stream'], term7['Coefficient'], term7['Coeff_v1_2'],
                 term7['Coeff_v1_1'], term7['Coeff_v2_2'], term7['Coeff_v2_1'], term7['Coeff_v1v2'], term7['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)    
    
    ##Term 8
    term8 = {}
    term8['Parent_unit'] = 'ch1_4_cond'
    term8['Parent_eqn'] = 'ch1_4_evap_cond_link'
    term8['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types  
    term8['Coefficient'] = -1
    term8['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
    term8['Coeff_v1_1'] = 0
    term8['Coeff_v2_2'] = 0
    term8['Coeff_v2_1'] = 0
    term8['Coeff_v1v2'] = 1
    term8['Coeff_cst'] = 0

    terminput = [term8['Parent_unit'], term8['Parent_eqn'], term8['Parent_stream'], term8['Coefficient'], term8['Coeff_v1_2'],
                 term8['Coeff_v1_1'], term8['Coeff_v2_2'], term8['Coeff_v2_1'], term8['Coeff_v1v2'], term8['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True) 
    
    ##Term 9
    term9 = {}
    term9['Parent_unit'] = 'ch1_1_evap'
    term9['Parent_eqn'] = 'totaluse_ch1'
    term9['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types 
    term9['Coefficient'] = 1
    term9['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
    term9['Coeff_v1_1'] = 0
    term9['Coeff_v2_2'] = 0
    term9['Coeff_v2_1'] = 0
    term9['Coeff_v1v2'] = 0
    term9['Coeff_cst'] = 0

    terminput = [term9['Parent_unit'], term9['Parent_eqn'], term9['Parent_stream'], term9['Coefficient'], term9['Coeff_v1_2'],
                 term9['Coeff_v1_1'], term9['Coeff_v2_2'], term9['Coeff_v2_1'], term9['Coeff_v1v2'], term9['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True) 
    
    ##Term 10
    term10 = {}
    term10['Parent_unit'] = 'ch1_2_evap'
    term10['Parent_eqn'] = 'totaluse_ch1'
    term10['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types 
    term10['Coefficient'] = 1
    term10['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
    term10['Coeff_v1_1'] = 0
    term10['Coeff_v2_2'] = 0
    term10['Coeff_v2_1'] = 0
    term10['Coeff_v1v2'] = 0
    term10['Coeff_cst'] = 0

    terminput = [term10['Parent_unit'], term10['Parent_eqn'], term10['Parent_stream'], term10['Coefficient'], term10['Coeff_v1_2'],
                 term10['Coeff_v1_1'], term10['Coeff_v2_2'], term10['Coeff_v2_1'], term10['Coeff_v1v2'], term10['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True) 
    
    ##Term 11
    term11 = {}
    term11['Parent_unit'] = 'ch1_3_evap'
    term11['Parent_eqn'] = 'totaluse_ch1'
    term11['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types 
    term11['Coefficient'] = 1
    term11['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
    term11['Coeff_v1_1'] = 0
    term11['Coeff_v2_2'] = 0
    term11['Coeff_v2_1'] = 0
    term11['Coeff_v1v2'] = 0
    term11['Coeff_cst'] = 0

    terminput = [term11['Parent_unit'], term11['Parent_eqn'], term11['Parent_stream'], term11['Coefficient'], term11['Coeff_v1_2'],
                 term11['Coeff_v1_1'], term11['Coeff_v2_2'], term11['Coeff_v2_1'], term11['Coeff_v1v2'], term11['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True) 
    
    ##Term 12
    term12 = {}
    term12['Parent_unit'] = 'ch1_4_evap'
    term12['Parent_eqn'] = 'totaluse_ch1'
    term12['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types 
    term12['Coefficient'] = 1
    term12['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
    term12['Coeff_v1_1'] = 0
    term12['Coeff_v2_2'] = 0
    term12['Coeff_v2_1'] = 0
    term12['Coeff_v1v2'] = 0
    term12['Coeff_cst'] = 0

    terminput = [term12['Parent_unit'], term12['Parent_eqn'], term12['Parent_stream'], term12['Coefficient'], term12['Coeff_v1_2'],
                 term12['Coeff_v1_1'], term12['Coeff_v2_2'], term12['Coeff_v2_1'], term12['Coeff_v1v2'], term12['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True) 
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms
        
    
    