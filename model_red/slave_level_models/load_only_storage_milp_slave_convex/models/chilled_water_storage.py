## This is the simple thermal storage model, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype_chilled_water_storage (unit_type):                  ##Input the unit type here
    unit_type = 'storage'
    return unit_type
    
def chilled_water_storage (cws_mdv, storagelist, streams, cons_eqns, cons_eqns_terms, thermal_loss):
    import pandas as pd
    import numpy as np
    
    ##Model description: 
    ##This storage model assumes a 5% cold loss per hour
    ##It is just a simple storage model without any consideration for temperature variation etc.
    ##The main consideration is the quantity of energy stored and extracted at every time step
    
    
    ##cws_mdv --- the master decision variables which are used as parameters at this stage 
    ##storagelist --- a dataframe to hold essential values for writing the MILP script 
    ##streams --- a dataframe to write connections to other units 
    ##cons_eqns --- additional constraints are explicitly stated here 
    ##cons_eqns_terms --- the terms to the constraints 
    
    ##thermal_loss --- this is an additional dataframe for collecting loss information from thermal storages

    
    ##Defining inputs
    
    ##Processing list of master decision variables as parameters
    
    ##Defined constants 
    cws_max_capacity = 20000

    
    ##Calling a compute file to process dependent values
        ##Placing the values in a numpy array for easy data handling 

    
#################################################################################################################################################################################################        
    
    ##Unit definition 
    
    ##Unit 1
    ct1 = {}
    ct1['Name'] = 'cws'
    ct1['Variable1'] = 'q_stored_extracted'                                                                                                           
    ct1['Variable2'] = '-'                                                                                                          
    ct1['Fmin_v1'] = 0 
    ct1['Fmax_v1'] = cws_max_capacity                                                                           
    ct1['Fmin_v2'] = 0                                                                                             
    ct1['Fmax_v2'] = 0                                                                       
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
    ct1['Power_v1_1'] = 0
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
    storagelist = storagelist.append(unitdf, ignore_index=True)
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}                                                                ##For storage models, just state direction as 'in'. It will be modified anyway.                                        
    stream1['Parent'] = 'cws'
    stream1['Type'] = 'flow'
    stream1['Name'] = 'cws_q_stored'
    stream1['Layer'] = 'chillers_to_substations_storage_q_out'                  
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

    ##Thermal loss definition 
        ##For now it is the hourly thermal loss. The fraction of energy available in the next time-step
        ##The values will be multiplied as a constant onto the variables
    tl = {}
    tl['Name'] = 'cws'
    tl['Variable1'] = 'q_stored_extracted'    
    tl['Variable2'] = '-'  
    tl['Coeff_v1_2'] = 1                                                        ##A coefficient of 1 means no change                                                                                                             
    tl['Coeff_v1_1'] = 0.8   
    tl['Coeff_v2_2'] = 1
    tl['Coeff_v2_1'] = 1
    tl['Coeff_v1_v2'] = 1
    tl['Coeff_cst'] = 1
    
    tl_input = [tl['Name'], tl['Variable1'], tl['Variable2'], tl['Coeff_v1_2'], tl['Coeff_v1_1'], tl['Coeff_v2_2'], tl['Coeff_v2_1'], tl['Coeff_v1_v2'], tl['Coeff_cst']]
    tl_df = pd.DataFrame(data = [tl_input], columns = ['Name', 'Variable1', 'Variable2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2', 'Coeff_cst'])
    
    thermal_loss = thermal_loss.append(tl_df, ignore_index = True)
    
    return storagelist, streams, cons_eqns, cons_eqns_terms, thermal_loss

