## This is the ser substation model, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type 
    
def ser_substation (ser_ss_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    from ser_substation_compute import ser_substation_compute
    import pandas as pd
    import numpy as np 
    
    ##Model description 
    ##This is the ser substation model, it treats the demand as a parameter and outputs a tout
    
    ##Legend of input variables 
    
    ##serss_demand          --- the cooling load at the substation (kWh)
    ##serss_totalflownwk    --- the total flowrate through parallel systems to this substation (m3/h) 
    
    ##Processing list of master decision variables/inputs as parameters 
    serss_demand = ser_ss_mdv['Value'][0]
    serss_totalflownwk = ser_ss_mdv['Value'][1]

    ##Define dictionary of values   
    
    ser_substation = {}

    ##Input constants
    
    ##1
    ser_ss_demand = {}
    ser_ss_demand['value'] = serss_demand
    ser_ss_demand['units'] = 'kWh'
    ser_ss_demand['status'] = 'cst_input'
    ser_substation['ser_ss_demand'] = ser_ss_demand

    ##2
    ser_ss_totalflownwk = {}
    ser_ss_totalflownwk['value'] = serss_totalflownwk
    ser_ss_totalflownwk['units'] = 'm3/h'
    ser_ss_totalflownwk['status'] = 'cst_input'
    ser_substation['ser_ss_totalflownwk'] = ser_ss_totalflownwk

    ##Defined constants
    
    ##3
    ser_ss_tinmax = {}
    ser_ss_tinmax['value'] = 273.15 + 5                         ##The maximum temperature of water entering the substation 
    ser_ss_tinmax['units'] = 'K'
    ser_ss_tinmax['status'] = 'cst'
    ser_substation['ser_ss_tinmax'] = ser_ss_tinmax 

    ##4
    ser_ss_deltmax = {}
    ser_ss_deltmax['value'] = 10                                ##The maximum delta t of the substation on the cold side  
    ser_ss_deltmax['units'] = 'K'
    ser_ss_deltmax['status'] = 'cst'
    ser_substation['ser_ss_deltmax'] = ser_ss_deltmax    

    ##5
    ser_ss_cp = {}
    ser_ss_cp['value'] = 4.2                                    ##The heat capacity of water 
    ser_ss_cp['units'] = 'kJ/kgK'
    ser_ss_cp['status'] = 'cst'
    ser_substation['ser_ss_cp'] = ser_ss_cp 

    ##Dependent constants 
    ser_ss_dc = np.zeros((3,1))                                 ##Initialize the list, note the number of constants 
    
    ser_ss_dc[0,0] = ser_substation['ser_ss_demand']['value']
    ser_ss_dc[1,0] = ser_substation['ser_ss_totalflownwk']['value']
    ser_ss_dc[2,0] = ser_substation['ser_ss_cp']['value']

    ser_ss_calc = ser_substation_compute(ser_ss_dc)
    
    ##6
    ser_ss_temp_exit_cst = {}
    ser_ss_temp_exit_cst['value'] = ser_ss_calc[0,0]            ##The constant term for the exit temperature stream 
    ser_ss_temp_exit_cst['units'] = '-'
    ser_ss_temp_exit_cst['status'] = 'calc'
    ser_substation['ser_ss_temp_exit_cst'] = ser_ss_temp_exit_cst     
    
    ##Unit definition
    
    ##Unit 1
    ser_ss = {}
    ser_ss['Name'] = 'ser_ss'
    ser_ss['Variable1'] = 'm_serss_perc'                                        ##The percentage of the total flowrate into the system                                                                                                     
    ser_ss['Variable2'] = 'tserss_in'                                           ##Temperature of fluid entering the substation                                                              
    ser_ss['Fmin_v1'] = 0 
    ser_ss['Fmax_v1'] = 1                                                                                                                    
    ser_ss['Fmin_v2'] = 273.15 + 1                                                                                                           
    ser_ss['Fmax_v2'] = ser_substation['ser_ss_tinmax']['value']                                                                                    
    ser_ss['Coeff_v1_2'] = 0                                                                                                                 
    ser_ss['Coeff_v1_1'] = 0         
    ser_ss['Coeff_v2_2'] = 0
    ser_ss['Coeff_v2_1'] = 0
    ser_ss['Coeff_v1_v2'] = 0
    ser_ss['Coeff_cst'] = 0
    ser_ss['Fmin'] = 0
    ser_ss['Fmax'] = 0
    ser_ss['Cost_v1_2'] = 0
    ser_ss['Cost_v1_1'] = 0
    ser_ss['Cost_v2_2'] = 0
    ser_ss['Cost_v2_1'] = 0
    ser_ss['Cost_v1_v2'] = 0
    ser_ss['Cost_cst'] = 0
    ser_ss['Cinv_v1_2'] = 0
    ser_ss['Cinv_v1_1'] = 0
    ser_ss['Cinv_v2_2'] = 0
    ser_ss['Cinv_v2_1'] = 0
    ser_ss['Cinv_v1_v2'] = 0
    ser_ss['Cinv_cst'] = 0
    ser_ss['Power_v1_2'] = 0
    ser_ss['Power_v1_1'] = 0
    ser_ss['Power_v2_2'] = 0
    ser_ss['Power_v2_1'] = 0
    ser_ss['Power_v1_v2'] = 0
    ser_ss['Power_cst'] = 0
    ser_ss['Impact_v1_2'] = 0
    ser_ss['Impact_v1_1'] = 0
    ser_ss['Impact_v2_2'] = 0
    ser_ss['Impact_v2_1'] = 0
    ser_ss['Impact_v1_v2'] = 0
    ser_ss['Impact_cst'] = 0

    unitinput = [ser_ss['Name'], ser_ss['Variable1'], ser_ss['Variable2'], ser_ss['Fmin_v1'], ser_ss['Fmax_v1'], ser_ss['Fmin_v2'], ser_ss['Fmax_v2'], ser_ss['Coeff_v1_2'], 
                ser_ss['Coeff_v1_1'], ser_ss['Coeff_v2_2'], ser_ss['Coeff_v2_1'], ser_ss['Coeff_v1_v2'], ser_ss['Coeff_cst'], ser_ss['Fmin'], ser_ss['Fmax'], ser_ss['Cost_v1_2'], 
                ser_ss['Cost_v1_1'], ser_ss['Cost_v2_2'], ser_ss['Cost_v2_1'], ser_ss['Cost_v1_v2'], ser_ss['Cost_cst'], ser_ss['Cinv_v1_2'], ser_ss['Cinv_v1_1'], ser_ss['Cinv_v2_2'], 
                ser_ss['Cinv_v2_1'], ser_ss['Cinv_v1_v2'], ser_ss['Cinv_cst'], ser_ss['Power_v1_2'], ser_ss['Power_v1_1'], ser_ss['Power_v2_2'], ser_ss['Power_v2_1'], 
                ser_ss['Power_v1_v2'], ser_ss['Power_cst'], ser_ss['Impact_v1_2'], ser_ss['Impact_v1_1'], ser_ss['Impact_v2_2'], ser_ss['Impact_v2_1'], ser_ss['Impact_v1_v2'], 
                ser_ss['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)

    ##Layer and stream definition 

    ##Stream 1
    stream1 = {}                                                                
    stream1['Parent'] = 'ser_ss'                                                ##Temperature stream entering the substation 
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'ser_ss_tin'
    stream1['Layer'] = 'sp1_temp2ser'
    stream1['Stream_coeff_v1_2'] = 0
    stream1['Stream_coeff_v1_1'] = 0
    stream1['Stream_coeff_v2_2'] = 0
    stream1['Stream_coeff_v2_1'] = 1
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
    stream2['Parent'] = 'ser_ss'                                                ##Flowrate stream entering the substation 
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'ser_ss_mfin'
    stream2['Layer'] = 'ser_nwk2ser_ss'
    stream2['Stream_coeff_v1_2'] = 0
    stream2['Stream_coeff_v1_1'] = ser_substation['ser_ss_totalflownwk']['value']
    stream2['Stream_coeff_v2_2'] = 0
    stream2['Stream_coeff_v2_1'] = 0
    stream2['Stream_coeff_v1_v2'] = 0
    stream2['Stream_coeff_cst'] = 0
    stream2['InOut'] = 'in'
    
    streaminput = [stream2['Parent'], stream2['Type'], stream2['Name'], stream2['Layer'], stream2['Stream_coeff_v1_2'], stream2['Stream_coeff_v1_1'], stream2['Stream_coeff_v2_2'],
                   stream2['Stream_coeff_v2_1'], stream2['Stream_coeff_v1_v2'], stream2['Stream_coeff_cst'], stream2['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True) 
    
    ##Stream 3
    stream3 = {}                                                                
    stream3['Parent'] = 'ser_ss'                                                ##Flowrate stream entering the substation 
    stream3['Type'] = 'balancing_only'
    stream3['Name'] = 'ser_ss_tout'
    stream3['Layer'] = 'ss2sp2_temp'
    stream3['Stream_coeff_v1_2'] = 0
    stream3['Stream_coeff_v1_1'] = 0
    stream3['Stream_coeff_v2_2'] = 0
    stream3['Stream_coeff_v2_1'] = 0
    stream3['Stream_coeff_v1_v2'] = 1
    stream3['Stream_coeff_cst'] = ser_substation['ser_ss_temp_exit_cst']['value']
    stream3['InOut'] = 'out'
    
    streaminput = [stream3['Parent'], stream3['Type'], stream3['Name'], stream3['Layer'], stream3['Stream_coeff_v1_2'], stream3['Stream_coeff_v1_1'], stream3['Stream_coeff_v2_2'],
                   stream3['Stream_coeff_v2_1'], stream3['Stream_coeff_v1_v2'], stream3['Stream_coeff_cst'], stream3['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True) 
    
    ##Stream 4
    stream4 = {}                                                                
    stream4['Parent'] = 'ser_ss'                                                ##Flowrate stream exiting the substation 
    stream4['Type'] = 'balancing_only'
    stream4['Name'] = 'ser_ss_mfout'
    stream4['Layer'] = 'ss_2_dist_pump_flow'
    stream4['Stream_coeff_v1_2'] = 0
    stream4['Stream_coeff_v1_1'] = ser_substation['ser_ss_totalflownwk']['value']
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
    
    ##Constraint definition
    
    ##Equation definitions
    
    ##Equation 1
    eqn1 = {}
    eqn1['Name'] = 'ser_ss_tout_max'
    eqn1['Type'] = 'stream_limit_modified'                                      ##Stream modified constraints involving more than 1 variable which cannot be expressed easily
    eqn1['Sign'] = 'greater_than_equal_to'                                      ##Due to reciprocal less than equals to becomes greater than equals to, as both are positive
    eqn1['RHS_value'] = 1 / ser_substation['ser_ss_deltmax']['value']
    
    eqninput = [eqn1['Name'], eqn1['Type'], eqn1['Sign'], eqn1['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation terms
    
    ##Term 1
    term1 = {}
    term1['Parent_unit'] = 'ser_ss'
    term1['Parent_eqn'] = 'ser_ss_tout_max'
    term1['Parent_stream'] = 'ser_ss_tout'                                      ##Only applicable for stream_limit types 
    term1['Coefficient'] = 0
    term1['Coeff_v1_2'] = 0                                                     ##Only applicable for stream_limit_modified types 
    term1['Coeff_v1_1'] = (ser_substation['ser_ss_totalflownwk']['value'] * ser_substation['ser_ss_cp']['value']) / ser_substation['ser_ss_demand']['value']
    term1['Coeff_v2_2'] = 0
    term1['Coeff_v2_1'] = 0
    term1['Coeff_v1v2'] = 0
    term1['Coeff_cst'] = 0

    terminput = [term1['Parent_unit'], term1['Parent_eqn'], term1['Parent_stream'], term1['Coefficient'], term1['Coeff_v1_2'],
                 term1['Coeff_v1_1'], term1['Coeff_v2_2'], term1['Coeff_v2_1'], term1['Coeff_v1v2'], term1['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms    