## This is the cooling tower model, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype_cooling_tower2_4nc (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type
    
def cooling_tower2_4nc (ct2_4nc_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    from cooling_tower2_4nc_compute import cooling_tower2_4nc_compute
    import pandas as pd
    import numpy as np
    
    ##Model description: 
    ##Built based on Universal Engineering Cooling Tower Model by L.Lu
    ##It is simplified to a bilinear model with the upper and lower limits defined  
    
    
    ##ct2_4nc_mdv --- the master decision variables which are used as parameters at this stage 
    ##utilitylist --- a dataframe to hold essential values for writing the MILP script 
    ##streams --- a dataframe to write connections to other units 
    ##cons_eqns --- additional constraints are explicitly stated here 
    ##cons_eqns_terms --- the terms to the constraints 
    
    ##Defining inputs
    
    ##Processing list of master decision variables as parameters
    ct2_4nc_twb = ct2_4nc_mdv['Value'][0]                                       ##Thermodynamic wetbulb temperature
    ct2_4nc_c0 = ct2_4nc_mdv['Value'][1]                                        ##ma coeff    
    ct2_4nc_c1 = ct2_4nc_mdv['Value'][2]                                        ##twi coeff   
    ct2_4nc_c2 = ct2_4nc_mdv['Value'][3]                                        ##matwi coeff    
    ct2_4nc_c3 = ct2_4nc_mdv['Value'][4]                                        ##cst    
    ct2_4nc_tcnwkflow = ct2_4nc_mdv['Value'][5]                                 ##Total condenser network flow   
    
    ##Defined constants 
    ct2_4nc_num_towers_config = 5
    ct2_4nc_ma_min = 0.05
    ct2_4nc_ma_max = 1
    ct2_4nc_twi_range = 10
    ct2_4nc_max_ma_flow = 369117                                                ##kg/hr of air 
    ct2_4nc_min_approach = 1
    ct2_4nc_elect_max = 22
    ct2_4nc_make_up_water_correct_coeff = 2.3294122
    
    ##Calling a compute file to process dependent values
        ##Placing the values in a numpy array for easy data handling 
    ct2_4nc_dc = np.zeros((11, 1))    
    ct2_4nc_dc[0,0] = ct2_4nc_twb
    ct2_4nc_dc[1,0] = ct2_4nc_twi_range
    ct2_4nc_dc[2,0] = ct2_4nc_min_approach
    ct2_4nc_dc[3,0] = ct2_4nc_make_up_water_correct_coeff     
    ct2_4nc_dc[4,0] = ct2_4nc_tcnwkflow   
    ct2_4nc_dc[5,0] = ct2_4nc_num_towers_config  
    ct2_4nc_dc[6,0] = ct2_4nc_max_ma_flow 
    ct2_4nc_dc[7,0] = ct2_4nc_c0 
    ct2_4nc_dc[8,0] = ct2_4nc_c1 
    ct2_4nc_dc[9,0] = ct2_4nc_c2 
    ct2_4nc_dc[10,0] = ct2_4nc_c3 
    
    ct2_4nc_calc = cooling_tower2_4nc_compute(ct2_4nc_dc)
    
#################################################################################################################################################################################################        
    
    ##Unit definition 
    
    ##Unit 1
    ct1 = {}
    ct1['Name'] = 'ct2_4nc'
    ct1['Variable1'] = 'ma'                                                                                                           
    ct1['Variable2'] = 'twi'                                                                                                          
    ct1['Fmin_v1'] = ct2_4nc_ma_min 
    ct1['Fmax_v1'] = ct2_4nc_ma_max                                                                           
    ct1['Fmin_v2'] = 0                                                                                             
    ct1['Fmax_v2'] = 1                                                                       
    ct1['Coeff_v1_2'] = 0                                                                                                            
    ct1['Coeff_v1_1'] = 0   
    ct1['Coeff_v2_2'] = 0
    ct1['Coeff_v2_1'] = 0
    ct1['Coeff_v1_v2'] = 0
    ct1['Coeff_cst'] = 0
    ct1['Fmin'] = 0
    ct1['Fmax'] = 0
    ct1['Cost_v1_2'] = 0
    ct1['Cost_v1_1'] = 0
    ct1['Cost_v2_2'] = 0
    ct1['Cost_v2_1'] = 0
    ct1['Cost_v1_v2'] = 0
    ct1['Cost_cst'] = 0
    ct1['Cinv_v1_2'] = 0
    ct1['Cinv_v1_1'] = 0
    ct1['Cinv_v2_2'] = 0
    ct1['Cinv_v2_1'] = 0
    ct1['Cinv_v1_v2'] = 0
    ct1['Cinv_cst'] = 0
    ct1['Power_v1_2'] = 0
    ct1['Power_v1_1'] = ct2_4nc_elect_max
    ct1['Power_v2_2'] = 0
    ct1['Power_v2_1'] = 0
    ct1['Power_v1_v2'] = 0
    ct1['Power_cst'] = 0
    ct1['Impact_v1_2'] = 0
    ct1['Impact_v1_1'] = 0
    ct1['Impact_v2_2'] = 0
    ct1['Impact_v2_1'] = 0
    ct1['Impact_v1_v2'] = 0
    ct1['Impact_cst'] = 0

    unitinput = [ct1['Name'], ct1['Variable1'], ct1['Variable2'], ct1['Fmin_v1'], ct1['Fmax_v1'], ct1['Fmin_v2'], ct1['Fmax_v2'], ct1['Coeff_v1_2'], 
                ct1['Coeff_v1_1'], ct1['Coeff_v2_2'], ct1['Coeff_v2_1'], ct1['Coeff_v1_v2'], ct1['Coeff_cst'], ct1['Fmin'], ct1['Fmax'], ct1['Cost_v1_2'], 
                ct1['Cost_v1_1'], ct1['Cost_v2_2'], ct1['Cost_v2_1'], ct1['Cost_v1_v2'], ct1['Cost_cst'], ct1['Cinv_v1_2'], ct1['Cinv_v1_1'], ct1['Cinv_v2_2'], 
                ct1['Cinv_v2_1'], ct1['Cinv_v1_v2'], ct1['Cinv_cst'], ct1['Power_v1_2'], ct1['Power_v1_1'], ct1['Power_v2_2'], ct1['Power_v2_1'], 
                ct1['Power_v1_v2'], ct1['Power_cst'], ct1['Impact_v1_2'], ct1['Impact_v1_1'], ct1['Impact_v2_2'], ct1['Impact_v2_1'], ct1['Impact_v1_v2'], 
                ct1['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}                                                                ##The inlet temperature flow into the cooling tower                                          
    stream1['Parent'] = 'ct2_4nc'
    stream1['Type'] = 'temp_chil'
    stream1['Name'] = 'ct2_4nc_tin'
    stream1['Layer'] = 'sp3_2_ct2_temp'
    stream1['Stream_coeff_v1_2'] = 0
    stream1['Stream_coeff_v1_1'] = 0
    stream1['Stream_coeff_v2_2'] = 0
    stream1['Stream_coeff_v2_1'] = ct2_4nc_calc[1,0] - ct2_4nc_calc[0,0]
    stream1['Stream_coeff_v1_v2'] = 0
    stream1['Stream_coeff_cst'] = ct2_4nc_calc[0,0]
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Parent'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Stream_coeff_v1_2'], stream1['Stream_coeff_v1_1'], stream1['Stream_coeff_v2_2'],
                   stream1['Stream_coeff_v2_1'], stream1['Stream_coeff_v1_v2'], stream1['Stream_coeff_cst'], stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)

    ##Stream 2
    stream2 = {}                                                                
    stream2['Parent'] = 'ct2_4nc'                                               ##the outlet temperature flow out of the cooling tower as a fraction
    stream2['Type'] = 'temp_chil'
    stream2['Name'] = 'ct2_4nc_tout'
    stream2['Layer'] = 'ct_2_sp4_temp'
    stream2['Stream_coeff_v1_2'] = 0
    stream2['Stream_coeff_v1_1'] = -(ct2_4nc_calc[2,0]) / ct2_4nc_num_towers_config
    stream2['Stream_coeff_v2_2'] = 0
    stream2['Stream_coeff_v2_1'] = ((ct2_4nc_calc[1,0] - ct2_4nc_calc[0,0]) - ct2_4nc_calc[3,0]) / ct2_4nc_num_towers_config 
    stream2['Stream_coeff_v1_v2'] = -(ct2_4nc_calc[4,0]) / ct2_4nc_num_towers_config 
    stream2['Stream_coeff_cst'] = (ct2_4nc_calc[0,0] - ct2_4nc_calc[5,0]) / ct2_4nc_num_towers_config
    stream2['InOut'] = 'out'
    
    streaminput = [stream2['Parent'], stream2['Type'], stream2['Name'], stream2['Layer'], stream2['Stream_coeff_v1_2'], stream2['Stream_coeff_v1_1'], stream2['Stream_coeff_v2_2'],
                   stream2['Stream_coeff_v2_1'], stream2['Stream_coeff_v1_v2'], stream2['Stream_coeff_cst'], stream2['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    
    ##Constraint definition
    
    ##Equation definitions
    
    ##Ensure that the totaluse is equals to 1
    eqn = {}                                                                    ##This is to make sure that this unit is always turn on
    eqn['Name'] = 'totaluse_ct2_4nc'
    eqn['Type'] = 'unit_binary'
    eqn['Sign'] = 'equal_to'
    eqn['RHS_value'] = 1
    
    eqninput = [eqn['Name'], eqn['Type'], eqn['Sign'], eqn['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)      
    
#    eqn = {}                                                                    ##This is to make sure that the outlet temperature does not go lower than 1 degree approach
#    eqn['Name'] = 'ct2_4nc_min_frac_tout'
#    eqn['Type'] = 'stream_limit_modified'                                       ##Note that if it is greater than equal to, the RHS need to be 0 ALWAYS!
#    eqn['Sign'] = 'greater_than_equal_to'
#    eqn['RHS_value'] = 0
#    
#    eqninput = [eqn['Name'], eqn['Type'], eqn['Sign'], eqn['RHS_value']]
#    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
#    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)    
    
    ##Equation terms
    
    term = {}
    term['Parent_unit'] = 'ct2_4nc'
    term['Parent_eqn'] = 'totaluse_ct2_4nc'
    term['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types 
    term['Coefficient'] = 1
    term['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
    term['Coeff_v1_1'] = 0
    term['Coeff_v2_2'] = 0
    term['Coeff_v2_1'] = 0
    term['Coeff_v1_v2'] = 0
    term['Coeff_cst'] = 0

    terminput = [term['Parent_unit'], term['Parent_eqn'], term['Parent_stream'], term['Coefficient'], term['Coeff_v1_2'],
                 term['Coeff_v1_1'], term['Coeff_v2_2'], term['Coeff_v2_1'], term['Coeff_v1_v2'], term['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)     
    
#    term = {}
#    term['Parent_unit'] = 'ct2_4nc'
#    term['Parent_eqn'] = 'ct2_4nc_min_frac_tout'
#    term['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types 
#    term['Coefficient'] = 0
#    term['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
#    term['Coeff_v1_1'] = -(ct2_4nc_calc[2,0]) / ct2_4nc_num_towers_config
#    term['Coeff_v2_2'] = 0
#    term['Coeff_v2_1'] = ((ct2_4nc_calc[1,0] - ct2_4nc_calc[0,0]) - ct2_4nc_calc[3,0]) / ct2_4nc_num_towers_config
#    term['Coeff_v1_v2'] = -(ct2_4nc_calc[4,0]) / ct2_4nc_num_towers_config
#    term['Coeff_cst'] = ((ct2_4nc_calc[0,0] - ct2_4nc_calc[5,0]) / ct2_4nc_num_towers_config) - ct2_4nc_calc[6,0]
#
#    terminput = [term['Parent_unit'], term['Parent_eqn'], term['Parent_stream'], term['Coefficient'], term['Coeff_v1_2'],
#                 term['Coeff_v1_1'], term['Coeff_v2_2'], term['Coeff_v2_1'], term['Coeff_v1_v2'], term['Coeff_cst']]
#    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
#                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2',
#                                                              'Coeff_cst'])
#    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)     
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms
    
    
