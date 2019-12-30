##This is the Chiller 1 evaporator network, it will consolidate the flowrate and calculate the corresponding pressure drop 

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type
    
def chiller1_evap_nwk (ch1_e_nwk_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    from chiller1_evap_nwk_compute import chiller1_evap_nwk_compute
    import pandas as pd
    import numpy as np
    
    ##Model description: 
    ##This model takes in the flowrate from the corresponding chiller unit and calculates the associated pressure-drop and hence delivers it to the pump   
    
    ##Legend of input variables 
    
    ##ch1_e_nwk_tf     --- the totalflowrate through all 
    
    ##Processing list of master decision variables as parameters   
    ch1_e_nwk_tf = ch1_e_nwk_mdv['value'][0]

    ##Define dictionary of values 
    
    chiller1_evap_nwk  = {}
    ##Input constants 
    
    ##1
    ch1_e_nwk_totalflow = {}
    ch1_e_nwk_totalflow['value'] = ch1_e_nwk_tf
    ch1_e_nwk_totalflow['units'] = 'm3/h'
    ch1_e_nwk_totalflow['status'] = 'cst_input'
    chiller1_evap_nwk['ch1_e_nwk_totalflow'] = ch1_e_nwk_totalflow

    ##Defined constants 
    
    ##2
    ch1_e_nwk_evap_delp_coeff = {}
    ch1_e_nwk_evap_delp_coeff['value'] = 0.000246472
    ch1_e_nwk_evap_delp_coeff['units'] = '-'
    ch1_e_nwk_evap_delp_coeff['status'] = 'cst'
    chiller1_evap_nwk['ch1_e_nwk_evap_delp_coeff'] = ch1_e_nwk_evap_delp_coeff

    ##3
    ch1_e_nwk_common_nwk_delp_coeff = {}
    ch1_e_nwk_common_nwk_delp_coeff['value'] = 1.66667E-05
    ch1_e_nwk_common_nwk_delp_coeff['units'] = '-'
    ch1_e_nwk_common_nwk_delp_coeff['status'] = 'cst'
    chiller1_evap_nwk['ch1_e_nwk_common_nwk_delp_coeff'] = ch1_e_nwk_common_nwk_delp_coeff    

    ##4
    ch1_e_nwk_max_flow = {}
    ch1_e_nwk_max_flow['value'] = 246                                           ##Calculated for the lowest pressure drop case 
    ch1_e_nwk_max_flow['units'] = 'm3/h'
    ch1_e_nwk_max_flow['status'] = 'cst'
    chiller1_evap_nwk['ch1_e_nwk_max_flow'] = ch1_e_nwk_max_flow        

    ##Dependent constants 
    ch1_e_nwk_dc = np.zeros((4,1))
    
    ch1_e_nwk_dc[0,0] = chiller1_evap_nwk['ch1_e_nwk_totalflow']['value']
    ch1_e_nwk_dc[1,0] = chiller1_evap_nwk['ch1_e_nwk_evap_delp_coeff']['value']
    ch1_e_nwk_dc[2,0] = chiller1_evap_nwk['ch1_e_nwk_common_nwk_delp_coeff']['value']
    ch1_e_nwk_dc[3,0] = chiller1_evap_nwk['ch1_e_nwk_max_flow']['value']

    ch1_e_nwk_calc = chiller1_evap_nwk_compute(ch1_e_nwk_dc)
    
    ##5
    ch1_e_nwk_grad1 = {}
    ch1_e_nwk_grad1['value'] = ch1_e_nwk_calc[0,0]
    ch1_e_nwk_grad1['units'] = '-'
    ch1_e_nwk_grad1['status'] = 'calc'
    chiller1_evap_nwk['ch1_e_nwk_grad1'] = ch1_e_nwk_grad1     

    ##6
    ch1_e_nwk_grad2 = {}
    ch1_e_nwk_grad2['value'] = ch1_e_nwk_calc[1,0]
    ch1_e_nwk_grad2['units'] = '-'
    ch1_e_nwk_grad2['status'] = 'calc'
    chiller1_evap_nwk['ch1_e_nwk_grad2'] = ch1_e_nwk_grad2     

    ##7
    ch1_e_nwk_grad3 = {}
    ch1_e_nwk_grad3['value'] = ch1_e_nwk_calc[2,0]
    ch1_e_nwk_grad3['units'] = '-'
    ch1_e_nwk_grad3['status'] = 'calc'
    chiller1_evap_nwk['ch1_e_nwk_grad3'] = ch1_e_nwk_grad3

    ##8
    ch1_e_nwk_grad4 = {}
    ch1_e_nwk_grad4['value'] = ch1_e_nwk_calc[3,0]
    ch1_e_nwk_grad4['units'] = '-'
    ch1_e_nwk_grad4['status'] = 'calc'
    chiller1_evap_nwk['ch1_e_nwk_grad4'] = ch1_e_nwk_grad4

    ##9
    ch1_e_nwk_int1 = {}
    ch1_e_nwk_int1['value'] = ch1_e_nwk_calc[4,0]
    ch1_e_nwk_int1['units'] = '-'
    ch1_e_nwk_int1['status'] = 'calc'
    chiller1_evap_nwk['ch1_e_nwk_int1'] = ch1_e_nwk_int1

    ##10
    ch1_e_nwk_int2 = {}
    ch1_e_nwk_int2['value'] = ch1_e_nwk_calc[5,0]
    ch1_e_nwk_int2['units'] = '-'
    ch1_e_nwk_int2['status'] = 'calc'
    chiller1_evap_nwk['ch1_e_nwk_int2'] = ch1_e_nwk_int2

    ##11
    ch1_e_nwk_int3 = {}
    ch1_e_nwk_int3['value'] = ch1_e_nwk_calc[6,0]
    ch1_e_nwk_int3['units'] = '-'
    ch1_e_nwk_int3['status'] = 'calc'
    chiller1_evap_nwk['ch1_e_nwk_int3'] = ch1_e_nwk_int3

    ##12
    ch1_e_nwk_int4 = {}
    ch1_e_nwk_int4['value'] = ch1_e_nwk_calc[7,0]
    ch1_e_nwk_int4['units'] = '-'
    ch1_e_nwk_int4['status'] = 'calc'
    chiller1_evap_nwk['ch1_e_nwk_int4'] = ch1_e_nwk_int4

    ##13
    ch1_e_nwk_f1 = {}
    ch1_e_nwk_f1['value'] = ch1_e_nwk_calc[8,0]
    ch1_e_nwk_f1['units'] = '-'
    ch1_e_nwk_f1['status'] = 'calc'
    chiller1_evap_nwk['ch1_e_nwk_f1'] = ch1_e_nwk_f1

    ##14
    ch1_e_nwk_f2 = {}
    ch1_e_nwk_f2['value'] = ch1_e_nwk_calc[9,0]
    ch1_e_nwk_f2['units'] = '-'
    ch1_e_nwk_f2['status'] = 'calc'
    chiller1_evap_nwk['ch1_e_nwk_f2'] = ch1_e_nwk_f2

    ##15
    ch1_e_nwk_f3 = {}
    ch1_e_nwk_f3['value'] = ch1_e_nwk_calc[10,0]
    ch1_e_nwk_f3['units'] = '-'
    ch1_e_nwk_f3['status'] = 'calc'
    chiller1_evap_nwk['ch1_e_nwk_f3'] = ch1_e_nwk_f3

    ##16
    ch1_e_nwk_f4 = {}
    ch1_e_nwk_f4['value'] = ch1_e_nwk_calc[11,0]
    ch1_e_nwk_f4['units'] = '-'
    ch1_e_nwk_f4['status'] = 'calc'
    chiller1_evap_nwk['ch1_e_nwk_f4'] = ch1_e_nwk_f4

    ##17
    ch1_e_nwk_f5 = {}
    ch1_e_nwk_f5['value'] = ch1_e_nwk_calc[12,0]
    ch1_e_nwk_f5['units'] = '-'
    ch1_e_nwk_f5['status'] = 'calc'
    chiller1_evap_nwk['ch1_e_nwk_f5'] = ch1_e_nwk_f5

    ##Unit definition 
    
    ##Unit 1
    ch1_e_nwk_1 = {}
    ch1_e_nwk_1['Name'] = 'ch1_e_nwk_1'
    ch1_e_nwk_1['Variable1'] = 'm_perc'         ##Percentage of total flowrate which goes to chiller 1
    ch1_e_nwk_1['Variable2'] = '-'
    ch1_e_nwk_1['Fmin_v1'] = chiller1_evap_nwk['ch1_e_nwk_f1']['value']
    ch1_e_nwk_1['Fmax_v1'] = chiller1_evap_nwk['ch1_e_nwk_f2']['value']
    ch1_e_nwk_1['Fmin_v2'] = 0                                                
    ch1_e_nwk_1['Fmax_v2'] = 0
    ch1_e_nwk_1['Coeff_v1_2'] = 0                                                                                 
    ch1_e_nwk_1['Coeff_v1_1'] = 0                                                 
    ch1_e_nwk_1['Coeff_v2_2'] = 0
    ch1_e_nwk_1['Coeff_v2_1'] = 0
    ch1_e_nwk_1['Coeff_v1_v2'] = 0
    ch1_e_nwk_1['Coeff_cst'] = 0
    ch1_e_nwk_1['Fmin'] = 0
    ch1_e_nwk_1['Fmax'] = 0
    ch1_e_nwk_1['Cost_v1_2'] = 0
    ch1_e_nwk_1['Cost_v1_1'] = 0
    ch1_e_nwk_1['Cost_v2_2'] = 0
    ch1_e_nwk_1['Cost_v2_1'] = 0
    ch1_e_nwk_1['Cost_v1_v2'] = 0
    ch1_e_nwk_1['Cost_cst'] = 0
    ch1_e_nwk_1['Cinv_v1_2'] = 0
    ch1_e_nwk_1['Cinv_v1_1'] = 0
    ch1_e_nwk_1['Cinv_v2_2'] = 0
    ch1_e_nwk_1['Cinv_v2_1'] = 0
    ch1_e_nwk_1['Cinv_v1_v2'] = 0
    ch1_e_nwk_1['Cinv_cst'] = 0
    ch1_e_nwk_1['Power_v1_2'] = 0
    ch1_e_nwk_1['Power_v1_1'] = 0
    ch1_e_nwk_1['Power_v2_2'] = 0
    ch1_e_nwk_1['Power_v2_1'] = 0
    ch1_e_nwk_1['Power_v1_v2'] = 0
    ch1_e_nwk_1['Power_cst'] = 0
    ch1_e_nwk_1['Impact_v1_2'] = 0
    ch1_e_nwk_1['Impact_v1_1'] = 0
    ch1_e_nwk_1['Impact_v2_2'] = 0
    ch1_e_nwk_1['Impact_v2_1'] = 0
    ch1_e_nwk_1['Impact_v1_v2'] = 0
    ch1_e_nwk_1['Impact_cst'] = 0

    unitinput = [ch1_e_nwk_1['Name'], ch1_e_nwk_1['Variable1'], ch1_e_nwk_1['Variable2'], ch1_e_nwk_1['Fmin_v1'], ch1_e_nwk_1['Fmax_v1'], ch1_e_nwk_1['Fmin_v2'], ch1_e_nwk_1['Fmax_v2'], ch1_e_nwk_1['Coeff_v1_2'], 
                ch1_e_nwk_1['Coeff_v1_1'], ch1_e_nwk_1['Coeff_v2_2'], ch1_e_nwk_1['Coeff_v2_1'], ch1_e_nwk_1['Coeff_v1_v2'], ch1_e_nwk_1['Coeff_cst'], ch1_e_nwk_1['Fmin'], ch1_e_nwk_1['Fmax'], ch1_e_nwk_1['Cost_v1_2'], 
                ch1_e_nwk_1['Cost_v1_1'], ch1_e_nwk_1['Cost_v2_2'], ch1_e_nwk_1['Cost_v2_1'], ch1_e_nwk_1['Cost_v1_v2'], ch1_e_nwk_1['Cost_cst'], ch1_e_nwk_1['Cinv_v1_2'], ch1_e_nwk_1['Cinv_v1_1'], ch1_e_nwk_1['Cinv_v2_2'], 
                ch1_e_nwk_1['Cinv_v2_1'], ch1_e_nwk_1['Cinv_v1_v2'], ch1_e_nwk_1['Cinv_cst'], ch1_e_nwk_1['Power_v1_2'], ch1_e_nwk_1['Power_v1_1'], ch1_e_nwk_1['Power_v2_2'], ch1_e_nwk_1['Power_v2_1'], 
                ch1_e_nwk_1['Power_v1_v2'], ch1_e_nwk_1['Power_cst'], ch1_e_nwk_1['Impact_v1_2'], ch1_e_nwk_1['Impact_v1_1'], ch1_e_nwk_1['Impact_v2_2'], ch1_e_nwk_1['Impact_v2_1'], ch1_e_nwk_1['Impact_v1_v2'], 
                ch1_e_nwk_1['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)       
    
    ##Unit 2
    ch1_e_nwk_2 = {}
    ch1_e_nwk_2['Name'] = 'ch1_e_nwk_2'
    ch1_e_nwk_2['Variable1'] = 'm_perc'         ##Percentage of total flowrate which goes to chiller 1
    ch1_e_nwk_2['Variable2'] = '-'
    ch1_e_nwk_2['Fmin_v1'] = chiller1_evap_nwk['ch1_e_nwk_f2']['value']
    ch1_e_nwk_2['Fmax_v1'] = chiller1_evap_nwk['ch1_e_nwk_f3']['value']
    ch1_e_nwk_2['Fmin_v2'] = 0                                                
    ch1_e_nwk_2['Fmax_v2'] = 0
    ch1_e_nwk_2['Coeff_v1_2'] = 0                                                                                 
    ch1_e_nwk_2['Coeff_v1_1'] = 0                                                 
    ch1_e_nwk_2['Coeff_v2_2'] = 0
    ch1_e_nwk_2['Coeff_v2_1'] = 0
    ch1_e_nwk_2['Coeff_v1_v2'] = 0
    ch1_e_nwk_2['Coeff_cst'] = 0
    ch1_e_nwk_2['Fmin'] = 0
    ch1_e_nwk_2['Fmax'] = 0
    ch1_e_nwk_2['Cost_v1_2'] = 0
    ch1_e_nwk_2['Cost_v1_1'] = 0
    ch1_e_nwk_2['Cost_v2_2'] = 0
    ch1_e_nwk_2['Cost_v2_1'] = 0
    ch1_e_nwk_2['Cost_v1_v2'] = 0
    ch1_e_nwk_2['Cost_cst'] = 0
    ch1_e_nwk_2['Cinv_v1_2'] = 0
    ch1_e_nwk_2['Cinv_v1_1'] = 0
    ch1_e_nwk_2['Cinv_v2_2'] = 0
    ch1_e_nwk_2['Cinv_v2_1'] = 0
    ch1_e_nwk_2['Cinv_v1_v2'] = 0
    ch1_e_nwk_2['Cinv_cst'] = 0
    ch1_e_nwk_2['Power_v1_2'] = 0
    ch1_e_nwk_2['Power_v1_1'] = 0
    ch1_e_nwk_2['Power_v2_2'] = 0
    ch1_e_nwk_2['Power_v2_1'] = 0
    ch1_e_nwk_2['Power_v1_v2'] = 0
    ch1_e_nwk_2['Power_cst'] = 0
    ch1_e_nwk_2['Impact_v1_2'] = 0
    ch1_e_nwk_2['Impact_v1_1'] = 0
    ch1_e_nwk_2['Impact_v2_2'] = 0
    ch1_e_nwk_2['Impact_v2_1'] = 0
    ch1_e_nwk_2['Impact_v1_v2'] = 0
    ch1_e_nwk_2['Impact_cst'] = 0

    unitinput = [ch1_e_nwk_2['Name'], ch1_e_nwk_2['Variable1'], ch1_e_nwk_2['Variable2'], ch1_e_nwk_2['Fmin_v1'], ch1_e_nwk_2['Fmax_v1'], ch1_e_nwk_2['Fmin_v2'], ch1_e_nwk_2['Fmax_v2'], ch1_e_nwk_2['Coeff_v1_2'], 
                ch1_e_nwk_2['Coeff_v1_1'], ch1_e_nwk_2['Coeff_v2_2'], ch1_e_nwk_2['Coeff_v2_1'], ch1_e_nwk_2['Coeff_v1_v2'], ch1_e_nwk_2['Coeff_cst'], ch1_e_nwk_2['Fmin'], ch1_e_nwk_2['Fmax'], ch1_e_nwk_2['Cost_v1_2'], 
                ch1_e_nwk_2['Cost_v1_1'], ch1_e_nwk_2['Cost_v2_2'], ch1_e_nwk_2['Cost_v2_1'], ch1_e_nwk_2['Cost_v1_v2'], ch1_e_nwk_2['Cost_cst'], ch1_e_nwk_2['Cinv_v1_2'], ch1_e_nwk_2['Cinv_v1_1'], ch1_e_nwk_2['Cinv_v2_2'], 
                ch1_e_nwk_2['Cinv_v2_1'], ch1_e_nwk_2['Cinv_v1_v2'], ch1_e_nwk_2['Cinv_cst'], ch1_e_nwk_2['Power_v1_2'], ch1_e_nwk_2['Power_v1_1'], ch1_e_nwk_2['Power_v2_2'], ch1_e_nwk_2['Power_v2_1'], 
                ch1_e_nwk_2['Power_v1_v2'], ch1_e_nwk_2['Power_cst'], ch1_e_nwk_2['Impact_v1_2'], ch1_e_nwk_2['Impact_v1_1'], ch1_e_nwk_2['Impact_v2_2'], ch1_e_nwk_2['Impact_v2_1'], ch1_e_nwk_2['Impact_v1_v2'], 
                ch1_e_nwk_2['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)    
    
    ##Unit 3
    ch1_e_nwk_3 = {}
    ch1_e_nwk_3['Name'] = 'ch1_e_nwk_3'
    ch1_e_nwk_3['Variable1'] = 'm_perc'         ##Percentage of total flowrate which goes to chiller 1
    ch1_e_nwk_3['Variable2'] = '-'
    ch1_e_nwk_3['Fmin_v1'] = chiller1_evap_nwk['ch1_e_nwk_f3']['value']
    ch1_e_nwk_3['Fmax_v1'] = chiller1_evap_nwk['ch1_e_nwk_f4']['value']
    ch1_e_nwk_3['Fmin_v2'] = 0                                                
    ch1_e_nwk_3['Fmax_v2'] = 0
    ch1_e_nwk_3['Coeff_v1_2'] = 0                                                                                 
    ch1_e_nwk_3['Coeff_v1_1'] = 0                                                 
    ch1_e_nwk_3['Coeff_v2_2'] = 0
    ch1_e_nwk_3['Coeff_v2_1'] = 0
    ch1_e_nwk_3['Coeff_v1_v2'] = 0
    ch1_e_nwk_3['Coeff_cst'] = 0
    ch1_e_nwk_3['Fmin'] = 0
    ch1_e_nwk_3['Fmax'] = 0
    ch1_e_nwk_3['Cost_v1_2'] = 0
    ch1_e_nwk_3['Cost_v1_1'] = 0
    ch1_e_nwk_3['Cost_v2_2'] = 0
    ch1_e_nwk_3['Cost_v2_1'] = 0
    ch1_e_nwk_3['Cost_v1_v2'] = 0
    ch1_e_nwk_3['Cost_cst'] = 0
    ch1_e_nwk_3['Cinv_v1_2'] = 0
    ch1_e_nwk_3['Cinv_v1_1'] = 0
    ch1_e_nwk_3['Cinv_v2_2'] = 0
    ch1_e_nwk_3['Cinv_v2_1'] = 0
    ch1_e_nwk_3['Cinv_v1_v2'] = 0
    ch1_e_nwk_3['Cinv_cst'] = 0
    ch1_e_nwk_3['Power_v1_2'] = 0
    ch1_e_nwk_3['Power_v1_1'] = 0
    ch1_e_nwk_3['Power_v2_2'] = 0
    ch1_e_nwk_3['Power_v2_1'] = 0
    ch1_e_nwk_3['Power_v1_v2'] = 0
    ch1_e_nwk_3['Power_cst'] = 0
    ch1_e_nwk_3['Impact_v1_2'] = 0
    ch1_e_nwk_3['Impact_v1_1'] = 0
    ch1_e_nwk_3['Impact_v2_2'] = 0
    ch1_e_nwk_3['Impact_v2_1'] = 0
    ch1_e_nwk_3['Impact_v1_v2'] = 0
    ch1_e_nwk_3['Impact_cst'] = 0

    unitinput = [ch1_e_nwk_3['Name'], ch1_e_nwk_3['Variable1'], ch1_e_nwk_3['Variable2'], ch1_e_nwk_3['Fmin_v1'], ch1_e_nwk_3['Fmax_v1'], ch1_e_nwk_3['Fmin_v2'], ch1_e_nwk_3['Fmax_v2'], ch1_e_nwk_3['Coeff_v1_2'], 
                ch1_e_nwk_3['Coeff_v1_1'], ch1_e_nwk_3['Coeff_v2_2'], ch1_e_nwk_3['Coeff_v2_1'], ch1_e_nwk_3['Coeff_v1_v2'], ch1_e_nwk_3['Coeff_cst'], ch1_e_nwk_3['Fmin'], ch1_e_nwk_3['Fmax'], ch1_e_nwk_3['Cost_v1_2'], 
                ch1_e_nwk_3['Cost_v1_1'], ch1_e_nwk_3['Cost_v2_2'], ch1_e_nwk_3['Cost_v2_1'], ch1_e_nwk_3['Cost_v1_v2'], ch1_e_nwk_3['Cost_cst'], ch1_e_nwk_3['Cinv_v1_2'], ch1_e_nwk_3['Cinv_v1_1'], ch1_e_nwk_3['Cinv_v2_2'], 
                ch1_e_nwk_3['Cinv_v2_1'], ch1_e_nwk_3['Cinv_v1_v2'], ch1_e_nwk_3['Cinv_cst'], ch1_e_nwk_3['Power_v1_2'], ch1_e_nwk_3['Power_v1_1'], ch1_e_nwk_3['Power_v2_2'], ch1_e_nwk_3['Power_v2_1'], 
                ch1_e_nwk_3['Power_v1_v2'], ch1_e_nwk_3['Power_cst'], ch1_e_nwk_3['Impact_v1_2'], ch1_e_nwk_3['Impact_v1_1'], ch1_e_nwk_3['Impact_v2_2'], ch1_e_nwk_3['Impact_v2_1'], ch1_e_nwk_3['Impact_v1_v2'], 
                ch1_e_nwk_3['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True) 
    
    ##Unit 4
    ch1_e_nwk_4 = {}
    ch1_e_nwk_4['Name'] = 'ch1_e_nwk_4'
    ch1_e_nwk_4['Variable1'] = 'm_perc'         ##Percentage of total flowrate which goes to chiller 1
    ch1_e_nwk_4['Variable2'] = '-'
    ch1_e_nwk_4['Fmin_v1'] = chiller1_evap_nwk['ch1_e_nwk_f4']['value']
    ch1_e_nwk_4['Fmax_v1'] = chiller1_evap_nwk['ch1_e_nwk_f5']['value']
    ch1_e_nwk_4['Fmin_v2'] = 0                                                
    ch1_e_nwk_4['Fmax_v2'] = 0
    ch1_e_nwk_4['Coeff_v1_2'] = 0                                                                                 
    ch1_e_nwk_4['Coeff_v1_1'] = 0                                                 
    ch1_e_nwk_4['Coeff_v2_2'] = 0
    ch1_e_nwk_4['Coeff_v2_1'] = 0
    ch1_e_nwk_4['Coeff_v1_v2'] = 0
    ch1_e_nwk_4['Coeff_cst'] = 0
    ch1_e_nwk_4['Fmin'] = 0
    ch1_e_nwk_4['Fmax'] = 0
    ch1_e_nwk_4['Cost_v1_2'] = 0
    ch1_e_nwk_4['Cost_v1_1'] = 0
    ch1_e_nwk_4['Cost_v2_2'] = 0
    ch1_e_nwk_4['Cost_v2_1'] = 0
    ch1_e_nwk_4['Cost_v1_v2'] = 0
    ch1_e_nwk_4['Cost_cst'] = 0
    ch1_e_nwk_4['Cinv_v1_2'] = 0
    ch1_e_nwk_4['Cinv_v1_1'] = 0
    ch1_e_nwk_4['Cinv_v2_2'] = 0
    ch1_e_nwk_4['Cinv_v2_1'] = 0
    ch1_e_nwk_4['Cinv_v1_v2'] = 0
    ch1_e_nwk_4['Cinv_cst'] = 0
    ch1_e_nwk_4['Power_v1_2'] = 0
    ch1_e_nwk_4['Power_v1_1'] = 0
    ch1_e_nwk_4['Power_v2_2'] = 0
    ch1_e_nwk_4['Power_v2_1'] = 0
    ch1_e_nwk_4['Power_v1_v2'] = 0
    ch1_e_nwk_4['Power_cst'] = 0
    ch1_e_nwk_4['Impact_v1_2'] = 0
    ch1_e_nwk_4['Impact_v1_1'] = 0
    ch1_e_nwk_4['Impact_v2_2'] = 0
    ch1_e_nwk_4['Impact_v2_1'] = 0
    ch1_e_nwk_4['Impact_v1_v2'] = 0
    ch1_e_nwk_4['Impact_cst'] = 0

    unitinput = [ch1_e_nwk_4['Name'], ch1_e_nwk_4['Variable1'], ch1_e_nwk_4['Variable2'], ch1_e_nwk_4['Fmin_v1'], ch1_e_nwk_4['Fmax_v1'], ch1_e_nwk_4['Fmin_v2'], ch1_e_nwk_4['Fmax_v2'], ch1_e_nwk_4['Coeff_v1_2'], 
                ch1_e_nwk_4['Coeff_v1_1'], ch1_e_nwk_4['Coeff_v2_2'], ch1_e_nwk_4['Coeff_v2_1'], ch1_e_nwk_4['Coeff_v1_v2'], ch1_e_nwk_4['Coeff_cst'], ch1_e_nwk_4['Fmin'], ch1_e_nwk_4['Fmax'], ch1_e_nwk_4['Cost_v1_2'], 
                ch1_e_nwk_4['Cost_v1_1'], ch1_e_nwk_4['Cost_v2_2'], ch1_e_nwk_4['Cost_v2_1'], ch1_e_nwk_4['Cost_v1_v2'], ch1_e_nwk_4['Cost_cst'], ch1_e_nwk_4['Cinv_v1_2'], ch1_e_nwk_4['Cinv_v1_1'], ch1_e_nwk_4['Cinv_v2_2'], 
                ch1_e_nwk_4['Cinv_v2_1'], ch1_e_nwk_4['Cinv_v1_v2'], ch1_e_nwk_4['Cinv_cst'], ch1_e_nwk_4['Power_v1_2'], ch1_e_nwk_4['Power_v1_1'], ch1_e_nwk_4['Power_v2_2'], ch1_e_nwk_4['Power_v2_1'], 
                ch1_e_nwk_4['Power_v1_v2'], ch1_e_nwk_4['Power_cst'], ch1_e_nwk_4['Impact_v1_2'], ch1_e_nwk_4['Impact_v1_1'], ch1_e_nwk_4['Impact_v2_2'], ch1_e_nwk_4['Impact_v2_1'], ch1_e_nwk_4['Impact_v1_v2'], 
                ch1_e_nwk_4['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True) 

    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}                                                                ##Inlet flowrate stream 
    stream1['Parent'] = 'ch1_e_nwk_1'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'ch1_e_nwk_1_mf_in'
    stream1['Layer'] = 'ch1_2_evap_flow'
    stream1['Stream_coeff_v1_2'] = 0
    stream1['Stream_coeff_v1_1'] = chiller1_evap_nwk['ch1_e_nwk_totalflow']['value']
    stream1['Stream_coeff_v2_2'] = 0
    stream1['Stream_coeff_v2_1'] = 0
    stream1['Stream_coeff_v1_v2'] = 0
    stream1['Stream_coeff_cst'] = 0
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Parent'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Stream_coeff_v1_2'], stream1['Stream_coeff_v1_1'], stream1['Stream_coeff_v2_2'],
                   stream1['Stream_coeff_v2_1'], stream1['Stream_coeff_v1_v2'], stream1['Stream_coeff_cst'], stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 2
    stream2 = {}                                                                ##Outlet flowrate stream 
    stream2['Parent'] = 'ch1_e_nwk_1'
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'ch1_e_nwk_1_2_pump_flow'
    stream2['Layer'] = 'ch1_evap_2_pump_flow'
    stream2['Stream_coeff_v1_2'] = 0
    stream2['Stream_coeff_v1_1'] = chiller1_evap_nwk['ch1_e_nwk_totalflow']['value']
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
    stream3 = {}                                                                ##Outlet pressure-drop stream 
    stream3['Parent'] = 'ch1_e_nwk_1'
    stream3['Type'] = 'balancing_only'
    stream3['Name'] = 'ch1_e_nwk_1_2_pump_delp'
    stream3['Layer'] = 'ch1_evap_2_pump_delp'
    stream3['Stream_coeff_v1_2'] = 0
    stream3['Stream_coeff_v1_1'] = chiller1_evap_nwk['ch1_e_nwk_grad1']['value'] * chiller1_evap_nwk['ch1_e_nwk_totalflow']['value']
    stream3['Stream_coeff_v2_2'] = 0
    stream3['Stream_coeff_v2_1'] = 0
    stream3['Stream_coeff_v1_v2'] = 0
    stream3['Stream_coeff_cst'] = chiller1_evap_nwk['ch1_e_nwk_int1']['value']
    stream3['InOut'] = 'out'
    
    streaminput = [stream3['Parent'], stream3['Type'], stream3['Name'], stream3['Layer'], stream3['Stream_coeff_v1_2'], stream3['Stream_coeff_v1_1'], stream3['Stream_coeff_v2_2'],
                   stream3['Stream_coeff_v2_1'], stream3['Stream_coeff_v1_v2'], stream3['Stream_coeff_cst'], stream3['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 4
    stream4 = {}                                                                ##Inlet flowrate stream 
    stream4['Parent'] = 'ch1_e_nwk_2'
    stream4['Type'] = 'balancing_only'
    stream4['Name'] = 'ch1_e_nwk_1_mf_in'
    stream4['Layer'] = 'ch1_2_evap_flow'
    stream4['Stream_coeff_v1_2'] = 0
    stream4['Stream_coeff_v1_1'] = chiller1_evap_nwk['ch1_e_nwk_totalflow']['value']
    stream4['Stream_coeff_v2_2'] = 0
    stream4['Stream_coeff_v2_1'] = 0
    stream4['Stream_coeff_v1_v2'] = 0
    stream4['Stream_coeff_cst'] = 0
    stream4['InOut'] = 'in'
    
    streaminput = [stream4['Parent'], stream4['Type'], stream4['Name'], stream4['Layer'], stream4['Stream_coeff_v1_2'], stream4['Stream_coeff_v1_1'], stream4['Stream_coeff_v2_2'],
                   stream4['Stream_coeff_v2_1'], stream4['Stream_coeff_v1_v2'], stream4['Stream_coeff_cst'], stream4['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 5
    stream5 = {}                                                                ##Outlet flowrate stream 
    stream5['Parent'] = 'ch1_e_nwk_2'
    stream5['Type'] = 'balancing_only'
    stream5['Name'] = 'ch1_e_nwk_2_2_pump_flow'
    stream5['Layer'] = 'ch1_evap_2_pump_flow'
    stream5['Stream_coeff_v1_2'] = 0
    stream5['Stream_coeff_v1_1'] = chiller1_evap_nwk['ch1_e_nwk_totalflow']['value']
    stream5['Stream_coeff_v2_2'] = 0
    stream5['Stream_coeff_v2_1'] = 0
    stream5['Stream_coeff_v1_v2'] = 0
    stream5['Stream_coeff_cst'] = 0
    stream5['InOut'] = 'out'
    
    streaminput = [stream5['Parent'], stream5['Type'], stream5['Name'], stream5['Layer'], stream5['Stream_coeff_v1_2'], stream5['Stream_coeff_v1_1'], stream5['Stream_coeff_v2_2'],
                   stream5['Stream_coeff_v2_1'], stream5['Stream_coeff_v1_v2'], stream5['Stream_coeff_cst'], stream5['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 6
    stream6 = {}                                                                ##Outlet pressure-drop stream 
    stream6['Parent'] = 'ch1_e_nwk_2'
    stream6['Type'] = 'balancing_only'
    stream6['Name'] = 'ch1_e_nwk_2_pump_delp'
    stream6['Layer'] = 'ch1_evap_2_pump_delp'
    stream6['Stream_coeff_v1_2'] = 0
    stream6['Stream_coeff_v1_1'] = chiller1_evap_nwk['ch1_e_nwk_grad2']['value'] * chiller1_evap_nwk['ch1_e_nwk_totalflow']['value']
    stream6['Stream_coeff_v2_2'] = 0
    stream6['Stream_coeff_v2_1'] = 0
    stream6['Stream_coeff_v1_v2'] = 0
    stream6['Stream_coeff_cst'] = chiller1_evap_nwk['ch1_e_nwk_int2']['value']
    stream6['InOut'] = 'out'
    
    streaminput = [stream6['Parent'], stream6['Type'], stream6['Name'], stream6['Layer'], stream6['Stream_coeff_v1_2'], stream6['Stream_coeff_v1_1'], stream6['Stream_coeff_v2_2'],
                   stream6['Stream_coeff_v2_1'], stream6['Stream_coeff_v1_v2'], stream6['Stream_coeff_cst'], stream6['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 7
    stream7 = {}                                                                ##Inlet flowrate stream 
    stream7['Parent'] = 'ch1_e_nwk_3'
    stream7['Type'] = 'balancing_only'
    stream7['Name'] = 'ch1_e_nwk_1_mf_in'
    stream7['Layer'] = 'ch1_2_evap_flow'
    stream7['Stream_coeff_v1_2'] = 0
    stream7['Stream_coeff_v1_1'] = chiller1_evap_nwk['ch1_e_nwk_totalflow']['value']
    stream7['Stream_coeff_v2_2'] = 0
    stream7['Stream_coeff_v2_1'] = 0
    stream7['Stream_coeff_v1_v2'] = 0
    stream7['Stream_coeff_cst'] = 0
    stream7['InOut'] = 'in'
    
    streaminput = [stream7['Parent'], stream7['Type'], stream7['Name'], stream7['Layer'], stream7['Stream_coeff_v1_2'], stream7['Stream_coeff_v1_1'], stream7['Stream_coeff_v2_2'],
                   stream7['Stream_coeff_v2_1'], stream7['Stream_coeff_v1_v2'], stream7['Stream_coeff_cst'], stream7['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 8
    stream8 = {}                                                                ##Outlet flowrate stream 
    stream8['Parent'] = 'ch1_e_nwk_3'
    stream8['Type'] = 'balancing_only'
    stream8['Name'] = 'ch1_e_nwk_1_2_pump_flow'
    stream8['Layer'] = 'ch1_evap_2_pump_flow'
    stream8['Stream_coeff_v1_2'] = 0
    stream8['Stream_coeff_v1_1'] = chiller1_evap_nwk['ch1_e_nwk_totalflow']['value']
    stream8['Stream_coeff_v2_2'] = 0
    stream8['Stream_coeff_v2_1'] = 0
    stream8['Stream_coeff_v1_v2'] = 0
    stream8['Stream_coeff_cst'] = 0
    stream8['InOut'] = 'out'
    
    streaminput = [stream8['Parent'], stream8['Type'], stream8['Name'], stream8['Layer'], stream8['Stream_coeff_v1_2'], stream8['Stream_coeff_v1_1'], stream8['Stream_coeff_v2_2'],
                   stream8['Stream_coeff_v2_1'], stream8['Stream_coeff_v1_v2'], stream8['Stream_coeff_cst'], stream8['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 9
    stream9 = {}                                                                ##Outlet pressure-drop stream 
    stream9['Parent'] = 'ch1_e_nwk_3'
    stream9['Type'] = 'balancing_only'
    stream9['Name'] = 'ch1_e_nwk_1_2_pump_delp'
    stream9['Layer'] = 'ch1_evap_2_pump_delp'
    stream9['Stream_coeff_v1_2'] = 0
    stream9['Stream_coeff_v1_1'] = chiller1_evap_nwk['ch1_e_nwk_grad3']['value'] * chiller1_evap_nwk['ch1_e_nwk_totalflow']['value']
    stream9['Stream_coeff_v2_2'] = 0
    stream9['Stream_coeff_v2_1'] = 0
    stream9['Stream_coeff_v1_v2'] = 0
    stream9['Stream_coeff_cst'] = chiller1_evap_nwk['ch1_e_nwk_int3']['value']
    stream9['InOut'] = 'out'
    
    streaminput = [stream9['Parent'], stream9['Type'], stream9['Name'], stream9['Layer'], stream9['Stream_coeff_v1_2'], stream9['Stream_coeff_v1_1'], stream9['Stream_coeff_v2_2'],
                   stream9['Stream_coeff_v2_1'], stream9['Stream_coeff_v1_v2'], stream9['Stream_coeff_cst'], stream9['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 10
    stream10 = {}                                                                ##Inlet flowrate stream 
    stream10['Parent'] = 'ch1_e_nwk_4'
    stream10['Type'] = 'balancing_only'
    stream10['Name'] = 'ch1_e_nwk_1_mf_in'
    stream10['Layer'] = 'ch1_2_evap_flow'
    stream10['Stream_coeff_v1_2'] = 0
    stream10['Stream_coeff_v1_1'] = chiller1_evap_nwk['ch1_e_nwk_totalflow']['value']
    stream10['Stream_coeff_v2_2'] = 0
    stream10['Stream_coeff_v2_1'] = 0
    stream10['Stream_coeff_v1_v2'] = 0
    stream10['Stream_coeff_cst'] = 0
    stream10['InOut'] = 'in'
    
    streaminput = [stream10['Parent'], stream10['Type'], stream10['Name'], stream10['Layer'], stream10['Stream_coeff_v1_2'], stream10['Stream_coeff_v1_1'], stream10['Stream_coeff_v2_2'],
                   stream10['Stream_coeff_v2_1'], stream10['Stream_coeff_v1_v2'], stream10['Stream_coeff_cst'], stream10['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 11
    stream11 = {}                                                                ##Outlet flowrate stream 
    stream11['Parent'] = 'ch1_e_nwk_4'
    stream11['Type'] = 'balancing_only'
    stream11['Name'] = 'ch1_e_nwk_1_2_pump_flow'
    stream11['Layer'] = 'ch1_evap_2_pump_flow'
    stream11['Stream_coeff_v1_2'] = 0
    stream11['Stream_coeff_v1_1'] = chiller1_evap_nwk['ch1_e_nwk_totalflow']['value']
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
    
    ##Stream 12
    stream12 = {}                                                                ##Outlet pressure-drop stream 
    stream12['Parent'] = 'ch1_e_nwk_4'
    stream12['Type'] = 'balancing_only'
    stream12['Name'] = 'ch1_e_nwk_1_2_pump_delp'
    stream12['Layer'] = 'ch1_evap_2_pump_delp'
    stream12['Stream_coeff_v1_2'] = 0
    stream12['Stream_coeff_v1_1'] = chiller1_evap_nwk['ch1_e_nwk_grad4']['value'] * chiller1_evap_nwk['ch1_e_nwk_totalflow']['value']
    stream12['Stream_coeff_v2_2'] = 0
    stream12['Stream_coeff_v2_1'] = 0
    stream12['Stream_coeff_v1_v2'] = 0
    stream12['Stream_coeff_cst'] = chiller1_evap_nwk['ch1_e_nwk_int4']['value']
    stream12['InOut'] = 'out'
    
    streaminput = [stream12['Parent'], stream12['Type'], stream12['Name'], stream12['Layer'], stream12['Stream_coeff_v1_2'], stream12['Stream_coeff_v1_1'], stream12['Stream_coeff_v2_2'],
                   stream12['Stream_coeff_v2_1'], stream12['Stream_coeff_v1_v2'], stream12['Stream_coeff_cst'], stream12['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Constraint definition
    
    ##Equation definitions
    
    eqn1 = {}
    eqn1['Name'] = 'totaluse_ch1_e_nwk'
    eqn1['Type'] = 'unit_binary'
    eqn1['Sign'] = 'less_than_equal_to'
    eqn1['RHS_value'] = 1
    
    eqninput = [eqn1['Name'], eqn1['Type'], eqn1['Sign'], eqn1['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation terms 
    
    ##Term 1
    term1 = {}
    term1['Parent_unit'] = 'ch1_e_nwk_1'
    term1['Parent_eqn'] = 'totaluse_ch1_e_nwk'
    term1['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types 
    term1['Coefficient'] = 1
    term1['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
    term1['Coeff_v1_1'] = 0
    term1['Coeff_v2_2'] = 0
    term1['Coeff_v2_1'] = 0
    term1['Coeff_v1v2'] = 0
    term1['Coeff_cst'] = 0

    terminput = [term1['Parent_unit'], term1['Parent_eqn'], term1['Parent_stream'], term1['Coefficient'], term1['Coeff_v1_2'],
                 term1['Coeff_v1_1'], term1['Coeff_v2_2'], term1['Coeff_v2_1'], term1['Coeff_v1v2'], term1['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    ##Term 2
    term2 = {}
    term2['Parent_unit'] = 'ch1_e_nwk_2'
    term2['Parent_eqn'] = 'totaluse_ch1_e_nwk'
    term2['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types 
    term2['Coefficient'] = 1
    term2['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
    term2['Coeff_v1_1'] = 0
    term2['Coeff_v2_2'] = 0
    term2['Coeff_v2_1'] = 0
    term2['Coeff_v1v2'] = 0
    term2['Coeff_cst'] = 0

    terminput = [term2['Parent_unit'], term2['Parent_eqn'], term2['Parent_stream'], term2['Coefficient'], term2['Coeff_v1_2'],
                 term2['Coeff_v1_1'], term2['Coeff_v2_2'], term2['Coeff_v2_1'], term2['Coeff_v1v2'], term2['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    ##Term 3
    term3 = {}
    term3['Parent_unit'] = 'ch1_e_nwk_3'
    term3['Parent_eqn'] = 'totaluse_ch1_e_nwk'
    term3['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types 
    term3['Coefficient'] = 1
    term3['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
    term3['Coeff_v1_1'] = 0
    term3['Coeff_v2_2'] = 0
    term3['Coeff_v2_1'] = 0
    term3['Coeff_v1v2'] = 0
    term3['Coeff_cst'] = 0

    terminput = [term3['Parent_unit'], term3['Parent_eqn'], term3['Parent_stream'], term3['Coefficient'], term3['Coeff_v1_2'],
                 term3['Coeff_v1_1'], term3['Coeff_v2_2'], term3['Coeff_v2_1'], term3['Coeff_v1v2'], term3['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    ##Term 4
    term4 = {}
    term4['Parent_unit'] = 'ch1_e_nwk_4'
    term4['Parent_eqn'] = 'totaluse_ch1_e_nwk'
    term4['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types 
    term4['Coefficient'] = 1
    term4['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
    term4['Coeff_v1_1'] = 0
    term4['Coeff_v2_2'] = 0
    term4['Coeff_v2_1'] = 0
    term4['Coeff_v1v2'] = 0
    term4['Coeff_cst'] = 0

    terminput = [term4['Parent_unit'], term4['Parent_eqn'], term4['Parent_stream'], term4['Coefficient'], term4['Coeff_v1_2'],
                 term4['Coeff_v1_1'], term4['Coeff_v2_2'], term4['Coeff_v2_1'], term4['Coeff_v1v2'], term4['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms