## This is the common pipe model, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype_cp_network_nwk_choice_4 (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type 
    
def cp_network_nwk_choice_4 (cp_nwk_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    import numpy as np 
    
    ##Model description: 
    ##This the the common pipe model. It serves as a short circuit for chilled water from the evaporator
    
    ##Legend of input variables 
    
    ##cp_nwk_totalnwkflow       - The total flowrate in the entire parallel configuration (m3/h)
    
    ##Processing list of master decision variables as parameters
    totalnwkflow = cp_nwk_mdv['Value'][0]

    ##Defining dictionary of values 
    
    cp_network = {}
    ##Input constants
    
    ##1
    cp_nwk_totalnwkflow = {}
    cp_nwk_totalnwkflow['value'] = totalnwkflow
    cp_nwk_totalnwkflow['units'] = 'K'
    cp_nwk_totalnwkflow['status'] = 'cst_input'
    cp_network['cp_nwk_totalnwkflow'] = cp_nwk_totalnwkflow 

    ##Unit definition 

    ##Unit 1
    cp_nwk = {}
    cp_nwk['Name'] = 'cp_nwk'
    cp_nwk['Variable1'] = 'm_perc'                                                                                                    
    cp_nwk['Variable2'] = 'tinout'                                                                                                     
    cp_nwk['Fmin_v1'] = 0 
    cp_nwk['Fmax_v1'] = 1                                                                                                            
    cp_nwk['Fmin_v2'] = 0                                                                                                          
    cp_nwk['Fmax_v2'] = 1                                                                                  
    cp_nwk['Coeff_v1_2'] = 0                                                    ##No related constraints for the 2 variables                                                                                      
    cp_nwk['Coeff_v1_1'] = 0          
    cp_nwk['Coeff_v2_2'] = 0
    cp_nwk['Coeff_v2_1'] = 0
    cp_nwk['Coeff_v1_v2'] = 0 
    cp_nwk['Coeff_cst'] = 0
    cp_nwk['Fmin'] = 0
    cp_nwk['Fmax'] = 0
    cp_nwk['Cost_v1_2'] = 0
    cp_nwk['Cost_v1_1'] = 0
    cp_nwk['Cost_v2_2'] = 0
    cp_nwk['Cost_v2_1'] = 0
    cp_nwk['Cost_v1_v2'] = 0
    cp_nwk['Cost_cst'] = 0
    cp_nwk['Cinv_v1_2'] = 0
    cp_nwk['Cinv_v1_1'] = 0
    cp_nwk['Cinv_v2_2'] = 0
    cp_nwk['Cinv_v2_1'] = 0
    cp_nwk['Cinv_v1_v2'] = 0
    cp_nwk['Cinv_cst'] = 0
    cp_nwk['Power_v1_2'] = 0
    cp_nwk['Power_v1_1'] = 0
    cp_nwk['Power_v2_2'] = 0
    cp_nwk['Power_v2_1'] = 0
    cp_nwk['Power_v1_v2'] = 0
    cp_nwk['Power_cst'] = 0
    cp_nwk['Impact_v1_2'] = 0
    cp_nwk['Impact_v1_1'] = 0
    cp_nwk['Impact_v2_2'] = 0
    cp_nwk['Impact_v2_1'] = 0
    cp_nwk['Impact_v1_v2'] = 0
    cp_nwk['Impact_cst'] = 0

    unitinput = [cp_nwk['Name'], cp_nwk['Variable1'], cp_nwk['Variable2'], cp_nwk['Fmin_v1'], cp_nwk['Fmax_v1'], cp_nwk['Fmin_v2'], cp_nwk['Fmax_v2'], cp_nwk['Coeff_v1_2'], 
                cp_nwk['Coeff_v1_1'], cp_nwk['Coeff_v2_2'], cp_nwk['Coeff_v2_1'], cp_nwk['Coeff_v1_v2'], cp_nwk['Coeff_cst'], cp_nwk['Fmin'], cp_nwk['Fmax'], cp_nwk['Cost_v1_2'], 
                cp_nwk['Cost_v1_1'], cp_nwk['Cost_v2_2'], cp_nwk['Cost_v2_1'], cp_nwk['Cost_v1_v2'], cp_nwk['Cost_cst'], cp_nwk['Cinv_v1_2'], cp_nwk['Cinv_v1_1'], cp_nwk['Cinv_v2_2'], 
                cp_nwk['Cinv_v2_1'], cp_nwk['Cinv_v1_v2'], cp_nwk['Cinv_cst'], cp_nwk['Power_v1_2'], cp_nwk['Power_v1_1'], cp_nwk['Power_v2_2'], cp_nwk['Power_v2_1'], 
                cp_nwk['Power_v1_v2'], cp_nwk['Power_cst'], cp_nwk['Impact_v1_2'], cp_nwk['Impact_v1_1'], cp_nwk['Impact_v2_2'], cp_nwk['Impact_v2_1'], cp_nwk['Impact_v1_v2'], 
                cp_nwk['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)

    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}                                                                ##Temperature of fluid entering the unit 
    stream1['Parent'] = 'cp_nwk'
    stream1['Type'] = 'temp_chil'
    stream1['Name'] = 'cp_nwk_tin'
    stream1['Layer'] = 'sp1_temp2cp'
    stream1['Stream_coeff_v1_2'] = 0
    stream1['Stream_coeff_v1_1'] = 0
    stream1['Stream_coeff_v2_2'] = 0
    stream1['Stream_coeff_v2_1'] = 30
    stream1['Stream_coeff_v1_v2'] = 0
    stream1['Stream_coeff_cst'] = 273.15
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Parent'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Stream_coeff_v1_2'], stream1['Stream_coeff_v1_1'], stream1['Stream_coeff_v2_2'],
                   stream1['Stream_coeff_v2_1'], stream1['Stream_coeff_v1_v2'], stream1['Stream_coeff_cst'], stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 2
    stream2 = {}                                                                ##Temperature of fluid exiting the unit 
    stream2['Parent'] = 'cp_nwk'
    stream2['Type'] = 'temp_chil'
    stream2['Name'] = 'cp_nwk_tout'
    stream2['Layer'] = 'ss2sp2_temp'
    stream2['Stream_coeff_v1_2'] = 0
    stream2['Stream_coeff_v1_1'] = 273.15
    stream2['Stream_coeff_v2_2'] = 0
    stream2['Stream_coeff_v2_1'] = 0
    stream2['Stream_coeff_v1_v2'] = 30
    stream2['Stream_coeff_cst'] = 0
    stream2['InOut'] = 'out'
    
    streaminput = [stream2['Parent'], stream2['Type'], stream2['Name'], stream2['Layer'], stream2['Stream_coeff_v1_2'], stream2['Stream_coeff_v1_1'], stream2['Stream_coeff_v2_2'],
                   stream2['Stream_coeff_v2_1'], stream2['Stream_coeff_v1_v2'], stream2['Stream_coeff_cst'], stream2['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 3
    stream3 = {}                                                                ##Flowrate of water into the common pipe, it is unnecessary to have an outlet for this 
    stream3['Parent'] = 'cp_nwk'
    stream3['Type'] = 'flow'
    stream3['Name'] = 'cp_nwk_mf_in'
    stream3['Layer'] = 'chil2distnwk_flow'
    stream3['Stream_coeff_v1_2'] = 0
    stream3['Stream_coeff_v1_1'] = cp_network['cp_nwk_totalnwkflow']['value']
    stream3['Stream_coeff_v2_2'] = 0
    stream3['Stream_coeff_v2_1'] = 0
    stream3['Stream_coeff_v1_v2'] = 0
    stream3['Stream_coeff_cst'] = 0
    stream3['InOut'] = 'in'
    
    streaminput = [stream3['Parent'], stream3['Type'], stream3['Name'], stream3['Layer'], stream3['Stream_coeff_v1_2'], stream3['Stream_coeff_v1_1'], stream3['Stream_coeff_v2_2'],
                   stream3['Stream_coeff_v2_1'], stream3['Stream_coeff_v1_v2'], stream3['Stream_coeff_cst'], stream3['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 4
    stream = {}                                                                
    stream['Parent'] = 'cp_nwk'                                                ##Temperture stream exiting the substation 
    stream['Type'] = 'balancing_only'
    stream['Name'] = 'cp_mf_out'
    stream['Layer'] = 'distnwk_flow_consol'
    stream['Stream_coeff_v1_2'] = 0
    stream['Stream_coeff_v1_1'] = cp_network['cp_nwk_totalnwkflow']['value'] 
    stream['Stream_coeff_v2_2'] = 0
    stream['Stream_coeff_v2_1'] = 0
    stream['Stream_coeff_v1_v2'] = 0
    stream['Stream_coeff_cst'] = 0
    stream['InOut'] = 'out'
    
    streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
                   stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True) 
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms
    
    
    