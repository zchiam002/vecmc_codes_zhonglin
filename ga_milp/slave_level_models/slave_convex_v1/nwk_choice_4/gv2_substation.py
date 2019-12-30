## This is the gv2 substation model, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type 
    
def gv2_substation (gv2_ss_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    from nwk_choice_4.gv2_substation_compute import gv2_substation_compute
    import pandas as pd
    import numpy as np 
    
    ##Model description 
    ##This is the gv2 substation model, it treats the demand as a parameter and outputs a tout
    
    ##Legend of input variables 
    
    ##gv2ss_demand          --- the cooling load at the substation (kWh)
    ##gv2ss_totalflownwk    --- the total flowrate through parallel systems to this substation (m3/h) 
    
    ##Processing list of master decision variables/inputs as parameters 
    gv2ss_demand = gv2_ss_mdv['Value'][0]
    gv2ss_totalflownwk = gv2_ss_mdv['Value'][1]

    ##Define dictionary of values   
    
    gv2_substation = {}

    ##Input constants
    
    ##1
    gv2_ss_demand = {}
    gv2_ss_demand['value'] = gv2ss_demand
    gv2_ss_demand['units'] = 'kWh'
    gv2_ss_demand['status'] = 'cst_input'
    gv2_substation['gv2_ss_demand'] = gv2_ss_demand

    ##2
    gv2_ss_totalflownwk = {}
    gv2_ss_totalflownwk['value'] = gv2ss_totalflownwk
    gv2_ss_totalflownwk['units'] = 'm3/h'
    gv2_ss_totalflownwk['status'] = 'cst_input'
    gv2_substation['gv2_ss_totalflownwk'] = gv2_ss_totalflownwk

    ##Defined constants
    
    ##3
    gv2_ss_tinmax = {}
    gv2_ss_tinmax['value'] = 273.15 + 5                         ##The maximum temperature of water entering the substation 
    gv2_ss_tinmax['units'] = 'K'
    gv2_ss_tinmax['status'] = 'cst'
    gv2_substation['gv2_ss_tinmax'] = gv2_ss_tinmax 

    ##4
    gv2_ss_deltmax = {}
    gv2_ss_deltmax['value'] = 10                                ##The maximum delta t of the substation on the cold side  
    gv2_ss_deltmax['units'] = 'K'
    gv2_ss_deltmax['status'] = 'cst'
    gv2_substation['gv2_ss_deltmax'] = gv2_ss_deltmax    

    ##5
    gv2_ss_cp = {}
    gv2_ss_cp['value'] = 4.2                                    ##The heat capacity of water 
    gv2_ss_cp['units'] = 'kJ/kgK'
    gv2_ss_cp['status'] = 'cst'
    gv2_substation['gv2_ss_cp'] = gv2_ss_cp 

    ##Dependent constants 
    gv2_ss_dc = np.zeros((5,1))                                 ##Initialize the list, note the number of constants 
    
    gv2_ss_dc[0,0] = gv2_substation['gv2_ss_demand']['value']
    gv2_ss_dc[1,0] = gv2_substation['gv2_ss_totalflownwk']['value']
    gv2_ss_dc[2,0] = gv2_substation['gv2_ss_cp']['value']
    gv2_ss_dc[3,0] = gv2_substation['gv2_ss_tinmax']['value']
    gv2_ss_dc[4,0] = gv2_substation['gv2_ss_deltmax']['value']

    gv2_ss_calc = gv2_substation_compute(gv2_ss_dc)
    
    ##6
    gv2_ss_temp_exit_cst = {}
    gv2_ss_temp_exit_cst['value'] = gv2_ss_calc[0,0]            ##The constant term for the exit temperature stream 
    gv2_ss_temp_exit_cst['units'] = '-'
    gv2_ss_temp_exit_cst['status'] = 'calc'
    gv2_substation['gv2_ss_temp_exit_cst'] = gv2_ss_temp_exit_cst  

    ##7 
    gv2_ss_constraint_eqn_coeff = {}
    gv2_ss_constraint_eqn_coeff['value'] = gv2_ss_calc[1,0]     ##The constraint coefficient term to ensure that the delta t of the hx on the cold side does not exceed max delta t
    gv2_ss_constraint_eqn_coeff['units'] = '-'
    gv2_ss_constraint_eqn_coeff['status'] = 'calc'
    gv2_ss_constraint_eqn_coeff['gv2_ss_constraint_eqn_coeff'] = gv2_ss_constraint_eqn_coeff      

    ##Unit definition
    
    ##Unit 1
    gv2_ss = {}
    gv2_ss['Name'] = 'gv2_ss'
    gv2_ss['Variable1'] = 'm_perc'                                        ##The percentage of the total flowrate into the system                                                                                                     
    gv2_ss['Variable2'] = 't_in'                                           ##Temperature of fluid entering the substation                                                              
    gv2_ss['Fmin_v1'] = 0 
    gv2_ss['Fmax_v1'] = 1                                                                                                                    
    gv2_ss['Fmin_v2'] = 273.15 + 1                                                                                                           
    gv2_ss['Fmax_v2'] = gv2_substation['gv2_ss_tinmax']['value']                                                                                    
    gv2_ss['Coeff_v1_2'] = 0                                                                                                                 
    gv2_ss['Coeff_v1_1'] = 0         
    gv2_ss['Coeff_v2_2'] = 0
    gv2_ss['Coeff_v2_1'] = 0
    gv2_ss['Coeff_v1_v2'] = 0
    gv2_ss['Coeff_cst'] = 0
    gv2_ss['Fmin'] = 0
    gv2_ss['Fmax'] = 0
    gv2_ss['Cost_v1_2'] = 0
    gv2_ss['Cost_v1_1'] = 0
    gv2_ss['Cost_v2_2'] = 0
    gv2_ss['Cost_v2_1'] = 0
    gv2_ss['Cost_v1_v2'] = 0
    gv2_ss['Cost_cst'] = 0
    gv2_ss['Cinv_v1_2'] = 0
    gv2_ss['Cinv_v1_1'] = 0
    gv2_ss['Cinv_v2_2'] = 0
    gv2_ss['Cinv_v2_1'] = 0
    gv2_ss['Cinv_v1_v2'] = 0
    gv2_ss['Cinv_cst'] = 0
    gv2_ss['Power_v1_2'] = 0
    gv2_ss['Power_v1_1'] = 0
    gv2_ss['Power_v2_2'] = 0
    gv2_ss['Power_v2_1'] = 0
    gv2_ss['Power_v1_v2'] = 0
    gv2_ss['Power_cst'] = 0
    gv2_ss['Impact_v1_2'] = 0
    gv2_ss['Impact_v1_1'] = 0
    gv2_ss['Impact_v2_2'] = 0
    gv2_ss['Impact_v2_1'] = 0
    gv2_ss['Impact_v1_v2'] = 0
    gv2_ss['Impact_cst'] = 0

    unitinput = [gv2_ss['Name'], gv2_ss['Variable1'], gv2_ss['Variable2'], gv2_ss['Fmin_v1'], gv2_ss['Fmax_v1'], gv2_ss['Fmin_v2'], gv2_ss['Fmax_v2'], gv2_ss['Coeff_v1_2'], 
                gv2_ss['Coeff_v1_1'], gv2_ss['Coeff_v2_2'], gv2_ss['Coeff_v2_1'], gv2_ss['Coeff_v1_v2'], gv2_ss['Coeff_cst'], gv2_ss['Fmin'], gv2_ss['Fmax'], gv2_ss['Cost_v1_2'], 
                gv2_ss['Cost_v1_1'], gv2_ss['Cost_v2_2'], gv2_ss['Cost_v2_1'], gv2_ss['Cost_v1_v2'], gv2_ss['Cost_cst'], gv2_ss['Cinv_v1_2'], gv2_ss['Cinv_v1_1'], gv2_ss['Cinv_v2_2'], 
                gv2_ss['Cinv_v2_1'], gv2_ss['Cinv_v1_v2'], gv2_ss['Cinv_cst'], gv2_ss['Power_v1_2'], gv2_ss['Power_v1_1'], gv2_ss['Power_v2_2'], gv2_ss['Power_v2_1'], 
                gv2_ss['Power_v1_v2'], gv2_ss['Power_cst'], gv2_ss['Impact_v1_2'], gv2_ss['Impact_v1_1'], gv2_ss['Impact_v2_2'], gv2_ss['Impact_v2_1'], gv2_ss['Impact_v1_v2'], 
                gv2_ss['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)

    ##Layer and stream definition 

    ##Stream 1
    stream1 = {}                                                                
    stream1['Parent'] = 'gv2_ss'                                                ##Temperature stream entering the substation 
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'gv2_ss_tin'
    stream1['Layer'] = 'sp1_temp2gv2'
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
    stream2['Parent'] = 'gv2_ss'                                                ##Flowrate stream entering the substation 
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'gv2_ss_mfin'
    stream2['Layer'] = 'gv2_nwk2gv2_ss'
    stream2['Stream_coeff_v1_2'] = 0
    stream2['Stream_coeff_v1_1'] = gv2_substation['gv2_ss_totalflownwk']['value']
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
    stream3['Parent'] = 'gv2_ss'                                                ##Temperture stream exiting the substation 
    stream3['Type'] = 'balancing_only'
    stream3['Name'] = 'gv2_ss_tout'
    stream3['Layer'] = 'ss2sp2_temp'
    stream3['Stream_coeff_v1_2'] = 0
    stream3['Stream_coeff_v1_1'] = 0
    stream3['Stream_coeff_v2_2'] = 0
    stream3['Stream_coeff_v2_1'] = 0
    stream3['Stream_coeff_v1_v2'] = 1
    stream3['Stream_coeff_cst'] = gv2_substation['gv2_ss_temp_exit_cst']['value']
    stream3['InOut'] = 'out'
    
    streaminput = [stream3['Parent'], stream3['Type'], stream3['Name'], stream3['Layer'], stream3['Stream_coeff_v1_2'], stream3['Stream_coeff_v1_1'], stream3['Stream_coeff_v2_2'],
                   stream3['Stream_coeff_v2_1'], stream3['Stream_coeff_v1_v2'], stream3['Stream_coeff_cst'], stream3['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True) 
    
    ##Stream 4
    stream4 = {}                                                                
    stream4['Parent'] = 'gv2_ss'                                                ##Flowrate stream exiting the substation 
    stream4['Type'] = 'balancing_only'
    stream4['Name'] = 'gv2_ss_mfout'
    stream4['Layer'] = 'ss_2_dist_pump1_flow'
    stream4['Stream_coeff_v1_2'] = 0
    stream4['Stream_coeff_v1_1'] = gv2_substation['gv2_ss_totalflownwk']['value']
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
    eqn1['Name'] = 'gv2_ss_tout_max'
    eqn1['Type'] = 'stream_limit_modified'                                      ##Stream modified constraints involving more than 1 variable which cannot be expressed easily
    eqn1['Sign'] = 'greater_than_equal_to'                                      ##Due to reciprocal less than equals to becomes greater than equals to, as both are positive
    eqn1['RHS_value'] = 1 / gv2_substation['gv2_ss_deltmax']['value']
    
    eqninput = [eqn1['Name'], eqn1['Type'], eqn1['Sign'], eqn1['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation terms
    
    ##Term 1
    term1 = {}
    term1['Parent_unit'] = 'gv2_ss'
    term1['Parent_eqn'] = 'gv2_ss_tout_max'
    term1['Parent_stream'] = 'gv2_ss_tout'                                      ##Only applicable for stream_limit types 
    term1['Coefficient'] = 0
    term1['Coeff_v1_2'] = 0                                                     ##Only applicable for stream_limit_modified types 
    term1['Coeff_v1_1'] = gv2_ss_constraint_eqn_coeff['gv2_ss_constraint_eqn_coeff']['value']
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