## This is the hsb substation model, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    
def checktype_hsb_substation (unit_type):                  ##Input the unit type here

    ##unit_type     --- a variable to store the type of unit

    unit_type = 'utility'
    
    return unit_type
 
##Model description 
    ##This is the hsb substation model, it treats the demand as a parameter and outputs a tout    
def hsb_substation (mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):

    ##mdv               --- the associated decision variables from the GA, or parameters 
    ##utilitylist       --- a dataframe to extract general information from the model 
    ##streams           --- a dataframe to extract stream information from the model 
    ##cons_eqns         --- a dataframe to extract constraint equations from the model 
    ##cons_eqns_terms   --- a dataframe to extract terms in the constraint equation from the model 

    import os 
    current_path = os.path.dirname(__file__)[:-12] + '//'   
    from hsb_substation_compute import hsb_substation_compute
    import pandas as pd
    import numpy as np 
    
    ##Defining inputs 
   
    ##Importing local MILP model parameters 
    add_param = pd.read_csv(current_path + 'model_param//model_param.csv')
    
    ##Processing list of master decision variables/inputs as parameters 
    hsb_ss_demand = mdv['Value'][0]
    hsb_ss_totalflownwk = mdv['Value'][1]

    ##Defined constants
    hsb_ss_tinmax  = add_param['Value'][0]                                              ##The maximum temperature of water entering the substation 
    hsb_ss_deltmax  = 10                                                                ##The maximum delta t of the substation on the cold side  (value based on hsb)
    hsb_ss_cp = 4.2                                                                     ##The heat capacity of water 

    ##Dependent constants 
    hsb_ss_dc = np.zeros((5,1))                                                         ##Initialize the list, note the number of constants 
    
    hsb_ss_dc[0,0] = hsb_ss_demand
    hsb_ss_dc[1,0] = hsb_ss_totalflownwk
    hsb_ss_dc[2,0] = hsb_ss_cp
    hsb_ss_dc[3,0] = hsb_ss_tinmax
    hsb_ss_dc[4,0] = hsb_ss_deltmax

    hsb_ss_calc = hsb_substation_compute(hsb_ss_dc)
    
    hsb_ss_temp_exit_cst = hsb_ss_calc[0,0]                                             ##The constant term for the exit temperature stream 
    hsb_ss_constraint_eqn_coeff = hsb_ss_calc[1,0]                                      ##The constraint coefficient term to ensure that the delta t of the hx on the cold side does not exceed max delta t

#################################################################################################################################################################################################    
    ##Unit definition
    
    ##Unit 1
    ud = {}
    ud['Name'] = 'hsb_ss'
    ud['Variable1'] = 'm_perc'                                                          ##The percentage of the total flowrate into the system                                                                                                     
    ud['Variable2'] = 't_in'                                                            ##Temperature of fluid entering the substation                                                              
    ud['Fmin_v1'] = 0
    ud['Fmax_v1'] = 1                                                                                                                   
    ud['Fmin_v2'] = 0                                                                                                           
    ud['Fmax_v2'] = 1                                                                                  
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
    ##Layer and stream definition 

    ##Stream 1
    stream = {}                                                                
    stream['Parent'] = 'hsb_ss'                                                        ##Temperature stream entering the substation 
    stream['Type'] = 'temp_chil'
    stream['Name'] = 'hsb_ss_tin'
    stream['Layer'] = 'sp12hsb_temp'
    stream['Stream_coeff_v1_2'] = 0
    stream['Stream_coeff_v1_1'] = 0
    stream['Stream_coeff_v2_2'] = 0
    stream['Stream_coeff_v2_1'] = (hsb_ss_tinmax - 273.15 - 1)
    stream['Stream_coeff_v1_v2'] = 0
    stream['Stream_coeff_cst'] = 273.15 + 1
    stream['InOut'] = 'in'
    
    streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
                   stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 2
    stream = {}                                                                
    stream['Parent'] = 'hsb_ss'                                                         ##Flowrate stream entering the substation 
    stream['Type'] = 'flow'
    stream['Name'] = 'hsb_ss_mfin'
    stream['Layer'] = 'hsbnwk2ss_flow'
    stream['Stream_coeff_v1_2'] = 0
    stream['Stream_coeff_v1_1'] = hsb_ss_totalflownwk 
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
    
    ##Stream 3
    stream = {}                                                                
    stream['Parent'] = 'hsb_ss'                                                        ##Temperture stream exiting the substation 
    stream['Type'] = 'temp_chil'
    stream['Name'] = 'hsb_ss_tout'
    stream['Layer'] = 'sp22chilret_temp'
    stream['Stream_coeff_v1_2'] = 0
    stream['Stream_coeff_v1_1'] = (273.15 + 1) 
    stream['Stream_coeff_v2_2'] = 0
    stream['Stream_coeff_v2_1'] = 0
    stream['Stream_coeff_v1_v2'] = (hsb_ss_tinmax - 273.15 - 1)
    stream['Stream_coeff_cst'] = hsb_ss_temp_exit_cst
    stream['InOut'] = 'out'
    
    streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
                   stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True) 
    
    ##Stream 4
    stream = {}                                                                
    stream['Parent'] = 'hsb_ss'                                                        ##Flowrate out to the distribution pump
    stream['Type'] = 'flow'
    stream['Name'] = 'hsb_ss_flow_out'
    stream['Layer'] = 'distnwk_consol_flow'
    stream['Stream_coeff_v1_2'] = 0
    stream['Stream_coeff_v1_1'] = hsb_ss_totalflownwk  
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
    
####################################################################################################################################################################################################        
    ##Constraint definition
    
    ##Equation definitions
    
    ##Equation 1
    eqn = {}
    eqn['Name'] = 'hsb_ss_tout_max'
    eqn['Type'] = 'stream_limit_modified'                                              ##Stream modified constraints involving more than 1 variable which cannot be expressed easily
    eqn['Sign'] = 'greater_than_equal_to'                                              ##Due to reciprocal less than equals to becomes greater than equals to, as both are positive
    eqn['RHS_value'] = 0
    
    eqninput = [eqn['Name'], eqn['Type'], eqn['Sign'], eqn['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation terms
    
    ##Term 1
    term = {}
    term['Parent_unit'] = 'hsb_ss'
    term['Parent_eqn'] = 'hsb_ss_tout_max'
    term['Parent_stream'] = '-'                                                       ##Only applicable for stream_limit types 
    term['Coefficient'] = 0
    term['Coeff_v1_2'] = 0                                                            ##Only applicable for stream_limit_modified types 
    term['Coeff_v1_1'] = hsb_ss_constraint_eqn_coeff
    term['Coeff_v2_2'] = 0
    term['Coeff_v2_1'] = 0
    term['Coeff_v1_v2'] = 0
    term['Coeff_cst'] = -(1 / hsb_ss_deltmax)
    

    terminput = [term['Parent_unit'], term['Parent_eqn'], term['Parent_stream'], term['Coefficient'], term['Coeff_v1_2'],
                 term['Coeff_v1_1'], term['Coeff_v2_2'], term['Coeff_v2_1'], term['Coeff_v1_v2'], term['Coeff_cst']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 
                                                              'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2',
                                                              'Coeff_cst'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms    