##This is an additional unit to ensure that the flowrate of the chillers match that of the master decision variable is totally consumed

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype_chiller_evap_flow_consol (unit_type):                  ##Input the unit type here
    unit_type = 'process'
    return unit_type
    
def chiller_evap_flow_consol (ch_e_f_c_mdv, processlist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    
    ##Model description 
    ##This model ensures that all the flowrate from the chillers tally to the the decided total flowrate by the master optimizer
    ##The purpose of this model is just to introduce some additional equality constraints  
    
    ##Processing the list of master decision variables as parameters 
    ch_e_f_c_tf = ch_e_f_c_mdv['Value'][0]
    
    ##Unit definition 
    
    ##Unit 1 
    ud = {}
    ud['Name'] = 'ch_e_f_c'
    ud['Variable1'] = 'm_perc'                                                                                                                 
    ud['Variable2'] = '-'                                                                                                          
    ud['Fmin_v1'] = 0 
    ud['Fmax_v1'] = 1                                                                                                                 
    ud['Fmin_v2'] = 0                                                                                                      
    ud['Fmax_v2'] = 0                                                                                    
    ud['Coeff_v1_2'] = 0                                                                                                                 
    ud['Coeff_v1_1'] = 0          
    ud['Coeff_v2_2'] = 0
    ud['Coeff_v2_1'] = 0
    ud['Coeff_v1_v2'] = 0
    ud['Coeff_cst'] = 0
    ud['Fmin'] = 0
    ud['Fmax'] = 0
    ud['Cost_v1_2'] = 0
    ud['Cost_v1_1'] = 0
    ud['Cost_v2_2'] = 0
    ud['Cost_v2_1'] = 0
    ud['Cost_v1_v2'] = 0
    ud['Cost_cst'] = 0
    ud['Cinv_v1_2'] = 0
    ud['Cinv_v1_1'] = 0
    ud['Cinv_v2_2'] = 0
    ud['Cinv_v2_1'] = 0
    ud['Cinv_v1_v2'] = 0
    ud['Cinv_cst'] = 0
    ud['Power_v1_2'] = 0
    ud['Power_v1_1'] = 0
    ud['Power_v2_2'] = 0
    ud['Power_v2_1'] = 0
    ud['Power_v1_v2'] = 0
    ud['Power_cst'] = 0
    ud['Impact_v1_2'] = 0
    ud['Impact_v1_1'] = 0
    ud['Impact_v2_2'] = 0
    ud['Impact_v2_1'] = 0
    ud['Impact_v1_v2'] = 0
    ud['Impact_cst'] = 0

    unitinput = [ud['Name'], ud['Variable1'], ud['Variable2'], ud['Fmin_v1'], ud['Fmax_v1'], ud['Fmin_v2'], ud['Fmax_v2'], ud['Coeff_v1_2'], 
                ud['Coeff_v1_1'], ud['Coeff_v2_2'], ud['Coeff_v2_1'], ud['Coeff_v1_v2'], ud['Coeff_cst'], ud['Fmin'], ud['Fmax'], ud['Cost_v1_2'], 
                ud['Cost_v1_1'], ud['Cost_v2_2'], ud['Cost_v2_1'], ud['Cost_v1_v2'], ud['Cost_cst'], ud['Cinv_v1_2'], ud['Cinv_v1_1'], ud['Cinv_v2_2'], 
                ud['Cinv_v2_1'], ud['Cinv_v1_v2'], ud['Cinv_cst'], ud['Power_v1_2'], ud['Power_v1_1'], ud['Power_v2_2'], ud['Power_v2_1'], 
                ud['Power_v1_v2'], ud['Power_cst'], ud['Impact_v1_2'], ud['Impact_v1_1'], ud['Impact_v2_2'], ud['Impact_v2_1'], ud['Impact_v1_v2'], 
                ud['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    processlist = processlist.append(unitdf, ignore_index=True)   
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream = {}                                                                ##The input stream from the chillers need to match to that of the master decision 
    stream['Parent'] = 'ch_e_f_c'
    stream['Type'] = 'balancing_only'
    stream['Name'] = 'ch_e_f_c_flow_in'
    stream['Layer'] = 'evapnwk_consol_flow'
    stream['Stream_coeff_v1_2'] = 0
    stream['Stream_coeff_v1_1'] = ch_e_f_c_tf 
    stream['Stream_coeff_v2_2'] = 0
    stream['Stream_coeff_v2_1'] = 0
    stream['Stream_coeff_v1_v2'] = 0
    stream['Stream_coeff_cst'] = 0
    stream['InOut'] = 'in'
    
    streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
                   stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)   
    
    return processlist, streams, cons_eqns, cons_eqns_terms
    