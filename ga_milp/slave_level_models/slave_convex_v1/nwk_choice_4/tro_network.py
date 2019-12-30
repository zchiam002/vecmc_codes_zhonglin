## This is the TRO network model, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type 
    
def tro_network (tro_nwk_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    from nwk_choice_4.tro_network_compute import tro_network_compute
    import pandas as pd
    import numpy as np 
    
    ##Model description 
    ##This is a 2 split parallel network model with 2 variables. It takes in a mass flowrate stream and gives off 2 mass flowrate and 1 pressure drop stream
        
    ##Define dictionary of values 
    
    tro_network = {}
    
    ##Defined constants 
    
    ##1
    tro_nwk_trocoeff = {}
    tro_nwk_trocoeff['value'] = 0.001162790697674419
    tro_nwk_trocoeff['units'] = '-'
    tro_nwk_trocoeff['status'] = 'cst'
    tro_network['tro_nwk_trocoeff'] = tro_nwk_trocoeff

    ##2
    tro_nwk_tromaxflow = {}
    tro_nwk_tromaxflow['value'] = 600                                           ##The upperlimits are needed for stepwise linearization 
    tro_nwk_tromaxflow['units'] = 'm3/h'
    tro_nwk_tromaxflow['status'] = 'cst'
    tro_network['tro_nwk_tromaxflow'] = tro_nwk_tromaxflow    

    ##3
    tro_nwk_pfamaxflow = {}
    tro_nwk_pfamaxflow['value'] = 300                                           ##The upperlimits for the first variable
    tro_nwk_pfamaxflow['units'] = 'm3/h'
    tro_nwk_pfamaxflow['status'] = 'cst'
    tro_network['tro_nwk_pfamaxflow'] = tro_nwk_pfamaxflow  

    ##4
    tro_nwk_sermaxflow = {}
    tro_nwk_sermaxflow['value'] = 300                                           ##The upperlimits for the second variable 
    tro_nwk_sermaxflow['units'] = 'm3/h'
    tro_nwk_sermaxflow['status'] = 'cst'
    tro_network['tro_nwk_sermaxflow'] = tro_nwk_sermaxflow  

    ##Dependent constants
    tro_nwk_dc = np.zeros((2,1))                                                #initialize the list, note the number of constants
    
    tro_nwk_dc[0,0] = tro_network['tro_nwk_trocoeff']['value']
    tro_nwk_dc[1,0] = tro_network['tro_nwk_tromaxflow']['value']

    tro_nwk_calc = tro_network_compute(tro_nwk_dc)
    
    ##5
    tro_nwk_tro_grad1 = {}
    tro_nwk_tro_grad1['value'] = tro_nwk_calc[0,0]                                                           
    tro_nwk_tro_grad1['units'] = '-'
    tro_nwk_tro_grad1['status'] = 'calc'
    tro_network['tro_nwk_tro_grad1'] = tro_nwk_tro_grad1

    ##6
    tro_nwk_tro_grad2 = {}
    tro_nwk_tro_grad2['value'] = tro_nwk_calc[1,0]                                                           
    tro_nwk_tro_grad2['units'] = '-'
    tro_nwk_tro_grad2['status'] = 'calc'
    tro_network['tro_nwk_tro_grad2'] = tro_nwk_tro_grad2

    ##7
    tro_nwk_tro_grad3 = {}
    tro_nwk_tro_grad3['value'] = tro_nwk_calc[2,0]                                                           
    tro_nwk_tro_grad3['units'] = '-'
    tro_nwk_tro_grad3['status'] = 'calc'
    tro_network['tro_nwk_tro_grad3'] = tro_nwk_tro_grad3

    ##8
    tro_nwk_tro_grad4 = {}
    tro_nwk_tro_grad4['value'] = tro_nwk_calc[3,0]                                                           
    tro_nwk_tro_grad4['units'] = '-'
    tro_nwk_tro_grad4['status'] = 'calc'
    tro_network['tro_nwk_tro_grad4'] = tro_nwk_tro_grad4

    ##9
    tro_nwk_tro_int1 = {}
    tro_nwk_tro_int1['value'] = tro_nwk_calc[4,0]                                                           
    tro_nwk_tro_int1['units'] = '-'
    tro_nwk_tro_int1['status'] = 'calc'
    tro_network['tro_nwk_tro_int1'] = tro_nwk_tro_int1

    ##10
    tro_nwk_tro_int2 = {}
    tro_nwk_tro_int2['value'] = tro_nwk_calc[5,0]                                                           
    tro_nwk_tro_int2['units'] = '-'
    tro_nwk_tro_int2['status'] = 'calc'
    tro_network['tro_nwk_tro_int2'] = tro_nwk_tro_int2

    ##11
    tro_nwk_tro_int3 = {}
    tro_nwk_tro_int3['value'] = tro_nwk_calc[6,0]                                                           
    tro_nwk_tro_int3['units'] = '-'
    tro_nwk_tro_int3['status'] = 'calc'
    tro_network['tro_nwk_tro_int3'] = tro_nwk_tro_int3

    ##12
    tro_nwk_tro_int4 = {}
    tro_nwk_tro_int4['value'] = tro_nwk_calc[7,0]                                                           
    tro_nwk_tro_int4['units'] = '-'
    tro_nwk_tro_int4['status'] = 'calc'
    tro_network['tro_nwk_tro_int4'] = tro_nwk_tro_int4

    ##13
    tro_nwk_f1 = {}
    tro_nwk_f1['value'] = tro_nwk_calc[8,0]
    tro_nwk_f1['units'] = '-'
    tro_nwk_f1['status'] = 'calc'
    tro_network['tro_nwk_f1'] = tro_nwk_f1

    ##14
    tro_nwk_f2 = {}
    tro_nwk_f2['value'] = tro_nwk_calc[9,0]
    tro_nwk_f2['units'] = '-'
    tro_nwk_f2['status'] = 'calc'
    tro_network['tro_nwk_f2'] = tro_nwk_f2

    ##15
    tro_nwk_f3 = {}
    tro_nwk_f3['value'] = tro_nwk_calc[10,0]
    tro_nwk_f3['units'] = '-'
    tro_nwk_f3['status'] = 'calc'
    tro_network['tro_nwk_f3'] = tro_nwk_f3

    ##16
    tro_nwk_f4 = {}
    tro_nwk_f4['value'] = tro_nwk_calc[11,0]
    tro_nwk_f4['units'] = '-'
    tro_nwk_f4['status'] = 'calc'
    tro_network['tro_nwk_f4'] = tro_nwk_f4

    ##17
    tro_nwk_f5 = {}
    tro_nwk_f5['value'] = tro_nwk_calc[12,0]
    tro_nwk_f5['units'] = '-'
    tro_nwk_f5['status'] = 'calc'
    tro_network['tro_nwk_f5'] = tro_nwk_f5

    ##Unit definition 
    
    ##Unit 1
    tro_nwk_1 = {}
    tro_nwk_1['Name'] = 'tro_nwk_1'
    tro_nwk_1['Variable1'] = 'm_pfa'                                                    ##Flowrate to pfa 
    tro_nwk_1['Variable2'] = 'm_ser'                                                    ##Flowrate to ser 
    tro_nwk_1['Fmin_v1'] = 0 
    tro_nwk_1['Fmax_v1'] = tro_network['tro_nwk_pfamaxflow']['value']                   ##Maximum value of flow to pfa 
    tro_nwk_1['Fmin_v2'] = 0                                                
    tro_nwk_1['Fmax_v2'] = tro_network['tro_nwk_sermaxflow']['value']                   ##Maximum value of flow to ser
    tro_nwk_1['Coeff_v1_2'] = 0                                          
    tro_nwk_1['Coeff_v1_1'] = 1                                                 
    tro_nwk_1['Coeff_v2_2'] = 0
    tro_nwk_1['Coeff_v2_1'] = 1
    tro_nwk_1['Coeff_v1_v2'] = 0
    tro_nwk_1['Coeff_cst'] = 0
    tro_nwk_1['Fmin'] = tro_network['tro_nwk_f1']['value'] * tro_network['tro_nwk_tromaxflow']['value']
    tro_nwk_1['Fmax'] = tro_network['tro_nwk_f2']['value'] * tro_network['tro_nwk_tromaxflow']['value']
    tro_nwk_1['Cost_v1_2'] = 0
    tro_nwk_1['Cost_v1_1'] = 0
    tro_nwk_1['Cost_v2_2'] = 0
    tro_nwk_1['Cost_v2_1'] = 0
    tro_nwk_1['Cost_v1_v2'] = 0
    tro_nwk_1['Cost_cst'] = 0
    tro_nwk_1['Cinv_v1_2'] = 0
    tro_nwk_1['Cinv_v1_1'] = 0
    tro_nwk_1['Cinv_v2_2'] = 0
    tro_nwk_1['Cinv_v2_1'] = 0
    tro_nwk_1['Cinv_v1_v2'] = 0
    tro_nwk_1['Cinv_cst'] = 0
    tro_nwk_1['Power_v1_2'] = 0
    tro_nwk_1['Power_v1_1'] = 0
    tro_nwk_1['Power_v2_2'] = 0
    tro_nwk_1['Power_v2_1'] = 0
    tro_nwk_1['Power_v1_v2'] = 0
    tro_nwk_1['Power_cst'] = 0
    tro_nwk_1['Impact_v1_2'] = 0
    tro_nwk_1['Impact_v1_1'] = 0
    tro_nwk_1['Impact_v2_2'] = 0
    tro_nwk_1['Impact_v2_1'] = 0
    tro_nwk_1['Impact_v1_v2'] = 0
    tro_nwk_1['Impact_cst'] = 0

    unitinput = [tro_nwk_1['Name'], tro_nwk_1['Variable1'], tro_nwk_1['Variable2'], tro_nwk_1['Fmin_v1'], tro_nwk_1['Fmax_v1'], tro_nwk_1['Fmin_v2'], tro_nwk_1['Fmax_v2'], tro_nwk_1['Coeff_v1_2'], 
                tro_nwk_1['Coeff_v1_1'], tro_nwk_1['Coeff_v2_2'], tro_nwk_1['Coeff_v2_1'], tro_nwk_1['Coeff_v1_v2'], tro_nwk_1['Coeff_cst'], tro_nwk_1['Fmin'], tro_nwk_1['Fmax'], tro_nwk_1['Cost_v1_2'], 
                tro_nwk_1['Cost_v1_1'], tro_nwk_1['Cost_v2_2'], tro_nwk_1['Cost_v2_1'], tro_nwk_1['Cost_v1_v2'], tro_nwk_1['Cost_cst'], tro_nwk_1['Cinv_v1_2'], tro_nwk_1['Cinv_v1_1'], tro_nwk_1['Cinv_v2_2'], 
                tro_nwk_1['Cinv_v2_1'], tro_nwk_1['Cinv_v1_v2'], tro_nwk_1['Cinv_cst'], tro_nwk_1['Power_v1_2'], tro_nwk_1['Power_v1_1'], tro_nwk_1['Power_v2_2'], tro_nwk_1['Power_v2_1'], 
                tro_nwk_1['Power_v1_v2'], tro_nwk_1['Power_cst'], tro_nwk_1['Impact_v1_2'], tro_nwk_1['Impact_v1_1'], tro_nwk_1['Impact_v2_2'], tro_nwk_1['Impact_v2_1'], tro_nwk_1['Impact_v1_v2'], 
                tro_nwk_1['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)   
    
    ##Unit 2
    tro_nwk_2 = {}
    tro_nwk_2['Name'] = 'tro_nwk_2'
    tro_nwk_2['Variable1'] = 'm_pfa'                                                    ##Flowrate to pfa 
    tro_nwk_2['Variable2'] = 'm_ser'                                                    ##Flowrate to ser 
    tro_nwk_2['Fmin_v1'] = 0 
    tro_nwk_2['Fmax_v1'] = tro_network['tro_nwk_pfamaxflow']['value']                 ##Maximum value of flow to pfa 
    tro_nwk_2['Fmin_v2'] = 0                                                
    tro_nwk_2['Fmax_v2'] = tro_network['tro_nwk_sermaxflow']['value']                 ##Maximum value of flow to ser
    tro_nwk_2['Coeff_v1_2'] = 0                                          
    tro_nwk_2['Coeff_v1_1'] = 1                                                 
    tro_nwk_2['Coeff_v2_2'] = 0
    tro_nwk_2['Coeff_v2_1'] = 1
    tro_nwk_2['Coeff_v1_v2'] = 0
    tro_nwk_2['Coeff_cst'] = 0
    tro_nwk_2['Fmin'] = tro_network['tro_nwk_f2']['value'] * tro_network['tro_nwk_tromaxflow']['value']
    tro_nwk_2['Fmax'] = tro_network['tro_nwk_f3']['value'] * tro_network['tro_nwk_tromaxflow']['value']
    tro_nwk_2['Cost_v1_2'] = 0
    tro_nwk_2['Cost_v1_1'] = 0
    tro_nwk_2['Cost_v2_2'] = 0
    tro_nwk_2['Cost_v2_1'] = 0
    tro_nwk_2['Cost_v1_v2'] = 0
    tro_nwk_2['Cost_cst'] = 0
    tro_nwk_2['Cinv_v1_2'] = 0
    tro_nwk_2['Cinv_v1_1'] = 0
    tro_nwk_2['Cinv_v2_2'] = 0
    tro_nwk_2['Cinv_v2_1'] = 0
    tro_nwk_2['Cinv_v1_v2'] = 0
    tro_nwk_2['Cinv_cst'] = 0
    tro_nwk_2['Power_v1_2'] = 0
    tro_nwk_2['Power_v1_1'] = 0
    tro_nwk_2['Power_v2_2'] = 0
    tro_nwk_2['Power_v2_1'] = 0
    tro_nwk_2['Power_v1_v2'] = 0
    tro_nwk_2['Power_cst'] = 0
    tro_nwk_2['Impact_v1_2'] = 0
    tro_nwk_2['Impact_v1_1'] = 0
    tro_nwk_2['Impact_v2_2'] = 0
    tro_nwk_2['Impact_v2_1'] = 0
    tro_nwk_2['Impact_v1_v2'] = 0
    tro_nwk_2['Impact_cst'] = 0

    unitinput = [tro_nwk_2['Name'], tro_nwk_2['Variable1'], tro_nwk_2['Variable2'], tro_nwk_2['Fmin_v1'], tro_nwk_2['Fmax_v1'], tro_nwk_2['Fmin_v2'], tro_nwk_2['Fmax_v2'], tro_nwk_2['Coeff_v1_2'], 
                tro_nwk_2['Coeff_v1_1'], tro_nwk_2['Coeff_v2_2'], tro_nwk_2['Coeff_v2_1'], tro_nwk_2['Coeff_v1_v2'], tro_nwk_2['Coeff_cst'], tro_nwk_2['Fmin'], tro_nwk_2['Fmax'], tro_nwk_2['Cost_v1_2'], 
                tro_nwk_2['Cost_v1_1'], tro_nwk_2['Cost_v2_2'], tro_nwk_2['Cost_v2_1'], tro_nwk_2['Cost_v1_v2'], tro_nwk_2['Cost_cst'], tro_nwk_2['Cinv_v1_2'], tro_nwk_2['Cinv_v1_1'], tro_nwk_2['Cinv_v2_2'], 
                tro_nwk_2['Cinv_v2_1'], tro_nwk_2['Cinv_v1_v2'], tro_nwk_2['Cinv_cst'], tro_nwk_2['Power_v1_2'], tro_nwk_2['Power_v1_1'], tro_nwk_2['Power_v2_2'], tro_nwk_2['Power_v2_1'], 
                tro_nwk_2['Power_v1_v2'], tro_nwk_2['Power_cst'], tro_nwk_2['Impact_v1_2'], tro_nwk_2['Impact_v1_1'], tro_nwk_2['Impact_v2_2'], tro_nwk_2['Impact_v2_1'], tro_nwk_2['Impact_v1_v2'], 
                tro_nwk_2['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True) 
    
    ##Unit 3
    tro_nwk_3 = {}
    tro_nwk_3['Name'] = 'tro_nwk_3'
    tro_nwk_3['Variable1'] = 'm_pfa'                                                    ##Flowrate to pfa 
    tro_nwk_3['Variable2'] = 'm_ser'                                                    ##Flowrate to ser 
    tro_nwk_3['Fmin_v1'] = 0 
    tro_nwk_3['Fmax_v1'] = tro_network['tro_nwk_pfamaxflow']['value']                 ##Maximum value of flow to pfa 
    tro_nwk_3['Fmin_v2'] = 0                                                
    tro_nwk_3['Fmax_v2'] = tro_network['tro_nwk_sermaxflow']['value']                 ##Maximum value of flow to ser
    tro_nwk_3['Coeff_v1_2'] = 0                                          
    tro_nwk_3['Coeff_v1_1'] = 1                                                 
    tro_nwk_3['Coeff_v2_2'] = 0
    tro_nwk_3['Coeff_v2_1'] = 1
    tro_nwk_3['Coeff_v1_v2'] = 0
    tro_nwk_3['Coeff_cst'] = 0
    tro_nwk_3['Fmin'] = tro_network['tro_nwk_f3']['value'] * tro_network['tro_nwk_tromaxflow']['value']
    tro_nwk_3['Fmax'] = tro_network['tro_nwk_f4']['value'] * tro_network['tro_nwk_tromaxflow']['value']
    tro_nwk_3['Cost_v1_2'] = 0
    tro_nwk_3['Cost_v1_1'] = 0
    tro_nwk_3['Cost_v2_2'] = 0
    tro_nwk_3['Cost_v2_1'] = 0
    tro_nwk_3['Cost_v1_v2'] = 0
    tro_nwk_3['Cost_cst'] = 0
    tro_nwk_3['Cinv_v1_2'] = 0
    tro_nwk_3['Cinv_v1_1'] = 0
    tro_nwk_3['Cinv_v2_2'] = 0
    tro_nwk_3['Cinv_v2_1'] = 0
    tro_nwk_3['Cinv_v1_v2'] = 0
    tro_nwk_3['Cinv_cst'] = 0
    tro_nwk_3['Power_v1_2'] = 0
    tro_nwk_3['Power_v1_1'] = 0
    tro_nwk_3['Power_v2_2'] = 0
    tro_nwk_3['Power_v2_1'] = 0
    tro_nwk_3['Power_v1_v2'] = 0
    tro_nwk_3['Power_cst'] = 0
    tro_nwk_3['Impact_v1_2'] = 0
    tro_nwk_3['Impact_v1_1'] = 0
    tro_nwk_3['Impact_v2_2'] = 0
    tro_nwk_3['Impact_v2_1'] = 0
    tro_nwk_3['Impact_v1_v2'] = 0
    tro_nwk_3['Impact_cst'] = 0

    unitinput = [tro_nwk_3['Name'], tro_nwk_3['Variable1'], tro_nwk_3['Variable2'], tro_nwk_3['Fmin_v1'], tro_nwk_3['Fmax_v1'], tro_nwk_3['Fmin_v2'], tro_nwk_3['Fmax_v2'], tro_nwk_3['Coeff_v1_2'], 
                tro_nwk_3['Coeff_v1_1'], tro_nwk_3['Coeff_v2_2'], tro_nwk_3['Coeff_v2_1'], tro_nwk_3['Coeff_v1_v2'], tro_nwk_3['Coeff_cst'], tro_nwk_3['Fmin'], tro_nwk_3['Fmax'], tro_nwk_3['Cost_v1_2'], 
                tro_nwk_3['Cost_v1_1'], tro_nwk_3['Cost_v2_2'], tro_nwk_3['Cost_v2_1'], tro_nwk_3['Cost_v1_v2'], tro_nwk_3['Cost_cst'], tro_nwk_3['Cinv_v1_2'], tro_nwk_3['Cinv_v1_1'], tro_nwk_3['Cinv_v2_2'], 
                tro_nwk_3['Cinv_v2_1'], tro_nwk_3['Cinv_v1_v2'], tro_nwk_3['Cinv_cst'], tro_nwk_3['Power_v1_2'], tro_nwk_3['Power_v1_1'], tro_nwk_3['Power_v2_2'], tro_nwk_3['Power_v2_1'], 
                tro_nwk_3['Power_v1_v2'], tro_nwk_3['Power_cst'], tro_nwk_3['Impact_v1_2'], tro_nwk_3['Impact_v1_1'], tro_nwk_3['Impact_v2_2'], tro_nwk_3['Impact_v2_1'], tro_nwk_3['Impact_v1_v2'], 
                tro_nwk_3['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True) 
    
    ##Unit 4
    tro_nwk_4 = {}
    tro_nwk_4['Name'] = 'tro_nwk_4'
    tro_nwk_4['Variable1'] = 'm_pfa'                                                    ##Flowrate to pfa 
    tro_nwk_4['Variable2'] = 'm_ser'                                                    ##Flowrate to ser 
    tro_nwk_4['Fmin_v1'] = 0 
    tro_nwk_4['Fmax_v1'] = tro_network['tro_nwk_pfamaxflow']['value']                 ##Maximum value of flow to pfa 
    tro_nwk_4['Fmin_v2'] = 0                                                
    tro_nwk_4['Fmax_v2'] = tro_network['tro_nwk_sermaxflow']['value']                 ##Maximum value of flow to ser
    tro_nwk_4['Coeff_v1_2'] = 0                                          
    tro_nwk_4['Coeff_v1_1'] = 1                                                 
    tro_nwk_4['Coeff_v2_2'] = 0
    tro_nwk_4['Coeff_v2_1'] = 1
    tro_nwk_4['Coeff_v1_v2'] = 0
    tro_nwk_4['Coeff_cst'] = 0
    tro_nwk_4['Fmin'] = tro_network['tro_nwk_f4']['value'] * tro_network['tro_nwk_tromaxflow']['value']
    tro_nwk_4['Fmax'] = tro_network['tro_nwk_f5']['value'] * tro_network['tro_nwk_tromaxflow']['value']
    tro_nwk_4['Cost_v1_2'] = 0
    tro_nwk_4['Cost_v1_1'] = 0
    tro_nwk_4['Cost_v2_2'] = 0
    tro_nwk_4['Cost_v2_1'] = 0
    tro_nwk_4['Cost_v1_v2'] = 0
    tro_nwk_4['Cost_cst'] = 0
    tro_nwk_4['Cinv_v1_2'] = 0
    tro_nwk_4['Cinv_v1_1'] = 0
    tro_nwk_4['Cinv_v2_2'] = 0
    tro_nwk_4['Cinv_v2_1'] = 0
    tro_nwk_4['Cinv_v1_v2'] = 0
    tro_nwk_4['Cinv_cst'] = 0
    tro_nwk_4['Power_v1_2'] = 0
    tro_nwk_4['Power_v1_1'] = 0
    tro_nwk_4['Power_v2_2'] = 0
    tro_nwk_4['Power_v2_1'] = 0
    tro_nwk_4['Power_v1_v2'] = 0
    tro_nwk_4['Power_cst'] = 0
    tro_nwk_4['Impact_v1_2'] = 0
    tro_nwk_4['Impact_v1_1'] = 0
    tro_nwk_4['Impact_v2_2'] = 0
    tro_nwk_4['Impact_v2_1'] = 0
    tro_nwk_4['Impact_v1_v2'] = 0
    tro_nwk_4['Impact_cst'] = 0

    unitinput = [tro_nwk_4['Name'], tro_nwk_4['Variable1'], tro_nwk_4['Variable2'], tro_nwk_4['Fmin_v1'], tro_nwk_4['Fmax_v1'], tro_nwk_4['Fmin_v2'], tro_nwk_4['Fmax_v2'], tro_nwk_4['Coeff_v1_2'], 
                tro_nwk_4['Coeff_v1_1'], tro_nwk_4['Coeff_v2_2'], tro_nwk_4['Coeff_v2_1'], tro_nwk_4['Coeff_v1_v2'], tro_nwk_4['Coeff_cst'], tro_nwk_4['Fmin'], tro_nwk_4['Fmax'], tro_nwk_4['Cost_v1_2'], 
                tro_nwk_4['Cost_v1_1'], tro_nwk_4['Cost_v2_2'], tro_nwk_4['Cost_v2_1'], tro_nwk_4['Cost_v1_v2'], tro_nwk_4['Cost_cst'], tro_nwk_4['Cinv_v1_2'], tro_nwk_4['Cinv_v1_1'], tro_nwk_4['Cinv_v2_2'], 
                tro_nwk_4['Cinv_v2_1'], tro_nwk_4['Cinv_v1_v2'], tro_nwk_4['Cinv_cst'], tro_nwk_4['Power_v1_2'], tro_nwk_4['Power_v1_1'], tro_nwk_4['Power_v2_2'], tro_nwk_4['Power_v2_1'], 
                tro_nwk_4['Power_v1_v2'], tro_nwk_4['Power_cst'], tro_nwk_4['Impact_v1_2'], tro_nwk_4['Impact_v1_1'], tro_nwk_4['Impact_v2_2'], tro_nwk_4['Impact_v2_1'], tro_nwk_4['Impact_v1_v2'], 
                tro_nwk_4['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True) 
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}                                                                ##The flowrate into the tro branch is the sum of the flowrates to pfa and ser   
    stream1['Parent'] = 'tro_nwk_1'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'tro_nwk_1_flow_in'
    stream1['Layer'] = 'chil2distnwk_flow'
    stream1['Stream_coeff_v1_2'] = 0
    stream1['Stream_coeff_v1_1'] = 1
    stream1['Stream_coeff_v2_2'] = 0
    stream1['Stream_coeff_v2_1'] = 1
    stream1['Stream_coeff_v1_v2'] = 0
    stream1['Stream_coeff_cst'] = 0
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Parent'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Stream_coeff_v1_2'], stream1['Stream_coeff_v1_1'], stream1['Stream_coeff_v2_2'],
                   stream1['Stream_coeff_v2_1'], stream1['Stream_coeff_v1_v2'], stream1['Stream_coeff_cst'], stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)

    ##Stream 2
    stream2 = {}                                                                ##The flowrate to the pfa network from tro network    
    stream2['Parent'] = 'tro_nwk_1'
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'tro_nwk_1_2_pfa'
    stream2['Layer'] = 'tro_nwk2pfa_nwk'
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
    stream3 = {}                                                                ##The flowrate to the ser network from tro network    
    stream3['Parent'] = 'tro_nwk_1'
    stream3['Type'] = 'balancing_only'
    stream3['Name'] = 'tro_nwk_1_2_ser'
    stream3['Layer'] = 'tro_nwk2ser_nwk'
    stream3['Stream_coeff_v1_2'] = 0
    stream3['Stream_coeff_v1_1'] = 0
    stream3['Stream_coeff_v2_2'] = 0
    stream3['Stream_coeff_v2_1'] = 1
    stream3['Stream_coeff_v1_v2'] = 0
    stream3['Stream_coeff_cst'] = 0
    stream3['InOut'] = 'out'
    
    streaminput = [stream3['Parent'], stream3['Type'], stream3['Name'], stream3['Layer'], stream3['Stream_coeff_v1_2'], stream3['Stream_coeff_v1_1'], stream3['Stream_coeff_v2_2'],
                   stream3['Stream_coeff_v2_1'], stream3['Stream_coeff_v1_v2'], stream3['Stream_coeff_cst'], stream3['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 4
    stream4 = {}                                                                ##The associated pressure-drop component from the tro common network     
    stream4['Parent'] = 'tro_nwk_1'
    stream4['Type'] = 'balancing_only'
    stream4['Name'] = 'tro_nwk_1_pfa_delp_component'
    stream4['Layer'] = 'tro_nwkandpfa_nwk_delp'
    stream4['Stream_coeff_v1_2'] = 0
    stream4['Stream_coeff_v1_1'] = tro_network['tro_nwk_tro_grad1']['value']
    stream4['Stream_coeff_v2_2'] = 0
    stream4['Stream_coeff_v2_1'] = tro_network['tro_nwk_tro_grad1']['value']
    stream4['Stream_coeff_v1_v2'] = 0
    stream4['Stream_coeff_cst'] = tro_network['tro_nwk_tro_int1']['value']
    stream4['InOut'] = 'out'
    
    streaminput = [stream4['Parent'], stream4['Type'], stream4['Name'], stream4['Layer'], stream4['Stream_coeff_v1_2'], stream4['Stream_coeff_v1_1'], stream4['Stream_coeff_v2_2'],
                   stream4['Stream_coeff_v2_1'], stream4['Stream_coeff_v1_v2'], stream4['Stream_coeff_cst'], stream4['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 5
    stream5 = {}                                                                ##The associated pressure-drop component from the tro common network     
    stream5['Parent'] = 'tro_nwk_1'
    stream5['Type'] = 'balancing_only'
    stream5['Name'] = 'tro_nwk_1_ser_delp_component'
    stream5['Layer'] = 'tro_nwkandser_nwk_delp'
    stream5['Stream_coeff_v1_2'] = 0
    stream5['Stream_coeff_v1_1'] = tro_network['tro_nwk_tro_grad1']['value']
    stream5['Stream_coeff_v2_2'] = 0
    stream5['Stream_coeff_v2_1'] = tro_network['tro_nwk_tro_grad1']['value']
    stream5['Stream_coeff_v1_v2'] = 0
    stream5['Stream_coeff_cst'] = tro_network['tro_nwk_tro_int1']['value']
    stream5['InOut'] = 'out'
    
    streaminput = [stream5['Parent'], stream5['Type'], stream5['Name'], stream5['Layer'], stream5['Stream_coeff_v1_2'], stream5['Stream_coeff_v1_1'], stream5['Stream_coeff_v2_2'],
                   stream5['Stream_coeff_v2_1'], stream5['Stream_coeff_v1_v2'], stream5['Stream_coeff_cst'], stream5['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 6
    stream6 = {}                                                                ##The flowrate into the tro branch is the sum of the flowrates to pfa and ser   
    stream6['Parent'] = 'tro_nwk_2'
    stream6['Type'] = 'balancing_only'
    stream6['Name'] = 'tro_nwk_2_flow_in'
    stream6['Layer'] = 'chil2distnwk_flow'
    stream6['Stream_coeff_v1_2'] = 0
    stream6['Stream_coeff_v1_1'] = 1
    stream6['Stream_coeff_v2_2'] = 0
    stream6['Stream_coeff_v2_1'] = 1
    stream6['Stream_coeff_v1_v2'] = 0
    stream6['Stream_coeff_cst'] = 0
    stream6['InOut'] = 'in'
    
    streaminput = [stream6['Parent'], stream6['Type'], stream6['Name'], stream6['Layer'], stream6['Stream_coeff_v1_2'], stream6['Stream_coeff_v1_1'], stream6['Stream_coeff_v2_2'],
                   stream6['Stream_coeff_v2_1'], stream6['Stream_coeff_v1_v2'], stream6['Stream_coeff_cst'], stream6['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)

    ##Stream 7
    stream7 = {}                                                                ##The flowrate to the pfa network from tro network    
    stream7['Parent'] = 'tro_nwk_2'
    stream7['Type'] = 'balancing_only'
    stream7['Name'] = 'tro_nwk_2_2_pfa'
    stream7['Layer'] = 'tro_nwk2pfa_nwk'
    stream7['Stream_coeff_v1_2'] = 0
    stream7['Stream_coeff_v1_1'] = 1
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

    ##Stream 8
    stream8 = {}                                                                ##The flowrate to the ser network from tro network    
    stream8['Parent'] = 'tro_nwk_2'
    stream8['Type'] = 'balancing_only'
    stream8['Name'] = 'tro_nwk_2_2_ser'
    stream8['Layer'] = 'tro_nwk2ser_nwk'
    stream8['Stream_coeff_v1_2'] = 0
    stream8['Stream_coeff_v1_1'] = 0
    stream8['Stream_coeff_v2_2'] = 0
    stream8['Stream_coeff_v2_1'] = 1
    stream8['Stream_coeff_v1_v2'] = 0
    stream8['Stream_coeff_cst'] = 0
    stream8['InOut'] = 'out'
    
    streaminput = [stream8['Parent'], stream8['Type'], stream8['Name'], stream8['Layer'], stream8['Stream_coeff_v1_2'], stream8['Stream_coeff_v1_1'], stream8['Stream_coeff_v2_2'],
                   stream8['Stream_coeff_v2_1'], stream8['Stream_coeff_v1_v2'], stream8['Stream_coeff_cst'], stream8['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 9
    stream9 = {}                                                                ##The associated pressure-drop component from the tro common network     
    stream9['Parent'] = 'tro_nwk_2'
    stream9['Type'] = 'balancing_only'
    stream9['Name'] = 'tro_nwk_2_pfa_delp_component'
    stream9['Layer'] = 'tro_nwkandpfa_nwk_delp'
    stream9['Stream_coeff_v1_2'] = 0
    stream9['Stream_coeff_v1_1'] = tro_network['tro_nwk_tro_grad2']['value']
    stream9['Stream_coeff_v2_2'] = 0
    stream9['Stream_coeff_v2_1'] = tro_network['tro_nwk_tro_grad2']['value']
    stream9['Stream_coeff_v1_v2'] = 0
    stream9['Stream_coeff_cst'] = tro_network['tro_nwk_tro_int2']['value']
    stream9['InOut'] = 'out'
    
    streaminput = [stream9['Parent'], stream9['Type'], stream9['Name'], stream9['Layer'], stream9['Stream_coeff_v1_2'], stream9['Stream_coeff_v1_1'], stream9['Stream_coeff_v2_2'],
                   stream9['Stream_coeff_v2_1'], stream9['Stream_coeff_v1_v2'], stream9['Stream_coeff_cst'], stream9['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 10
    stream10 = {}                                                                ##The associated pressure-drop component from the tro common network     
    stream10['Parent'] = 'tro_nwk_2'
    stream10['Type'] = 'balancing_only'
    stream10['Name'] = 'tro_nwk_2_ser_delp_component'
    stream10['Layer'] = 'tro_nwkandser_nwk_delp'
    stream10['Stream_coeff_v1_2'] = 0
    stream10['Stream_coeff_v1_1'] = tro_network['tro_nwk_tro_grad2']['value']
    stream10['Stream_coeff_v2_2'] = 0
    stream10['Stream_coeff_v2_1'] = tro_network['tro_nwk_tro_grad2']['value']
    stream10['Stream_coeff_v1_v2'] = 0
    stream10['Stream_coeff_cst'] = tro_network['tro_nwk_tro_int2']['value']
    stream10['InOut'] = 'out'
    
    streaminput = [stream10['Parent'], stream10['Type'], stream10['Name'], stream10['Layer'], stream10['Stream_coeff_v1_2'], stream10['Stream_coeff_v1_1'], stream10['Stream_coeff_v2_2'],
                   stream10['Stream_coeff_v2_1'], stream10['Stream_coeff_v1_v2'], stream10['Stream_coeff_cst'], stream10['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 11
    stream11 = {}                                                                ##The flowrate into the tro branch is the sum of the flowrates to pfa and ser   
    stream11['Parent'] = 'tro_nwk_3'
    stream11['Type'] = 'balancing_only'
    stream11['Name'] = 'tro_nwk_3_flow_in'
    stream11['Layer'] = 'chil2distnwk_flow'
    stream11['Stream_coeff_v1_2'] = 0
    stream11['Stream_coeff_v1_1'] = 1
    stream11['Stream_coeff_v2_2'] = 0
    stream11['Stream_coeff_v2_1'] = 1
    stream11['Stream_coeff_v1_v2'] = 0
    stream11['Stream_coeff_cst'] = 0
    stream11['InOut'] = 'in'
    
    streaminput = [stream11['Parent'], stream11['Type'], stream11['Name'], stream11['Layer'], stream11['Stream_coeff_v1_2'], stream11['Stream_coeff_v1_1'], stream11['Stream_coeff_v2_2'],
                   stream11['Stream_coeff_v2_1'], stream11['Stream_coeff_v1_v2'], stream11['Stream_coeff_cst'], stream11['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)

    ##Stream 12
    stream12 = {}                                                                ##The flowrate to the pfa network from tro network    
    stream12['Parent'] = 'tro_nwk_3'
    stream12['Type'] = 'balancing_only'
    stream12['Name'] = 'tro_nwk_3_2_pfa'
    stream12['Layer'] = 'tro_nwk2pfa_nwk'
    stream12['Stream_coeff_v1_2'] = 0
    stream12['Stream_coeff_v1_1'] = 1
    stream12['Stream_coeff_v2_2'] = 0
    stream12['Stream_coeff_v2_1'] = 0
    stream12['Stream_coeff_v1_v2'] = 0
    stream12['Stream_coeff_cst'] = 0
    stream12['InOut'] = 'out'
    
    streaminput = [stream12['Parent'], stream12['Type'], stream12['Name'], stream12['Layer'], stream12['Stream_coeff_v1_2'], stream12['Stream_coeff_v1_1'], stream12['Stream_coeff_v2_2'],
                   stream12['Stream_coeff_v2_1'], stream12['Stream_coeff_v1_v2'], stream12['Stream_coeff_cst'], stream12['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)

    ##Stream 13
    stream13 = {}                                                                ##The flowrate to the ser network from tro network    
    stream13['Parent'] = 'tro_nwk_3'
    stream13['Type'] = 'balancing_only'
    stream13['Name'] = 'tro_nwk_3_2_ser'
    stream13['Layer'] = 'tro_nwk2ser_nwk'
    stream13['Stream_coeff_v1_2'] = 0
    stream13['Stream_coeff_v1_1'] = 0
    stream13['Stream_coeff_v2_2'] = 0
    stream13['Stream_coeff_v2_1'] = 1
    stream13['Stream_coeff_v1_v2'] = 0
    stream13['Stream_coeff_cst'] = 0
    stream13['InOut'] = 'out'
    
    streaminput = [stream13['Parent'], stream13['Type'], stream13['Name'], stream13['Layer'], stream13['Stream_coeff_v1_2'], stream13['Stream_coeff_v1_1'], stream13['Stream_coeff_v2_2'],
                   stream13['Stream_coeff_v2_1'], stream13['Stream_coeff_v1_v2'], stream13['Stream_coeff_cst'], stream13['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 14
    stream14 = {}                                                                ##The associated pressure-drop component from the tro common network     
    stream14['Parent'] = 'tro_nwk_3'
    stream14['Type'] = 'balancing_only'
    stream14['Name'] = 'tro_nwk_3_pfa_delp_component'
    stream14['Layer'] = 'tro_nwkandpfa_nwk_delp'
    stream14['Stream_coeff_v1_2'] = 0
    stream14['Stream_coeff_v1_1'] = tro_network['tro_nwk_tro_grad3']['value']
    stream14['Stream_coeff_v2_2'] = 0
    stream14['Stream_coeff_v2_1'] = tro_network['tro_nwk_tro_grad3']['value']
    stream14['Stream_coeff_v1_v2'] = 0
    stream14['Stream_coeff_cst'] = tro_network['tro_nwk_tro_int3']['value']
    stream14['InOut'] = 'out'
    
    streaminput = [stream14['Parent'], stream14['Type'], stream14['Name'], stream14['Layer'], stream14['Stream_coeff_v1_2'], stream14['Stream_coeff_v1_1'], stream14['Stream_coeff_v2_2'],
                   stream14['Stream_coeff_v2_1'], stream14['Stream_coeff_v1_v2'], stream14['Stream_coeff_cst'], stream14['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 15
    stream15 = {}                                                                ##The associated pressure-drop component from the tro common network     
    stream15['Parent'] = 'tro_nwk_3'
    stream15['Type'] = 'balancing_only'
    stream15['Name'] = 'tro_nwk_3_ser_delp_component'
    stream15['Layer'] = 'tro_nwkandser_nwk_delp'
    stream15['Stream_coeff_v1_2'] = 0
    stream15['Stream_coeff_v1_1'] = tro_network['tro_nwk_tro_grad3']['value']
    stream15['Stream_coeff_v2_2'] = 0
    stream15['Stream_coeff_v2_1'] = tro_network['tro_nwk_tro_grad3']['value']
    stream15['Stream_coeff_v1_v2'] = 0
    stream15['Stream_coeff_cst'] = tro_network['tro_nwk_tro_int3']['value']
    stream15['InOut'] = 'out'
    
    streaminput = [stream15['Parent'], stream15['Type'], stream15['Name'], stream15['Layer'], stream15['Stream_coeff_v1_2'], stream15['Stream_coeff_v1_1'], stream15['Stream_coeff_v2_2'],
                   stream15['Stream_coeff_v2_1'], stream15['Stream_coeff_v1_v2'], stream15['Stream_coeff_cst'], stream15['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 16
    stream16 = {}                                                                ##The flowrate into the tro branch is the sum of the flowrates to pfa and ser   
    stream16['Parent'] = 'tro_nwk_4'
    stream16['Type'] = 'balancing_only'
    stream16['Name'] = 'tro_nwk_4_flow_in'
    stream16['Layer'] = 'chil2distnwk_flow'
    stream16['Stream_coeff_v1_2'] = 0
    stream16['Stream_coeff_v1_1'] = 1
    stream16['Stream_coeff_v2_2'] = 0
    stream16['Stream_coeff_v2_1'] = 1
    stream16['Stream_coeff_v1_v2'] = 0
    stream16['Stream_coeff_cst'] = 0
    stream16['InOut'] = 'in'
    
    streaminput = [stream16['Parent'], stream16['Type'], stream16['Name'], stream16['Layer'], stream16['Stream_coeff_v1_2'], stream16['Stream_coeff_v1_1'], stream16['Stream_coeff_v2_2'],
                   stream16['Stream_coeff_v2_1'], stream16['Stream_coeff_v1_v2'], stream16['Stream_coeff_cst'], stream16['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)

    ##Stream 17
    stream17 = {}                                                                ##The flowrate to the pfa network from tro network    
    stream17['Parent'] = 'tro_nwk_4'
    stream17['Type'] = 'balancing_only'
    stream17['Name'] = 'tro_nwk_4_2_pfa'
    stream17['Layer'] = 'tro_nwk2pfa_nwk'
    stream17['Stream_coeff_v1_2'] = 0
    stream17['Stream_coeff_v1_1'] = 1
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
    stream18 = {}                                                                ##The flowrate to the ser network from tro network    
    stream18['Parent'] = 'tro_nwk_4'
    stream18['Type'] = 'balancing_only'
    stream18['Name'] = 'tro_nwk_4_2_ser'
    stream18['Layer'] = 'tro_nwk2ser_nwk'
    stream18['Stream_coeff_v1_2'] = 0
    stream18['Stream_coeff_v1_1'] = 0
    stream18['Stream_coeff_v2_2'] = 0
    stream18['Stream_coeff_v2_1'] = 1
    stream18['Stream_coeff_v1_v2'] = 0
    stream18['Stream_coeff_cst'] = 0
    stream18['InOut'] = 'out'
    
    streaminput = [stream18['Parent'], stream18['Type'], stream18['Name'], stream18['Layer'], stream18['Stream_coeff_v1_2'], stream18['Stream_coeff_v1_1'], stream18['Stream_coeff_v2_2'],
                   stream18['Stream_coeff_v2_1'], stream18['Stream_coeff_v1_v2'], stream18['Stream_coeff_cst'], stream18['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 19
    stream19 = {}                                                                ##The associated pressure-drop component from the tro common network     
    stream19['Parent'] = 'tro_nwk_4'
    stream19['Type'] = 'balancing_only'
    stream19['Name'] = 'tro_nwk_4_pfa_delp_component'
    stream19['Layer'] = 'tro_nwkandpfa_nwk_delp'
    stream19['Stream_coeff_v1_2'] = 0
    stream19['Stream_coeff_v1_1'] = tro_network['tro_nwk_tro_grad4']['value']
    stream19['Stream_coeff_v2_2'] = 0
    stream19['Stream_coeff_v2_1'] = tro_network['tro_nwk_tro_grad4']['value']
    stream19['Stream_coeff_v1_v2'] = 0
    stream19['Stream_coeff_cst'] = tro_network['tro_nwk_tro_int4']['value']
    stream19['InOut'] = 'out'
    
    streaminput = [stream19['Parent'], stream19['Type'], stream19['Name'], stream19['Layer'], stream19['Stream_coeff_v1_2'], stream19['Stream_coeff_v1_1'], stream19['Stream_coeff_v2_2'],
                   stream19['Stream_coeff_v2_1'], stream19['Stream_coeff_v1_v2'], stream19['Stream_coeff_cst'], stream19['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 20
    stream20 = {}                                                                ##The associated pressure-drop component from the tro common network     
    stream20['Parent'] = 'tro_nwk_4'
    stream20['Type'] = 'balancing_only'
    stream20['Name'] = 'tro_nwk_4_ser_delp_component'
    stream20['Layer'] = 'tro_nwkandser_nwk_delp'
    stream20['Stream_coeff_v1_2'] = 0
    stream20['Stream_coeff_v1_1'] = tro_network['tro_nwk_tro_grad4']['value']
    stream20['Stream_coeff_v2_2'] = 0
    stream20['Stream_coeff_v2_1'] = tro_network['tro_nwk_tro_grad4']['value']
    stream20['Stream_coeff_v1_v2'] = 0
    stream20['Stream_coeff_cst'] = tro_network['tro_nwk_tro_int4']['value']
    stream20['InOut'] = 'out'
    
    streaminput = [stream20['Parent'], stream20['Type'], stream20['Name'], stream20['Layer'], stream20['Stream_coeff_v1_2'], stream20['Stream_coeff_v1_1'], stream20['Stream_coeff_v2_2'],
                   stream20['Stream_coeff_v2_1'], stream20['Stream_coeff_v1_v2'], stream20['Stream_coeff_cst'], stream20['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Constraint definition
    
    ##Equation definitions
    
    ##Equation 1
    eqn1 = {}
    eqn1['Name'] = 'totaluse_tro_nwk'
    eqn1['Type'] = 'unit_binary'
    eqn1['Sign'] = 'less_than_equal_to'
    eqn1['RHS_value'] = 1
    
    eqninput = [eqn1['Name'], eqn1['Type'], eqn1['Sign'], eqn1['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation terms
    
    ##Term 1
    term1 = {}
    term1['Parent_unit'] = 'tro_nwk_1'
    term1['Parent_eqn'] = 'totaluse_tro_nwk'
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
    term2['Parent_unit'] = 'tro_nwk_2'
    term2['Parent_eqn'] = 'totaluse_tro_nwk'
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
    term3['Parent_unit'] = 'tro_nwk_3'
    term3['Parent_eqn'] = 'totaluse_tro_nwk'
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
    term4['Parent_unit'] = 'tro_nwk_4'
    term4['Parent_eqn'] = 'totaluse_tro_nwk'
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