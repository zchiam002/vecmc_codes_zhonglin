##This script consolidates the models for the Genetic Algorithm
##It takes in decision variables and outputs the objective function value 

def overall_model (decision_variables):
    
    import pandas as pd 
    import os
    
    ##decision_variables --- an array of decision_variables
    
        ##Chiller related 
            ##decision_variables[0]     ---      chiller_evap_return_temperature (K)
            ##decision_variables[1]     ---      chiller_cond_inlet_temperature (range)
            ##decision_variables[2]     ---      chiller1_onoff (binary)
            ##decision_variables[3]     ---      chiller1_mevap (m3/h)
            ##decision_variables[4]     ---      chiller1_evap_delt (range)
            ##decision_variables[5]     ---      chiller2_onoff (binary)
            ##decision_variables[6]     ---      chiller2_mevap (m3/h)
            ##decision_variables[7]     ---      chiller2_evap_delt (range)
            ##decision_variables[8]     ---      chiller3_onoff (binary)
            ##decision_variables[9]     ---      chiller3_mevap (m3/h)
            ##decision_variables[10]    ---      chiller3_evap_delt (range)
       
        ##Distribution network related 
            ##decision_variables[11]    ---      dist_nwk_cp_split (range)
            ##decision_variables[12]    ---      dist_nwk_pump_select (discrete 0-7)
            ##decision_variables[13]    ---      dist_nwk_gv2_split_perc (range)  
            ##decision_variables[14]    ---      dist_nwk_hsb_split_perc (range)  
            ##decision_variables[15]    ---      dist_nwk_pfa_split_perc (range)
            ##decision_variables[16]    ---      dist_nwk_ser_split_perc (range)
            
        ##Cooling tower related
            ##decision_variables[17]    ---      cooling_tower_1_air (range)
            ##decision_variables[18]    ---      cooling_tower_2_air (range)
            ##decision_variables[19]    ---      cooling_tower_3_air (range)
            ##decision_variables[20]    ---      cooling_tower_4_air (range)
            ##decision_variables[21]    ---      cooling_tower_5_air (range)                                                                     
        
    ##Importing the weather conditions and raw data 
    load_type = 'high'
    hour_of_the_day = 0
    
        ##Determine the current path directory 
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'
    
    print(current_path)
    
        ##Determine the directory of the input data 
    input_data_dir = current_path + 'input_data\\paper_ga_only_case_input_data\\' + load_type + '_load\\' + str(load_type) + '_demand_' + str(hour_of_the_day) + '.csv'
    input_weather_conditions_dir = current_path + 'input_data\\paper_ga_only_case_input_data\\' + load_type + '_load\\' + str(load_type) + '_demand_weather' + '.csv'
    
    demand_data = pd.read_csv(input_data_dir)
    weather_data = pd.read_csv(input_weather_conditions_dir)
    
        ##Extracting the relevant wet-bulb temperature 
    twb = weather_data['T_WB'][hour_of_the_day]
    
    ##Determining the flowrate in the condenser network 
    total_cond_flow = 0
    if decision_variables[2] == 1:
        total_cond_flow = total_cond_flow + 407
    if decision_variables[5] == 1:
        total_cond_flow = total_cond_flow + 1476    
    if decision_variables[8] == 1:
        total_cond_flow = total_cond_flow + 1476   
        
    ##The maximum temperature difference for each of the substations 
    max_delt_substation = {}
    max_delt_substation['gv2_delt_max'] = 5
    max_delt_substation['hsb_delt_max'] = 10
    max_delt_substation['pfa_delt_max'] = 7
    max_delt_substation['ser_delt_max'] = 7    
    

    ##Calculating the electricity consumed by the chillers
    from chiller_setup import chiller_convert_variables
    chiller_decision_variables = chiller_convert_variables (decision_variables, twb)
    from chiller_setup import chiller_setup 
    chiller_obj_func, chiller_t_out_cond, chiller_load_violation = chiller_setup (chiller_decision_variables)

    ##Calculating the electricity consumed by the evaporator pumps 
    from evap_nwk_setup import evap_nwk_convert_variables
    evap_nwk_decision_variables = evap_nwk_convert_variables (decision_variables)
    from evap_nwk_setup import evap_nwk_setup
    evap_nwk_obj_func, evap_nwk_outlet_temperature = evap_nwk_setup (evap_nwk_decision_variables)

    ##Calculating the electricity consumed by the distribution network 
    from dist_nwk_setup import dist_nwk_convert_variables
    dist_nwk_decision_variables, consumer_demand, outputs_from_other_models = dist_nwk_convert_variables (decision_variables, demand_data, evap_nwk_outlet_temperature)
    from dist_nwk_setup import dist_nwk_setup
    dist_nwk_obj_func, dist_nwk_outlet_temperature, customer_delts, dist_nwk_flow_violation = dist_nwk_setup (dist_nwk_decision_variables, consumer_demand, 
                                                                                                              outputs_from_other_models)
    
    ##Calculating the electricity consumed by the condenser pumps 
    from cond_nwk_setup import cond_nwk_convert_variables
    cond_nwk_decision_variables = cond_nwk_convert_variables (decision_variables, twb, chiller_t_out_cond)
    from cond_nwk_setup import cond_nwk_setup
    cond_nwk_obj_func, cond_nwk_outlet_temperature = cond_nwk_setup (cond_nwk_decision_variables)
    
    ##Calculating the electricity consumed by the cooling towers 
    from cooling_tower_setup import cooling_tower_convert_variables
    cooling_tower_decision_variables = cooling_tower_convert_variables (decision_variables, twb, total_cond_flow, cond_nwk_outlet_temperature)
    from cooling_tower_setup import cooling_tower_setup
    cooling_tower_obj_func, ct_delt = cooling_tower_setup (cooling_tower_decision_variables)
    
    ##A function to consolidate the objective functions as well as to check if the constraints are violated.
    from auxillary_functions import calc_obj_func
    obj_function_value = calc_obj_func (chiller_obj_func, evap_nwk_obj_func, dist_nwk_obj_func, cond_nwk_obj_func, cooling_tower_obj_func, chiller_load_violation, dist_nwk_flow_violation)
    
    ##A function to check if the temperature difference at the substations exceed the threshold values.
    from auxillary_functions import check_delt_substation
    obj_function_value = check_delt_substation (obj_function_value, customer_delts, max_delt_substation)
    
    ##A function to check the temperature differences on the condenser and evaporator sides 
    from auxillary_functions import check_balance_temperature_balance
    obj_function_value = check_balance_temperature_balance (obj_function_value , decision_variables, dist_nwk_outlet_temperature, ct_delt, twb, cond_nwk_outlet_temperature)
    
    
    return obj_function_value 


    
    