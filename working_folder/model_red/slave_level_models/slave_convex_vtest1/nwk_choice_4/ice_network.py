## This is the ICE network model, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type 
    
def ice_network (ice_nwk_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    from nwk_choice_4.ice_network_compute import ice_network_compute
    import pandas as pd
    import numpy as np 
    
    ##Model description 
    ##This is a 2 split parallel network model with 2 variables. It takes in a mass flowrate stream and gives off 2 mass flowrate and 1 pressure drop stream
        
    ##Define dictionary of values 
    
    ice_network = {}
    
    ##Defined constants 
    
    ##1
    ice_nwk_icecoeff = {}
    ice_nwk_icecoeff['value'] = 0.00011627906976743445
    ice_nwk_icecoeff['units'] = '-'
    ice_nwk_icecoeff['status'] = 'cst'
    ice_network['ice_nwk_icecoeff'] = ice_nwk_icecoeff

    ##2
    ice_nwk_icemaxflow = {}
    ice_nwk_icemaxflow['value'] = 1200                                          ##The upperlimits are needed for stepwise linearization 
    ice_nwk_icemaxflow['units'] = 'm3/h'
    ice_nwk_icemaxflow['status'] = 'cst'
    ice_network['ice_nwk_icemaxflow'] = ice_nwk_icemaxflow    

    ##3
    ice_nwk_gv2maxflow = {}
    ice_nwk_gv2maxflow['value'] = 1000                                          ##The upperlimits for the first variable
    ice_nwk_gv2maxflow['units'] = 'm3/h'
    ice_nwk_gv2maxflow['status'] = 'cst'
    ice_network['ice_nwk_gv2maxflow'] = ice_nwk_gv2maxflow  

    ##4
    ice_nwk_hsbmaxflow = {}
    ice_nwk_hsbmaxflow['value'] = 200                                           ##The upperlimits for the second variable 
    ice_nwk_hsbmaxflow['units'] = 'm3/h'
    ice_nwk_hsbmaxflow['status'] = 'cst'
    ice_network['ice_nwk_hsbmaxflow'] = ice_nwk_hsbmaxflow  

    ##Dependent constants
    ice_nwk_dc = np.zeros((2,1))                                                #initialize the list, note the number of constants
    
    ice_nwk_dc[0,0] = ice_network['ice_nwk_icecoeff']['value']
    ice_nwk_dc[1,0] = ice_network['ice_nwk_icemaxflow']['value']

    ice_nwk_calc = ice_network_compute(ice_nwk_dc)
    
    ##5
    ice_nwk_ice_grad1 = {}
    ice_nwk_ice_grad1['value'] = ice_nwk_calc[0,0]                                                           
    ice_nwk_ice_grad1['units'] = '-'
    ice_nwk_ice_grad1['status'] = 'calc'
    ice_network['ice_nwk_ice_grad1'] = ice_nwk_ice_grad1

    ##6
    ice_nwk_ice_grad2 = {}
    ice_nwk_ice_grad2['value'] = ice_nwk_calc[1,0]                                                           
    ice_nwk_ice_grad2['units'] = '-'
    ice_nwk_ice_grad2['status'] = 'calc'
    ice_network['ice_nwk_ice_grad2'] = ice_nwk_ice_grad2

    ##7
    ice_nwk_ice_grad3 = {}
    ice_nwk_ice_grad3['value'] = ice_nwk_calc[2,0]                                                           
    ice_nwk_ice_grad3['units'] = '-'
    ice_nwk_ice_grad3['status'] = 'calc'
    ice_network['ice_nwk_ice_grad3'] = ice_nwk_ice_grad3

    ##8
    ice_nwk_ice_grad4 = {}
    ice_nwk_ice_grad4['value'] = ice_nwk_calc[3,0]                                                           
    ice_nwk_ice_grad4['units'] = '-'
    ice_nwk_ice_grad4['status'] = 'calc'
    ice_network['ice_nwk_ice_grad4'] = ice_nwk_ice_grad4

    ##9
    ice_nwk_ice_int1 = {}
    ice_nwk_ice_int1['value'] = ice_nwk_calc[4,0]                                                           
    ice_nwk_ice_int1['units'] = '-'
    ice_nwk_ice_int1['status'] = 'calc'
    ice_network['ice_nwk_ice_int1'] = ice_nwk_ice_int1

    ##10
    ice_nwk_ice_int2 = {}
    ice_nwk_ice_int2['value'] = ice_nwk_calc[5,0]                                                           
    ice_nwk_ice_int2['units'] = '-'
    ice_nwk_ice_int2['status'] = 'calc'
    ice_network['ice_nwk_ice_int2'] = ice_nwk_ice_int2

    ##11
    ice_nwk_ice_int3 = {}
    ice_nwk_ice_int3['value'] = ice_nwk_calc[6,0]                                                           
    ice_nwk_ice_int3['units'] = '-'
    ice_nwk_ice_int3['status'] = 'calc'
    ice_network['ice_nwk_ice_int3'] = ice_nwk_ice_int3

    ##12
    ice_nwk_ice_int4 = {}
    ice_nwk_ice_int4['value'] = ice_nwk_calc[7,0]                                                           
    ice_nwk_ice_int4['units'] = '-'
    ice_nwk_ice_int4['status'] = 'calc'
    ice_network['ice_nwk_ice_int4'] = ice_nwk_ice_int4

    ##13
    ice_nwk_f1 = {}
    ice_nwk_f1['value'] = ice_nwk_calc[8,0]
    ice_nwk_f1['units'] = '-'
    ice_nwk_f1['status'] = 'calc'
    ice_network['ice_nwk_f1'] = ice_nwk_f1

    ##14
    ice_nwk_f2 = {}
    ice_nwk_f2['value'] = ice_nwk_calc[9,0]
    ice_nwk_f2['units'] = '-'
    ice_nwk_f2['status'] = 'calc'
    ice_network['ice_nwk_f2'] = ice_nwk_f2

    ##15
    ice_nwk_f3 = {}
    ice_nwk_f3['value'] = ice_nwk_calc[10,0]
    ice_nwk_f3['units'] = '-'
    ice_nwk_f3['status'] = 'calc'
    ice_network['ice_nwk_f3'] = ice_nwk_f3

    ##16
    ice_nwk_f4 = {}
    ice_nwk_f4['value'] = ice_nwk_calc[11,0]
    ice_nwk_f4['units'] = '-'
    ice_nwk_f4['status'] = 'calc'
    ice_network['ice_nwk_f4'] = ice_nwk_f4

    ##17
    ice_nwk_f5 = {}
    ice_nwk_f5['value'] = ice_nwk_calc[12,0]
    ice_nwk_f5['units'] = '-'
    ice_nwk_f5['status'] = 'calc'
    ice_network['ice_nwk_f5'] = ice_nwk_f5

    ##Unit definition 
    
    ##Unit 1
    ice_nwk_1 = {}
    ice_nwk_1['Name'] = 'ice_nwk_1'
    ice_nwk_1['Variable1'] = 'm_gv2'                                                    ##Flowrate to GV2 
    ice_nwk_1['Variable2'] = 'm_hsb'                                                    ##Flowrate to HSB 
    ice_nwk_1['Fmin_v1'] = 0 
    ice_nwk_1['Fmax_v1'] = ice_network['ice_nwk_gv2maxflow']['value']                 ##Maximum value of flow to GV2 
    ice_nwk_1['Fmin_v2'] = 0                                                
    ice_nwk_1['Fmax_v2'] = ice_network['ice_nwk_hsbmaxflow']['value']                 ##Maximum value of flow to HSB
    ice_nwk_1['Coeff_v1_2'] = 0                                          
    ice_nwk_1['Coeff_v1_1'] = 1                                                 
    ice_nwk_1['Coeff_v2_2'] = 0
    ice_nwk_1['Coeff_v2_1'] = 1
    ice_nwk_1['Coeff_v1_v2'] = 0
    ice_nwk_1['Coeff_cst'] = 0
    ice_nwk_1['Fmin'] = ice_network['ice_nwk_f1']['value'] * ice_network['ice_nwk_icemaxflow']['value']
    ice_nwk_1['Fmax'] = ice_network['ice_nwk_f2']['value'] * ice_network['ice_nwk_icemaxflow']['value']
    ice_nwk_1['Cost_v1_2'] = 0
    ice_nwk_1['Cost_v1_1'] = 0
    ice_nwk_1['Cost_v2_2'] = 0
    ice_nwk_1['Cost_v2_1'] = 0
    ice_nwk_1['Cost_v1_v2'] = 0
    ice_nwk_1['Cost_cst'] = 0
    ice_nwk_1['Cinv_v1_2'] = 0
    ice_nwk_1['Cinv_v1_1'] = 0
    ice_nwk_1['Cinv_v2_2'] = 0
    ice_nwk_1['Cinv_v2_1'] = 0
    ice_nwk_1['Cinv_v1_v2'] = 0
    ice_nwk_1['Cinv_cst'] = 0
    ice_nwk_1['Power_v1_2'] = 0
    ice_nwk_1['Power_v1_1'] = 0
    ice_nwk_1['Power_v2_2'] = 0
    ice_nwk_1['Power_v2_1'] = 0
    ice_nwk_1['Power_v1_v2'] = 0
    ice_nwk_1['Power_cst'] = 0
    ice_nwk_1['Impact_v1_2'] = 0
    ice_nwk_1['Impact_v1_1'] = 0
    ice_nwk_1['Impact_v2_2'] = 0
    ice_nwk_1['Impact_v2_1'] = 0
    ice_nwk_1['Impact_v1_v2'] = 0
    ice_nwk_1['Impact_cst'] = 0

    unitinput = [ice_nwk_1['Name'], ice_nwk_1['Variable1'], ice_nwk_1['Variable2'], ice_nwk_1['Fmin_v1'], ice_nwk_1['Fmax_v1'], ice_nwk_1['Fmin_v2'], ice_nwk_1['Fmax_v2'], ice_nwk_1['Coeff_v1_2'], 
                ice_nwk_1['Coeff_v1_1'], ice_nwk_1['Coeff_v2_2'], ice_nwk_1['Coeff_v2_1'], ice_nwk_1['Coeff_v1_v2'], ice_nwk_1['Coeff_cst'], ice_nwk_1['Fmin'], ice_nwk_1['Fmax'], ice_nwk_1['Cost_v1_2'], 
                ice_nwk_1['Cost_v1_1'], ice_nwk_1['Cost_v2_2'], ice_nwk_1['Cost_v2_1'], ice_nwk_1['Cost_v1_v2'], ice_nwk_1['Cost_cst'], ice_nwk_1['Cinv_v1_2'], ice_nwk_1['Cinv_v1_1'], ice_nwk_1['Cinv_v2_2'], 
                ice_nwk_1['Cinv_v2_1'], ice_nwk_1['Cinv_v1_v2'], ice_nwk_1['Cinv_cst'], ice_nwk_1['Power_v1_2'], ice_nwk_1['Power_v1_1'], ice_nwk_1['Power_v2_2'], ice_nwk_1['Power_v2_1'], 
                ice_nwk_1['Power_v1_v2'], ice_nwk_1['Power_cst'], ice_nwk_1['Impact_v1_2'], ice_nwk_1['Impact_v1_1'], ice_nwk_1['Impact_v2_2'], ice_nwk_1['Impact_v2_1'], ice_nwk_1['Impact_v1_v2'], 
                ice_nwk_1['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)   
    
    ##Unit 2
    ice_nwk_2 = {}
    ice_nwk_2['Name'] = 'ice_nwk_2'
    ice_nwk_2['Variable1'] = 'm_gv2'                                                    ##Flowrate to GV2 
    ice_nwk_2['Variable2'] = 'm_hsb'                                                    ##Flowrate to HSB 
    ice_nwk_2['Fmin_v1'] = 0 
    ice_nwk_2['Fmax_v1'] = ice_network['ice_nwk_gv2maxflow']['value']                 ##Maximum value of flow to GV2 
    ice_nwk_2['Fmin_v2'] = 0                                                
    ice_nwk_2['Fmax_v2'] = ice_network['ice_nwk_hsbmaxflow']['value']                 ##Maximum value of flow to HSB
    ice_nwk_2['Coeff_v1_2'] = 0                                          
    ice_nwk_2['Coeff_v1_1'] = 1                                                 
    ice_nwk_2['Coeff_v2_2'] = 0
    ice_nwk_2['Coeff_v2_1'] = 1
    ice_nwk_2['Coeff_v1_v2'] = 0
    ice_nwk_2['Coeff_cst'] = 0
    ice_nwk_2['Fmin'] = ice_network['ice_nwk_f2']['value'] * ice_network['ice_nwk_icemaxflow']['value']
    ice_nwk_2['Fmax'] = ice_network['ice_nwk_f3']['value'] * ice_network['ice_nwk_icemaxflow']['value']
    ice_nwk_2['Cost_v1_2'] = 0
    ice_nwk_2['Cost_v1_1'] = 0
    ice_nwk_2['Cost_v2_2'] = 0
    ice_nwk_2['Cost_v2_1'] = 0
    ice_nwk_2['Cost_v1_v2'] = 0
    ice_nwk_2['Cost_cst'] = 0
    ice_nwk_2['Cinv_v1_2'] = 0
    ice_nwk_2['Cinv_v1_1'] = 0
    ice_nwk_2['Cinv_v2_2'] = 0
    ice_nwk_2['Cinv_v2_1'] = 0
    ice_nwk_2['Cinv_v1_v2'] = 0
    ice_nwk_2['Cinv_cst'] = 0
    ice_nwk_2['Power_v1_2'] = 0
    ice_nwk_2['Power_v1_1'] = 0
    ice_nwk_2['Power_v2_2'] = 0
    ice_nwk_2['Power_v2_1'] = 0
    ice_nwk_2['Power_v1_v2'] = 0
    ice_nwk_2['Power_cst'] = 0
    ice_nwk_2['Impact_v1_2'] = 0
    ice_nwk_2['Impact_v1_1'] = 0
    ice_nwk_2['Impact_v2_2'] = 0
    ice_nwk_2['Impact_v2_1'] = 0
    ice_nwk_2['Impact_v1_v2'] = 0
    ice_nwk_2['Impact_cst'] = 0

    unitinput = [ice_nwk_2['Name'], ice_nwk_2['Variable1'], ice_nwk_2['Variable2'], ice_nwk_2['Fmin_v1'], ice_nwk_2['Fmax_v1'], ice_nwk_2['Fmin_v2'], ice_nwk_2['Fmax_v2'], ice_nwk_2['Coeff_v1_2'], 
                ice_nwk_2['Coeff_v1_1'], ice_nwk_2['Coeff_v2_2'], ice_nwk_2['Coeff_v2_1'], ice_nwk_2['Coeff_v1_v2'], ice_nwk_2['Coeff_cst'], ice_nwk_2['Fmin'], ice_nwk_2['Fmax'], ice_nwk_2['Cost_v1_2'], 
                ice_nwk_2['Cost_v1_1'], ice_nwk_2['Cost_v2_2'], ice_nwk_2['Cost_v2_1'], ice_nwk_2['Cost_v1_v2'], ice_nwk_2['Cost_cst'], ice_nwk_2['Cinv_v1_2'], ice_nwk_2['Cinv_v1_1'], ice_nwk_2['Cinv_v2_2'], 
                ice_nwk_2['Cinv_v2_1'], ice_nwk_2['Cinv_v1_v2'], ice_nwk_2['Cinv_cst'], ice_nwk_2['Power_v1_2'], ice_nwk_2['Power_v1_1'], ice_nwk_2['Power_v2_2'], ice_nwk_2['Power_v2_1'], 
                ice_nwk_2['Power_v1_v2'], ice_nwk_2['Power_cst'], ice_nwk_2['Impact_v1_2'], ice_nwk_2['Impact_v1_1'], ice_nwk_2['Impact_v2_2'], ice_nwk_2['Impact_v2_1'], ice_nwk_2['Impact_v1_v2'], 
                ice_nwk_2['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True) 
    
    ##Unit 3
    ice_nwk_3 = {}
    ice_nwk_3['Name'] = 'ice_nwk_3'
    ice_nwk_3['Variable1'] = 'm_gv2'                                                    ##Flowrate to GV2 
    ice_nwk_3['Variable2'] = 'm_hsb'                                                    ##Flowrate to HSB 
    ice_nwk_3['Fmin_v1'] = 0 
    ice_nwk_3['Fmax_v1'] = ice_network['ice_nwk_gv2maxflow']['value']                 ##Maximum value of flow to GV2 
    ice_nwk_3['Fmin_v2'] = 0                                                
    ice_nwk_3['Fmax_v2'] = ice_network['ice_nwk_hsbmaxflow']['value']                 ##Maximum value of flow to HSB
    ice_nwk_3['Coeff_v1_2'] = 0                                          
    ice_nwk_3['Coeff_v1_1'] = 1                                                 
    ice_nwk_3['Coeff_v2_2'] = 0
    ice_nwk_3['Coeff_v2_1'] = 1
    ice_nwk_3['Coeff_v1_v2'] = 0
    ice_nwk_3['Coeff_cst'] = 0
    ice_nwk_3['Fmin'] = ice_network['ice_nwk_f3']['value'] * ice_network['ice_nwk_icemaxflow']['value']
    ice_nwk_3['Fmax'] = ice_network['ice_nwk_f4']['value'] * ice_network['ice_nwk_icemaxflow']['value']
    ice_nwk_3['Cost_v1_2'] = 0
    ice_nwk_3['Cost_v1_1'] = 0
    ice_nwk_3['Cost_v2_2'] = 0
    ice_nwk_3['Cost_v2_1'] = 0
    ice_nwk_3['Cost_v1_v2'] = 0
    ice_nwk_3['Cost_cst'] = 0
    ice_nwk_3['Cinv_v1_2'] = 0
    ice_nwk_3['Cinv_v1_1'] = 0
    ice_nwk_3['Cinv_v2_2'] = 0
    ice_nwk_3['Cinv_v2_1'] = 0
    ice_nwk_3['Cinv_v1_v2'] = 0
    ice_nwk_3['Cinv_cst'] = 0
    ice_nwk_3['Power_v1_2'] = 0
    ice_nwk_3['Power_v1_1'] = 0
    ice_nwk_3['Power_v2_2'] = 0
    ice_nwk_3['Power_v2_1'] = 0
    ice_nwk_3['Power_v1_v2'] = 0
    ice_nwk_3['Power_cst'] = 0
    ice_nwk_3['Impact_v1_2'] = 0
    ice_nwk_3['Impact_v1_1'] = 0
    ice_nwk_3['Impact_v2_2'] = 0
    ice_nwk_3['Impact_v2_1'] = 0
    ice_nwk_3['Impact_v1_v2'] = 0
    ice_nwk_3['Impact_cst'] = 0

    unitinput = [ice_nwk_3['Name'], ice_nwk_3['Variable1'], ice_nwk_3['Variable2'], ice_nwk_3['Fmin_v1'], ice_nwk_3['Fmax_v1'], ice_nwk_3['Fmin_v2'], ice_nwk_3['Fmax_v2'], ice_nwk_3['Coeff_v1_2'], 
                ice_nwk_3['Coeff_v1_1'], ice_nwk_3['Coeff_v2_2'], ice_nwk_3['Coeff_v2_1'], ice_nwk_3['Coeff_v1_v2'], ice_nwk_3['Coeff_cst'], ice_nwk_3['Fmin'], ice_nwk_3['Fmax'], ice_nwk_3['Cost_v1_2'], 
                ice_nwk_3['Cost_v1_1'], ice_nwk_3['Cost_v2_2'], ice_nwk_3['Cost_v2_1'], ice_nwk_3['Cost_v1_v2'], ice_nwk_3['Cost_cst'], ice_nwk_3['Cinv_v1_2'], ice_nwk_3['Cinv_v1_1'], ice_nwk_3['Cinv_v2_2'], 
                ice_nwk_3['Cinv_v2_1'], ice_nwk_3['Cinv_v1_v2'], ice_nwk_3['Cinv_cst'], ice_nwk_3['Power_v1_2'], ice_nwk_3['Power_v1_1'], ice_nwk_3['Power_v2_2'], ice_nwk_3['Power_v2_1'], 
                ice_nwk_3['Power_v1_v2'], ice_nwk_3['Power_cst'], ice_nwk_3['Impact_v1_2'], ice_nwk_3['Impact_v1_1'], ice_nwk_3['Impact_v2_2'], ice_nwk_3['Impact_v2_1'], ice_nwk_3['Impact_v1_v2'], 
                ice_nwk_3['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True) 
    
    ##Unit 4
    ice_nwk_4 = {}
    ice_nwk_4['Name'] = 'ice_nwk_4'
    ice_nwk_4['Variable1'] = 'm_gv2'                                                    ##Flowrate to GV2 
    ice_nwk_4['Variable2'] = 'm_hsb'                                                    ##Flowrate to HSB 
    ice_nwk_4['Fmin_v1'] = 0 
    ice_nwk_4['Fmax_v1'] = ice_network['ice_nwk_gv2maxflow']['value']                 ##Maximum value of flow to GV2 
    ice_nwk_4['Fmin_v2'] = 0                                                
    ice_nwk_4['Fmax_v2'] = ice_network['ice_nwk_hsbmaxflow']['value']                 ##Maximum value of flow to HSB
    ice_nwk_4['Coeff_v1_2'] = 0                                          
    ice_nwk_4['Coeff_v1_1'] = 1                                                 
    ice_nwk_4['Coeff_v2_2'] = 0
    ice_nwk_4['Coeff_v2_1'] = 1
    ice_nwk_4['Coeff_v1_v2'] = 0
    ice_nwk_4['Coeff_cst'] = 0
    ice_nwk_4['Fmin'] = ice_network['ice_nwk_f4']['value'] * ice_network['ice_nwk_icemaxflow']['value']
    ice_nwk_4['Fmax'] = ice_network['ice_nwk_f5']['value'] * ice_network['ice_nwk_icemaxflow']['value']
    ice_nwk_4['Cost_v1_2'] = 0
    ice_nwk_4['Cost_v1_1'] = 0
    ice_nwk_4['Cost_v2_2'] = 0
    ice_nwk_4['Cost_v2_1'] = 0
    ice_nwk_4['Cost_v1_v2'] = 0
    ice_nwk_4['Cost_cst'] = 0
    ice_nwk_4['Cinv_v1_2'] = 0
    ice_nwk_4['Cinv_v1_1'] = 0
    ice_nwk_4['Cinv_v2_2'] = 0
    ice_nwk_4['Cinv_v2_1'] = 0
    ice_nwk_4['Cinv_v1_v2'] = 0
    ice_nwk_4['Cinv_cst'] = 0
    ice_nwk_4['Power_v1_2'] = 0
    ice_nwk_4['Power_v1_1'] = 0
    ice_nwk_4['Power_v2_2'] = 0
    ice_nwk_4['Power_v2_1'] = 0
    ice_nwk_4['Power_v1_v2'] = 0
    ice_nwk_4['Power_cst'] = 0
    ice_nwk_4['Impact_v1_2'] = 0
    ice_nwk_4['Impact_v1_1'] = 0
    ice_nwk_4['Impact_v2_2'] = 0
    ice_nwk_4['Impact_v2_1'] = 0
    ice_nwk_4['Impact_v1_v2'] = 0
    ice_nwk_4['Impact_cst'] = 0

    unitinput = [ice_nwk_4['Name'], ice_nwk_4['Variable1'], ice_nwk_4['Variable2'], ice_nwk_4['Fmin_v1'], ice_nwk_4['Fmax_v1'], ice_nwk_4['Fmin_v2'], ice_nwk_4['Fmax_v2'], ice_nwk_4['Coeff_v1_2'], 
                ice_nwk_4['Coeff_v1_1'], ice_nwk_4['Coeff_v2_2'], ice_nwk_4['Coeff_v2_1'], ice_nwk_4['Coeff_v1_v2'], ice_nwk_4['Coeff_cst'], ice_nwk_4['Fmin'], ice_nwk_4['Fmax'], ice_nwk_4['Cost_v1_2'], 
                ice_nwk_4['Cost_v1_1'], ice_nwk_4['Cost_v2_2'], ice_nwk_4['Cost_v2_1'], ice_nwk_4['Cost_v1_v2'], ice_nwk_4['Cost_cst'], ice_nwk_4['Cinv_v1_2'], ice_nwk_4['Cinv_v1_1'], ice_nwk_4['Cinv_v2_2'], 
                ice_nwk_4['Cinv_v2_1'], ice_nwk_4['Cinv_v1_v2'], ice_nwk_4['Cinv_cst'], ice_nwk_4['Power_v1_2'], ice_nwk_4['Power_v1_1'], ice_nwk_4['Power_v2_2'], ice_nwk_4['Power_v2_1'], 
                ice_nwk_4['Power_v1_v2'], ice_nwk_4['Power_cst'], ice_nwk_4['Impact_v1_2'], ice_nwk_4['Impact_v1_1'], ice_nwk_4['Impact_v2_2'], ice_nwk_4['Impact_v2_1'], ice_nwk_4['Impact_v1_v2'], 
                ice_nwk_4['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True) 
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}                                                                ##The flowrate into the ice branch is the sum of the flowrates to gv2 and hsb   
    stream1['Parent'] = 'ice_nwk_1'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'ice_nwk_1_flow_in'
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
    stream2 = {}                                                                ##The flowrate to the gv2 network from ice network    
    stream2['Parent'] = 'ice_nwk_1'
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'ice_nwk_1_2_gv2'
    stream2['Layer'] = 'ice_nwk2gv2_nwk'
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
    stream3 = {}                                                                ##The flowrate to the hsb network from ice network    
    stream3['Parent'] = 'ice_nwk_1'
    stream3['Type'] = 'balancing_only'
    stream3['Name'] = 'ice_nwk_1_2_hsb'
    stream3['Layer'] = 'ice_nwk2hsb_nwk'
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
    stream4 = {}                                                                ##The associated pressure-drop component from the ice common network     
    stream4['Parent'] = 'ice_nwk_1'
    stream4['Type'] = 'balancing_only'
    stream4['Name'] = 'ice_nwk_1_gv2_delp_component'
    stream4['Layer'] = 'ice_nwkandgv2_nwk_delp'
    stream4['Stream_coeff_v1_2'] = 0
    stream4['Stream_coeff_v1_1'] = ice_network['ice_nwk_ice_grad1']['value']
    stream4['Stream_coeff_v2_2'] = 0
    stream4['Stream_coeff_v2_1'] = ice_network['ice_nwk_ice_grad1']['value']
    stream4['Stream_coeff_v1_v2'] = 0
    stream4['Stream_coeff_cst'] = ice_network['ice_nwk_ice_int1']['value']
    stream4['InOut'] = 'out'
    
    streaminput = [stream4['Parent'], stream4['Type'], stream4['Name'], stream4['Layer'], stream4['Stream_coeff_v1_2'], stream4['Stream_coeff_v1_1'], stream4['Stream_coeff_v2_2'],
                   stream4['Stream_coeff_v2_1'], stream4['Stream_coeff_v1_v2'], stream4['Stream_coeff_cst'], stream4['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 5
    stream5 = {}                                                                ##The associated pressure-drop component from the ice common network     
    stream5['Parent'] = 'ice_nwk_1'
    stream5['Type'] = 'balancing_only'
    stream5['Name'] = 'ice_nwk_1_hsb_delp_component'
    stream5['Layer'] = 'ice_nwkandhsb_nwk_delp'
    stream5['Stream_coeff_v1_2'] = 0
    stream5['Stream_coeff_v1_1'] = ice_network['ice_nwk_ice_grad1']['value']
    stream5['Stream_coeff_v2_2'] = 0
    stream5['Stream_coeff_v2_1'] = ice_network['ice_nwk_ice_grad1']['value']
    stream5['Stream_coeff_v1_v2'] = 0
    stream5['Stream_coeff_cst'] = ice_network['ice_nwk_ice_int1']['value']
    stream5['InOut'] = 'out'
    
    streaminput = [stream5['Parent'], stream5['Type'], stream5['Name'], stream5['Layer'], stream5['Stream_coeff_v1_2'], stream5['Stream_coeff_v1_1'], stream5['Stream_coeff_v2_2'],
                   stream5['Stream_coeff_v2_1'], stream5['Stream_coeff_v1_v2'], stream5['Stream_coeff_cst'], stream5['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 6
    stream6 = {}                                                                ##The flowrate into the ice branch is the sum of the flowrates to gv2 and hsb   
    stream6['Parent'] = 'ice_nwk_2'
    stream6['Type'] = 'balancing_only'
    stream6['Name'] = 'ice_nwk_2_flow_in'
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
    stream7 = {}                                                                ##The flowrate to the gv2 network from ice network    
    stream7['Parent'] = 'ice_nwk_2'
    stream7['Type'] = 'balancing_only'
    stream7['Name'] = 'ice_nwk_2_2_gv2'
    stream7['Layer'] = 'ice_nwk2gv2_nwk'
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
    stream8 = {}                                                                ##The flowrate to the hsb network from ice network    
    stream8['Parent'] = 'ice_nwk_2'
    stream8['Type'] = 'balancing_only'
    stream8['Name'] = 'ice_nwk_2_2_hsb'
    stream8['Layer'] = 'ice_nwk2hsb_nwk'
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
    stream9 = {}                                                                ##The associated pressure-drop component from the ice common network     
    stream9['Parent'] = 'ice_nwk_2'
    stream9['Type'] = 'balancing_only'
    stream9['Name'] = 'ice_nwk_2_gv2_delp_component'
    stream9['Layer'] = 'ice_nwkandgv2_nwk_delp'
    stream9['Stream_coeff_v1_2'] = 0
    stream9['Stream_coeff_v1_1'] = ice_network['ice_nwk_ice_grad2']['value']
    stream9['Stream_coeff_v2_2'] = 0
    stream9['Stream_coeff_v2_1'] = ice_network['ice_nwk_ice_grad2']['value']
    stream9['Stream_coeff_v1_v2'] = 0
    stream9['Stream_coeff_cst'] = ice_network['ice_nwk_ice_int2']['value']
    stream9['InOut'] = 'out'
    
    streaminput = [stream9['Parent'], stream9['Type'], stream9['Name'], stream9['Layer'], stream9['Stream_coeff_v1_2'], stream9['Stream_coeff_v1_1'], stream9['Stream_coeff_v2_2'],
                   stream9['Stream_coeff_v2_1'], stream9['Stream_coeff_v1_v2'], stream9['Stream_coeff_cst'], stream9['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 10
    stream10 = {}                                                                ##The associated pressure-drop component from the ice common network     
    stream10['Parent'] = 'ice_nwk_2'
    stream10['Type'] = 'balancing_only'
    stream10['Name'] = 'ice_nwk_2_hsb_delp_component'
    stream10['Layer'] = 'ice_nwkandhsb_nwk_delp'
    stream10['Stream_coeff_v1_2'] = 0
    stream10['Stream_coeff_v1_1'] = ice_network['ice_nwk_ice_grad2']['value']
    stream10['Stream_coeff_v2_2'] = 0
    stream10['Stream_coeff_v2_1'] = ice_network['ice_nwk_ice_grad2']['value']
    stream10['Stream_coeff_v1_v2'] = 0
    stream10['Stream_coeff_cst'] = ice_network['ice_nwk_ice_int2']['value']
    stream10['InOut'] = 'out'
    
    streaminput = [stream10['Parent'], stream10['Type'], stream10['Name'], stream10['Layer'], stream10['Stream_coeff_v1_2'], stream10['Stream_coeff_v1_1'], stream10['Stream_coeff_v2_2'],
                   stream10['Stream_coeff_v2_1'], stream10['Stream_coeff_v1_v2'], stream10['Stream_coeff_cst'], stream10['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 11
    stream11 = {}                                                                ##The flowrate into the ice branch is the sum of the flowrates to gv2 and hsb   
    stream11['Parent'] = 'ice_nwk_3'
    stream11['Type'] = 'balancing_only'
    stream11['Name'] = 'ice_nwk_3_flow_in'
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
    stream12 = {}                                                                ##The flowrate to the gv2 network from ice network    
    stream12['Parent'] = 'ice_nwk_3'
    stream12['Type'] = 'balancing_only'
    stream12['Name'] = 'ice_nwk_3_2_gv2'
    stream12['Layer'] = 'ice_nwk2gv2_nwk'
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
    stream13 = {}                                                                ##The flowrate to the hsb network from ice network    
    stream13['Parent'] = 'ice_nwk_3'
    stream13['Type'] = 'balancing_only'
    stream13['Name'] = 'ice_nwk_3_2_hsb'
    stream13['Layer'] = 'ice_nwk2hsb_nwk'
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
    stream14 = {}                                                                ##The associated pressure-drop component from the ice common network     
    stream14['Parent'] = 'ice_nwk_3'
    stream14['Type'] = 'balancing_only'
    stream14['Name'] = 'ice_nwk_3_gv2_delp_component'
    stream14['Layer'] = 'ice_nwkandgv2_nwk_delp'
    stream14['Stream_coeff_v1_2'] = 0
    stream14['Stream_coeff_v1_1'] = ice_network['ice_nwk_ice_grad3']['value']
    stream14['Stream_coeff_v2_2'] = 0
    stream14['Stream_coeff_v2_1'] = ice_network['ice_nwk_ice_grad3']['value']
    stream14['Stream_coeff_v1_v2'] = 0
    stream14['Stream_coeff_cst'] = ice_network['ice_nwk_ice_int3']['value']
    stream14['InOut'] = 'out'
    
    streaminput = [stream14['Parent'], stream14['Type'], stream14['Name'], stream14['Layer'], stream14['Stream_coeff_v1_2'], stream14['Stream_coeff_v1_1'], stream14['Stream_coeff_v2_2'],
                   stream14['Stream_coeff_v2_1'], stream14['Stream_coeff_v1_v2'], stream14['Stream_coeff_cst'], stream14['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 15
    stream15 = {}                                                                ##The associated pressure-drop component from the ice common network     
    stream15['Parent'] = 'ice_nwk_3'
    stream15['Type'] = 'balancing_only'
    stream15['Name'] = 'ice_nwk_3_hsb_delp_component'
    stream15['Layer'] = 'ice_nwkandhsb_nwk_delp'
    stream15['Stream_coeff_v1_2'] = 0
    stream15['Stream_coeff_v1_1'] = ice_network['ice_nwk_ice_grad3']['value']
    stream15['Stream_coeff_v2_2'] = 0
    stream15['Stream_coeff_v2_1'] = ice_network['ice_nwk_ice_grad3']['value']
    stream15['Stream_coeff_v1_v2'] = 0
    stream15['Stream_coeff_cst'] = ice_network['ice_nwk_ice_int3']['value']
    stream15['InOut'] = 'out'
    
    streaminput = [stream15['Parent'], stream15['Type'], stream15['Name'], stream15['Layer'], stream15['Stream_coeff_v1_2'], stream15['Stream_coeff_v1_1'], stream15['Stream_coeff_v2_2'],
                   stream15['Stream_coeff_v2_1'], stream15['Stream_coeff_v1_v2'], stream15['Stream_coeff_cst'], stream15['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 16
    stream16 = {}                                                                ##The flowrate into the ice branch is the sum of the flowrates to gv2 and hsb   
    stream16['Parent'] = 'ice_nwk_4'
    stream16['Type'] = 'balancing_only'
    stream16['Name'] = 'ice_nwk_4_flow_in'
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
    stream17 = {}                                                                ##The flowrate to the gv2 network from ice network    
    stream17['Parent'] = 'ice_nwk_4'
    stream17['Type'] = 'balancing_only'
    stream17['Name'] = 'ice_nwk_4_2_gv2'
    stream17['Layer'] = 'ice_nwk2gv2_nwk'
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
    stream18 = {}                                                                ##The flowrate to the hsb network from ice network    
    stream18['Parent'] = 'ice_nwk_4'
    stream18['Type'] = 'balancing_only'
    stream18['Name'] = 'ice_nwk_4_2_hsb'
    stream18['Layer'] = 'ice_nwk2hsb_nwk'
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
    stream19 = {}                                                                ##The associated pressure-drop component from the ice common network     
    stream19['Parent'] = 'ice_nwk_4'
    stream19['Type'] = 'balancing_only'
    stream19['Name'] = 'ice_nwk_4_gv2_delp_component'
    stream19['Layer'] = 'ice_nwkandgv2_nwk_delp'
    stream19['Stream_coeff_v1_2'] = 0
    stream19['Stream_coeff_v1_1'] = ice_network['ice_nwk_ice_grad4']['value']
    stream19['Stream_coeff_v2_2'] = 0
    stream19['Stream_coeff_v2_1'] = ice_network['ice_nwk_ice_grad4']['value']
    stream19['Stream_coeff_v1_v2'] = 0
    stream19['Stream_coeff_cst'] = ice_network['ice_nwk_ice_int4']['value']
    stream19['InOut'] = 'out'
    
    streaminput = [stream19['Parent'], stream19['Type'], stream19['Name'], stream19['Layer'], stream19['Stream_coeff_v1_2'], stream19['Stream_coeff_v1_1'], stream19['Stream_coeff_v2_2'],
                   stream19['Stream_coeff_v2_1'], stream19['Stream_coeff_v1_v2'], stream19['Stream_coeff_cst'], stream19['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 20
    stream20 = {}                                                                ##The associated pressure-drop component from the ice common network     
    stream20['Parent'] = 'ice_nwk_4'
    stream20['Type'] = 'balancing_only'
    stream20['Name'] = 'ice_nwk_4_hsb_delp_component'
    stream20['Layer'] = 'ice_nwkandhsb_nwk_delp'
    stream20['Stream_coeff_v1_2'] = 0
    stream20['Stream_coeff_v1_1'] = ice_network['ice_nwk_ice_grad4']['value']
    stream20['Stream_coeff_v2_2'] = 0
    stream20['Stream_coeff_v2_1'] = ice_network['ice_nwk_ice_grad4']['value']
    stream20['Stream_coeff_v1_v2'] = 0
    stream20['Stream_coeff_cst'] = ice_network['ice_nwk_ice_int4']['value']
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
    eqn1['Name'] = 'totaluse_ice_nwk'
    eqn1['Type'] = 'unit_binary'
    eqn1['Sign'] = 'less_than_equal_to'
    eqn1['RHS_value'] = 1
    
    eqninput = [eqn1['Name'], eqn1['Type'], eqn1['Sign'], eqn1['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation terms
    
    ##Term 1
    term1 = {}
    term1['Parent_unit'] = 'ice_nwk_1'
    term1['Parent_eqn'] = 'totaluse_ice_nwk'
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
    term2['Parent_unit'] = 'ice_nwk_2'
    term2['Parent_eqn'] = 'totaluse_ice_nwk'
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
    term3['Parent_unit'] = 'ice_nwk_3'
    term3['Parent_eqn'] = 'totaluse_ice_nwk'
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
    term4['Parent_unit'] = 'ice_nwk_4'
    term4['Parent_eqn'] = 'totaluse_ice_nwk'
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