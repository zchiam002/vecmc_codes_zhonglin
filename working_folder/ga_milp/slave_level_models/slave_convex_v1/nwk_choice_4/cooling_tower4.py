## This is the cooling tower model, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type
    
def cooling_tower4 (ct4_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    from nwk_choice_4.cooling_tower4_compute import cooling_tower4_compute
    import pandas as pd
    import numpy as np
    
    ##Model description: 
    ##Built based on Universal Engineering Cooling Tower Model by L.Lu
    ##It is simplified to a bilinear model with the upper and lower limits defined  
    
    ##Legend of input variables 
    
    ##ct4_tmfr       - the total massflowrate through all cooling towers
    ##ct4_mfr        - the ratio of flowrate through the tower
    ##ct4_twb        - the thermodynamic wetbulb temperature condition which the tower is subjected to 
    
    ##Processing list of master decision variables as parameters
    ct4_tmfr = ct4_mdv['Value'][0]
    ct4_mfr = ct4_mdv['Value'][1]
    ct4_twb = ct4_mdv['Value'][2]

    ##Define dictionary of values 
    
    cooling_tower4 = {}
    ##Input constants 
    
    ##1
    ct4_totalmassflowrate = {}
    ct4_totalmassflowrate['value'] = ct4_tmfr
    ct4_totalmassflowrate['units'] = 'm3/h'
    ct4_totalmassflowrate['status'] = 'cst_input'
    cooling_tower4['ct4_totalmassflowrate'] = ct4_totalmassflowrate    

    ##2
    ct4_massflowrateratio = {}
    ct4_massflowrateratio['value'] = ct4_mfr
    ct4_massflowrateratio['units'] = '-'
    ct4_massflowrateratio['status'] = 'cst_input'
    cooling_tower4['ct4_massflowrateratio'] = ct4_massflowrateratio

    ##3
    ct4_wetblubtemp = {}
    ct4_wetblubtemp['value'] = ct4_twb
    ct4_wetblubtemp['units'] = '-'
    ct4_wetblubtemp['status'] = 'cst_input'
    cooling_tower4['ct4_wetblubtemp'] = ct4_wetblubtemp

    ##Defined constants     
    
    ##4
    ct4_b0 = {}
    ct4_b0['value'] = 0.14029549639345207
    ct4_b0['units'] = '-'
    ct4_b0['status'] = 'cst'
    cooling_tower4['ct4_b0'] = ct4_b0    

    ##5
    ct4_b1 = {}
    ct4_b1['value'] = 0.600266127023157
    ct4_b1['units'] = '-'
    ct4_b1['status'] = 'cst'
    cooling_tower4['ct4_b1'] = ct4_b1

    ##6
    ct4_b2 = {}
    ct4_b2['value'] = -0.0211475692653011
    ct4_b2['units'] = '-'
    ct4_b2['status'] = 'cst'
    cooling_tower4['ct4_b2'] = ct4_b2

    ##7
    ct4_b3 = {}
    ct4_b3['value'] = 0.2792094538127389
    ct4_b3['units'] = '-'
    ct4_b3['status'] = 'cst'
    cooling_tower4['ct4_b3'] = ct4_b3  

    ##8
    ct4_b4 = {}
    ct4_b4['value'] = 9.294683422723725E-4
    ct4_b4['units'] = '-'
    ct4_b4['status'] = 'cst'
    cooling_tower4['ct4_b4'] = ct4_b4       

    ##9
    ct4_b5 = {}
    ct4_b5['value'] = 0.16052557022400754
    ct4_b5['units'] = '-'
    ct4_b5['status'] = 'cst'
    cooling_tower4['ct4_b5'] = ct4_b5    

    ##10
    ct4_ma_min = {}                                                             ##This is with reference to air flowrate through the fans, not as a result 
    ct4_ma_min['value'] = 0                                                     ##of natural convection 
    ct4_ma_min['units'] = 'kg/h'
    ct4_ma_min['status'] = 'cst'
    cooling_tower4['ct4_ma_min'] = ct4_ma_min

    ##11
    ct4_ma_max = {}
    ct4_ma_max['value'] = 369117
    ct4_ma_max['units'] = 'kg/h'
    ct4_ma_max['status'] = 'cst'
    cooling_tower4['ct4_ma_max'] = ct4_ma_max     

    ##12
    ct4_twi_max = {}
    ct4_twi_max['value'] = 45 + 273.15
    ct4_twi_max['units'] = 'K'
    ct4_twi_max['status'] = 'cst'
    cooling_tower4['ct4_twi_max'] = ct4_twi_max

    ##13
    ct4_efanmax = {}
    ct4_efanmax['value'] = 22
    ct4_efanmax['units'] = 'kWh'
    ct4_efanmax['status'] = 'cst'
    cooling_tower4['ct4_efanmax'] = ct4_efanmax  

    ##Dependent constants
    ct4_dc = np.zeros((13,1))                       #Initialize the list, note the number of constants
    
    ct4_dc[0,0] = cooling_tower4['ct4_totalmassflowrate']['value']
    ct4_dc[1,0] = cooling_tower4['ct4_massflowrateratio']['value']
    ct4_dc[2,0] = cooling_tower4['ct4_wetblubtemp']['value']
    ct4_dc[3,0] = cooling_tower4['ct4_b0']['value']
    ct4_dc[4,0] = cooling_tower4['ct4_b1']['value']
    ct4_dc[5,0] = cooling_tower4['ct4_b2']['value']
    ct4_dc[6,0] = cooling_tower4['ct4_b3']['value']
    ct4_dc[7,0] = cooling_tower4['ct4_b4']['value']
    ct4_dc[8,0] = cooling_tower4['ct4_b5']['value']
    ct4_dc[9,0] = cooling_tower4['ct4_ma_min']['value']
    ct4_dc[10,0] = cooling_tower4['ct4_ma_max']['value']
    ct4_dc[11,0] = cooling_tower4['ct4_twi_max']['value']
    ct4_dc[12,0] = cooling_tower4['ct4_efanmax']['value']

    ct4_calc = cooling_tower4_compute(ct4_dc)
    
    ##14
    ct4_ma_coeff = {}
    ct4_ma_coeff['value'] = ct4_calc[0,0]
    ct4_ma_coeff['units'] = '-'
    ct4_ma_coeff['status'] = 'calc'
    cooling_tower4['ct4_ma_coeff'] = ct4_ma_coeff       

    ##15
    ct4_twi_coeff = {}
    ct4_twi_coeff['value'] = ct4_calc[1,0]
    ct4_twi_coeff['units'] = '-'
    ct4_twi_coeff['status'] = 'calc'
    cooling_tower4['ct4_twi_coeff'] = ct4_twi_coeff  

    ##16
    ct4_matwi_coeff = {}
    ct4_matwi_coeff['value'] = ct4_calc[2,0]
    ct4_matwi_coeff['units'] = '-'
    ct4_matwi_coeff['status'] = 'calc'
    cooling_tower4['ct4_matwi_coeff'] = ct4_matwi_coeff     

    ##17
    ct4_cst_term = {}
    ct4_cst_term['value'] = ct4_calc[3,0]
    ct4_cst_term['units'] = '-'
    ct4_cst_term['status'] = 'calc'
    cooling_tower4['ct4_cst_term'] = ct4_cst_term

    ##18
    ct4_linfancoeff = {}
    ct4_linfancoeff['value'] = ct4_calc[4,0]
    ct4_linfancoeff['units'] = '-'
    ct4_linfancoeff['status'] = 'calc'
    cooling_tower4['ct4_linfancoeff'] = ct4_linfancoeff

    ##Unit definition 
    
    ##Unit 1
    ct4 = {}
    ct4['Name'] = 'ct4'
    ct4['Variable1'] = 'ma'                                                                                                           
    ct4['Variable2'] = 'twi'                                                                                                          
    ct4['Fmin_v1'] = 0 
    ct4['Fmax_v1'] = cooling_tower4['ct4_ma_max']['value']                                                                            
    ct4['Fmin_v2'] = cooling_tower4['ct4_wetblubtemp']['value']                                                                                                           ##The minimum supply temperature of the chiller is 1 deg 
    ct4['Fmax_v2'] = cooling_tower4['ct4_twi_max']['value']                                                                          
    ct4['Coeff_v1_2'] = 0                                                                                                            
    ct4['Coeff_v1_1'] = cooling_tower4['ct4_ma_coeff']['value']   
    ct4['Coeff_v2_2'] = 0
    ct4['Coeff_v2_1'] = cooling_tower4['ct4_twi_coeff']['value']
    ct4['Coeff_v1_v2'] = cooling_tower4['ct4_matwi_coeff']['value']
    ct4['Coeff_cst'] = cooling_tower4['ct4_cst_term']['value']
    ct4['Fmin'] = 0
    ct4['Fmax'] = cooling_tower4['ct4_twi_max']['value'] - cooling_tower4['ct4_wetblubtemp']['value']
    ct4['Cost_v1_2'] = 0
    ct4['Cost_v1_1'] = 0
    ct4['Cost_v2_2'] = 0
    ct4['Cost_v2_1'] = 0
    ct4['Cost_v1_v2'] = 0
    ct4['Cost_cst'] = 0
    ct4['Cinv_v1_2'] = 0
    ct4['Cinv_v1_1'] = 0
    ct4['Cinv_v2_2'] = 0
    ct4['Cinv_v2_1'] = 0
    ct4['Cinv_v1_v2'] = 0
    ct4['Cinv_cst'] = 0
    ct4['Power_v1_2'] = 0
    ct4['Power_v1_1'] = cooling_tower4['ct4_linfancoeff']['value']
    ct4['Power_v2_2'] = 0
    ct4['Power_v2_1'] = 0
    ct4['Power_v1_v2'] = 0
    ct4['Power_cst'] = 0
    ct4['Impact_v1_2'] = 0
    ct4['Impact_v1_1'] = 0
    ct4['Impact_v2_2'] = 0
    ct4['Impact_v2_1'] = 0
    ct4['Impact_v1_v2'] = 0
    ct4['Impact_cst'] = 0

    unitinput = [ct4['Name'], ct4['Variable1'], ct4['Variable2'], ct4['Fmin_v1'], ct4['Fmax_v1'], ct4['Fmin_v2'], ct4['Fmax_v2'], ct4['Coeff_v1_2'], 
                ct4['Coeff_v1_1'], ct4['Coeff_v2_2'], ct4['Coeff_v2_1'], ct4['Coeff_v1_v2'], ct4['Coeff_cst'], ct4['Fmin'], ct4['Fmax'], ct4['Cost_v1_2'], 
                ct4['Cost_v1_1'], ct4['Cost_v2_2'], ct4['Cost_v2_1'], ct4['Cost_v1_v2'], ct4['Cost_cst'], ct4['Cinv_v1_2'], ct4['Cinv_v1_1'], ct4['Cinv_v2_2'], 
                ct4['Cinv_v2_1'], ct4['Cinv_v1_v2'], ct4['Cinv_cst'], ct4['Power_v1_2'], ct4['Power_v1_1'], ct4['Power_v2_2'], ct4['Power_v2_1'], 
                ct4['Power_v1_v2'], ct4['Power_cst'], ct4['Impact_v1_2'], ct4['Impact_v1_1'], ct4['Impact_v2_2'], ct4['Impact_v2_1'], ct4['Impact_v1_v2'], 
                ct4['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}                                                                
    stream1['Parent'] = 'ct4'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'ct4_tin'
    stream1['Layer'] = 'sp3_2_ct4_temp'
    stream1['Stream_coeff_v1_2'] = 0
    stream1['Stream_coeff_v1_1'] = 0
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
    stream2 = {}                                                                
    stream2['Parent'] = 'ct4'
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'ct_tout'
    stream2['Layer'] = 'ct_cond_ret_temp'
    stream2['Stream_coeff_v1_2'] = 0
    stream2['Stream_coeff_v1_1'] = cooling_tower4['ct4_ma_coeff']['value'] 
    stream2['Stream_coeff_v2_2'] = 0
    stream2['Stream_coeff_v2_1'] = cooling_tower4['ct4_twi_coeff']['value'] + 1
    stream2['Stream_coeff_v1_v2'] = cooling_tower4['ct4_matwi_coeff']['value']
    stream2['Stream_coeff_cst'] = cooling_tower4['ct4_cst_term']['value']
    stream2['InOut'] = 'out'
    
    streaminput = [stream2['Parent'], stream2['Type'], stream2['Name'], stream2['Layer'], stream2['Stream_coeff_v1_2'], stream2['Stream_coeff_v1_1'], stream2['Stream_coeff_v2_2'],
                   stream2['Stream_coeff_v2_1'], stream2['Stream_coeff_v1_v2'], stream2['Stream_coeff_cst'], stream2['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Constraint definition
    
    ##Equation definitions
    
    ##Equation 1
    eqn1 = {}
    eqn1['Name'] = 'ct4_toutmax'
    eqn1['Type'] = 'stream_limit_modified'                                      ##Stream modified constraints involving more than 1 variable which cannot be expressed easily
    eqn1['Sign'] = 'less_than_equal_to'
    eqn1['RHS_value'] = -cooling_tower4['ct4_wetblubtemp']['value']
    
    eqninput = [eqn1['Name'], eqn1['Type'], eqn1['Sign'], eqn1['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Term 1
    term1 = {}
    term1['Parent_unit'] = 'ct4'
    term1['Parent_eqn'] = 'ct4_toutmax'
    term1['Parent_stream'] = 'ct_tout'                                          ##Only applicable for stream_limit types 
    term1['Coefficient'] = 0
    term1['Coeff_v1_2'] = 0                                                     ##Only applicable for stream_limit_modified types 
    term1['Coeff_v1_1'] = cooling_tower4['ct4_ma_coeff']['value'] 
    term1['Coeff_v2_2'] = 0
    term1['Coeff_v2_1'] = cooling_tower4['ct4_twi_coeff']['value'] - 1
    term1['Coeff_v1v2'] = cooling_tower4['ct4_matwi_coeff']['value']
    term1['Coeff_cst'] = cooling_tower4['ct4_cst_term']['value']

    terminput = [term1['Parent_unit'], term1['Parent_eqn'], term1['Parent_stream'], term1['Coefficient'], term1['Coeff_v1_2'],
                 term1['Coeff_v1_1'], term1['Coeff_v2_2'], term1['Coeff_v2_1'], term1['Coeff_v1v2'], term1['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms
    
    
