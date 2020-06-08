## This is a chiller model, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype_chiller1_evap_4nc (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type

def chiller1_evap_4nc (ch1_4nc_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    from chiller1_evap_4nc_compute import chiller1_evap_4nc_compute
    import pandas as pd
    import numpy as np
    
    ##This is the evaporator side of chiller1_evap_4nc
    
    ##Model description: 
    ##Built based on Gordon-Ng's Universal Chiller model
    ##The COP is kept constant at 4 predefined steps in equally spaced intervals 
    ##The inputs to this function are variables to the eyes of the Master optimizer 
    
    ##ch1_4nc_mdv --- the master decision variables which are used as parameters at this stage 
    ##utilitylist --- a dataframe to hold essential values for writing the MILP script 
    ##streams --- a dataframe to write connections to other units 
    ##cons_eqns --- additional constraints are explicitly stated here 
    ##cons_eqns_terms --- the terms to the constraints 
    
    ##Defining inputs 
    
    ##Processing list of master decision variables
    ch1_4nc_evap_ret_temp = ch1_4nc_mdv['Value'][0]
    ch1_4nc_ctin = ch1_4nc_mdv['Value'][1]
    ch1_4nc_tenwkflow = ch1_4nc_mdv['Value'][2]                     ##Total flowrate through all evaporators of all chillers  
    ch1_4nc_steps = ch1_4nc_mdv['Value'][3]                         ##The number of piecewise linear pieces
    
    ##Defined constants 
    ch1_4nc_rated_cap = 2000
    ch1_4nc_b0 = 0.123020043325872
    ch1_4nc_b1 = 1044.79734873891
    ch1_4nc_b2 = 0.0204660495029597
    ch1_4nc_qc_coeff = 1.09866273284186
    ch1_4nc_cp = 4.2
    ch1_4nc_min_flow = 0.5 * 218.3903135                            ##This is to ensure that the minimum flowrate through the evaporator is at least half that oc manufacturer's specifications
    
    ##Calling a compute file to process dependent values
        ##Placing the values in a numpy array for easy data handling 
    ch1_4nc_dc = np.zeros((9, 1))
    ch1_4nc_dc[0,0] = ch1_4nc_evap_ret_temp
    ch1_4nc_dc[1,0] = ch1_4nc_ctin
    ch1_4nc_dc[2,0] = ch1_4nc_rated_cap
    ch1_4nc_dc[3,0] = ch1_4nc_b0
    ch1_4nc_dc[4,0] = ch1_4nc_b1
    ch1_4nc_dc[5,0] = ch1_4nc_b2
    ch1_4nc_dc[6,0] = ch1_4nc_qc_coeff
    ch1_4nc_dc[7,0] = ch1_4nc_tenwkflow
    ch1_4nc_dc[8,0] = ch1_4nc_steps
    
    ch1_4nc_ret_vals = chiller1_evap_4nc_compute(ch1_4nc_dc)
    
#################################################################################################################################################################################################        
    ##Unit definition 
    
    ##Evaporator stepwise
    for i in range (0, int(ch1_4nc_steps)):
        ud = {}
        ud['Name'] = 'ch1_4nc_' + str(i + 1) + '_evap'
        ud['Variable1'] = 'm_perc'                                                                                      ##Percentage of flowrate from the entire evaporator network 
        ud['Variable2'] = 't_out'                                                                                       ##Chilled water setpoint temperature 
        ud['Fmin_v1'] = 0
        ud['Fmax_v1'] = 1                                                                                               ##Maximum percentage is 100% 
        ud['Fmin_v2'] = 0                                                                                               ##The minimum supply temperature of the chiller is 1 deg 
        ud['Fmax_v2'] = 1                                                                                               ##The maximum supply temperature of the chiller is that of the return temperature
        ud['Coeff_v1_2'] = 0                                                                                            ##This illustrates the relationship between the variables  
        ud['Coeff_v1_1'] = ((ch1_4nc_tenwkflow * ch1_4nc_cp * 998.2 * (ch1_4nc_evap_ret_temp - 273.15 - 1) / 3600))     ##The relationship is Qe = m_evap_perc*m_total*Cp*Tevap_in - m_evap_perc*m_total*Cp*Tevap_out
        ud['Coeff_v2_2'] = 0
        ud['Coeff_v2_1'] = 0
        ud['Coeff_v1_v2'] = -((ch1_4nc_tenwkflow * ch1_4nc_cp * 998.2 * (ch1_4nc_evap_ret_temp - 273.15 - 1)/ 3600)) 
        ud['Coeff_cst'] = 0
        ud['Fmin'] = ch1_4nc_ret_vals['lb'][i] * ch1_4nc_rated_cap
        ud['Fmax'] = ch1_4nc_ret_vals['ub'][i] * ch1_4nc_rated_cap
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
        ud['Power_v1_1'] = (ch1_4nc_ret_vals['grad'][i] * ch1_4nc_tenwkflow * 4.2 * (ch1_4nc_evap_ret_temp - 273.15 - 1) * 998.2 / 3600)
        ud['Power_v2_2'] = 0
        ud['Power_v2_1'] = 0
        ud['Power_v1_v2'] = -(ch1_4nc_ret_vals['grad'][i] * ch1_4nc_tenwkflow * 4.2 * (ch1_4nc_evap_ret_temp - 273.15 - 1) * 998.2 / 3600)
        ud['Power_cst'] = ch1_4nc_ret_vals['int'][i]
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
    for i in range (0, int(ch1_4nc_steps)):
        
        ##Stream --- temperature 
        stream = {}                         
        stream['Parent'] = 'ch1_4nc_' + str(i + 1) + '_evap'
        stream['Type'] = 'temp_chil'
        stream['Name'] = 'ch1_4nc_' + str(i + 1) + '_evap_tout'
        stream['Layer'] = 'chil2sp1_temp'
        stream['Stream_coeff_v1_2'] = 0
        stream['Stream_coeff_v1_1'] = (273.15 + 1)
        stream['Stream_coeff_v2_2'] = 0
        stream['Stream_coeff_v2_1'] = 0
        stream['Stream_coeff_v1_v2'] = (ch1_4nc_evap_ret_temp - 273.15 - 1)
        stream['Stream_coeff_cst'] = 0
        stream['InOut'] = 'out'
        
        streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
                       stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
        streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                              'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
        streams = streams.append(streamdf, ignore_index=True)

        ##Stream --- flowrate 
        stream = {}                                                                
        stream['Parent'] = 'ch1_4nc_' + str(i + 1) + '_evap'
        stream['Type'] = 'flow'
        stream['Name'] = 'ch1_4nc_' + str(i + 1) + '_evap_mfout'
        stream['Layer'] = 'ch1_2_ch1evapnwk_flow'
        stream['Stream_coeff_v1_2'] = 0
        stream['Stream_coeff_v1_1'] = ch1_4nc_tenwkflow 
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
    eqn['Name'] = 'totaluse_ch1_e_4nc'
    eqn['Type'] = 'unit_binary'
    eqn['Sign'] = 'less_than_equal_to'
    eqn['RHS_value'] = 1
    
    eqninput = [eqn['Name'], eqn['Type'], eqn['Sign'], eqn['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)    

    eqn = {}
    eqn['Name'] = 'ch1_e_4nc_flow_min'
    eqn['Type'] = 'stream_limit_modified'                                      
    eqn['Sign'] = 'greater_than_equal_to'                                    
    eqn['RHS_value'] = 0
    
    eqninput = [eqn['Name'], eqn['Type'], eqn['Sign'], eqn['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)                                                          
    
    ##Equation terms 

    for i in range (0, int(ch1_4nc_steps)):   
        term = {}
        term['Parent_unit'] = 'ch1_4nc_' + str(i + 1) + '_evap'
        term['Parent_eqn'] = 'totaluse_ch1_e_4nc'
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
        term['Parent_unit'] = 'ch1_4nc_' + str(i + 1) + '_evap'
        term['Parent_eqn'] = 'ch1_e_4nc_flow_min'
        term['Parent_stream'] = '-'                                    ##Only applicable for stream_limit types 
        term['Coefficient'] = 0
        term['Coeff_v1_2'] = 0                                         ##Only applicable for stream_limit_modified types 
        term['Coeff_v1_1'] = ch1_4nc_tenwkflow
        term['Coeff_v2_2'] = 0
        term['Coeff_v2_1'] = 0
        term['Coeff_v1_v2'] = 0
        term['Coeff_cst'] = -ch1_4nc_min_flow
    
        terminput = [term['Parent_unit'], term['Parent_eqn'], term['Parent_stream'], term['Coefficient'], term['Coeff_v1_2'],
                     term['Coeff_v1_1'], term['Coeff_v2_2'], term['Coeff_v2_1'], term['Coeff_v1_v2'], term['Coeff_cst']]
        terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                                  'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2',
                                                                  'Coeff_cst'])
        cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True) 

    return utilitylist, streams, cons_eqns, cons_eqns_terms    