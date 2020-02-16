## This is the gv2 substation model, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype_gv2_substation_4nc (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type 
    
def gv2_substation_4nc (gv2_ss_4nc_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    from gv2_substation_4nc_compute import gv2_substation_4nc_compute
    import pandas as pd
    import numpy as np 
    
    ##Model description 
    ##This is the gv2 substation model, it treats the demand as a parameter and outputs a tout
    
    ##Defining inputs 

    ##Processing list of master decision variables/inputs as parameters 
    gv2_ss_demand = gv2_ss_4nc_mdv['Value'][0]
    gv2_ss_totalflownwk = gv2_ss_4nc_mdv['Value'][1]
    gv2_ss_tinevap = gv2_ss_4nc_mdv['Value'][2]

    ##Defined constants
    gv2_ss_tinmax  = 273.15 + 5       ##The maximum temperature of water entering the substation 
    gv2_ss_deltmax  = 5               ##The maximum delta t of the substation on the cold side  (value based on gv2)
    gv2_ss_cp = 4.2                   ##The heat capacity of water 

    ##Dependent constants 
    gv2_ss_dc = np.zeros((5,1))                                 ##Initialize the list, note the number of constants 
    
    gv2_ss_dc[0,0] = gv2_ss_demand
    gv2_ss_dc[1,0] = gv2_ss_totalflownwk
    gv2_ss_dc[2,0] = gv2_ss_cp
    gv2_ss_dc[3,0] = gv2_ss_tinmax
    gv2_ss_dc[4,0] = gv2_ss_deltmax

    gv2_ss_calc = gv2_substation_4nc_compute(gv2_ss_dc)
    
    gv2_ss_temp_exit_cst = gv2_ss_calc[0,0]            ##The constant term for the exit temperature stream 
    gv2_ss_constraint_eqn_coeff = gv2_ss_calc[1,0]     ##The constraint coefficient term to ensure that the delta t of the hx on the cold side does not exceed max delta t

############################################################################################################################################################################################################
    
    ##Unit definition
    
    ##Unit 1
    ud = {}
    ud['Name'] = 'gv2_ss_4nc'
    ud['Variable1'] = 'm_perc'                                          ##The percentage of the total flowrate into the system                                                                                                     
    ud['Variable2'] = '-'                                            ##Temperature of fluid entering the substation                                                              
    ud['Fmin_v1'] = 0
    ud['Fmax_v1'] = 1                                                                                                                   
    ud['Fmin_v2'] = '-'                                                                                                          
    ud['Fmax_v2'] = '-'                                                                                 
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
    utilitylist = utilitylist.append(unitdf, ignore_index=True)

############################################################################################################################################################################################################

    ##Layer and stream definition 

    ##Stream 1
    stream = {}                                                                
    stream['Parent'] = 'gv2_ss_4nc'                                                ##Flowrate out to the distribution pump
    stream['Type'] = 'flow'
    stream['Name'] = 'gv2_ss_4nc_flow_out'
    stream['Layer'] = 'evapnwk_consol_flow'
    stream['Stream_coeff_v1_2'] = 0
    stream['Stream_coeff_v1_1'] = gv2_ss_totalflownwk  
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
    
    ##Stream 2
    stream = {}                                                                
    stream['Parent'] = 'gv2_ss_4nc'                                                ##Temperture stream exiting the substation 
    stream['Type'] = 'temp_chil'
    stream['Name'] = 'gv2_ss_4nc_tout'
    stream['Layer'] = 'dist_nwk_outlet'
    stream['Stream_coeff_v1_2'] = 0
    stream['Stream_coeff_v1_1'] = gv2_ss_tinevap 
    stream['Stream_coeff_v2_2'] = 0
    stream['Stream_coeff_v2_1'] = 0
    stream['Stream_coeff_v1_v2'] = 0
    stream['Stream_coeff_cst'] = gv2_ss_temp_exit_cst
    stream['InOut'] = 'out'
    
    
    streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
                   stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True) 

############################################################################################################################################################################################################
        
    ##Constraint definition
    
    ##Equation definitions
    
    ##Equation 1
    eqn = {}
    eqn['Name'] = 'gv2_ss_4nc_tout_max'
    eqn['Type'] = 'stream_limit_modified'                                      ##Stream modified constraints involving more than 1 variable which cannot be expressed easily
    eqn['Sign'] = 'greater_than_equal_to'                                      ##Due to reciprocal less than equals to becomes greater than equals to, as both are positive
    eqn['RHS_value'] = 0
    
    eqninput = [eqn['Name'], eqn['Type'], eqn['Sign'], eqn['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Ensure that the totaluse is equals to 0 or 1 
    eqn = {}
    eqn['Name'] = 'totaluse_gv2_ss_4nc'
    eqn['Type'] = 'unit_binary'
    eqn['Sign'] = 'equal_to'
    eqn['RHS_value'] = 1
    
    eqninput = [eqn['Name'], eqn['Type'], eqn['Sign'], eqn['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)   
    
    ##Equation terms
    
    ##Term 1
    term = {}
    term['Parent_unit'] = 'gv2_ss_4nc'
    term['Parent_eqn'] = 'gv2_ss_4nc_tout_max'
    term['Parent_stream'] = '-'                                                ##Only applicable for stream_limit types 
    term['Coefficient'] = 0
    term['Coeff_v1_2'] = 0                                                     ##Only applicable for stream_limit_modified types 
    term['Coeff_v1_1'] = gv2_ss_constraint_eqn_coeff
    term['Coeff_v2_2'] = 0
    term['Coeff_v2_1'] = 0
    term['Coeff_v1_v2'] = 0
    term['Coeff_cst'] = -(1 / gv2_ss_deltmax)
    

    terminput = [term['Parent_unit'], term['Parent_eqn'], term['Parent_stream'], term['Coefficient'], term['Coeff_v1_2'],
                 term['Coeff_v1_1'], term['Coeff_v2_2'], term['Coeff_v2_1'], term['Coeff_v1_v2'], term['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    term = {}
    term['Parent_unit'] = 'gv2_ss_4nc'
    term['Parent_eqn'] = 'totaluse_gv2_ss_4nc'
    term['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types 
    term['Coefficient'] = 1
    term['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
    term['Coeff_v1_1'] = 0
    term['Coeff_v2_2'] = 0
    term['Coeff_v2_1'] = 0
    term['Coeff_v1_v2'] = 0
    term['Coeff_cst'] = 0

    terminput = [term['Parent_unit'], term['Parent_eqn'], term['Parent_stream'], term['Coefficient'], term['Coeff_v1_2'],
                 term['Coeff_v1_1'], term['Coeff_v2_2'], term['Coeff_v2_1'], term['Coeff_v1_v2'], term['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)  
    
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms    