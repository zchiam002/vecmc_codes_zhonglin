##This is an additional unit to ensure that the flowrate of the chillers match that of the master decision variable is totally consumed

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'process'
    return unit_type
    
def chiller_evap_flow_consol (ch_e_f_c_mdv, processlist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    
    ##Model description 
    ##This model ensures that all the flowrate from the chillers tally to the the decided total flowrate by the master optimizer
    ##The purpose of this model is just to introduce some additional equality constraints 
    
    ##Legend of input variables 
    
    ##ch_e_f_c_tf = ch_e_f_c_mdv['Value'][0]        -the total flowrate which has to come out of the chiller evaporators 
    
    ##Processing the list of master decision variables as parameters 
    ch_e_f_c_tf = ch_e_f_c_mdv['Value'][0]

    ##Define the dictionary of values 
    
    chiller_evap_flow_consol = {}
    ##Input constants 
    
    ##1
    ch_e_f_c_totalflow = {}
    ch_e_f_c_totalflow['value'] = ch_e_f_c_tf
    ch_e_f_c_totalflow['units'] = 'm3/h'
    ch_e_f_c_totalflow['status'] = 'cst_input'
    chiller_evap_flow_consol['ch_e_f_c_totalflow'] = ch_e_f_c_tf

    ##Unit definition 
    
    ##Unit 1 
    ch_e_f_c = {}
    ch_e_f_c['Name'] = 'ch_e_f_c'
    ch_e_f_c['Variable1'] = 'm'                                                                                                                 
    ch_e_f_c['Variable2'] = '-'                                                                                                          
    ch_e_f_c['Fmin_v1'] = 0 
    ch_e_f_c['Fmax_v1'] = chiller_evap_flow_consol['ch_e_f_c_totalflow']['value']                                                                                                                    
    ch_e_f_c['Fmin_v2'] = 0                                                                                                      
    ch_e_f_c['Fmax_v2'] = 0                                                                                    
    ch_e_f_c['Coeff_v1_2'] = 0                                                                                                                 
    ch_e_f_c['Coeff_v1_1'] = 0          
    ch_e_f_c['Coeff_v2_2'] = 0
    ch_e_f_c['Coeff_v2_1'] = 0
    ch_e_f_c['Coeff_v1_v2'] = 0
    ch_e_f_c['Coeff_cst'] = 0
    ch_e_f_c['Fmin'] = 0
    ch_e_f_c['Fmax'] = 0
    ch_e_f_c['Cost_v1_2'] = 0
    ch_e_f_c['Cost_v1_1'] = 0
    ch_e_f_c['Cost_v2_2'] = 0
    ch_e_f_c['Cost_v2_1'] = 0
    ch_e_f_c['Cost_v1_v2'] = 0
    ch_e_f_c['Cost_cst'] = 0
    ch_e_f_c['Cinv_v1_2'] = 0
    ch_e_f_c['Cinv_v1_1'] = 0
    ch_e_f_c['Cinv_v2_2'] = 0
    ch_e_f_c['Cinv_v2_1'] = 0
    ch_e_f_c['Cinv_v1_v2'] = 0
    ch_e_f_c['Cinv_cst'] = 0
    ch_e_f_c['Power_v1_2'] = 0
    ch_e_f_c['Power_v1_1'] = 0
    ch_e_f_c['Power_v2_2'] = 0
    ch_e_f_c['Power_v2_1'] = 0
    ch_e_f_c['Power_v1_v2'] = 0
    ch_e_f_c['Power_cst'] = 0
    ch_e_f_c['Impact_v1_2'] = 0
    ch_e_f_c['Impact_v1_1'] = 0
    ch_e_f_c['Impact_v2_2'] = 0
    ch_e_f_c['Impact_v2_1'] = 0
    ch_e_f_c['Impact_v1_v2'] = 0
    ch_e_f_c['Impact_cst'] = 0

    unitinput = [ch_e_f_c['Name'], ch_e_f_c['Variable1'], ch_e_f_c['Variable2'], ch_e_f_c['Fmin_v1'], ch_e_f_c['Fmax_v1'], ch_e_f_c['Fmin_v2'], ch_e_f_c['Fmax_v2'], ch_e_f_c['Coeff_v1_2'], 
                ch_e_f_c['Coeff_v1_1'], ch_e_f_c['Coeff_v2_2'], ch_e_f_c['Coeff_v2_1'], ch_e_f_c['Coeff_v1_v2'], ch_e_f_c['Coeff_cst'], ch_e_f_c['Fmin'], ch_e_f_c['Fmax'], ch_e_f_c['Cost_v1_2'], 
                ch_e_f_c['Cost_v1_1'], ch_e_f_c['Cost_v2_2'], ch_e_f_c['Cost_v2_1'], ch_e_f_c['Cost_v1_v2'], ch_e_f_c['Cost_cst'], ch_e_f_c['Cinv_v1_2'], ch_e_f_c['Cinv_v1_1'], ch_e_f_c['Cinv_v2_2'], 
                ch_e_f_c['Cinv_v2_1'], ch_e_f_c['Cinv_v1_v2'], ch_e_f_c['Cinv_cst'], ch_e_f_c['Power_v1_2'], ch_e_f_c['Power_v1_1'], ch_e_f_c['Power_v2_2'], ch_e_f_c['Power_v2_1'], 
                ch_e_f_c['Power_v1_v2'], ch_e_f_c['Power_cst'], ch_e_f_c['Impact_v1_2'], ch_e_f_c['Impact_v1_1'], ch_e_f_c['Impact_v2_2'], ch_e_f_c['Impact_v2_1'], ch_e_f_c['Impact_v1_v2'], 
                ch_e_f_c['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    processlist = processlist.append(unitdf, ignore_index=True)   
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}                                                                ##The input stream from the chillers need to match to that of the master decision 
    stream1['Parent'] = 'ch_e_f_c'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'ch_e_f_c_mf_in'
    stream1['Layer'] = 'chil2distnwk_flow_check'
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
    
    return processlist, streams, cons_eqns, cons_eqns_terms
    