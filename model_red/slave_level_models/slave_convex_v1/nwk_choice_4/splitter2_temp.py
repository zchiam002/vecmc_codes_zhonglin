##This is the temperature aggregator and stream splitter model 

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type

def splitter2_temp (sp2_temp_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    
    #Model description 
    ##This model copies the inlet stream and duplicates it to the required number of outlet streams 
    
    ##Unit definition
    
    ##Unit 1

    sp2_temp = {}
    sp2_temp['Name'] = 'sp2_temp'
    sp2_temp['Variable1'] = 't_inout'                                                                                                     
    sp2_temp['Variable2'] = '-'                                                                                                       
    sp2_temp['Fmin_v1'] = 0 
    sp2_temp['Fmax_v1'] = 1000                                                                                                                  
    sp2_temp['Fmin_v2'] = 0                                                                                                        
    sp2_temp['Fmax_v2'] = 0                                                                                  
    sp2_temp['Coeff_v1_2'] = 0                                                                                                                 
    sp2_temp['Coeff_v1_1'] = 1         
    sp2_temp['Coeff_v2_2'] = 0
    sp2_temp['Coeff_v2_1'] = 0
    sp2_temp['Coeff_v1_v2'] = 0 
    sp2_temp['Coeff_cst'] = 0
    sp2_temp['Fmin'] = 0
    sp2_temp['Fmax'] = 1000
    sp2_temp['Cost_v1_2'] = 0
    sp2_temp['Cost_v1_1'] = 0
    sp2_temp['Cost_v2_2'] = 0
    sp2_temp['Cost_v2_1'] = 0
    sp2_temp['Cost_v1_v2'] = 0
    sp2_temp['Cost_cst'] = 0
    sp2_temp['Cinv_v1_2'] = 0
    sp2_temp['Cinv_v1_1'] = 0
    sp2_temp['Cinv_v2_2'] = 0
    sp2_temp['Cinv_v2_1'] = 0
    sp2_temp['Cinv_v1_v2'] = 0
    sp2_temp['Cinv_cst'] = 0
    sp2_temp['Power_v1_2'] = 0
    sp2_temp['Power_v1_1'] = 0
    sp2_temp['Power_v2_2'] = 0
    sp2_temp['Power_v2_1'] = 0
    sp2_temp['Power_v1_v2'] = 0
    sp2_temp['Power_cst'] = 0
    sp2_temp['Impact_v1_2'] = 0
    sp2_temp['Impact_v1_1'] = 0
    sp2_temp['Impact_v2_2'] = 0
    sp2_temp['Impact_v2_1'] = 0
    sp2_temp['Impact_v1_v2'] = 0
    sp2_temp['Impact_cst'] = 0

    unitinput = [sp2_temp['Name'], sp2_temp['Variable1'], sp2_temp['Variable2'], sp2_temp['Fmin_v1'], sp2_temp['Fmax_v1'], sp2_temp['Fmin_v2'], sp2_temp['Fmax_v2'], sp2_temp['Coeff_v1_2'], 
                sp2_temp['Coeff_v1_1'], sp2_temp['Coeff_v2_2'], sp2_temp['Coeff_v2_1'], sp2_temp['Coeff_v1_v2'], sp2_temp['Coeff_cst'], sp2_temp['Fmin'], sp2_temp['Fmax'], sp2_temp['Cost_v1_2'], 
                sp2_temp['Cost_v1_1'], sp2_temp['Cost_v2_2'], sp2_temp['Cost_v2_1'], sp2_temp['Cost_v1_v2'], sp2_temp['Cost_cst'], sp2_temp['Cinv_v1_2'], sp2_temp['Cinv_v1_1'], sp2_temp['Cinv_v2_2'], 
                sp2_temp['Cinv_v2_1'], sp2_temp['Cinv_v1_v2'], sp2_temp['Cinv_cst'], sp2_temp['Power_v1_2'], sp2_temp['Power_v1_1'], sp2_temp['Power_v2_2'], sp2_temp['Power_v2_1'], 
                sp2_temp['Power_v1_v2'], sp2_temp['Power_cst'], sp2_temp['Impact_v1_2'], sp2_temp['Impact_v1_1'], sp2_temp['Impact_v2_2'], sp2_temp['Impact_v2_1'], sp2_temp['Impact_v1_v2'], 
                sp2_temp['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}                                                                
    stream1['Parent'] = 'sp2_temp'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'ss2sp2_tin'
    stream1['Layer'] = 'ss2sp2_temp'
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
    stream2['Parent'] = 'sp2_temp'                                              ##Copied output to chiller 1 return
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'sp2_temp2ch1ret_tout'
    stream2['Layer'] = 'sp2_2_ch1ret_temp'
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
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms
