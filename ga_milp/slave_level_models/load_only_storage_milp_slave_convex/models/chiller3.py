## This is a chiller model, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype_chiller3 (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type

def chiller3 (ch3_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    from chiller3_compute import chiller3_compute
    import pandas as pd
    import numpy as np
    
    ##This is the chiller3 model, it is simplified by having 
    
    ##Model description: 
    ##Built based on Gordon-Ng's Universal Chiller model
    ##The COP is kept constant at predefined steps in equally spaced intervals 
    ##The inputs to this function are variables to the eyes of the Master optimizer 
    
    ##ch3_mdv --- the master decision variables which are used as parameters at this stage 
    ##utilitylist --- a dataframe to hold essential values for writing the MILP script 
    ##streams --- a dataframe to write connections to other units 
    ##cons_eqns --- additional constraints are explicitly stated here 
    ##cons_eqns_terms --- the terms to the constraints 
    
    ##Defining inputs 
    
    ##Processing list of master decision variables
    ch3_twb = ch3_mdv['Value'][0]                           ##The associated thermodynamic wetbulb temperature 
    ch3_steps = ch3_mdv['Value'][1]                         ##The number of piecewise linear pieces
    ch3_time_dependent_elect_tariff = ch3_mdv['Value'][2]   ##Time dependent electricity tariff per kWh used. 
    
    ##Defined constants 
    ch3_rated_cap = 7330                                    ##Rated capacity of the chiller
    ch3_tevap_out = 5 + 273.15                              ##Chiller supply temperature
    ch3_delt_evap = 5                                       ##Temperature difference at the evaporator side
    ch3_delt_cond = 5                                       ##Temperature difference at the condenser side
    ch3_b0 = 1.35049420632748                               ##Chiller regression derived coefficients
    ch3_b1 = -134.853705222833
    ch3_b2 = 0.00430128306723068
    ch3_qc_coeff = 1.10348067074030
    ch3_cp = 4.2                                            ##Specific heat of water
    ch3_evap_nwk_coeff = 3.07492E-05
    ch3_cond_nwk_coeff = 0.000017825112553599
    
    ##Calling a compute file to process dependent values
        ##Placing the values in a numpy array for easy data handling 
    ch3_dc = np.zeros((13, 1))
    ch3_dc[0,0] = ch3_twb
    ch3_dc[1,0] = ch3_rated_cap
    ch3_dc[2,0] = ch3_b0
    ch3_dc[3,0] = ch3_b1
    ch3_dc[4,0] = ch3_b2
    ch3_dc[5,0] = ch3_qc_coeff
    ch3_dc[6,0] = ch3_steps
    ch3_dc[7,0] = ch3_tevap_out
    ch3_dc[8,0] = ch3_delt_evap
    ch3_dc[9,0] = ch3_delt_cond
    ch3_dc[10,0] = ch3_evap_nwk_coeff
    ch3_dc[11,0] = ch3_cp
    ch3_dc[12,0] = ch3_cond_nwk_coeff

    ch3_ret_vals, ch3_evap_nwk_ret_vals, ch3_cond_nwk_ret_vals = chiller3_compute(ch3_dc)
    
#################################################################################################################################################################################################        
    ##Unit definition 
    
    ##Evaporator stepwise
    for i in range (0, int(ch3_steps)):
        ud = {}
        ud['Name'] = 'ch3_' + str(i + 1)
        ud['Variable1'] = 'q_out'                                              
        ud['Variable2'] = '-'                                                
        ud['Fmin_v1'] = ch3_ret_vals['lb'][i] * ch3_rated_cap
        ud['Fmax_v1'] = ch3_ret_vals['ub'][i] * ch3_rated_cap                                                                                             
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
        ud['Cost_v1_1'] = ch3_time_dependent_elect_tariff * ch3_ret_vals['grad'][i]
        ud['Cost_v2_2'] = 0
        ud['Cost_v2_1'] = 0
        ud['Cost_v1_v2'] = 0
        ud['Cost_cst'] = ch3_time_dependent_elect_tariff * ch3_ret_vals['int'][i]
        ud['Cinv_v1_2'] = 0
        ud['Cinv_v1_1'] = 0
        ud['Cinv_v2_2'] = 0
        ud['Cinv_v2_1'] = 0
        ud['Cinv_v1_v2'] = 0
        ud['Cinv_cst'] = 0
        ud['Power_v1_2'] = 0
        ud['Power_v1_1'] = ch3_ret_vals['grad'][i]
        ud['Power_v2_2'] = 0
        ud['Power_v2_1'] = 0
        ud['Power_v1_v2'] = 0
        ud['Power_cst'] = ch3_ret_vals['int'][i]
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
    
    ##Evaporator stepwise 
    for i in range (0, int(ch3_steps)):

        ##Stream --- cooling out
        stream = {}                                                                
        stream['Parent'] = 'ch3_' + str(i + 1)
        stream['Type'] = 'flow'
        stream['Name'] = 'ch3_' + str(i + 1) + '_q_out'
        stream['Layer'] = 'chillers_to_substations_storage_q_out'
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
        
        ##Stream --- heat rejection   
        stream = {}                                                                
        stream['Parent'] = 'ch3_' + str(i + 1)
        stream['Type'] = 'flow'
        stream['Name'] = 'ch3_' + str(i + 1) + '_heatrej'
        stream['Layer'] = 'chiller_heat_rej'
        stream['Stream_coeff_v1_2'] = 0
        stream['Stream_coeff_v1_1'] = (ch3_dc[5,0] * ch3_ret_vals['grad'][i]) + (ch3_dc[5,0]) 
        stream['Stream_coeff_v2_2'] = 0
        stream['Stream_coeff_v2_1'] = 0
        stream['Stream_coeff_v1_v2'] = 0
        stream['Stream_coeff_cst'] = ch3_ret_vals['int'][i] * ch3_dc[5,0]
        stream['InOut'] = 'out'
        
        streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
                       stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
        streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                              'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
        streams = streams.append(streamdf, ignore_index=True)

        ##Stream --- flowrate to the evaporator pump   
        stream = {}                                                                
        stream['Parent'] = 'ch3_' + str(i + 1)
        stream['Type'] = 'flow'
        stream['Name'] = 'ch3_' + str(i + 1) + '_flow_ep'
        stream['Layer'] = 'chiller3_flow_evap_pump'
        stream['Stream_coeff_v1_2'] = 0
        stream['Stream_coeff_v1_1'] = 3600 / (998.2 * ch3_cp * ch3_dc[8,0])
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
        
        ##Stream --- pressure flow to the evaporator pump   
        stream = {}                                                                
        stream['Parent'] = 'ch3_' + str(i + 1)
        stream['Type'] = 'pressure'
        stream['Name'] = 'ch3_' + str(i + 1) + '_pressure_flow_ep'
        stream['Layer'] = 'e_nwk_2_ep3'
        stream['Stream_coeff_v1_2'] = 0
        stream['Stream_coeff_v1_1'] = (3600 / (998.2 * ch3_cp * ch3_dc[8,0])) * ch3_evap_nwk_ret_vals['grad'][i]
        stream['Stream_coeff_v2_2'] = 0
        stream['Stream_coeff_v2_1'] = 0
        stream['Stream_coeff_v1_v2'] = 0
        stream['Stream_coeff_cst'] = ch3_evap_nwk_ret_vals['int'][i]
        stream['InOut'] = 'out'
        
        streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
                       stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
        streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                              'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
        streams = streams.append(streamdf, ignore_index=True) 
        
        ##Stream --- flowrate to the condenser pump   
        stream = {}                                                                
        stream['Parent'] = 'ch3_' + str(i + 1)
        stream['Type'] = 'flow'
        stream['Name'] = 'ch3_' + str(i + 1) + '_flow_cp'
        stream['Layer'] = 'chiller3_flow_cond_pump'
        stream['Stream_coeff_v1_2'] = 0
        stream['Stream_coeff_v1_1'] = (3600 * ((ch3_dc[5,0] * ch3_ret_vals['grad'][i]) + ch3_dc[5,0])) / (998.2 * ch3_cp * ch3_dc[9,0])
        stream['Stream_coeff_v2_2'] = 0
        stream['Stream_coeff_v2_1'] = 0
        stream['Stream_coeff_v1_v2'] = 0
        stream['Stream_coeff_cst'] = (3600 * ch3_dc[5,0] * ch3_ret_vals['int'][i]) / (998.2 * ch3_cp * ch3_dc[9,0])
        stream['InOut'] = 'out'
        
        streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
                       stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
        streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                              'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
        streams = streams.append(streamdf, ignore_index=True)
        
        ##Stream --- pressure flow to the condenser pump   
        stream = {}                                                                
        stream['Parent'] = 'ch3_' + str(i + 1)
        stream['Type'] = 'pressure'
        stream['Name'] = 'ch3_' + str(i + 1) + 'pressure_flow_cp'
        stream['Layer'] = 'c_nwk_2_cp3'
        stream['Stream_coeff_v1_2'] = 0
        stream['Stream_coeff_v1_1'] = ch3_cond_nwk_ret_vals['grad'][i] * ((3600 * ((ch3_dc[5,0] * ch3_ret_vals['grad'][i]) + ch3_dc[5,0])) / (998.2 * ch3_cp * ch3_dc[9,0]))
        stream['Stream_coeff_v2_2'] = 0
        stream['Stream_coeff_v2_1'] = 0
        stream['Stream_coeff_v1_v2'] = 0
        stream['Stream_coeff_cst'] = (ch3_cond_nwk_ret_vals['grad'][i] * (3600 * ch3_dc[5,0] * ch3_ret_vals['int'][i]) / (998.2 * ch3_cp * ch3_dc[9,0])) + ch3_cond_nwk_ret_vals['int'][i]
        stream['InOut'] = 'out'
        
        streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
                       stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
        streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                              'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
        streams = streams.append(streamdf, ignore_index=True)

        ##Stream --- flowrate to the evaporator network  
        stream = {}                                                                
        stream['Parent'] = 'ch3_' + str(i + 1)
        stream['Type'] = 'flow'
        stream['Name'] = 'ch3_' + str(i + 1) + '_flow_enwk'
        stream['Layer'] = 'chiller_2_e_nwk_flow'
        stream['Stream_coeff_v1_2'] = 0
        stream['Stream_coeff_v1_1'] = 3600 / (998.2 * ch3_cp * ch3_dc[8,0])
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

        ##Stream --- flowrate to the condenser network
        stream = {}                                                                
        stream['Parent'] = 'ch3_' + str(i + 1)
        stream['Type'] = 'flow'
        stream['Name'] = 'ch3_' + str(i + 1) + '_flow_cnwk'
        stream['Layer'] = 'chiller_2_c_nwk_flow'
        stream['Stream_coeff_v1_2'] = 0
        stream['Stream_coeff_v1_1'] = (3600 * ((ch3_dc[5,0] * ch3_ret_vals['grad'][i]) + ch3_dc[5,0])) / (998.2 * ch3_cp * ch3_dc[9,0])
        stream['Stream_coeff_v2_2'] = 0
        stream['Stream_coeff_v2_1'] = 0
        stream['Stream_coeff_v1_v2'] = 0
        stream['Stream_coeff_cst'] = (3600 * ch3_dc[5,0] * ch3_ret_vals['int'][i]) / (998.2 * ch3_cp * ch3_dc[9,0])
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
    eqn['Name'] = 'totaluse_ch3'
    eqn['Type'] = 'unit_binary'
    eqn['Sign'] = 'less_than_equal_to'
    eqn['RHS_value'] = 1
    
    eqninput = [eqn['Name'], eqn['Type'], eqn['Sign'], eqn['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)    

    ##Equation terms 

    for i in range (0, int(ch3_steps)):   
        term = {}
        term['Parent_unit'] = 'ch3_' + str(i + 1)
        term['Parent_eqn'] = 'totaluse_ch3'
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