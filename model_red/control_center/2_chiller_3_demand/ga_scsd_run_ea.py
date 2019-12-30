##This is the evaluate objective function for the slave formulation 

def ga_scsd_run_ea (variables, iteration):
    
    import numpy as np
    import pandas as pd
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level\\auxillary')    
    from input_data_process import extract_temp
    from input_data_process import extract_demand   
    
    ##variables --- in 1D array form 
    ##iteration --- the code for parallel threading number

    ##Location for the weather conditions data
    weather_file_loc = 'C:\\Optimization_zlc\\input_data\\2_chiller_3_demand_input_data\\weather_data_day_170816.csv'

    ##Location for the demand data 
    demand_file_loc = 'C:\\Optimization_zlc\\input_data\\2_chiller_3_demand_input_data\\la_marina_demand_day_170816.csv'
    
    ##Importing them into dataFrames 
    weather = extract_temp(weather_file_loc)
    demand = extract_demand(demand_file_loc)
    
    ##Solver 
    ##glpk or gurobi
    solver_choice = 'gurobi'
    
    var_per_ts = 4
    num_time_steps = int(len(variables) / var_per_ts)
    parallel_thread_num = iteration
    piecewise_steps = 4
    bilinear_pieces = 12   
    network_choice = 4
    
    obj_func = np.zeros((num_time_steps, 1))
    print(num_time_steps)
    for i in range (0, num_time_steps):
        temp_weather_data = [weather['T_DB'][i], weather['T_WB'][i]]
        temp_weather_rec = pd.DataFrame(data = [temp_weather_data], columns = ['T_DB', 'T_WB'])
    
        temp_demand_data = [demand['ss_gv2_demand'][i], demand['ss_hsb_demand'][i], demand['ss_pfa_demand'][i], demand['ss_ser_demand'][i], demand['ss_fir_demand'][i]]
        temp_demand_rec = pd.DataFrame(data = [temp_demand_data], columns = ['ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'ss_fir_demand'])  
        
        var_input_cts = slave_var_input_curr_ts (i, variables, var_per_ts)
        
        ##Converting the master decision variables into slave readable form 
        convert_mdv_to_slave_param (parallel_thread_num, var_input_cts, temp_weather_rec, temp_demand_rec, network_choice,  piecewise_steps)
        ##From here onwards, activate the convex solver 
        ##The key issue here is that the different network choices links to different activation scripts
        ##Hence we need to check for the appropriate network choice
    
        ##Checking which script to run 
        if network_choice == 1:
            x = 1 #cvx_prog_run_nwk_1(parallel_thread_num)
        elif network_choice == 2:
            x = 1 #cvx_prog_run_nwk_2(parallel_thread_num)
        elif network_choice == 3:
            x = 1 #cvx_prog_run_nwk_3(parallel_thread_num)
        elif network_choice == 4:
            sys.path.append('C:\\Optimization_zlc\\slave_level_models\\slave_convex_vtest4\\')
            from nwk_choice_4.cvx_prog_run_nwk_4 import cvx_prog_run_nwk_4
            obj_value, results, results_y = cvx_prog_run_nwk_4(parallel_thread_num, bilinear_pieces, solver_choice)
            obj_func = append_obj_value (obj_value, obj_func, i)

    ##After running all the time steps, we process the information
    final_obj_value = sum(obj_func[:,0])
    
    
    return final_obj_value

###########################################################################################################################################################################
##Additional functions 

##This function writes the parameters for the slave solver 
def convert_mdv_to_slave_param (thread_number, var, weather, demand, nwk_choice,  piecewise_steps):
    
    import sys
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\2_chillers_3_demand_master_level_models\\look_up_tables\\')
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\2_chillers_3_demand_master_level_models\\prep_functions\\')
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
    dist_pump_lincoeff = pd.read_csv('C:\\Optimization_zlc\\master_level_models\\2_chillers_3_demand_master_level_models\\look_up_tables\\dist_pump_lincoeff.csv')
    evap_cond_pump_lincoeff = pd.read_csv('C:\\Optimization_zlc\\master_level_models\\2_chillers_3_demand_master_level_models\\look_up_tables\\evap_cond_pump_lincoeff.csv')    
    
    ##Dealing with distribution network mapping 
    dist_pump_1 = 0#[dist_pump_lincoeff['p1_m_coeff'][var[4]], dist_pump_lincoeff['p1_p_coeff'][var[4]], dist_pump_lincoeff['p1_cst'][var[4]], dist_pump_lincoeff['p1_max_m'][var[4]]]
    dist_pump_2 = 0#[dist_pump_lincoeff['p2_m_coeff'][var[4]], dist_pump_lincoeff['p2_p_coeff'][var[4]], dist_pump_lincoeff['p2_cst'][var[4]], dist_pump_lincoeff['p2_max_m'][var[4]]]
    dist_pump_3 = 0#[dist_pump_lincoeff['p3_m_coeff'][var[4]], dist_pump_lincoeff['p3_p_coeff'][var[4]], dist_pump_lincoeff['p3_cst'][var[4]], dist_pump_lincoeff['p3_max_m'][var[4]]]

    ##Putting the values into a dataframe
    mdv_slave_param = prepare_slave_param_csv_vtest2(var, evap_cond_pump_lincoeff, dist_pump_1, dist_pump_2, dist_pump_3, weather, demand, nwk_choice, piecewise_steps)

    mdv_slave_param.to_csv(csv_final_save)
    
    return 

##This function processes the variable inputs to the slave for the current time_step 
def slave_var_input_curr_ts (current_ts, total_var, num_var):
    ##current_ts --- the current time step 
    ##total_var --- the array of all variable in the 1D format
    ##num_var --- the number of variables for the associated time step
    
    ##Initializing a return array to hold the values for calculation 
    var_curr_ts = []
    
    ##Determining the starting index 
    start_index = current_ts * num_var
    
    for i in range (0, num_var):
        var_curr_ts.append(total_var[start_index + i])
    
    return var_curr_ts

##This function appends the objective function value for multiple time steps
def append_obj_value (obj_value, obj_func, curr_time_step):
    ##obj_value --- the slave objective function value 
    ##obj_func --- numpy array of objective function values 
    ##curr_time_step --- the associated time step 

    if obj_value == 'na':
        ret_val = 100000
    else:
        ret_val = obj_value 
    
    obj_func[curr_time_step,0] = ret_val
        
    return obj_func

