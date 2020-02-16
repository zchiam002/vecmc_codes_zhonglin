## This is a ser network model, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype_ser_nwk (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type

def ser_nwk (ser_nwk_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    from ser_nwk_compute import ser_nwk_compute
    import pandas as pd
    import numpy as np

    ##This model represents the hsb network model
    
    ##ser_nwk_mdv --- the master decision variables which are used as parameters at this stage 
    ##utilitylist --- a dataframe to hold essential values for writing the MILP script 
    ##streams --- a dataframe to write connections to other units 
    ##cons_eqns --- additional constraints are explicitly stated here 
    ##cons_eqns_terms --- the terms to the constraints 
    
    ##Defining inputs 
    
    ##Processing list of master decision variables
    ser_nwk_steps = ser_nwk_mdv['Value'][0]
    ser_nwk_tf = ser_nwk_mdv['Value'][1]
    ser_nwk_max_flow = ser_nwk_mdv['Value'][1] *0.35                ##This upper bound is needed for the computation of stepwise pressure
                                                                        ##The estimated proportion of cooling consumed by ser 
    ##Defined constants 
    ser_nwk_coeff = 0.000536956604603528
                                                   
    ##Calling a compute file to process dependent values
        ##Placing the values in a numpy array for easy data handling 
    ser_nwk_dc = np.zeros((4,1))
    
    ser_nwk_dc[0,0] = ser_nwk_tf
    ser_nwk_dc[1,0] = ser_nwk_coeff
    ser_nwk_dc[2,0] = ser_nwk_max_flow
    ser_nwk_dc[3,0] = ser_nwk_steps

    ser_nwk_calc = ser_nwk_compute(ser_nwk_dc)
    
#################################################################################################################################################################################################        
    ##Unit definition 
    
    #Network stepwise to calculate the system pressure
    
    for i in range (0, int(ser_nwk_steps)):
        ud = {}
        ud['Name'] = 'ser_nwk_' + str(i + 1)
        ud['Variable1'] = 'm_perc'                                                                        
        ud['Variable2'] = '-'                                                                  
        ud['Fmin_v1'] = ser_nwk_calc['lb'][i]
        ud['Fmax_v1'] = ser_nwk_calc['ub'][i]                                                                                
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
    
    ##Network stepwise 
    for i in range (0, int(ser_nwk_steps)):
        
        ##Stream --- flowrate into the ser network from tro network
        stream = {}                         
        stream['Parent'] = 'ser_nwk_' + str(i + 1)
        stream['Type'] = 'flow'
        stream['Name'] = 'ser_nwk_' + str(i + 1) + '_flow_in'
        stream['Layer'] = 'tro_outlet_flow'
        stream['Stream_coeff_v1_2'] = 0
        stream['Stream_coeff_v1_1'] = ser_nwk_tf
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

        ##Stream --- flowrate from ser network into ser substation
        stream = {}                                                                
        stream['Parent'] = 'ser_nwk_' + str(i + 1)
        stream['Type'] = 'flow'
        stream['Name'] = 'ser_nwk_' + str(i + 1) + '_flow_out'
        stream['Layer'] = 'sernwk2ss_flow'
        stream['Stream_coeff_v1_2'] = 0
        stream['Stream_coeff_v1_1'] = ser_nwk_tf 
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
        
        ##Stream --- pressure from ser network into ser pressure layer
        stream = {}                                                                
        stream['Parent'] = 'ser_nwk_' + str(i + 1)
        stream['Type'] = 'pressure'
        stream['Name'] = 'ser_nwk_' + str(i + 1) + '_delp_out'
        stream['Layer'] = 'ser_consol_delp'
        stream['Stream_coeff_v1_2'] = 0
        stream['Stream_coeff_v1_1'] = ser_nwk_tf  * ser_nwk_calc['grad'][i]
        stream['Stream_coeff_v2_2'] = 0
        stream['Stream_coeff_v2_1'] = 0
        stream['Stream_coeff_v1_v2'] = 0
        stream['Stream_coeff_cst'] = ser_nwk_calc['int'][i]
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
    eqn['Name'] = 'totaluse_ser_nwk'
    eqn['Type'] = 'unit_binary'
    eqn['Sign'] = 'less_than_equal_to'
    eqn['RHS_value'] = 1
    
    eqninput = [eqn['Name'], eqn['Type'], eqn['Sign'], eqn['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)                                                      
    
    ##Equation terms 

    for i in range (0, int(ser_nwk_steps)):   
        term = {}
        term['Parent_unit'] = 'ser_nwk_' + str(i + 1)
        term['Parent_eqn'] = 'totaluse_ser_nwk'
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