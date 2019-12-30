##This is chiller 2 condenser pump model 

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype_cond_pump2 (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type

def cond_pump2 (cp2_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    
    from cond_pump2_compute import cond_pump2_compute
    import pandas as pd
    import numpy as np
    
    ##Model description: 
    ##Built on pressure drop ratios based on a fixed flowrate to estimate the electricity cost  
    
    ##cp2_mdv --- the master decision variables which are used as parameters at this stage 
    ##utilitylist --- a dataframe to hold essential values for writing the MILP script 
    ##streams --- a dataframe to write connections to other units 
    ##cons_eqns --- additional constraints are explicitly stated here 
    ##cons_eqns_terms --- the terms to the constraints     ##Legend of input variables 
    
    ##Defining inputs    
    
    ##Processing list of master decision variables as parameters
    cp2_steps = cp2_mdv['Value'][0]
    cp2_time_dependent_elect_tariff = cp2_mdv['Value'][1]   ##Time dependent electricity tariff per kWh used. 

    ##Defined constants 
    cp2_c0 = -0.0000090818       ##These are pump cure coefficients which are needed to formulate constraints                   
    cp2_c1 = 0.0029568794
    cp2_c2 = 45.1880038403
    
    ##These values are pre-calculated and needs to be extracted from a specific location 
     
    cp2_p_look_up_table_loc = 'C:\\Optimization_zlc\\master_level_models\\load_only_storage_milp_master_level_models\\look_up_tables\\'      ##Distribution pump look up table location 
    cp2_p_table_filename = 'evap_cond_pump_lincoeff.csv'
    cp2_p_table = pd.read_csv(cp2_p_look_up_table_loc + cp2_p_table_filename)
    
    cp2_p_coeff = cp2_p_table['p_coeff'][4]
    cp2_m_coeff = cp2_p_table['m_coeff'][4]
    cp2_cst = cp2_p_table['cst'][4]
    cp2_max_m = cp2_p_table['max_flow'][4]
    cp2_maxpressureatmaxrpm = cp2_p_table['max_pressure'][4]
    
    ##Calling a compute file to process dependent values
        ##Placing the values in a numpy array for easy data handling 
    cp2_dc = np.zeros((5,1))
    
    cp2_dc[0,0] = cp2_c0
    cp2_dc[1,0] = cp2_c1
    cp2_dc[2,0] = cp2_c2
    cp2_dc[3,0] = cp2_max_m
    cp2_dc[4,0] = cp2_steps

    cp2_calc = cond_pump2_compute(cp2_dc)

#################################################################################################################################################################################################        
    ##Unit definition 
    
    ##Condenser pump stepwise
    
    for i in range (0, int(cp2_steps)):
        ud = {}
        ud['Name'] = 'cp2_' + str(i + 1)
        ud['Variable1'] = 'm_flow'                                                                        
        ud['Variable2'] = 'delp'                                                                  
        ud['Fmin_v1'] = cp2_calc['lb'][i] * cp2_max_m
        ud['Fmax_v1'] = cp2_calc['ub'][i] * cp2_max_m                                                                              
        ud['Fmin_v2'] = 0                                                                                      
        ud['Fmax_v2'] = cp2_maxpressureatmaxrpm                                                                                  
        ud['Coeff_v1_2'] = 0                                                                                    
        ud['Coeff_v1_1'] = 0 
        ud['Coeff_v2_2'] = 0
        ud['Coeff_v2_1'] = 0
        ud['Coeff_v1_v2'] = 0 
        ud['Coeff_cst'] = 0
        ud['Fmin'] = 0
        ud['Fmax'] = 0
        ud['Cost_v1_2'] = 0
        ud['Cost_v1_1'] = cp2_time_dependent_elect_tariff * cp2_m_coeff
        ud['Cost_v2_2'] = 0
        ud['Cost_v2_1'] = cp2_time_dependent_elect_tariff * cp2_p_coeff
        ud['Cost_v1_v2'] = 0
        ud['Cost_cst'] = cp2_time_dependent_elect_tariff * cp2_cst
        ud['Cinv_v1_2'] = 0
        ud['Cinv_v1_1'] = 0
        ud['Cinv_v2_2'] = 0
        ud['Cinv_v2_1'] = 0
        ud['Cinv_v1_v2'] = 0
        ud['Cinv_cst'] = 0
        ud['Power_v1_2'] = 0
        ud['Power_v1_1'] = cp2_m_coeff
        ud['Power_v2_2'] = 0
        ud['Power_v2_1'] = cp2_p_coeff
        ud['Power_v1_v2'] = 0
        ud['Power_cst'] = cp2_cst
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
    
    ##Condenser pump stepwise 
    for i in range (0, int(cp2_steps)):
        
        ##Stream --- flowrate into the chiller 2 condenser pump from chiller 2  
        stream = {}                         
        stream['Parent'] = 'cp2_' + str(i + 1)
        stream['Type'] = 'flow'
        stream['Name'] = 'cp2_' + str(i + 1) + '_flow_in'
        stream['Layer'] = 'chiller2_flow_cond_pump'
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

        ##Stream --- pressure from chiller 2 and condenser network to chiller 2 condenser pump 
        stream = {}                                                                
        stream['Parent'] = 'cp2_' + str(i + 1)
        stream['Type'] = 'pressure'
        stream['Name'] = 'cp2_' + str(i + 1) + '_delp_in'
        stream['Layer'] = 'c_nwk_2_cp2'
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
        
############################################################################################################################################################################################################
    
    ##Constraint definition
    
    ##Equation definitions     
    
    ##Ensure that the totaluse is equals to 0 or 1 
    eqn = {}
    eqn['Name'] = 'totaluse_cp2'
    eqn['Type'] = 'unit_binary'
    eqn['Sign'] = 'less_than_equal_to'
    eqn['RHS_value'] = 1
    
    eqninput = [eqn['Name'], eqn['Type'], eqn['Sign'], eqn['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)        

    for i in range (0, int(cp2_steps)):
        eqn = {}
        eqn['Name'] = 'cp2_' + str(i + 1) + '_max_pressure'
        eqn['Type'] = 'stream_limit_modified'                                      
        eqn['Sign'] = 'less_than_equal_to'                                    
        eqn['RHS_value'] = cp2_calc['int'][i]
        
        eqninput = [eqn['Name'], eqn['Type'], eqn['Sign'], eqn['RHS_value']]
        eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
        cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)                                                       
    
    ##Equation terms 

    for i in range (0, int(cp2_steps)):   
        term = {}
        term['Parent_unit'] = 'cp2_' + str(i + 1)
        term['Parent_eqn'] = 'totaluse_cp2'
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
        term['Parent_unit'] = 'cp2_' + str(i + 1)
        term['Parent_eqn'] = 'cp2_' + str(i + 1) + '_max_pressure'
        term['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types 
        term['Coefficient'] = 0
        term['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
        term['Coeff_v1_1'] = -cp2_calc['grad'][i]
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