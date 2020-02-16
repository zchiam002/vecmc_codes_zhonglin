##This script contains helper functions to communicate with the evaporator network model 

##This function converts the decision variables into readable from for the evaporator network model 
def evap_nwk_convert_variables (decision_variables):
    
    ##decision_variables        --- input from the GA level 
    
    evap_nwk_decision_variables = {}
    ##evap_nwk_decision_variables['chiller1_onoff']
    ##evap_nwk_decision_variables['chiller1_flow ']
    ##evap_nwk_decision_variables['chiller1_supply_temperature']
    ##evap_nwk_decision_variables['chiller2_onoff']
    ##evap_nwk_decision_variables['chiller2_flow ']
    ##evap_nwk_decision_variables['chiller2_supply_temperature']    
    ##evap_nwk_decision_variables['chiller3_onoff']
    ##evap_nwk_decision_variables['chiller3_flow ']
    ##evap_nwk_decision_variables['chiller3_supply_temperature']

    evap_nwk_decision_variables['chiller1_onoff'] = decision_variables[2]
    evap_nwk_decision_variables['chiller1_flow'] = decision_variables[3]
    
    chil_ret_temp = decision_variables[0]
    chil_water_range_temp = chil_ret_temp - 274.15
    dt_evap_range_temp = chil_ret_temp - chil_water_range_temp
    dt_real_temp = (decision_variables[4] / 100) * dt_evap_range_temp
    
    evap_nwk_decision_variables['chiller1_supply_temperature'] = dt_real_temp + 273.15
    
    evap_nwk_decision_variables['chiller2_onoff'] = decision_variables[5]
    evap_nwk_decision_variables['chiller2_flow'] = decision_variables[6]    
    
    chil_water_range_temp = chil_ret_temp - 274.15
    dt_evap_range_temp = chil_ret_temp - chil_water_range_temp
    dt_real_temp = (decision_variables[7] / 100) * dt_evap_range_temp
    
    evap_nwk_decision_variables['chiller2_supply_temperature'] = dt_real_temp + 273.15    
    
    evap_nwk_decision_variables['chiller3_onoff'] = decision_variables[8]
    evap_nwk_decision_variables['chiller3_flow'] = decision_variables[9]    
    
    chil_water_range_temp = chil_ret_temp - 274.15
    dt_evap_range_temp = chil_ret_temp - chil_water_range_temp
    dt_real_temp = (decision_variables[10] / 100) * dt_evap_range_temp
    
    evap_nwk_decision_variables['chiller3_supply_temperature'] = dt_real_temp + 273.15    
    
    return evap_nwk_decision_variables

###################################################################################################################################################################################################
##This function takes in the processed chiller decision variables and interacts with the evaporator network model 
def evap_nwk_setup (evap_nwk_decision_variables):
    
    ##evap_nwk_decision_variables['chiller1_onoff']
    ##evap_nwk_decision_variables['chiller1_flow']
    ##evap_nwk_decision_variables['chiller1_supply_temperature']
    ##evap_nwk_decision_variables['chiller2_onoff']
    ##evap_nwk_decision_variables['chiller2_flow']
    ##evap_nwk_decision_variables['chiller2_supply_temperature']    
    ##evap_nwk_decision_variables['chiller3_onoff']
    ##evap_nwk_decision_variables['chiller3_flow']
    ##evap_nwk_decision_variables['chiller3_supply_temperature']
    
    import pandas as pd
    
    ##Organizing the values into the format for the evap_nwk_org model 
    temp_data = [['chiller1_flow', evap_nwk_decision_variables['chiller1_flow']],
                 ['chiller1_supply_temperature', evap_nwk_decision_variables['chiller1_supply_temperature']],
                 ['chiller2_flow', evap_nwk_decision_variables['chiller2_flow']],
                 ['chiller2_supply_temperature', evap_nwk_decision_variables['chiller2_supply_temperature']],  
                 ['chiller3_flow', evap_nwk_decision_variables['chiller3_flow']],
                 ['chiller3_supply_temperature', evap_nwk_decision_variables['chiller3_supply_temperature']]]
    chiller_input = pd.DataFrame(data = temp_data, columns = ['Name', 'Value'])

    chiller_onoff = {}
    chiller_onoff['chiller1_onoff'] = evap_nwk_decision_variables['chiller1_onoff']
    chiller_onoff['chiller2_onoff'] = evap_nwk_decision_variables['chiller2_onoff']
    chiller_onoff['chiller3_onoff'] = evap_nwk_decision_variables['chiller3_onoff']
    
    ##Importing the evaporator network model 
    from evap_nwk_model import evap_nwk_org
    evap_nwk_calculated, evap_nwk_calculated_df = evap_nwk_org(chiller_input, chiller_onoff)
    
    ##Calculating the objective function 
    temp_data = [['evap_pump_1_e_cons', evap_nwk_calculated['Chiller1_evap_pump_elect_cons']],
                 ['evap_pump_2_e_cons', evap_nwk_calculated['Chiller2_evap_pump_elect_cons']],
                 ['evap_pump_3_e_cons', evap_nwk_calculated['Chiller3_evap_pump_elect_cons']]]
    obj_func = pd.DataFrame(data = temp_data, columns = ['Name', 'Value'])
    
    ##Determining the outlet temperature of the evaporator network
    outlet_temperature = evap_nwk_calculated['Exit_temperature']
    
    return obj_func, outlet_temperature



