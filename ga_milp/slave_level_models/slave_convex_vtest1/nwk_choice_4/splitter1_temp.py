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

def splitter1_temp (sp1_temp_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    
    #Model description 
    ##This model copies the inlet stream and duplicates it to the required number of outlet streams 
    
    ##Unit definition
    
    ##Unit 1

    sp1_temp = {}
    sp1_temp['Name'] = 'sp1_temp'
    sp1_temp['Variable1'] = 't_inout'                                                                                                     
    sp1_temp['Variable2'] = '-'                                                                                                       
    sp1_temp['Fmin_v1'] = 0 
    sp1_temp['Fmax_v1'] = 1000                                                                                                                  
    sp1_temp['Fmin_v2'] = 0                                                                                                        
    sp1_temp['Fmax_v2'] = 0                                                                                  
    sp1_temp['Coeff_v1_2'] = 0                                                                                                                 
    sp1_temp['Coeff_v1_1'] = 1         
    sp1_temp['Coeff_v2_2'] = 0
    sp1_temp['Coeff_v2_1'] = 0
    sp1_temp['Coeff_v1_v2'] = 0 
    sp1_temp['Coeff_cst'] = 0
    sp1_temp['Fmin'] = 0
    sp1_temp['Fmax'] = 1000
    sp1_temp['Cost_v1_2'] = 0
    sp1_temp['Cost_v1_1'] = 0
    sp1_temp['Cost_v2_2'] = 0
    sp1_temp['Cost_v2_1'] = 0
    sp1_temp['Cost_v1_v2'] = 0
    sp1_temp['Cost_cst'] = 0
    sp1_temp['Cinv_v1_2'] = 0
    sp1_temp['Cinv_v1_1'] = 0
    sp1_temp['Cinv_v2_2'] = 0
    sp1_temp['Cinv_v2_1'] = 0
    sp1_temp['Cinv_v1_v2'] = 0
    sp1_temp['Cinv_cst'] = 0
    sp1_temp['Power_v1_2'] = 0
    sp1_temp['Power_v1_1'] = 0
    sp1_temp['Power_v2_2'] = 0
    sp1_temp['Power_v2_1'] = 0
    sp1_temp['Power_v1_v2'] = 0
    sp1_temp['Power_cst'] = 0
    sp1_temp['Impact_v1_2'] = 0
    sp1_temp['Impact_v1_1'] = 0
    sp1_temp['Impact_v2_2'] = 0
    sp1_temp['Impact_v2_1'] = 0
    sp1_temp['Impact_v1_v2'] = 0
    sp1_temp['Impact_cst'] = 0

    unitinput = [sp1_temp['Name'], sp1_temp['Variable1'], sp1_temp['Variable2'], sp1_temp['Fmin_v1'], sp1_temp['Fmax_v1'], sp1_temp['Fmin_v2'], sp1_temp['Fmax_v2'], sp1_temp['Coeff_v1_2'], 
                sp1_temp['Coeff_v1_1'], sp1_temp['Coeff_v2_2'], sp1_temp['Coeff_v2_1'], sp1_temp['Coeff_v1_v2'], sp1_temp['Coeff_cst'], sp1_temp['Fmin'], sp1_temp['Fmax'], sp1_temp['Cost_v1_2'], 
                sp1_temp['Cost_v1_1'], sp1_temp['Cost_v2_2'], sp1_temp['Cost_v2_1'], sp1_temp['Cost_v1_v2'], sp1_temp['Cost_cst'], sp1_temp['Cinv_v1_2'], sp1_temp['Cinv_v1_1'], sp1_temp['Cinv_v2_2'], 
                sp1_temp['Cinv_v2_1'], sp1_temp['Cinv_v1_v2'], sp1_temp['Cinv_cst'], sp1_temp['Power_v1_2'], sp1_temp['Power_v1_1'], sp1_temp['Power_v2_2'], sp1_temp['Power_v2_1'], 
                sp1_temp['Power_v1_v2'], sp1_temp['Power_cst'], sp1_temp['Impact_v1_2'], sp1_temp['Impact_v1_1'], sp1_temp['Impact_v2_2'], sp1_temp['Impact_v2_1'], sp1_temp['Impact_v1_v2'], 
                sp1_temp['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}                                                                ##This is the input from the chillers. 
    stream1['Parent'] = 'sp1_temp'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'chil2sp1_tin'
    stream1['Layer'] = 'chil2sp1_temp'
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
    stream2['Parent'] = 'sp1_temp'                                              ##Copied output to the common pipe
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'sp1_temp2cp_tout'
    stream2['Layer'] = 'sp1_temp2cp'
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
    stream3 = {}                                                                ##Copied output to gv2 substation 
    stream3['Parent'] = 'sp1_temp'
    stream3['Type'] = 'balancing_only'
    stream3['Name'] = 'sp1_temp2gv2_tout'
    stream3['Layer'] = 'sp1_temp2gv2'
    stream3['Stream_coeff_v1_2'] = 0
    stream3['Stream_coeff_v1_1'] = 1
    stream3['Stream_coeff_v2_2'] = 0
    stream3['Stream_coeff_v2_1'] = 0
    stream3['Stream_coeff_v1_v2'] = 0
    stream3['Stream_coeff_cst'] = 0
    stream3['InOut'] = 'out'
    
    streaminput = [stream3['Parent'], stream3['Type'], stream3['Name'], stream3['Layer'], stream3['Stream_coeff_v1_2'], stream3['Stream_coeff_v1_1'], stream3['Stream_coeff_v2_2'],
                   stream3['Stream_coeff_v2_1'], stream3['Stream_coeff_v1_v2'], stream3['Stream_coeff_cst'], stream3['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)  
    
    ##Stream 4
    stream4 = {}                                                                ##Copied output to hsb substation 
    stream4['Parent'] = 'sp1_temp'
    stream4['Type'] = 'balancing_only'
    stream4['Name'] = 'sp1_temp2hsb_tout'
    stream4['Layer'] = 'sp1_temp2hsb'
    stream4['Stream_coeff_v1_2'] = 0
    stream4['Stream_coeff_v1_1'] = 1
    stream4['Stream_coeff_v2_2'] = 0
    stream4['Stream_coeff_v2_1'] = 0
    stream4['Stream_coeff_v1_v2'] = 0
    stream4['Stream_coeff_cst'] = 0
    stream4['InOut'] = 'out'
    
    streaminput = [stream4['Parent'], stream4['Type'], stream4['Name'], stream4['Layer'], stream4['Stream_coeff_v1_2'], stream4['Stream_coeff_v1_1'], stream4['Stream_coeff_v2_2'],
                   stream4['Stream_coeff_v2_1'], stream4['Stream_coeff_v1_v2'], stream4['Stream_coeff_cst'], stream4['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)  
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms
