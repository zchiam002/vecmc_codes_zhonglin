##This is the PFA network model, piecewise linearity is needed to account for the pressure drop flowrate linearity  

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type

def pfa_network (pfa_nwk_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    from pfa_network_compute import pfa_network_compute
    import pandas as pd
    import numpy as np
    
    ##Model description: 
    ##PFA network, accounts for pressure drop only

    ##Define dictionary of values 

    pfa_network = {}

    ##Defined constants
    
    ##1
    pfa_nwk_pfacoeff = {}
    pfa_nwk_pfacoeff['value'] = 0.0029069767441860417
    pfa_nwk_pfacoeff['units'] = '-'
    pfa_nwk_pfacoeff['status'] = 'cst'
    pfa_network['pfa_nwk_pfacoeff'] = pfa_nwk_pfacoeff

    ##2        
    pfa_nwk_pfamaxflow = {}
    pfa_nwk_pfamaxflow['value'] = 300
    pfa_nwk_pfamaxflow['units'] = 'm3/h'
    pfa_nwk_pfamaxflow['status'] = 'cst'
    pfa_network['pfa_nwk_pfamaxflow'] = pfa_nwk_pfamaxflow   

    ##Dependent constants
    pfa_nwk_dc = np.zeros((2,1))                                                #initialize the list, note the number of constants
    
    pfa_nwk_dc[0,0] = pfa_network['pfa_nwk_pfacoeff']['value']
    pfa_nwk_dc[1,0] = pfa_network['pfa_nwk_pfamaxflow']['value']

    pfa_nwk_calc = pfa_network_compute(pfa_nwk_dc)
    
    ##3
    pfa_nwk_pfa_grad1 = {}
    pfa_nwk_pfa_grad1['value'] = pfa_nwk_calc[0,0]                                                           
    pfa_nwk_pfa_grad1['units'] = '-'
    pfa_nwk_pfa_grad1['status'] = 'calc'
    pfa_network['pfa_nwk_pfa_grad1'] = pfa_nwk_pfa_grad1

    ##4
    pfa_nwk_pfa_grad2 = {}
    pfa_nwk_pfa_grad2['value'] = pfa_nwk_calc[1,0]                                                           
    pfa_nwk_pfa_grad2['units'] = '-'
    pfa_nwk_pfa_grad2['status'] = 'calc'
    pfa_network['pfa_nwk_pfa_grad2'] = pfa_nwk_pfa_grad2

    ##5
    pfa_nwk_pfa_grad3 = {}
    pfa_nwk_pfa_grad3['value'] = pfa_nwk_calc[2,0]                                                           
    pfa_nwk_pfa_grad3['units'] = '-'
    pfa_nwk_pfa_grad3['status'] = 'calc'
    pfa_network['pfa_nwk_pfa_grad3'] = pfa_nwk_pfa_grad3

    ##6
    pfa_nwk_pfa_grad4 = {}
    pfa_nwk_pfa_grad4['value'] = pfa_nwk_calc[3,0]                                                           
    pfa_nwk_pfa_grad4['units'] = '-'
    pfa_nwk_pfa_grad4['status'] = 'calc'
    pfa_network['pfa_nwk_pfa_grad4'] = pfa_nwk_pfa_grad4

    ##7
    pfa_nwk_pfa_int1 = {}
    pfa_nwk_pfa_int1['value'] = pfa_nwk_calc[4,0]                                                           
    pfa_nwk_pfa_int1['units'] = '-'
    pfa_nwk_pfa_int1['status'] = 'calc'
    pfa_network['pfa_nwk_pfa_int1'] = pfa_nwk_pfa_int1

    ##8
    pfa_nwk_pfa_int2 = {}
    pfa_nwk_pfa_int2['value'] = pfa_nwk_calc[5,0]                                                           
    pfa_nwk_pfa_int2['units'] = '-'
    pfa_nwk_pfa_int2['status'] = 'calc'
    pfa_network['pfa_nwk_pfa_int2'] = pfa_nwk_pfa_int2

    ##9
    pfa_nwk_pfa_int3 = {}
    pfa_nwk_pfa_int3['value'] = pfa_nwk_calc[6,0]                                                           
    pfa_nwk_pfa_int3['units'] = '-'
    pfa_nwk_pfa_int3['status'] = 'calc'
    pfa_network['pfa_nwk_pfa_int3'] = pfa_nwk_pfa_int3

    ##10
    pfa_nwk_pfa_int4 = {}
    pfa_nwk_pfa_int4['value'] = pfa_nwk_calc[7,0]                                                           
    pfa_nwk_pfa_int4['units'] = '-'
    pfa_nwk_pfa_int4['status'] = 'calc'
    pfa_network['pfa_nwk_pfa_int4'] = pfa_nwk_pfa_int4

    ##11
    pfa_nwk_f1 = {}
    pfa_nwk_f1['value'] = pfa_nwk_calc[8,0]
    pfa_nwk_f1['units'] = '-'
    pfa_nwk_f1['status'] = 'calc'
    pfa_network['pfa_nwk_f1'] = pfa_nwk_f1

    ##12
    pfa_nwk_f2 = {}
    pfa_nwk_f2['value'] = pfa_nwk_calc[9,0]
    pfa_nwk_f2['units'] = '-'
    pfa_nwk_f2['status'] = 'calc'
    pfa_network['pfa_nwk_f2'] = pfa_nwk_f2

    ##13
    pfa_nwk_f3 = {}
    pfa_nwk_f3['value'] = pfa_nwk_calc[10,0]
    pfa_nwk_f3['units'] = '-'
    pfa_nwk_f3['status'] = 'calc'
    pfa_network['pfa_nwk_f3'] = pfa_nwk_f3

    ##14
    pfa_nwk_f4 = {}
    pfa_nwk_f4['value'] = pfa_nwk_calc[11,0]
    pfa_nwk_f4['units'] = '-'
    pfa_nwk_f4['status'] = 'calc'
    pfa_network['pfa_nwk_f4'] = pfa_nwk_f4

    ##15
    pfa_nwk_f5 = {}
    pfa_nwk_f5['value'] = pfa_nwk_calc[12,0]
    pfa_nwk_f5['units'] = '-'
    pfa_nwk_f5['status'] = 'calc'
    pfa_network['pfa_nwk_f5'] = pfa_nwk_f5

    ##Unit definition 
    
    ##Unit 1
    pfa_nwk_1 = {}
    pfa_nwk_1['Name'] = 'pfa_nwk_1'
    pfa_nwk_1['Variable1'] = 'm_pfa'                                                                            ##Flowrate to pfa
    pfa_nwk_1['Variable2'] = '-'
    pfa_nwk_1['Fmin_v1'] = pfa_network['pfa_nwk_f1']['value'] * pfa_network['pfa_nwk_pfamaxflow']['value']      ##Minimum value of flow to pfa
    pfa_nwk_1['Fmax_v1'] = pfa_network['pfa_nwk_f2']['value'] * pfa_network['pfa_nwk_pfamaxflow']['value']      ##Maximum value of flow to pfa 
    pfa_nwk_1['Fmin_v2'] = 0                                                
    pfa_nwk_1['Fmax_v2'] = 0
    pfa_nwk_1['Coeff_v1_2'] = 0                                                                                 ##This is linear, no need for repeated constraints                                           
    pfa_nwk_1['Coeff_v1_1'] = 0                                                 
    pfa_nwk_1['Coeff_v2_2'] = 0
    pfa_nwk_1['Coeff_v2_1'] = 0
    pfa_nwk_1['Coeff_v1_v2'] = 0
    pfa_nwk_1['Coeff_cst'] = 0
    pfa_nwk_1['Fmin'] = 0
    pfa_nwk_1['Fmax'] = 0
    pfa_nwk_1['Cost_v1_2'] = 0
    pfa_nwk_1['Cost_v1_1'] = 0
    pfa_nwk_1['Cost_v2_2'] = 0
    pfa_nwk_1['Cost_v2_1'] = 0
    pfa_nwk_1['Cost_v1_v2'] = 0
    pfa_nwk_1['Cost_cst'] = 0
    pfa_nwk_1['Cinv_v1_2'] = 0
    pfa_nwk_1['Cinv_v1_1'] = 0
    pfa_nwk_1['Cinv_v2_2'] = 0
    pfa_nwk_1['Cinv_v2_1'] = 0
    pfa_nwk_1['Cinv_v1_v2'] = 0
    pfa_nwk_1['Cinv_cst'] = 0
    pfa_nwk_1['Power_v1_2'] = 0
    pfa_nwk_1['Power_v1_1'] = 0
    pfa_nwk_1['Power_v2_2'] = 0
    pfa_nwk_1['Power_v2_1'] = 0
    pfa_nwk_1['Power_v1_v2'] = 0
    pfa_nwk_1['Power_cst'] = 0
    pfa_nwk_1['Impact_v1_2'] = 0
    pfa_nwk_1['Impact_v1_1'] = 0
    pfa_nwk_1['Impact_v2_2'] = 0
    pfa_nwk_1['Impact_v2_1'] = 0
    pfa_nwk_1['Impact_v1_v2'] = 0
    pfa_nwk_1['Impact_cst'] = 0

    unitinput = [pfa_nwk_1['Name'], pfa_nwk_1['Variable1'], pfa_nwk_1['Variable2'], pfa_nwk_1['Fmin_v1'], pfa_nwk_1['Fmax_v1'], pfa_nwk_1['Fmin_v2'], pfa_nwk_1['Fmax_v2'], pfa_nwk_1['Coeff_v1_2'], 
                pfa_nwk_1['Coeff_v1_1'], pfa_nwk_1['Coeff_v2_2'], pfa_nwk_1['Coeff_v2_1'], pfa_nwk_1['Coeff_v1_v2'], pfa_nwk_1['Coeff_cst'], pfa_nwk_1['Fmin'], pfa_nwk_1['Fmax'], pfa_nwk_1['Cost_v1_2'], 
                pfa_nwk_1['Cost_v1_1'], pfa_nwk_1['Cost_v2_2'], pfa_nwk_1['Cost_v2_1'], pfa_nwk_1['Cost_v1_v2'], pfa_nwk_1['Cost_cst'], pfa_nwk_1['Cinv_v1_2'], pfa_nwk_1['Cinv_v1_1'], pfa_nwk_1['Cinv_v2_2'], 
                pfa_nwk_1['Cinv_v2_1'], pfa_nwk_1['Cinv_v1_v2'], pfa_nwk_1['Cinv_cst'], pfa_nwk_1['Power_v1_2'], pfa_nwk_1['Power_v1_1'], pfa_nwk_1['Power_v2_2'], pfa_nwk_1['Power_v2_1'], 
                pfa_nwk_1['Power_v1_v2'], pfa_nwk_1['Power_cst'], pfa_nwk_1['Impact_v1_2'], pfa_nwk_1['Impact_v1_1'], pfa_nwk_1['Impact_v2_2'], pfa_nwk_1['Impact_v2_1'], pfa_nwk_1['Impact_v1_v2'], 
                pfa_nwk_1['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)   
    
    ##Unit 2
    pfa_nwk_2 = {}
    pfa_nwk_2['Name'] = 'pfa_nwk_2'
    pfa_nwk_2['Variable1'] = 'm_pfa'                                                                            ##Flowrate to pfa 
    pfa_nwk_2['Variable2'] = '-'                                                 
    pfa_nwk_2['Fmin_v1'] = pfa_network['pfa_nwk_f2']['value'] * pfa_network['pfa_nwk_pfamaxflow']['value']      ##Minimum value of flow to pfa 
    pfa_nwk_2['Fmax_v1'] = pfa_network['pfa_nwk_f3']['value'] * pfa_network['pfa_nwk_pfamaxflow']['value']      ##Maximum value of flow to pfa 
    pfa_nwk_2['Fmin_v2'] = 0                                                
    pfa_nwk_2['Fmax_v2'] = 0
    pfa_nwk_2['Coeff_v1_2'] = 0                                                                                 ##This is linear, no need for repeated constraints                              
    pfa_nwk_2['Coeff_v1_1'] = 0                                                 
    pfa_nwk_2['Coeff_v2_2'] = 0
    pfa_nwk_2['Coeff_v2_1'] = 0
    pfa_nwk_2['Coeff_v1_v2'] = 0
    pfa_nwk_2['Coeff_cst'] = 0
    pfa_nwk_2['Fmin'] = 0
    pfa_nwk_2['Fmax'] = 0
    pfa_nwk_2['Cost_v1_2'] = 0
    pfa_nwk_2['Cost_v1_1'] = 0
    pfa_nwk_2['Cost_v2_2'] = 0
    pfa_nwk_2['Cost_v2_1'] = 0
    pfa_nwk_2['Cost_v1_v2'] = 0
    pfa_nwk_2['Cost_cst'] = 0
    pfa_nwk_2['Cinv_v1_2'] = 0
    pfa_nwk_2['Cinv_v1_1'] = 0
    pfa_nwk_2['Cinv_v2_2'] = 0
    pfa_nwk_2['Cinv_v2_1'] = 0
    pfa_nwk_2['Cinv_v1_v2'] = 0
    pfa_nwk_2['Cinv_cst'] = 0
    pfa_nwk_2['Power_v1_2'] = 0
    pfa_nwk_2['Power_v1_1'] = 0
    pfa_nwk_2['Power_v2_2'] = 0
    pfa_nwk_2['Power_v2_1'] = 0
    pfa_nwk_2['Power_v1_v2'] = 0
    pfa_nwk_2['Power_cst'] = 0
    pfa_nwk_2['Impact_v1_2'] = 0
    pfa_nwk_2['Impact_v1_1'] = 0
    pfa_nwk_2['Impact_v2_2'] = 0
    pfa_nwk_2['Impact_v2_1'] = 0
    pfa_nwk_2['Impact_v1_v2'] = 0
    pfa_nwk_2['Impact_cst'] = 0

    unitinput = [pfa_nwk_2['Name'], pfa_nwk_2['Variable1'], pfa_nwk_2['Variable2'], pfa_nwk_2['Fmin_v1'], pfa_nwk_2['Fmax_v1'], pfa_nwk_2['Fmin_v2'], pfa_nwk_2['Fmax_v2'], pfa_nwk_2['Coeff_v1_2'], 
                pfa_nwk_2['Coeff_v1_1'], pfa_nwk_2['Coeff_v2_2'], pfa_nwk_2['Coeff_v2_1'], pfa_nwk_2['Coeff_v1_v2'], pfa_nwk_2['Coeff_cst'], pfa_nwk_2['Fmin'], pfa_nwk_2['Fmax'], pfa_nwk_2['Cost_v1_2'], 
                pfa_nwk_2['Cost_v1_1'], pfa_nwk_2['Cost_v2_2'], pfa_nwk_2['Cost_v2_1'], pfa_nwk_2['Cost_v1_v2'], pfa_nwk_2['Cost_cst'], pfa_nwk_2['Cinv_v1_2'], pfa_nwk_2['Cinv_v1_1'], pfa_nwk_2['Cinv_v2_2'], 
                pfa_nwk_2['Cinv_v2_1'], pfa_nwk_2['Cinv_v1_v2'], pfa_nwk_2['Cinv_cst'], pfa_nwk_2['Power_v1_2'], pfa_nwk_2['Power_v1_1'], pfa_nwk_2['Power_v2_2'], pfa_nwk_2['Power_v2_1'], 
                pfa_nwk_2['Power_v1_v2'], pfa_nwk_2['Power_cst'], pfa_nwk_2['Impact_v1_2'], pfa_nwk_2['Impact_v1_1'], pfa_nwk_2['Impact_v2_2'], pfa_nwk_2['Impact_v2_1'], pfa_nwk_2['Impact_v1_v2'], 
                pfa_nwk_2['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True) 
    
    ##Unit 3
    pfa_nwk_3 = {}
    pfa_nwk_3['Name'] = 'pfa_nwk_3'
    pfa_nwk_3['Variable1'] = 'm_pfa'                                                                            ##Flowrate to pfa 
    pfa_nwk_3['Variable2'] = '-'                                                                                
    pfa_nwk_3['Fmin_v1'] = pfa_network['pfa_nwk_f3']['value'] * pfa_network['pfa_nwk_pfamaxflow']['value']      ##Minimum value of flow to pfa 
    pfa_nwk_3['Fmax_v1'] = pfa_network['pfa_nwk_f4']['value'] * pfa_network['pfa_nwk_pfamaxflow']['value']      ##Maximum value of flow to pfa
    pfa_nwk_3['Fmin_v2'] = 0                                                
    pfa_nwk_3['Fmax_v2'] = 0
    pfa_nwk_3['Coeff_v1_2'] = 0                                                                                 ##This is linear, no need for repeated constraints                                          
    pfa_nwk_3['Coeff_v1_1'] = 0                                                 
    pfa_nwk_3['Coeff_v2_2'] = 0
    pfa_nwk_3['Coeff_v2_1'] = 0
    pfa_nwk_3['Coeff_v1_v2'] = 0
    pfa_nwk_3['Coeff_cst'] = 0
    pfa_nwk_3['Fmin'] = 0
    pfa_nwk_3['Fmax'] = 0
    pfa_nwk_3['Cost_v1_2'] = 0
    pfa_nwk_3['Cost_v1_1'] = 0
    pfa_nwk_3['Cost_v2_2'] = 0
    pfa_nwk_3['Cost_v2_1'] = 0
    pfa_nwk_3['Cost_v1_v2'] = 0
    pfa_nwk_3['Cost_cst'] = 0
    pfa_nwk_3['Cinv_v1_2'] = 0
    pfa_nwk_3['Cinv_v1_1'] = 0
    pfa_nwk_3['Cinv_v2_2'] = 0
    pfa_nwk_3['Cinv_v2_1'] = 0
    pfa_nwk_3['Cinv_v1_v2'] = 0
    pfa_nwk_3['Cinv_cst'] = 0
    pfa_nwk_3['Power_v1_2'] = 0
    pfa_nwk_3['Power_v1_1'] = 0
    pfa_nwk_3['Power_v2_2'] = 0
    pfa_nwk_3['Power_v2_1'] = 0
    pfa_nwk_3['Power_v1_v2'] = 0
    pfa_nwk_3['Power_cst'] = 0
    pfa_nwk_3['Impact_v1_2'] = 0
    pfa_nwk_3['Impact_v1_1'] = 0
    pfa_nwk_3['Impact_v2_2'] = 0
    pfa_nwk_3['Impact_v2_1'] = 0
    pfa_nwk_3['Impact_v1_v2'] = 0
    pfa_nwk_3['Impact_cst'] = 0

    unitinput = [pfa_nwk_3['Name'], pfa_nwk_3['Variable1'], pfa_nwk_3['Variable2'], pfa_nwk_3['Fmin_v1'], pfa_nwk_3['Fmax_v1'], pfa_nwk_3['Fmin_v2'], pfa_nwk_3['Fmax_v2'], pfa_nwk_3['Coeff_v1_2'], 
                pfa_nwk_3['Coeff_v1_1'], pfa_nwk_3['Coeff_v2_2'], pfa_nwk_3['Coeff_v2_1'], pfa_nwk_3['Coeff_v1_v2'], pfa_nwk_3['Coeff_cst'], pfa_nwk_3['Fmin'], pfa_nwk_3['Fmax'], pfa_nwk_3['Cost_v1_2'], 
                pfa_nwk_3['Cost_v1_1'], pfa_nwk_3['Cost_v2_2'], pfa_nwk_3['Cost_v2_1'], pfa_nwk_3['Cost_v1_v2'], pfa_nwk_3['Cost_cst'], pfa_nwk_3['Cinv_v1_2'], pfa_nwk_3['Cinv_v1_1'], pfa_nwk_3['Cinv_v2_2'], 
                pfa_nwk_3['Cinv_v2_1'], pfa_nwk_3['Cinv_v1_v2'], pfa_nwk_3['Cinv_cst'], pfa_nwk_3['Power_v1_2'], pfa_nwk_3['Power_v1_1'], pfa_nwk_3['Power_v2_2'], pfa_nwk_3['Power_v2_1'], 
                pfa_nwk_3['Power_v1_v2'], pfa_nwk_3['Power_cst'], pfa_nwk_3['Impact_v1_2'], pfa_nwk_3['Impact_v1_1'], pfa_nwk_3['Impact_v2_2'], pfa_nwk_3['Impact_v2_1'], pfa_nwk_3['Impact_v1_v2'], 
                pfa_nwk_3['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True) 
    
    ##Unit 4
    pfa_nwk_4 = {}
    pfa_nwk_4['Name'] = 'pfa_nwk_4'
    pfa_nwk_4['Variable1'] = 'm_pfa'                                                                            ##Flowrate to pfa
    pfa_nwk_4['Variable2'] = '-'
    pfa_nwk_4['Fmin_v1'] = pfa_network['pfa_nwk_f4']['value'] * pfa_network['pfa_nwk_pfamaxflow']['value']      ##Minimum value of flow to pfa 
    pfa_nwk_4['Fmax_v1'] = pfa_network['pfa_nwk_f5']['value'] * pfa_network['pfa_nwk_pfamaxflow']['value']      ##Maximum value of flow to pfa 
    pfa_nwk_4['Fmin_v2'] = 0                                                
    pfa_nwk_4['Fmax_v2'] = 0
    pfa_nwk_4['Coeff_v1_2'] = 0                                          
    pfa_nwk_4['Coeff_v1_1'] = 0                                                 
    pfa_nwk_4['Coeff_v2_2'] = 0
    pfa_nwk_4['Coeff_v2_1'] = 0
    pfa_nwk_4['Coeff_v1_v2'] = 0
    pfa_nwk_4['Coeff_cst'] = 0
    pfa_nwk_4['Fmin'] = 0
    pfa_nwk_4['Fmax'] = 0
    pfa_nwk_4['Cost_v1_2'] = 0
    pfa_nwk_4['Cost_v1_1'] = 0
    pfa_nwk_4['Cost_v2_2'] = 0
    pfa_nwk_4['Cost_v2_1'] = 0
    pfa_nwk_4['Cost_v1_v2'] = 0
    pfa_nwk_4['Cost_cst'] = 0
    pfa_nwk_4['Cinv_v1_2'] = 0
    pfa_nwk_4['Cinv_v1_1'] = 0
    pfa_nwk_4['Cinv_v2_2'] = 0
    pfa_nwk_4['Cinv_v2_1'] = 0
    pfa_nwk_4['Cinv_v1_v2'] = 0
    pfa_nwk_4['Cinv_cst'] = 0
    pfa_nwk_4['Power_v1_2'] = 0
    pfa_nwk_4['Power_v1_1'] = 0
    pfa_nwk_4['Power_v2_2'] = 0
    pfa_nwk_4['Power_v2_1'] = 0
    pfa_nwk_4['Power_v1_v2'] = 0
    pfa_nwk_4['Power_cst'] = 0
    pfa_nwk_4['Impact_v1_2'] = 0
    pfa_nwk_4['Impact_v1_1'] = 0
    pfa_nwk_4['Impact_v2_2'] = 0
    pfa_nwk_4['Impact_v2_1'] = 0
    pfa_nwk_4['Impact_v1_v2'] = 0
    pfa_nwk_4['Impact_cst'] = 0

    unitinput = [pfa_nwk_4['Name'], pfa_nwk_4['Variable1'], pfa_nwk_4['Variable2'], pfa_nwk_4['Fmin_v1'], pfa_nwk_4['Fmax_v1'], pfa_nwk_4['Fmin_v2'], pfa_nwk_4['Fmax_v2'], pfa_nwk_4['Coeff_v1_2'], 
                pfa_nwk_4['Coeff_v1_1'], pfa_nwk_4['Coeff_v2_2'], pfa_nwk_4['Coeff_v2_1'], pfa_nwk_4['Coeff_v1_v2'], pfa_nwk_4['Coeff_cst'], pfa_nwk_4['Fmin'], pfa_nwk_4['Fmax'], pfa_nwk_4['Cost_v1_2'], 
                pfa_nwk_4['Cost_v1_1'], pfa_nwk_4['Cost_v2_2'], pfa_nwk_4['Cost_v2_1'], pfa_nwk_4['Cost_v1_v2'], pfa_nwk_4['Cost_cst'], pfa_nwk_4['Cinv_v1_2'], pfa_nwk_4['Cinv_v1_1'], pfa_nwk_4['Cinv_v2_2'], 
                pfa_nwk_4['Cinv_v2_1'], pfa_nwk_4['Cinv_v1_v2'], pfa_nwk_4['Cinv_cst'], pfa_nwk_4['Power_v1_2'], pfa_nwk_4['Power_v1_1'], pfa_nwk_4['Power_v2_2'], pfa_nwk_4['Power_v2_1'], 
                pfa_nwk_4['Power_v1_v2'], pfa_nwk_4['Power_cst'], pfa_nwk_4['Impact_v1_2'], pfa_nwk_4['Impact_v1_1'], pfa_nwk_4['Impact_v2_2'], pfa_nwk_4['Impact_v2_1'], pfa_nwk_4['Impact_v1_v2'], 
                pfa_nwk_4['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)    
    
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}                                                                ##The flowrate into the pfa branch from ice network  
    stream1['Parent'] = 'pfa_nwk_1'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'pfa_nwk_1_flow_in'
    stream1['Layer'] = 'tro_nwk2pfa_nwk'
    stream1['Stream_coeff_v1_2'] = 0
    stream1['Stream_coeff_v1_1'] = 1
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
    stream2 = {}                                                                ##The flowrate to the pfa branch to pfa substation     
    stream2['Parent'] = 'pfa_nwk_1'
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'pfa_nwk_1_2_pfa_ss'
    stream2['Layer'] = 'pfa_nwk2pfa_ss'
    stream2['Stream_coeff_v1_2'] = 0
    stream2['Stream_coeff_v1_1'] = 1
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
    stream3 = {}                                                                ##The associated pressure-drop component from the pfa branch network    
    stream3['Parent'] = 'pfa_nwk_1'
    stream3['Type'] = 'balancing_only'
    stream3['Name'] = 'pfa_nwk_1_delp_component'
    stream3['Layer'] = 'tro_nwkandpfa_nwk_delp'
    stream3['Stream_coeff_v1_2'] = 0
    stream3['Stream_coeff_v1_1'] = pfa_network['pfa_nwk_pfa_grad1']['value']
    stream3['Stream_coeff_v2_2'] = 0
    stream3['Stream_coeff_v2_1'] = 0
    stream3['Stream_coeff_v1_v2'] = 0
    stream3['Stream_coeff_cst'] = pfa_network['pfa_nwk_pfa_int1']['value']
    stream3['InOut'] = 'out'
    
    streaminput = [stream3['Parent'], stream3['Type'], stream3['Name'], stream3['Layer'], stream3['Stream_coeff_v1_2'], stream3['Stream_coeff_v1_1'], stream3['Stream_coeff_v2_2'],
                   stream3['Stream_coeff_v2_1'], stream3['Stream_coeff_v1_v2'], stream3['Stream_coeff_cst'], stream3['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)  
    
    ##Stream 4
    stream4 = {}                                                                ##The flowrate into the pfa branch from ice network  
    stream4['Parent'] = 'pfa_nwk_2'
    stream4['Type'] = 'balancing_only'
    stream4['Name'] = 'pfa_nwk_2_flow_in'
    stream4['Layer'] = 'tro_nwk2pfa_nwk'
    stream4['Stream_coeff_v1_2'] = 0
    stream4['Stream_coeff_v1_1'] = 1
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
    stream5 = {}                                                                ##The flowrate to the pfa branch to pfa substation     
    stream5['Parent'] = 'pfa_nwk_2'
    stream5['Type'] = 'balancing_only'
    stream5['Name'] = 'pfa_nwk_2_2_pfa_ss'
    stream5['Layer'] = 'pfa_nwk2pfa_ss'
    stream5['Stream_coeff_v1_2'] = 0
    stream5['Stream_coeff_v1_1'] = 1
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
    stream6 = {}                                                                ##The associated pressure-drop component from the pfa branch network      
    stream6['Parent'] = 'pfa_nwk_2'
    stream6['Type'] = 'balancing_only'
    stream6['Name'] = 'pfa_nwk_2_delp_component'
    stream6['Layer'] = 'tro_nwkandpfa_nwk_delp'
    stream6['Stream_coeff_v1_2'] = 0
    stream6['Stream_coeff_v1_1'] = pfa_network['pfa_nwk_pfa_grad2']['value']
    stream6['Stream_coeff_v2_2'] = 0
    stream6['Stream_coeff_v2_1'] = 0
    stream6['Stream_coeff_v1_v2'] = 0
    stream6['Stream_coeff_cst'] = pfa_network['pfa_nwk_pfa_int2']['value']
    stream6['InOut'] = 'out'
    
    streaminput = [stream6['Parent'], stream6['Type'], stream6['Name'], stream6['Layer'], stream6['Stream_coeff_v1_2'], stream6['Stream_coeff_v1_1'], stream6['Stream_coeff_v2_2'],
                   stream6['Stream_coeff_v2_1'], stream6['Stream_coeff_v1_v2'], stream6['Stream_coeff_cst'], stream6['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True) 

    ##Stream 7
    stream7 = {}                                                                ##The flowrate into the pfa branch from ice network  
    stream7['Parent'] = 'pfa_nwk_3'
    stream7['Type'] = 'balancing_only'
    stream7['Name'] = 'pfa_nwk_3_flow_in'
    stream7['Layer'] = 'tro_nwk2pfa_nwk'
    stream7['Stream_coeff_v1_2'] = 0
    stream7['Stream_coeff_v1_1'] = 1
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
    stream8 = {}                                                                ##The flowrate to the pfa branch to pfa substation     
    stream8['Parent'] = 'pfa_nwk_3'
    stream8['Type'] = 'balancing_only'
    stream8['Name'] = 'pfa_nwk_3_2_pfa_ss'
    stream8['Layer'] = 'pfa_nwk2pfa_ss'
    stream8['Stream_coeff_v1_2'] = 0
    stream8['Stream_coeff_v1_1'] = 1
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
    stream9 = {}                                                                ##The associated pressure-drop component from the pfa branch network      
    stream9['Parent'] = 'pfa_nwk_3'
    stream9['Type'] = 'balancing_only'
    stream9['Name'] = 'pfa_nwk_3_delp_component'
    stream9['Layer'] = 'tro_nwkandpfa_nwk_delp'
    stream9['Stream_coeff_v1_2'] = 0
    stream9['Stream_coeff_v1_1'] = pfa_network['pfa_nwk_pfa_grad3']['value']
    stream9['Stream_coeff_v2_2'] = 0
    stream9['Stream_coeff_v2_1'] = 0
    stream9['Stream_coeff_v1_v2'] = 0
    stream9['Stream_coeff_cst'] = pfa_network['pfa_nwk_pfa_int3']['value']
    stream9['InOut'] = 'out'
    
    streaminput = [stream9['Parent'], stream9['Type'], stream9['Name'], stream9['Layer'], stream9['Stream_coeff_v1_2'], stream9['Stream_coeff_v1_1'], stream9['Stream_coeff_v2_2'],
                   stream9['Stream_coeff_v2_1'], stream9['Stream_coeff_v1_v2'], stream9['Stream_coeff_cst'], stream9['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True) 
    
    ##Stream 10
    stream10 = {}                                                                ##The flowrate into the pfa branch from ice network  
    stream10['Parent'] = 'pfa_nwk_4'
    stream10['Type'] = 'balancing_only'
    stream10['Name'] = 'pfa_nwk_4_flow_in'
    stream10['Layer'] = 'tro_nwk2pfa_nwk'
    stream10['Stream_coeff_v1_2'] = 0
    stream10['Stream_coeff_v1_1'] = 1
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
    stream11 = {}                                                                ##The flowrate to the pfa branch to pfa substation     
    stream11['Parent'] = 'pfa_nwk_4'
    stream11['Type'] = 'balancing_only'
    stream11['Name'] = 'pfa_nwk_4_2_pfa_ss'
    stream11['Layer'] = 'pfa_nwk2pfa_ss'
    stream11['Stream_coeff_v1_2'] = 0
    stream11['Stream_coeff_v1_1'] = 1
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
    stream12 = {}                                                                ##The associated pressure-drop component from the pfa branch network      
    stream12['Parent'] = 'pfa_nwk_4'
    stream12['Type'] = 'balancing_only'
    stream12['Name'] = 'pfa_nwk_4_delp_component'
    stream12['Layer'] = 'tro_nwkandpfa_nwk_delp'
    stream12['Stream_coeff_v1_2'] = 0
    stream12['Stream_coeff_v1_1'] = pfa_network['pfa_nwk_pfa_grad4']['value']
    stream12['Stream_coeff_v2_2'] = 0
    stream12['Stream_coeff_v2_1'] = 0
    stream12['Stream_coeff_v1_v2'] = 0
    stream12['Stream_coeff_cst'] = pfa_network['pfa_nwk_pfa_int4']['value']
    stream12['InOut'] = 'out'
    
    streaminput = [stream12['Parent'], stream12['Type'], stream12['Name'], stream12['Layer'], stream12['Stream_coeff_v1_2'], stream12['Stream_coeff_v1_1'], stream12['Stream_coeff_v2_2'],
                   stream12['Stream_coeff_v2_1'], stream12['Stream_coeff_v1_v2'], stream12['Stream_coeff_cst'], stream12['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True) 
    
    ##Constraint definition
    
    ##Equation definitions
    
    ##Equation 1
    eqn1 = {}
    eqn1['Name'] = 'totaluse_pfa_nwk'
    eqn1['Type'] = 'unit_binary'
    eqn1['Sign'] = 'less_than_equal_to'
    eqn1['RHS_value'] = 1
    
    eqninput = [eqn1['Name'], eqn1['Type'], eqn1['Sign'], eqn1['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation terms
    
    ##Term 1
    term1 = {}
    term1['Parent_unit'] = 'pfa_nwk_1'
    term1['Parent_eqn'] = 'totaluse_pfa_nwk'
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
    term2['Parent_unit'] = 'pfa_nwk_2'
    term2['Parent_eqn'] = 'totaluse_pfa_nwk'
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
    term3['Parent_unit'] = 'pfa_nwk_3'
    term3['Parent_eqn'] = 'totaluse_pfa_nwk'
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
    term4['Parent_unit'] = 'pfa_nwk_4'
    term4['Parent_eqn'] = 'totaluse_pfa_nwk'
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
    