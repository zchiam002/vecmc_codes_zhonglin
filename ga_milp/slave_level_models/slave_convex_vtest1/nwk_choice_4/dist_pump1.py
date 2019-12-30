##This is the distribution pump model 

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type

def dist_pump1 (dp1_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    
    ##Model description: 
    ##Built on pressure drop ratios based on a fixed flowrate to estimate the electricity cost  
    
    ##Legend of input variables 
    
    ##dp1_p_coeff     --- the coefficient pertaining to the pressure term 
    ##dp1_m_coeff     --- the coefficient pertaining to the flowrate term 
    ##dp1_cst         --- the constant term pertaining to the electricity calculation
    ##dp1_max_m       --- the maximum flowrate of the pump configuration 
    
    ##Processing list of master decision variables as parameters
    dp1_p_coeff = dp1_mdv['Value'][0]
    dp1_m_coeff = dp1_mdv['Value'][1]
    dp1_cst = dp1_mdv['Value'][2]
    dp1_max_m = dp1_mdv['Value'][3]

    ##Define dictionary of values
    
    dist_pump1 = {}
    ##Input constants 
    
    ##1
    dp1_pressure_coeff = {}
    dp1_pressure_coeff['value'] = dp1_p_coeff
    dp1_pressure_coeff['units'] = '-'
    dp1_pressure_coeff['status'] = 'cst_input'
    dist_pump1['dp1_pressure_coeff'] = dp1_pressure_coeff

    ##2
    dp1_flowrate_coeff = {}
    dp1_flowrate_coeff['value'] = dp1_m_coeff
    dp1_flowrate_coeff['units'] = '-'
    dp1_flowrate_coeff['status'] = 'cst_input'
    dist_pump1['dp1_flowrate_coeff'] = dp1_flowrate_coeff

    ##3
    dp1_constant_term = {}
    dp1_constant_term['value'] = dp1_cst
    dp1_constant_term['units'] = '-'
    dp1_constant_term['status'] = 'cst_input'
    dist_pump1['dp1_constant_term'] = dp1_constant_term    

    ##4
    dp1_maximum_flowrate = {}
    dp1_maximum_flowrate['value'] = dp1_max_m
    dp1_maximum_flowrate['units'] = '-'
    dp1_maximum_flowrate['status'] = 'cst_input'
    dist_pump1['dp1_maximum_flowrate'] = dp1_maximum_flowrate

    ##Unit definition 
    
    ##Unit 1
    dist_p = {}
    dist_p['Name'] = 'dist_p1'
    dist_p['Variable1'] = 'm_f' 
    dist_p['Variable2'] = 'delp'                                                                                                            
    dist_p['Fmin_v1'] = 0 
    dist_p['Fmax_v1'] = dist_pump1['dp1_maximum_flowrate']['value']                                                                                                                   
    dist_p['Fmin_v2'] = 0                                                                                                         
    dist_p['Fmax_v2'] = 100                                                     ##Arbiturarily determined, not really important as it is already constrained                                  
    dist_p['Coeff_v1_2'] = 0                                                    ##With the regression analysis
    dist_p['Coeff_v1_1'] = 0          
    dist_p['Coeff_v2_2'] = 0
    dist_p['Coeff_v2_1'] = 0
    dist_p['Coeff_v1_v2'] = 0
    dist_p['Coeff_cst'] = 0
    dist_p['Fmin'] = 0
    dist_p['Fmax'] = 0
    dist_p['Cost_v1_2'] = 0
    dist_p['Cost_v1_1'] = 0
    dist_p['Cost_v2_2'] = 0
    dist_p['Cost_v2_1'] = 0
    dist_p['Cost_v1_v2'] = 0
    dist_p['Cost_cst'] = 0
    dist_p['Cinv_v1_2'] = 0
    dist_p['Cinv_v1_1'] = 0
    dist_p['Cinv_v2_2'] = 0
    dist_p['Cinv_v2_1'] = 0
    dist_p['Cinv_v1_v2'] = 0
    dist_p['Cinv_cst'] = 0
    dist_p['Power_v1_2'] = 0
    dist_p['Power_v1_1'] = dist_pump1['dp1_flowrate_coeff']['value']
    dist_p['Power_v2_2'] = 0
    dist_p['Power_v2_1'] = dist_pump1['dp1_pressure_coeff']['value']
    dist_p['Power_v1_v2'] = 0 
    dist_p['Power_cst'] = 0
    dist_p['Impact_v1_2'] = 0
    dist_p['Impact_v1_1'] = 0
    dist_p['Impact_v2_2'] = 0
    dist_p['Impact_v2_1'] = 0
    dist_p['Impact_v1_v2'] = 0
    dist_p['Impact_cst'] = 0

    unitinput = [dist_p['Name'], dist_p['Variable1'], dist_p['Variable2'], dist_p['Fmin_v1'], dist_p['Fmax_v1'], dist_p['Fmin_v2'], dist_p['Fmax_v2'], dist_p['Coeff_v1_2'], 
                dist_p['Coeff_v1_1'], dist_p['Coeff_v2_2'], dist_p['Coeff_v2_1'], dist_p['Coeff_v1_v2'], dist_p['Coeff_cst'], dist_p['Fmin'], dist_p['Fmax'], dist_p['Cost_v1_2'], 
                dist_p['Cost_v1_1'], dist_p['Cost_v2_2'], dist_p['Cost_v2_1'], dist_p['Cost_v1_v2'], dist_p['Cost_cst'], dist_p['Cinv_v1_2'], dist_p['Cinv_v1_1'], dist_p['Cinv_v2_2'], 
                dist_p['Cinv_v2_1'], dist_p['Cinv_v1_v2'], dist_p['Cinv_cst'], dist_p['Power_v1_2'], dist_p['Power_v1_1'], dist_p['Power_v2_2'], dist_p['Power_v2_1'], 
                dist_p['Power_v1_v2'], dist_p['Power_cst'], dist_p['Impact_v1_2'], dist_p['Impact_v1_1'], dist_p['Impact_v2_2'], dist_p['Impact_v2_1'], dist_p['Impact_v1_v2'], 
                dist_p['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)

    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}                                                                
    stream1['Parent'] = 'dist_p1'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'dp1_m_f_in'
    stream1['Layer'] = 'ss_2_dist_pump1_flow'
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
    stream2 = {}                                                                
    stream2['Parent'] = 'dist_p1'
    stream2['Type'] = 'network_parallel'
    stream2['Name'] = 'dp1_delp_in'
    stream2['Layer'] = 'dist_nwk2_selected_pump1'
    stream2['Stream_coeff_v1_2'] = 0
    stream2['Stream_coeff_v1_1'] = 0
    stream2['Stream_coeff_v2_2'] = 0
    stream2['Stream_coeff_v2_1'] = 1
    stream2['Stream_coeff_v1_v2'] = 0
    stream2['Stream_coeff_cst'] = 0
    stream2['InOut'] = 'in'
    
    streaminput = [stream2['Parent'], stream2['Type'], stream2['Name'], stream2['Layer'], stream2['Stream_coeff_v1_2'], stream2['Stream_coeff_v1_1'], stream2['Stream_coeff_v2_2'],
                   stream2['Stream_coeff_v2_1'], stream2['Stream_coeff_v1_v2'], stream2['Stream_coeff_cst'], stream2['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms