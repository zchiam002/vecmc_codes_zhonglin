##This is chiller 2 evaporator pump model 

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    
def checktype_chiller2_evap_pump (unit_type):                  ##Input the unit type here

    ##unit_type     --- a variable to store the type of unit  

    unit_type = 'utility'
    
    return unit_type

##Model description: 
    ##Built on pressure drop ratios based on a fixed flowrate to estimate the electricity cost  
def chiller2_evap_pump (mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):

    ##mdv               --- the associated decision variables from the GA, or parameters 
    ##utilitylist       --- a dataframe to extract general information from the model 
    ##streams           --- a dataframe to extract stream information from the model 
    ##cons_eqns         --- a dataframe to extract constraint equations from the model 
    ##cons_eqns_terms   --- a dataframe to extract terms in the constraint equation from the model 

    import os 
    current_path = os.path.dirname(__file__)[:-12] + '//'    
    from chiller2_evap_pump_compute import chiller2_evap_pump_compute
    import pandas as pd
    import numpy as np

    ##Defining inputs    
    
    ##Processing list of master decision variables as parameters
    ch2_ep_steps = mdv['Value'][0]

    ##Defined constants 
    ch2_ep_c0 = -0.0000136254       ##These are pump cure coefficients which are needed to formulate constraints                   
    ch2_ep_c1 = 0.0001647403
    ch2_ep_c2 = 21.4327511013
    
    ##These values are pre-calculated and needs to be extracted from a specific location 
     
    ch2_ep_p_look_up_table_loc = current_path + 'model_param//'       ##Distribution pump look up table location 
    ch2_ep_p_table_filename = 'evap_cond_pump_lincoeff.csv'
    ch2_ep_p_table = pd.read_csv(ch2_ep_p_look_up_table_loc + ch2_ep_p_table_filename)
    
    ch2_ep_p_coeff = ch2_ep_p_table['p_coeff'][1]
    ch2_ep_m_coeff = ch2_ep_p_table['m_coeff'][1]
    ch2_ep_cst = ch2_ep_p_table['cst'][1]
    ch2_ep_max_m = ch2_ep_p_table['max_flow'][1]
    ch2_ep_maxpressureatmaxrpm = ch2_ep_p_table['max_pressure'][1]    

    ##Calling a compute file to process dependent values
        ##Placing the values in a numpy array for easy data handling 
    ch2_ep_dc = np.zeros((5,1))
    
    ch2_ep_dc[0,0] = ch2_ep_c0
    ch2_ep_dc[1,0] = ch2_ep_c1
    ch2_ep_dc[2,0] = ch2_ep_c2
    ch2_ep_dc[3,0] = ch2_ep_max_m
    ch2_ep_dc[4,0] = ch2_ep_steps

    ch2_ep_calc = chiller2_evap_pump_compute(ch2_ep_dc)

#################################################################################################################################################################################################        
    ##Unit definition 
    
    ##Evaporator pump stepwise
    
    for i in range (0, int(ch2_ep_steps)):
        ud = {}
        ud['Name'] = 'ch2_ep_' + str(i + 1)
        ud['Variable1'] = 'm_flow'                                                                        
        ud['Variable2'] = 'delp'                                                                  
        ud['Fmin_v1'] = ch2_ep_calc['lb'][i] * ch2_ep_max_m
        ud['Fmax_v1'] = ch2_ep_calc['ub'][i] * ch2_ep_max_m                                                                              
        ud['Fmin_v2'] = 0                                                                                      
        ud['Fmax_v2'] = ch2_ep_maxpressureatmaxrpm                                                                                  
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
        ud['Power_v1_1'] = ch2_ep_m_coeff
        ud['Power_v2_2'] = 0
        ud['Power_v2_1'] = ch2_ep_p_coeff
        ud['Power_v1_v2'] = 0
        ud['Power_cst'] = ch2_ep_cst
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
    
    ##Evaporator pump stepwise 
    for i in range (0, int(ch2_ep_steps)):
        
        ##Stream --- flowrate into the chiller 2 evaporator pump from chiller 2 evaporator network 
        stream = {}                         
        stream['Parent'] = 'ch2_ep_' + str(i + 1)
        stream['Type'] = 'flow'
        stream['Name'] = 'ch2_ep_' + str(i + 1) + '_flow_in'
        stream['Layer'] = 'ch2evapnwk_2_ch2pump_flow'
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

        ##Stream --- pressure from chiller 2 evaporator network to chiller 2 evaporator pump
        stream = {}                                                                
        stream['Parent'] = 'ch2_ep_' + str(i + 1)
        stream['Type'] = 'pressure'
        stream['Name'] = 'ch2_ep_' + str(i + 1) + '_delp_in'
        stream['Layer'] = 'ch2evapnwk_2_ch2pump_delp'
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
        
        ##Stream --- flowrate from chiller 2 evaporator pump to distribution network
        stream = {}                                                                
        stream['Parent'] = 'ch2_ep_' + str(i + 1)
        stream['Type'] = 'flow'
        stream['Name'] = 'ch2_ep_' + str(i + 1) + '_flow_out'
        stream['Layer'] = 'evap_nwk_flow'
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
    eqn['Name'] = 'totaluse_ch2_ep'
    eqn['Type'] = 'unit_binary'
    eqn['Sign'] = 'less_than_equal_to'
    eqn['RHS_value'] = 1
    
    eqninput = [eqn['Name'], eqn['Type'], eqn['Sign'], eqn['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)        

    for i in range (0, int(ch2_ep_steps)):
        eqn = {}
        eqn['Name'] = 'ch2_ep_' + str(i + 1) + '_max_pressure'
        eqn['Type'] = 'stream_limit_modified'                                      
        eqn['Sign'] = 'less_than_equal_to'                                    
        eqn['RHS_value'] = ch2_ep_calc['int'][i]
        
        eqninput = [eqn['Name'], eqn['Type'], eqn['Sign'], eqn['RHS_value']]
        eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
        cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)                                                       
    
    ##Equation terms 

    for i in range (0, int(ch2_ep_steps)):   
        term = {}
        term['Parent_unit'] = 'ch2_ep_' + str(i + 1)
        term['Parent_eqn'] = 'totaluse_ch2_ep'
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
        term['Parent_unit'] = 'ch2_ep_' + str(i + 1)
        term['Parent_eqn'] = 'ch2_ep_' + str(i + 1) + '_max_pressure'
        term['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types 
        term['Coefficient'] = 0
        term['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
        term['Coeff_v1_1'] = -ch2_ep_calc['grad'][i]
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