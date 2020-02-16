## This is a chiller3 evaporator network model, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype_chiller3_evap_nwk (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type

def chiller3_evap_nwk (ch3_enwk_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    from chiller3_evap_nwk_compute import chiller3_evap_nwk_compute
    import pandas as pd
    import numpy as np

    ##This model represents the part of the evaportor network responsible for computing the pressure drop faced by chiller 3 evaporator pump
    
    ##ch3_enwk_mdv --- the master decision variables which are used as parameters at this stage 
    ##utilitylist --- a dataframe to hold essential values for writing the MILP script 
    ##streams --- a dataframe to write connections to other units 
    ##cons_eqns --- additional constraints are explicitly stated here 
    ##cons_eqns_terms --- the terms to the constraints 
    
    ##Defining inputs 
    
    ##Processing list of master decision variables
    ch3_enwk_steps = ch3_enwk_mdv['Value'][0]
    ch3_enwk_tf = ch3_enwk_mdv['Value'][1]
    
    ##Defined constants 
    ch3_enwk_coeff = 3.07492E-05
    ch3_enwk_com_coeff = 1.66667E-05
    ch3_enwk_max_flow = 1000                    ##This upper bound is needed for the computation of stepwise pressure
                                                   
    ##Calling a compute file to process dependent values
        ##Placing the values in a numpy array for easy data handling 
    ch3_enwk_dc = np.zeros((5,1))
    
    ch3_enwk_dc[0,0] = ch3_enwk_tf
    ch3_enwk_dc[1,0] = ch3_enwk_coeff
    ch3_enwk_dc[2,0] = ch3_enwk_com_coeff
    ch3_enwk_dc[3,0] = ch3_enwk_max_flow
    ch3_enwk_dc[4,0] = ch3_enwk_steps

    ch3_enwk_calc = chiller3_evap_nwk_compute(ch3_enwk_dc)
    
#################################################################################################################################################################################################        
    ##Unit definition 
    
    ##Evaporator network stepwise to calculate the system pressure
    
    for i in range (0, int(ch3_enwk_steps)):
        ud = {}
        ud['Name'] = 'ch3_enwk_' + str(i + 1)
        ud['Variable1'] = 'm_perc'                                                                        
        ud['Variable2'] = '-'                                                                  
        ud['Fmin_v1'] = ch3_enwk_calc['lb'][i]
        ud['Fmax_v1'] = ch3_enwk_calc['ub'][i]                                                                                
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
        utilitylist = utilitylist.append(unitdf, ignore_index=True)   
        
####################################################################################################################################################################################################        
    ##Stream definition 
    
    ##Evaporator network stepwise 
    for i in range (0, int(ch3_enwk_steps)):
        
        ##Stream --- flowrate into the chiller 3 evaporator network from chiller 3 
        stream = {}                         
        stream['Parent'] = 'ch3_enwk_' + str(i + 1)
        stream['Type'] = 'flow'
        stream['Name'] = 'ch3_enwk_' + str(i + 1) + '_flow_in'
        stream['Layer'] = 'ch3_2_ch3evapnwk_flow'
        stream['Stream_coeff_v1_2'] = 0
        stream['Stream_coeff_v1_1'] = ch3_enwk_tf
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

        ##Stream --- flowrate from chiller 3 evaporator network to chiller 3 evaporator pump
        stream = {}                                                                
        stream['Parent'] = 'ch3_enwk_' + str(i + 1)
        stream['Type'] = 'flow'
        stream['Name'] = 'ch3_enwk_' + str(i + 1) + '_flow_out'
        stream['Layer'] = 'ch3evapnwk_2_ch3pump_flow'
        stream['Stream_coeff_v1_2'] = 0
        stream['Stream_coeff_v1_1'] = ch3_enwk_tf 
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
        
        ##Stream --- pressure flow from chiller 3 evaporator network to chiller 3 evaporator pump
        stream = {}                                                                
        stream['Parent'] = 'ch3_enwk_' + str(i + 1)
        stream['Type'] = 'pressure'
        stream['Name'] = 'ch3_enwk_' + str(i + 1) + '_delp_out'
        stream['Layer'] = 'ch3evapnwk_2_ch3pump_delp'
        stream['Stream_coeff_v1_2'] = 0
        stream['Stream_coeff_v1_1'] = ch3_enwk_tf  * ch3_enwk_calc['grad'][i]
        stream['Stream_coeff_v2_2'] = 0
        stream['Stream_coeff_v2_1'] = 0
        stream['Stream_coeff_v1_v2'] = 0
        stream['Stream_coeff_cst'] = ch3_enwk_calc['int'][i]
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
    eqn['Name'] = 'totaluse_ch3_enwk'
    eqn['Type'] = 'unit_binary'
    eqn['Sign'] = 'less_than_equal_to'
    eqn['RHS_value'] = 1
    
    eqninput = [eqn['Name'], eqn['Type'], eqn['Sign'], eqn['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)                                                      
    
    ##Equation terms 

    for i in range (0, int(ch3_enwk_steps)):   
        term = {}
        term['Parent_unit'] = 'ch3_enwk_' + str(i + 1)
        term['Parent_eqn'] = 'totaluse_ch3_enwk'
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