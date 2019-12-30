## This is the cooling tower model, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype_cooling_towers (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type
    
def cooling_towers (cts_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    import numpy as np
    
    ##Model description: 
    ##This model assumes a linear relationship between the heat rejected and the fan electricity consumption.
    ##There is no consideration of wet-bulb temperature in this model 
    
    
    ##cts_mdv --- the master decision variables which are used as parameters at this stage 
    ##utilitylist --- a dataframe to hold essential values for writing the MILP script 
    ##streams --- a dataframe to write connections to other units 
    ##cons_eqns --- additional constraints are explicitly stated here 
    ##cons_eqns_terms --- the terms to the constraints 
    
    ##Defining inputs
    
    ##Processing list of master decision variables as parameters
    cts_time_dependent_elect_tariff = cts_mdv['Value'][0]   ##Time dependent electricity tariff per kWh used. 
    
    ##Defined constants 
    cts_num_towers_config = 5
    cts_elect_max = 22
    cts_max_cooling_per_tower = 5667.908

    
    ##Calling a compute file to process dependent values
        ##Placing the values in a numpy array for easy data handling 

    
#################################################################################################################################################################################################        
    
    ##Unit definition 
    
    ##Unit 1
    ct1 = {}
    ct1['Name'] = 'cts'
    ct1['Variable1'] = 'q_rej'                                                                                                           
    ct1['Variable2'] = '-'                                                                                                          
    ct1['Fmin_v1'] = 0 
    ct1['Fmax_v1'] = cts_max_cooling_per_tower * cts_num_towers_config                                                                           
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
    ct1['Cost_v1_1'] = cts_time_dependent_elect_tariff * (cts_elect_max / cts_max_cooling_per_tower)
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
    ct1['Power_v1_1'] = cts_elect_max / cts_max_cooling_per_tower
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
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}                                                                ##The inlet flowrate of heat to be rejected to the environment                                        
    stream1['Parent'] = 'cts'
    stream1['Type'] = 'flow'
    stream1['Name'] = 'cts_q_rej_in'
    stream1['Layer'] = 'chiller_heat_rej'
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
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms
    
    
