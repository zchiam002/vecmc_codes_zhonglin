##This is chiller 2 evaporator pump model 

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type

def ch2_evap_pump (ch2_ep_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    
    ##Model description: 
    ##Built on pressure drop ratios based on a fixed flowrate to estimate the electricity cost  
    
    ##Legend of input variables 
    
    ##ch2_ep_p_coeff     --- the coefficient pertaining to the pressure term 
    ##ch2_ep_m_coeff     --- the coefficient pertaining to the flowrate term 
    ##ch2_ep_cst         --- the constant term pertaining to the electricity calculation
    ##ch2_ep_max_m       --- the maximum flowrate of the pump configuration 
    
    ##Processing list of master decision variables as parameters
    ch2_ep_p_coeff = ch2_ep_mdv['Value'][0]
    ch2_ep_m_coeff = ch2_ep_mdv['Value'][1]
    ch2_ep_cst = ch2_ep_mdv['Value'][2]
    ch2_ep_max_m = ch2_ep_mdv['Value'][3]

    ##Define dictionary of values
    
    ch2_evap_pump = {}
    ##Input constants 
    
    ##1
    ch2_ep_pressure_coeff = {}
    ch2_ep_pressure_coeff['value'] = ch2_ep_p_coeff
    ch2_ep_pressure_coeff['units'] = '-'
    ch2_ep_pressure_coeff['status'] = 'cst_input'
    ch2_evap_pump['ch2_ep_pressure_coeff'] = ch2_ep_pressure_coeff

    ##2
    ch2_ep_flowrate_coeff = {}
    ch2_ep_flowrate_coeff['value'] = ch2_ep_m_coeff
    ch2_ep_flowrate_coeff['units'] = '-'
    ch2_ep_flowrate_coeff['status'] = 'cst_input'
    ch2_evap_pump['ch2_ep_flowrate_coeff'] = ch2_ep_flowrate_coeff

    ##3
    ch2_ep_constant_term = {}
    ch2_ep_constant_term['value'] = ch2_ep_cst
    ch2_ep_constant_term['units'] = '-'
    ch2_ep_constant_term['status'] = 'cst_input'
    ch2_evap_pump['ch2_ep_constant_term'] = ch2_ep_constant_term    

    ##4
    ch2_ep_maximum_flowrate = {}
    ch2_ep_maximum_flowrate['value'] = ch2_ep_max_m
    ch2_ep_maximum_flowrate['units'] = '-'
    ch2_ep_maximum_flowrate['status'] = 'cst_input'
    ch2_evap_pump['ch2_ep_maximum_flowrate'] = ch2_ep_maximum_flowrate

    ##Unit definition 
    
    ##Unit 1
    ch2_ep = {}
    ch2_ep['Name'] = 'ch2_ep'
    ch2_ep['Variable1'] = 'm_f' 
    ch2_ep['Variable2'] = 'delp'                                                                                                            
    ch2_ep['Fmin_v1'] = 0 
    ch2_ep['Fmax_v1'] = ch2_evap_pump['ch2_ep_maximum_flowrate']['value']                                                                                                                   
    ch2_ep['Fmin_v2'] = 0                                                                                                         
    ch2_ep['Fmax_v2'] = 100                                                     ##Arbiturarily determined, not really important as it is already constrained                                  
    ch2_ep['Coeff_v1_2'] = 0                                                    ##With the regression analysis
    ch2_ep['Coeff_v1_1'] = 0          
    ch2_ep['Coeff_v2_2'] = 0
    ch2_ep['Coeff_v2_1'] = 0
    ch2_ep['Coeff_v1_v2'] = 0
    ch2_ep['Coeff_cst'] = 0
    ch2_ep['Fmin'] = 0
    ch2_ep['Fmax'] = 0
    ch2_ep['Cost_v1_2'] = 0
    ch2_ep['Cost_v1_1'] = 0
    ch2_ep['Cost_v2_2'] = 0
    ch2_ep['Cost_v2_1'] = 0
    ch2_ep['Cost_v1_v2'] = 0
    ch2_ep['Cost_cst'] = 0
    ch2_ep['Cinv_v1_2'] = 0
    ch2_ep['Cinv_v1_1'] = 0
    ch2_ep['Cinv_v2_2'] = 0
    ch2_ep['Cinv_v2_1'] = 0
    ch2_ep['Cinv_v1_v2'] = 0
    ch2_ep['Cinv_cst'] = 0
    ch2_ep['Power_v1_2'] = 0
    ch2_ep['Power_v1_1'] = ch2_evap_pump['ch2_ep_flowrate_coeff']['value']
    ch2_ep['Power_v2_2'] = 0
    ch2_ep['Power_v2_1'] = ch2_evap_pump['ch2_ep_pressure_coeff']['value']
    ch2_ep['Power_v1_v2'] = 0 
    ch2_ep['Power_cst'] = 0
    ch2_ep['Impact_v1_2'] = 0
    ch2_ep['Impact_v1_1'] = 0
    ch2_ep['Impact_v2_2'] = 0
    ch2_ep['Impact_v2_1'] = 0
    ch2_ep['Impact_v1_v2'] = 0
    ch2_ep['Impact_cst'] = 0

    unitinput = [ch2_ep['Name'], ch2_ep['Variable1'], ch2_ep['Variable2'], ch2_ep['Fmin_v1'], ch2_ep['Fmax_v1'], ch2_ep['Fmin_v2'], ch2_ep['Fmax_v2'], ch2_ep['Coeff_v1_2'], 
                ch2_ep['Coeff_v1_1'], ch2_ep['Coeff_v2_2'], ch2_ep['Coeff_v2_1'], ch2_ep['Coeff_v1_v2'], ch2_ep['Coeff_cst'], ch2_ep['Fmin'], ch2_ep['Fmax'], ch2_ep['Cost_v1_2'], 
                ch2_ep['Cost_v1_1'], ch2_ep['Cost_v2_2'], ch2_ep['Cost_v2_1'], ch2_ep['Cost_v1_v2'], ch2_ep['Cost_cst'], ch2_ep['Cinv_v1_2'], ch2_ep['Cinv_v1_1'], ch2_ep['Cinv_v2_2'], 
                ch2_ep['Cinv_v2_1'], ch2_ep['Cinv_v1_v2'], ch2_ep['Cinv_cst'], ch2_ep['Power_v1_2'], ch2_ep['Power_v1_1'], ch2_ep['Power_v2_2'], ch2_ep['Power_v2_1'], 
                ch2_ep['Power_v1_v2'], ch2_ep['Power_cst'], ch2_ep['Impact_v1_2'], ch2_ep['Impact_v1_1'], ch2_ep['Impact_v2_2'], ch2_ep['Impact_v2_1'], ch2_ep['Impact_v1_v2'], 
                ch2_ep['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)

    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}                                                                
    stream1['Parent'] = 'ch2_ep'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'ch2_ep_m_f_in'
    stream1['Layer'] = 'ch2_evap_2_pump_flow'
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
    stream2['Parent'] = 'ch2_ep'
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'ch2_ep_delp_in'
    stream2['Layer'] = 'ch2_evap_2_pump_delp'
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
