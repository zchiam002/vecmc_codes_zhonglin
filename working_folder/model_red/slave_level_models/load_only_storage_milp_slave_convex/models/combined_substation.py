## This is the combined substation model, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype_combined_substation (unit_type):                  ##Input the unit type here
    unit_type = 'process'
    return unit_type 
    
def combined_substation (cb_ss_mdv, processlist, streams, cons_eqns, cons_eqns_terms):
    from combined_substation_compute import combined_substation_compute
    import pandas as pd
    import numpy as np 
    
    ##Model description 
    ##This is the combined substation model, it is a process for which the demand must be fulfilled.
    
    ##Defining inputs 

    ##Processing list of master decision variables/inputs as parameters
    cb_ss_gv2_demand = cb_ss_mdv['Value'][0]
    cb_ss_hsb_demand = cb_ss_mdv['Value'][1]
    cb_ss_pfa_demand = cb_ss_mdv['Value'][2]
    cb_ss_ser_demand = cb_ss_mdv['Value'][3]

    ##Defined constants 
    cb_ss_all_ss = 5                                            ##Temperature difference for the network and all of the substations 
    cb_ss_cp = 4.2                                              ##Specific heat capacity for water
    cb_ss_ice_coeff = 0.0000104227119644958
    cb_ss_tro_coeff = 0.00043901081005616
    cb_ss_gv2_coeff = 0.0000735647190189052
    cb_ss_hsb_coeff = 0.0075648885553576
    cb_ss_pfa_coeff = 0.00021850538714815
    cb_ss_ser_coeff = 0.000536956604603528

    ##Dependent constants 
    cb_ss_dc = np.zeros((12,1))                                 ##Initialize the list, note the number of constants 
    
    cb_ss_dc[0,0] = cb_ss_gv2_demand
    cb_ss_dc[1,0] = cb_ss_hsb_demand
    cb_ss_dc[2,0] = cb_ss_pfa_demand
    cb_ss_dc[3,0] = cb_ss_ser_demand
    cb_ss_dc[4,0] = cb_ss_all_ss
    cb_ss_dc[5,0] = cb_ss_cp  
    cb_ss_dc[6,0] = cb_ss_ice_coeff 
    cb_ss_dc[7,0] = cb_ss_tro_coeff
    cb_ss_dc[8,0] = cb_ss_gv2_coeff
    cb_ss_dc[9,0] = cb_ss_hsb_coeff 
    cb_ss_dc[10,0] = cb_ss_pfa_coeff 
    cb_ss_dc[11,0] = cb_ss_ser_coeff     

    cb_ss_calc = combined_substation_compute(cb_ss_dc)
    
    cb_ss_flow_dist_nwk = cb_ss_calc[0,0]                       ##Total flowrate in the distribution network  
    cb_ss_delp_dist_nwk = cb_ss_calc[1,0]                       ##Pressure drop in the distribution network 
    cb_ss_total_demand = cb_ss_calc[2,0]                        ##Total demand 

############################################################################################################################################################################################################
    
    ##Unit definition
    
    ##Unit 1
    ud = {}
    ud['Name'] = 'cb_ss'
    ud['Variable1'] = 'demand'                                                                                                                                             
    ud['Variable2'] = '-'                                                                                                    
    ud['Fmin_v1'] = 0                                           ##The total cooling demand by the substations
    ud['Fmax_v1'] = cb_ss_total_demand                                                                                                                   
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

############################################################################################################################################################################################################

    ##Layer and stream definition 

    ##Stream 1
    stream = {}                                                                
    stream['Parent'] = 'cb_ss'                                                  ##Cooling flow into the substation
    stream['Type'] = 'flow'
    stream['Name'] = 'cb_ss_q_in'
    stream['Layer'] = 'chillers_to_substations_storage_q_out'
    stream['Stream_coeff_v1_2'] = 0
    stream['Stream_coeff_v1_1'] = 1
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
    
    ##Stream 2
    stream = {}                                                                
    stream['Parent'] = 'cb_ss'                                                  ##Flowrate stream exiting the substation 
    stream['Type'] = 'flow'                                                     ##It is implicitly calculated and treated as a constant 
    stream['Name'] = 'cb_ss_m_flow_out'
    stream['Layer'] = 'combined_ss_to_dist_nwk_flow'
    stream['Stream_coeff_v1_2'] = 0
    stream['Stream_coeff_v1_1'] = 0
    stream['Stream_coeff_v2_2'] = 0
    stream['Stream_coeff_v2_1'] = 0
    stream['Stream_coeff_v1_v2'] = 0
    stream['Stream_coeff_cst'] = cb_ss_flow_dist_nwk
    stream['InOut'] = 'out'
    
    streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
                   stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True) 
    
    ##Stream 3
    stream = {}                                                                
    stream['Parent'] = 'cb_ss'                                                  ##Pressure stream exiting the substation 
    stream['Type'] = 'pressure'                                                 ##It is implicitly calculated and treated as a constant
    stream['Name'] = 'cb_ss_pressure_out'
    stream['Layer'] = 'combined_ss_to_dist_nwk_pressure'
    stream['Stream_coeff_v1_2'] = 0
    stream['Stream_coeff_v1_1'] = 0
    stream['Stream_coeff_v2_2'] = 0
    stream['Stream_coeff_v2_1'] = 0
    stream['Stream_coeff_v1_v2'] = 0
    stream['Stream_coeff_cst'] = cb_ss_delp_dist_nwk
    stream['InOut'] = 'out'
    
    streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
                   stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True) 

############################################################################################################################################################################################################
    
    return processlist, streams, cons_eqns, cons_eqns_terms    