##This is the temperature aggregator and stream splitter model 

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    
def checktype_splitter1_temp (unit_type):                  ##Input the unit type here

    ##unit_type     --- a variable to store the type of unit    

    unit_type = 'utility'

    return unit_type

#Model description 
    ##This model copies the inlet stream and duplicates it to the required number of outlet streams 
def splitter1_temp (mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    
    import pandas as pd

#################################################################################################################################################################################################    
    ##Unit definition
    
    ##Unit 1

    sp1_temp = {}
    sp1_temp['Name'] = 'sp1_temp'
    sp1_temp['Variable1'] = 't_inout'                                                                                                     
    sp1_temp['Variable2'] = '-'                                                                                                       
    sp1_temp['Fmin_v1'] = 0 
    sp1_temp['Fmax_v1'] = 1                                                                                                                
    sp1_temp['Fmin_v2'] = 0                                                                                                        
    sp1_temp['Fmax_v2'] = 0                                                                                  
    sp1_temp['Coeff_v1_2'] = 0                                                                                                                 
    sp1_temp['Coeff_v1_1'] = 0        
    sp1_temp['Coeff_v2_2'] = 0
    sp1_temp['Coeff_v2_1'] = 0
    sp1_temp['Coeff_v1_v2'] = 0 
    sp1_temp['Coeff_cst'] = 0
    sp1_temp['Fmin'] = 0
    sp1_temp['Fmax'] = 0
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

#################################################################################################################################################################################################    
    ##Layer and stream definition 
    
    ##Stream 1
    stream = {}                                                                          ##This is the input from the chillers. 
    stream['Parent'] = 'sp1_temp'
    stream['Type'] = 'temp_chil'
    stream['Name'] = 'chil2sp1_temp_tin'
    stream['Layer'] = 'chil2sp1_temp'
    stream['Stream_coeff_v1_2'] = 0
    stream['Stream_coeff_v1_1'] = 30
    stream['Stream_coeff_v2_2'] = 0
    stream['Stream_coeff_v2_1'] = 0
    stream['Stream_coeff_v1_v2'] = 0
    stream['Stream_coeff_cst'] = 273.15
    stream['InOut'] = 'in'
    
    streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
                   stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)

    ##Stream 2
    stream = {} 
    stream['Parent'] = 'sp1_temp'                                                       ##Copied output to the common pipe
    stream['Type'] = 'temp_chil'
    stream['Name'] = 'sp1_temp_2cp_nwk_tout'
    stream['Layer'] = 'sp12cp_temp'
    stream['Stream_coeff_v1_2'] = 0
    stream['Stream_coeff_v1_1'] = 30
    stream['Stream_coeff_v2_2'] = 0
    stream['Stream_coeff_v2_1'] = 0
    stream['Stream_coeff_v1_v2'] = 0
    stream['Stream_coeff_cst'] = 273.15
    stream['InOut'] = 'out'
    
    streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
                   stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)  
    
    ##Stream 3
    stream = {}                                                                         ##Copied output to gv2 substation 
    stream['Parent'] = 'sp1_temp'
    stream['Type'] = 'temp_chil'
    stream['Name'] = 'sp1_temp_2gv2_ss_tout'
    stream['Layer'] = 'sp12gv2_temp'
    stream['Stream_coeff_v1_2'] = 0
    stream['Stream_coeff_v1_1'] = 30
    stream['Stream_coeff_v2_2'] = 0
    stream['Stream_coeff_v2_1'] = 0
    stream['Stream_coeff_v1_v2'] = 0
    stream['Stream_coeff_cst'] = 273.15
    stream['InOut'] = 'out'
    
    streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
                   stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)  

    ##Stream 4
    stream = {}                                                                         ##Copied output to hsb substation 
    stream['Parent'] = 'sp1_temp'
    stream['Type'] = 'temp_chil'
    stream['Name'] = 'sp1_temp_2hsb_ss_tout'
    stream['Layer'] = 'sp12hsb_temp'
    stream['Stream_coeff_v1_2'] = 0
    stream['Stream_coeff_v1_1'] = 30
    stream['Stream_coeff_v2_2'] = 0
    stream['Stream_coeff_v2_1'] = 0
    stream['Stream_coeff_v1_v2'] = 0
    stream['Stream_coeff_cst'] = 273.15
    stream['InOut'] = 'out'
    
    streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
                   stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)     
            
    return utilitylist, streams, cons_eqns, cons_eqns_terms
