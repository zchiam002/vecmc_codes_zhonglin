##This function takes in the parameters and master decison variable and writes them in a slave readable form 

def convert_mdv_to_slave_param (thread_number, mdv_list, var, weather, demand, nwk_choice, piecewise_steps):
    import sys
    sys.path.append('C:\\Optimization_zlc\\master_level\\auxillary\\')
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\slave_convex_v1\\look_up_tables\\')
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\slave_convex_v1\\prep_functions\\')
    import os.path
    from prepare_slave_param_csv_vtest2 import prepare_slave_param_csv_vtest2    #Needs modification
    import pandas as pd
    
    ##thread_number --- the thread number for coding output files
    ##mdv_list --- the list of master decision variables with their bounds
    ##var --- variable values from the master decision 
    ##weather --- weather data 
    ##demand --- the demand of the substations
    
    ##The final csv location 
    csv_save_loc = 'C:\\Optimization_zlc\\slave_convex_handlers\\master_values\\'
    csv_save_name = 'master_slave_var_list_' + str(thread_number) + '.csv'
    csv_final_save = csv_save_loc + csv_save_name

    ##Checking if there are similar files with the same name, and removing if there is     
    exist_result = os.path.exists(csv_final_save)
    if exist_result == True:
        os.remove(csv_final_save)
    
    ##Preparing values which need to be read off csv files 
    dist_pump_lincoeff = pd.read_csv('C:\\Optimization_zlc\\master_level_models\\slave_convex_v1\\look_up_tables\\dist_pump_lincoeff.csv')
    evap_cond_pump_lincoeff = pd.read_csv('C:\\Optimization_zlc\\master_level_models\\slave_convex_v1\\look_up_tables\\evap_cond_pump_lincoeff.csv')
    
    
    ##Convert the var choices into the corresponding values for writing the slave csv file
    ##Dealing with discretized values 
    var_converted = []
    chiller_evap_return_temp = ((var[0] / mdv_list['Steps'][0]) * (mdv_list['UB'][0] - mdv_list['LB'][0])) + mdv_list['LB'][0]
    var_converted.append(chiller_evap_return_temp)
    chiller_cond_entry_temp = ((var[1] / mdv_list['Steps'][1]) * (mdv_list['UB'][1] - mdv_list['LB'][1])) + mdv_list['LB'][1]
    var_converted.append(chiller_cond_entry_temp)                            
    total_evap_nwk_flowrate = ((var[2] / mdv_list['Steps'][2]) * (mdv_list['UB'][2] - mdv_list['LB'][2])) + mdv_list['LB'][2]
    var_converted.append(total_evap_nwk_flowrate)                                 
    total_cond_nwk_flowrate = ((var[3] / mdv_list['Steps'][3]) * (mdv_list['UB'][3] - mdv_list['LB'][3])) + mdv_list['LB'][3]
    var_converted.append(total_cond_nwk_flowrate)
    
    ##Dealing with distribution network mapping 
    dist_pump_1 = [dist_pump_lincoeff['p1_m_coeff'][var[4]], dist_pump_lincoeff['p1_p_coeff'][var[4]], dist_pump_lincoeff['p1_cst'][var[4]], dist_pump_lincoeff['p1_max_m'][var[4]]]
    dist_pump_2 = [dist_pump_lincoeff['p2_m_coeff'][var[4]], dist_pump_lincoeff['p2_p_coeff'][var[4]], dist_pump_lincoeff['p2_cst'][var[4]], dist_pump_lincoeff['p2_max_m'][var[4]]]
    dist_pump_3 = [dist_pump_lincoeff['p3_m_coeff'][var[4]], dist_pump_lincoeff['p3_p_coeff'][var[4]], dist_pump_lincoeff['p3_cst'][var[4]], dist_pump_lincoeff['p3_max_m'][var[4]]]

    ##Putting the values into a dataframe
    mdv_slave_param = prepare_slave_param_csv_vtest2(var_converted, evap_cond_pump_lincoeff, dist_pump_1, dist_pump_2, dist_pump_3, weather, demand, nwk_choice, piecewise_steps)

    mdv_slave_param.to_csv(csv_final_save)
    
    return var_converted

##This function writes the parameters for the slave solver 
def convert_mdv_to_slave_param_v2 (thread_number, var, weather, demand, nwk_choice,  piecewise_steps):
    
    import sys
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\slave_convex_v1\\look_up_tables\\')
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\slave_convex_v1\\prep_functions\\')
    import os.path
    from prepare_slave_param_csv_vtest2 import prepare_slave_param_csv_vtest2    #Needs modification
    import pandas as pd    
    
    ##thread_number --- the thread number for coding output files
    ##mdv_list --- the list of master decision variables with their bounds
    ##var --- variable values from the master decision 
    ##weather --- weather data 
    ##demand --- the demand of the substations
    ##piecewise_steps --- the number of piecewise_steps 
    
    ##The final csv location 
    csv_save_loc = 'C:\\Optimization_zlc\\slave_convex_handlers\\master_values\\'
    csv_save_name = 'master_slave_var_list_' + str(thread_number) + '.csv'
    csv_final_save = csv_save_loc + csv_save_name

    ##Checking if there are similar files with the same name, and removing if there is     
    exist_result = os.path.exists(csv_final_save)
    if exist_result == True:
        os.remove(csv_final_save)
    
    ##Preparing values which need to be read off csv files 
    dist_pump_lincoeff = pd.read_csv('C:\\Optimization_zlc\\master_level_models\\slave_convex_v1\\look_up_tables\\dist_pump_lincoeff.csv')
    evap_cond_pump_lincoeff = pd.read_csv('C:\\Optimization_zlc\\master_level_models\\slave_convex_v1\\look_up_tables\\evap_cond_pump_lincoeff.csv')    
    
    ##Dealing with distribution network mapping 
    dist_pump_1 = 0#[dist_pump_lincoeff['p1_m_coeff'][var[4]], dist_pump_lincoeff['p1_p_coeff'][var[4]], dist_pump_lincoeff['p1_cst'][var[4]], dist_pump_lincoeff['p1_max_m'][var[4]]]
    dist_pump_2 = 0#[dist_pump_lincoeff['p2_m_coeff'][var[4]], dist_pump_lincoeff['p2_p_coeff'][var[4]], dist_pump_lincoeff['p2_cst'][var[4]], dist_pump_lincoeff['p2_max_m'][var[4]]]
    dist_pump_3 = 0#[dist_pump_lincoeff['p3_m_coeff'][var[4]], dist_pump_lincoeff['p3_p_coeff'][var[4]], dist_pump_lincoeff['p3_cst'][var[4]], dist_pump_lincoeff['p3_max_m'][var[4]]]

    ##Putting the values into a dataframe
    mdv_slave_param = prepare_slave_param_csv_vtest2(var, evap_cond_pump_lincoeff, dist_pump_1, dist_pump_2, dist_pump_3, weather, demand, nwk_choice, piecewise_steps)

    mdv_slave_param.to_csv(csv_final_save)
    
    return 