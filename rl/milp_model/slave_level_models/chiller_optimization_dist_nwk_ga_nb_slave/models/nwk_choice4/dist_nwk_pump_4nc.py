##This is distribution network pump model for the distribution pump combinations available (standalone only, no parallel operation)

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype_dist_nwk_pump_4nc (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type

def dist_nwk_pump_4nc (dist_np_4nc_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    
    from dist_nwk_pump_4nc_compute import dist_nwk_pump_4nc_compute
    import pandas as pd
    import numpy as np
    import os
    current_directory = os.path.dirname(__file__)[:-81] + '//' 
    
    ##Model description: 
    ##Built on pressure drop ratios based on a fixed flowrate to estimate the electricity cost  
    
    ##dist_np_4nc_mdv --- the master decision variables which are used as parameters at this stage 
    ##utilitylist --- a dataframe to hold essential values for writing the MILP script 
    ##streams --- a dataframe to write connections to other units 
    ##cons_eqns --- additional constraints are explicitly stated here 
    ##cons_eqns_terms --- the terms to the constraints     ##Legend of input variables 
    
    ##Defining inputs    
    
    ##Processing list of master decision variables as parameters
    
    dist_np_nwk_choice = dist_np_4nc_mdv['Value'][0]
    dist_np_steps = dist_np_4nc_mdv['Value'][1]

    ##Defined constants
    
    ##The constants are chosen based on predefined pumps combinations
     
    dist_np_look_up_table_loc = current_directory + 'master_level_models\\\chiller_optimization_dist_nwk_ga_nb_master_level_models\\look_up_tables\\'      ##Distribution pump look up table location 
    dist_np_table_filename = 'dist_pump_lincoeff.csv'
    dist_np_table = pd.read_csv(dist_np_look_up_table_loc + dist_np_table_filename)
    dist_np_pres_table_filename = 'dist_pump_presscoeff.csv'
    dist_np_pres_table = pd.read_csv(dist_np_look_up_table_loc + dist_np_pres_table_filename)
        
    ##Calling a compute file to process dependent values
        ##Placing the values in a numpy array for easy data handling 
    dist_np_dc = np.zeros((2,1))
    
    dist_np_dc[0,0] = dist_np_nwk_choice
    dist_np_dc[1,0] = dist_np_steps
    
    ret_values_pump = dist_nwk_pump_4nc_compute(dist_np_dc, dist_np_table, dist_np_pres_table)

#################################################################################################################################################################################################        
    ##Unit definition 
    
    ##Distribution network pump stepwise, this is done depending on the selected network in the master level 
    
    ##calculating the number times to run the loop
    dim_ret_values_pump = ret_values_pump.shape 
    
    for i in range (0, int(dim_ret_values_pump[0])):
        ud = {}
        ud['Name'] = 'dist_np_4nc_combi_' + str(ret_values_pump['combi'][i]) + '_' + str(ret_values_pump['step'][i])
        ud['Variable1'] = 'm_flow'                                                                        
        ud['Variable2'] = 'delp'                                                                  
        ud['Fmin_v1'] = ret_values_pump['lb'][i] * ret_values_pump['max_m'][i]
        ud['Fmax_v1'] = ret_values_pump['ub'][i] * ret_values_pump['max_m'][i]                                                                              
        ud['Fmin_v2'] = 0                                                                                      
        ud['Fmax_v2'] = ret_values_pump['max_p'][i]                                                                                   
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
        ud['Power_v1_1'] = ret_values_pump['m_coeff'][i]
        ud['Power_v2_2'] = 0
        ud['Power_v2_1'] = ret_values_pump['p_coeff'][i]
        ud['Power_v1_v2'] = 0
        ud['Power_cst'] = ret_values_pump['cst'][i]
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

####################################################################################################################################################################################################        
    ##Stream definition 
    
    ##Distribution network pump stepwise 
    for i in range (0, int(dim_ret_values_pump[0])):
        
        ##Stream --- flowrate into the distribution network pump from the distribution network 
        stream = {}                         
        stream['Parent'] = 'dist_np_4nc_combi_' + str(ret_values_pump['combi'][i]) + '_' + str(ret_values_pump['step'][i])
        stream['Type'] = 'flow'
        stream['Name'] = 'dist_np_4nc_combi_' + str(ret_values_pump['combi'][i]) + '_' + str(ret_values_pump['step'][i]) + '_flow_in'
        stream['Layer'] = 'distnwk_consol_flow'
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

        ##Stream --- pressure from parallel_nwk_consol into the distribution pump
        stream = {}                                                                
        stream['Parent'] = 'dist_np_4nc_combi_' + str(ret_values_pump['combi'][i]) + '_' + str(ret_values_pump['step'][i])
        stream['Type'] = 'pressure'
        stream['Name'] = 'dist_np_4nc_combi_' + str(ret_values_pump['combi'][i]) + '_' + str(ret_values_pump['step'][i]) + '_delp_in'
        stream['Layer'] = 'paranwk2distpump_delp'
        stream['Stream_coeff_v1_2'] = 0
        stream['Stream_coeff_v1_1'] = 0 
        stream['Stream_coeff_v2_2'] = 0
        stream['Stream_coeff_v2_1'] = 1
        stream['Stream_coeff_v1_v2'] = 0
        stream['Stream_coeff_cst'] = 0
        stream['InOut'] = 'in'
        
        streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
                       stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
        streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                              'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
        streams = streams.append(streamdf, ignore_index=True)
        
        ##Stream --- flowrate from distribution network pump to chiller_evap_consol_flow
        stream = {}                                                                
        stream['Parent'] = 'dist_np_4nc_combi_' + str(ret_values_pump['combi'][i]) + '_' + str(ret_values_pump['step'][i])
        stream['Type'] = 'balancing_only'
        stream['Name'] = 'dist_np_4nc_combi_' + str(ret_values_pump['combi'][i]) + '_' + str(ret_values_pump['step'][i]) + '_flow_out'
        stream['Layer'] = 'evapnwk_consol_flow'
        stream['Stream_coeff_v1_2'] = 0
        stream['Stream_coeff_v1_1'] = 1
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
        
############################################################################################################################################################################################################
    
    ##Constraint definition
    
    ##Equation definitions     
    
    ##Ensure that the totaluse is equals to 0 or 1 
    eqn = {}
    eqn['Name'] = 'totaluse_dist_np_4nc'
    eqn['Type'] = 'unit_binary'
    eqn['Sign'] = 'less_than_equal_to'
    eqn['RHS_value'] = 1
    
    eqninput = [eqn['Name'], eqn['Type'], eqn['Sign'], eqn['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)        

    for i in range (0, int(dim_ret_values_pump[0])):
        eqn = {}
        eqn['Name'] = 'dist_np_4nc_combi_' + str(ret_values_pump['combi'][i]) + '_' + str(ret_values_pump['step'][i]) + '_max_pressure'
        eqn['Type'] = 'stream_limit_modified'                                      
        eqn['Sign'] = 'less_than_equal_to'                                    
        eqn['RHS_value'] = ret_values_pump['int'][i]
        
        eqninput = [eqn['Name'], eqn['Type'], eqn['Sign'], eqn['RHS_value']]
        eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
        cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)                                                       
    
    ##Equation terms 

    for i in range (0, int(dim_ret_values_pump[0])):   
        term = {}
        term['Parent_unit'] = 'dist_np_4nc_combi_' + str(ret_values_pump['combi'][i]) + '_' + str(ret_values_pump['step'][i])
        term['Parent_eqn'] = 'totaluse_dist_np_4nc'
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
        
        term = {}
        term['Parent_unit'] = 'dist_np_4nc_combi_' + str(ret_values_pump['combi'][i]) + '_' + str(ret_values_pump['step'][i])
        term['Parent_eqn'] = 'dist_np_4nc_combi_' + str(ret_values_pump['combi'][i]) + '_' + str(ret_values_pump['step'][i]) + '_max_pressure'
        term['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types 
        term['Coefficient'] = 0
        term['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
        term['Coeff_v1_1'] = -ret_values_pump['grad'][i]
        term['Coeff_v2_2'] = 0
        term['Coeff_v2_1'] = 1
        term['Coeff_v1_v2'] = 0
        term['Coeff_cst'] = 0
    
        terminput = [term['Parent_unit'], term['Parent_eqn'], term['Parent_stream'], term['Coefficient'], term['Coeff_v1_2'],
                     term['Coeff_v1_1'], term['Coeff_v2_2'], term['Coeff_v2_1'], term['Coeff_v1_v2'], term['Coeff_cst']]
        terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                                  'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2',
                                                                  'Coeff_cst'])
        cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True) 
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms     