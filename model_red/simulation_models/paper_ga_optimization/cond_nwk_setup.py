##This script contains helper functions to communicate with the condenser network model 


##This function converts the decision variables into readable form for the condenser network model 
def cond_nwk_convert_variables (decision_variables, twb, cond_ret_temp):
    
    ##decision_variables        --- input from the GA level 
    
    cond_nwk_decision_variables = {}
    ##cond_nwk_decision_variables['chiller1_onoff']
    ##cond_nwk_decision_variables['chiller1_flow']
    ##cond_nwk_decision_variables['chiller1_cond_return_temperature']
    ##cond_nwk_decision_variables['chiller2_onoff']
    ##cond_nwk_decision_variables['chiller2_flow']
    ##cond_nwk_decision_variables['chiller2_cond_return_temperature']    
    ##cond_nwk_decision_variables['chiller3_onoff']
    ##cond_nwk_decision_variables['chiller3_flow']
    ##cond_nwk_decision_variables['chiller3_cond_return_temperature']
    ##cond_nwk_decision_variables['cp_dist_nwk_split']    

    cond_nwk_decision_variables['chiller1_onoff'] = decision_variables[2]
    
    if cond_nwk_decision_variables['chiller1_onoff'] == 1:
        cond_nwk_decision_variables['chiller1_flow'] = 407
    else:
        cond_nwk_decision_variables['chiller1_flow'] = 0
        
    cond_nwk_decision_variables['chiller1_cond_return_temperature'] = cond_ret_temp['Value'][0]

    
    cond_nwk_decision_variables['chiller2_onoff'] = decision_variables[5]
    
    if cond_nwk_decision_variables['chiller2_onoff'] == 1:
        cond_nwk_decision_variables['chiller2_flow'] = 1476
    else:
        cond_nwk_decision_variables['chiller2_flow'] = 0
        
    cond_nwk_decision_variables['chiller2_cond_return_temperature'] = cond_ret_temp['Value'][1]    

    
    cond_nwk_decision_variables['chiller3_onoff'] = decision_variables[8]
    
    if cond_nwk_decision_variables['chiller3_onoff'] == 1:
        cond_nwk_decision_variables['chiller3_flow'] = 1476   
    else:
        cond_nwk_decision_variables['chiller3_flow'] = 0
        
    cond_nwk_decision_variables['chiller3_cond_return_temperature'] = cond_ret_temp['Value'][2]   

    cond_nwk_decision_variables['cp_dist_nwk_split'] = (decision_variables[11] / 100)
    
    
    return cond_nwk_decision_variables

###################################################################################################################################################################################################
##This function takes in the processed chiller decision variables and interacts with the condenser network model 
def cond_nwk_setup (cond_nwk_decision_variables):
    
    ##cond_nwk_decision_variables['chiller1_onoff']
    ##cond_nwk_decision_variables['chiller1_flow']
    ##cond_nwk_decision_variables['chiller1_cond_return_temperature']
    ##cond_nwk_decision_variables['chiller2_onoff']
    ##cond_nwk_decision_variables['chiller2_flow']
    ##cond_nwk_decision_variables['chiller2_cond_return_temperature']    
    ##cond_nwk_decision_variables['chiller3_onoff']
    ##cond_nwk_decision_variables['chiller3_flow']
    ##cond_nwk_decision_variables['chiller3_cond_return_temperature']
    ##cond_nwk_decision_variables['cp_dist_nwk_split']
    
    import pandas as pd
    
    ##Organizing the values into the format for the cond_nwk_org model 
    temp_data = [['chiller1_flow', cond_nwk_decision_variables['chiller1_flow']],
                 ['chiller1_cond_return_temperature', cond_nwk_decision_variables['chiller1_cond_return_temperature']],
                 ['chiller2_flow', cond_nwk_decision_variables['chiller2_flow']],
                 ['chiller2_cond_return_temperature', cond_nwk_decision_variables['chiller2_cond_return_temperature']],  
                 ['chiller3_flow', cond_nwk_decision_variables['chiller3_flow']],
                 ['chiller3_cond_return_temperature', cond_nwk_decision_variables['chiller3_cond_return_temperature']]]
    chiller_input = pd.DataFrame(data = temp_data, columns = ['Name', 'Value'])

    chiller_onoff = {}
    chiller_onoff['chiller1_onoff'] = cond_nwk_decision_variables['chiller1_onoff']
    chiller_onoff['chiller2_onoff'] = cond_nwk_decision_variables['chiller2_onoff']
    chiller_onoff['chiller3_onoff'] = cond_nwk_decision_variables['chiller3_onoff']
    
    ##Importing the condenser network model 
    from cond_nwk_model import cond_nwk_org
    cond_nwk_calculated, cond_nwk_calculated_df = cond_nwk_org(chiller_input, chiller_onoff)
    
    ##Calculating the objective function 
    temp_data = [['cond_pump_1_e_cons', cond_nwk_calculated['Chiller1_cond_pump_elect_cons']],
                 ['cond_pump_2_e_cons', cond_nwk_calculated['Chiller2_cond_pump_elect_cons']],
                 ['cond_pump_3_e_cons', cond_nwk_calculated['Chiller3_cond_pump_elect_cons']]]
    obj_func = pd.DataFrame(data = temp_data, columns = ['Name', 'Value'])

    ##Determining the outlet temperature of the evaporator network
    outlet_temperature = cond_nwk_calculated['Exit_temperature']
    
    return obj_func, outlet_temperature
