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

def splitter3_temp (sp3_temp_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    
    #Model description 
    ##This model copies the inlet stream and duplicates it to the required number of outlet streams 
    
    ##Unit definition
    
    ##Unit 1

    sp3_temp = {}
    sp3_temp['Name'] = 'sp3_temp'
    sp3_temp['Variable1'] = 't_inout'                                                                                                     
    sp3_temp['Variable2'] = '-'                                                                                                       
    sp3_temp['Fmin_v1'] = 0 
    sp3_temp['Fmax_v1'] = 1000                                                                                                                  
    sp3_temp['Fmin_v2'] = 0                                                                                                        
    sp3_temp['Fmax_v2'] = 0                                                                                  
    sp3_temp['Coeff_v1_2'] = 0                                                                                                                 
    sp3_temp['Coeff_v1_1'] = 1         
    sp3_temp['Coeff_v2_2'] = 0
    sp3_temp['Coeff_v2_1'] = 0
    sp3_temp['Coeff_v1_v2'] = 0 
    sp3_temp['Coeff_cst'] = 0
    sp3_temp['Fmin'] = 0
    sp3_temp['Fmax'] = 1000
    sp3_temp['Cost_v1_2'] = 0
    sp3_temp['Cost_v1_1'] = 0
    sp3_temp['Cost_v2_2'] = 0
    sp3_temp['Cost_v2_1'] = 0
    sp3_temp['Cost_v1_v2'] = 0
    sp3_temp['Cost_cst'] = 0
    sp3_temp['Cinv_v1_2'] = 0
    sp3_temp['Cinv_v1_1'] = 0
    sp3_temp['Cinv_v2_2'] = 0
    sp3_temp['Cinv_v2_1'] = 0
    sp3_temp['Cinv_v1_v2'] = 0
    sp3_temp['Cinv_cst'] = 0
    sp3_temp['Power_v1_2'] = 0
    sp3_temp['Power_v1_1'] = 0
    sp3_temp['Power_v2_2'] = 0
    sp3_temp['Power_v2_1'] = 0
    sp3_temp['Power_v1_v2'] = 0
    sp3_temp['Power_cst'] = 0
    sp3_temp['Impact_v1_2'] = 0
    sp3_temp['Impact_v1_1'] = 0
    sp3_temp['Impact_v2_2'] = 0
    sp3_temp['Impact_v2_1'] = 0
    sp3_temp['Impact_v1_v2'] = 0
    sp3_temp['Impact_cst'] = 0

    unitinput = [sp3_temp['Name'], sp3_temp['Variable1'], sp3_temp['Variable2'], sp3_temp['Fmin_v1'], sp3_temp['Fmax_v1'], sp3_temp['Fmin_v2'], sp3_temp['Fmax_v2'], sp3_temp['Coeff_v1_2'], 
                sp3_temp['Coeff_v1_1'], sp3_temp['Coeff_v2_2'], sp3_temp['Coeff_v2_1'], sp3_temp['Coeff_v1_v2'], sp3_temp['Coeff_cst'], sp3_temp['Fmin'], sp3_temp['Fmax'], sp3_temp['Cost_v1_2'], 
                sp3_temp['Cost_v1_1'], sp3_temp['Cost_v2_2'], sp3_temp['Cost_v2_1'], sp3_temp['Cost_v1_v2'], sp3_temp['Cost_cst'], sp3_temp['Cinv_v1_2'], sp3_temp['Cinv_v1_1'], sp3_temp['Cinv_v2_2'], 
                sp3_temp['Cinv_v2_1'], sp3_temp['Cinv_v1_v2'], sp3_temp['Cinv_cst'], sp3_temp['Power_v1_2'], sp3_temp['Power_v1_1'], sp3_temp['Power_v2_2'], sp3_temp['Power_v2_1'], 
                sp3_temp['Power_v1_v2'], sp3_temp['Power_cst'], sp3_temp['Impact_v1_2'], sp3_temp['Impact_v1_1'], sp3_temp['Impact_v2_2'], sp3_temp['Impact_v2_1'], sp3_temp['Impact_v1_v2'], 
                sp3_temp['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}                                                                ##This is the input from the chillers condensers
    stream1['Parent'] = 'sp3_temp'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'chil2condret_temp'
    stream1['Layer'] = 'chil2sp3_temp'
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
    stream2['Parent'] = 'sp3_temp'                                              ##Copied output to cooling tower 1
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'sp3_temp2ct1_tout'
    stream2['Layer'] = 'sp3_2_ct1_temp'
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
    stream3 = {} 
    stream3['Parent'] = 'sp3_temp'                                              ##Copied output to cooling tower 2
    stream3['Type'] = 'balancing_only'
    stream3['Name'] = 'sp3_temp2ct2_tout'
    stream3['Layer'] = 'sp3_2_ct2_temp'
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
    stream4 = {} 
    stream4['Parent'] = 'sp3_temp'                                              ##Copied output to cooling tower 3
    stream4['Type'] = 'balancing_only'
    stream4['Name'] = 'sp3_temp2ct3_tout'
    stream4['Layer'] = 'sp3_2_ct3_temp'
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
    
    ##Stream 5
    stream5 = {} 
    stream5['Parent'] = 'sp3_temp'                                              ##Copied output to cooling tower 4
    stream5['Type'] = 'balancing_only'
    stream5['Name'] = 'sp3_temp2ct4_tout'
    stream5['Layer'] = 'sp3_2_ct4_temp'
    stream5['Stream_coeff_v1_2'] = 0
    stream5['Stream_coeff_v1_1'] = 1
    stream5['Stream_coeff_v2_2'] = 0
    stream5['Stream_coeff_v2_1'] = 0
    stream5['Stream_coeff_v1_v2'] = 0
    stream5['Stream_coeff_cst'] = 0
    stream5['InOut'] = 'out'
    
    streaminput = [stream5['Parent'], stream5['Type'], stream5['Name'], stream5['Layer'], stream5['Stream_coeff_v1_2'], stream5['Stream_coeff_v1_1'], stream5['Stream_coeff_v2_2'],
                   stream5['Stream_coeff_v2_1'], stream5['Stream_coeff_v1_v2'], stream5['Stream_coeff_cst'], stream5['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)  
    
    ##Stream 6
    stream6 = {} 
    stream6['Parent'] = 'sp3_temp'                                              ##Copied output to cooling tower 5
    stream6['Type'] = 'balancing_only'
    stream6['Name'] = 'sp3_temp2ct5_tout'
    stream6['Layer'] = 'sp3_2_ct5_temp'
    stream6['Stream_coeff_v1_2'] = 0
    stream6['Stream_coeff_v1_1'] = 1
    stream6['Stream_coeff_v2_2'] = 0
    stream6['Stream_coeff_v2_1'] = 0
    stream6['Stream_coeff_v1_v2'] = 0
    stream6['Stream_coeff_cst'] = 0
    stream6['InOut'] = 'out'
    
    streaminput = [stream6['Parent'], stream6['Type'], stream6['Name'], stream6['Layer'], stream6['Stream_coeff_v1_2'], stream6['Stream_coeff_v1_1'], stream6['Stream_coeff_v2_2'],
                   stream6['Stream_coeff_v2_1'], stream6['Stream_coeff_v1_v2'], stream6['Stream_coeff_cst'], stream6['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)  
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms