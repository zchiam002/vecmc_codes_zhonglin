##This is the evaluate objective function for the slave formulation 

def ga_scsd_run_ea (variables, iteration):
    
    import numpy as np
    import pandas as pd
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level\\auxillary')    
    from input_data_process import extract_demand   
    
    ##variables --- in 1D array form 
    ##iteration --- the code for parallel threading number

    ##Location for the demand data 
    demand_file_loc = 'C:\\Optimization_zlc\\input_data\\3_chiller_1_demand_12ts_3_period_input_data\\low_load\\low_demand_2.csv'
    
    ##Importing them into dataFrames 
    demand = extract_demand(demand_file_loc)
    
    ##Solver 
    ##glpk or gurobi
    solver_choice = 'gurobi'
    
    var_per_ts = 2
    num_time_steps = int(len(variables) / var_per_ts)
    parallel_thread_num = iteration
    piecewise_steps = 4
    bilinear_pieces = 20   
    
    obj_func = np.zeros((num_time_steps, 1))
    
    ##Manually defining the chiller condenser inlet temperature
    tcond_in_ch = 298.15
    
    for i in range (0, num_time_steps):    
        temp_demand_data = [demand['ss_gv2_demand'][i], demand['ss_hsb_demand'][i], demand['ss_pfa_demand'][i], demand['ss_ser_demand'][i], demand['ss_fir_demand'][i]]
        temp_demand_rec = pd.DataFrame(data = [temp_demand_data], columns = ['ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'ss_fir_demand'])  
        
        var_input_cts = slave_var_input_curr_ts (i, variables, var_per_ts, tcond_in_ch)
        
        ##Converting the master decision variables into slave readable form 
        convert_mdv_to_slave_param (parallel_thread_num, var_input_cts, temp_demand_rec, piecewise_steps)
        ##From here onwards, activate the convex solver 
        ##The key issue here is that the different network choices links to different activation scripts
        ##Hence we need to check for the appropriate network choice
    
        sys.path.append('C:\\Optimization_zlc\\slave_level_models\\slave_convex_chillers_only\\')
        from models.cvx_prog_run import cvx_prog_run
        obj_value, results, results_y = cvx_prog_run(parallel_thread_num, bilinear_pieces, solver_choice)
        obj_func = append_obj_value (obj_value, obj_func, i, var_input_cts, temp_demand_data, results)
    
    ##After running all the time steps, we process the information
    final_obj_value = sum(obj_func[:,0])
    
    
    return final_obj_value

###########################################################################################################################################################################
##Additional functions 

##This function writes the parameters for the slave solver 
def convert_mdv_to_slave_param (thread_number, var, demand,  piecewise_steps):
    
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\3_chiller_1_demand_12ts_3_period_master_level_models\\prep_functions\\')
    import os.path
    from prepare_slave_param_csv_vtest2 import prepare_slave_param_csv_vtest2    #Needs modification
    import pandas as pd    
    
    ##thread_number --- the thread number for coding output files
    ##var --- variable values from the master decision 
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

    ##Putting the values into a dataframe
    mdv_slave_param = prepare_slave_param_csv_vtest2(var, demand, piecewise_steps)

    mdv_slave_param.to_csv(csv_final_save)
    
    return 

##This function processes the variable inputs to the slave for the current time_step 
def slave_var_input_curr_ts (current_ts, total_var, num_var, tcond_in_ch):
    ##current_ts --- the current time step 
    ##total_var --- the array of all variable in the 1D format
    ##num_var --- the number of variables for the associated time step
    ##tcond_in_ch --- manually defined value
    
    ##Initializing a return array to hold the values for calculation 
    var_curr_ts = []
    
    ##Determining the starting index 
    start_index = current_ts * num_var
    
    for i in range (0, num_var):
        var_curr_ts.append(total_var[start_index + i])
        
    var_curr_ts.append(tcond_in_ch)
    
    return var_curr_ts

##This function appends the objective function value for multiple time steps
def append_obj_value (obj_value, obj_func, curr_time_step, var_input_cts, temp_demand_data, results):
    ##obj_value --- the slave objective function value 
    ##obj_func --- numpy array of objective function values 
    ##curr_time_step --- the associated time step 

    if obj_value == 'na':
        ret_val = 100000
    else:
        calculated_return_temperature = additional_check_function (var_input_cts, temp_demand_data, results)
        difference = var_input_cts[0] - calculated_return_temperature
        penalty = abs(difference) * 10000
        obj_value = obj_value + penalty
        ret_val = obj_value 
    
    obj_func[curr_time_step,0] = ret_val
        
    return obj_func


##This function checks the calculated return temperature of the setup 
def additional_check_function (var_input_cts, temp_demand_data, results):
    ##Implementing a check function
        
    ##Calculating the constant value for the exting stream of the combined substation
    if var_input_cts[1] == 0:
        exit_cst_value = 0
    else:
        flow = var_input_cts[1] * 998.2 / 3600
        demand_for_combined = sum(temp_demand_data)
        exit_cst_value = demand_for_combined / (flow * 4.2)
    
    dim_results = results.shape
    check = 4
    for i in range (0, dim_results[0]):
        if results['Name'][i] == 'cb_ss_m_perc':
            cb_ss_m_perc = results['Values'][i]
            check = check - 1
        elif results['Name'][i] == 'cb_ss_t_in':
            cb_ss_t_in = results['Values'][i]
            check = check - 1 
        elif results['Name'][i] == 'cp_nwk_m_perc':
            cp_nwk_m_perc = results['Values'][i]
            check = check - 1 
        elif results['Name'][i] == 'cp_nwk_tinout':
            cp_nwk_tinout = results['Values'][i]
            check = check - 1       
        if check == 0:
            break
        
    ##Calculating outlet temperature for the combined substation
    cb_ss_tinmax = 273.15 + 5
    tout_cb_ss = (274.15 * cb_ss_m_perc) + ((cb_ss_tinmax - 273.15 - 1) * cb_ss_m_perc * cb_ss_t_in) + exit_cst_value
    
    ##Calculating outlet temperature for the common pipe 
    tout_cp = (273.15 * cp_nwk_m_perc) + (30 * cp_nwk_m_perc * cp_nwk_tinout)
    
    calculated_return_temperature = tout_cb_ss + tout_cp

    return calculated_return_temperature

