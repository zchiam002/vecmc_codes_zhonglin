##This function processes the best performing master parameters and extracts the corresponding slave values 

def process_extract_best_slave ():
    
    import numpy as np
    import pandas as pd 
    
    ##First we will have to extract the values from the solution files 
    sol_file_loc = 'C:\\Optimization_zlc\\control_center\\single_chiller_single_demand_run\\ga_results_current_store\\test_run\\best_obj_per_gen.csv'
    sol_file = np.genfromtxt(sol_file_loc, delimiter=',')
    dim_sol_file = sol_file.shape
    
    main_working_folder_loc = 'C:\\Optimization_zlc\\control_center\\single_chiller_single_demand_run\\'
    
    ##Time steps 
    time_steps = 2
    
    ##Parallel processing
    ##yes or no
    parallel_process = 'yes'
    
    ##Parallel processing cores 
    cores = 8
    
    if parallel_process == 'no':
        iteration_id = 1001
        all_var_values = run_extract_series (sol_file, time_steps, iteration_id, main_working_folder_loc)
        all_var_values.to_csv('C:\\Optimization_zlc\\control_center\\single_chiller_single_demand_run\\ga_results_current_store\\test_run\\best_performing_all.csv')
    
    if parallel_process == 'yes':
        iteration_id = 1002
        all_var_values = run_extract_parallel (dim_sol_file, sol_file, cores, main_working_folder_loc, time_steps, iteration_id)
        all_var_values.to_csv('C:\\Optimization_zlc\\control_center\\single_chiller_single_demand_run\\ga_results_current_store\\test_run\\best_performing_all.csv')    
    
    return

######################################################################################################################################################################
##Additional Functions

##This function uses the slave formulation with the best performing master decision variables extract the slave values 
def ga_scsd_run_ea_extract_values (variables, iteration):
        
    import numpy as np
    import pandas as pd
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level\\auxillary\\')  
    sys.path.append('C:\\Optimization_zlc\\control_center\\single_chiller_single_demand_run\\')
    from input_data_process import extract_temp
    from input_data_process import extract_demand   
    from ga_scsd_run_ea import convert_mdv_to_slave_param
    from ga_scsd_run_ea import slave_var_input_curr_ts
    
    ##variables --- in 1D array form 
    ##iteration --- the code for parallel threading number

    ##Location for the weather conditions data
    weather_file_loc = 'C:\\Optimization_zlc\\input_data\\master_decision_vtest1\\weather_data_day_170816.csv'

    ##Location for the demand data 
    demand_file_loc = 'C:\\Optimization_zlc\\input_data\\master_decision_vtest1\\la_marina_demand_day_170816.csv'
    
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
    bilinear_pieces = 40    
    network_choice = 4
    
    ##Return data storage formats 
    return_data = {}
        
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
            sys.path.append('C:\\Optimization_zlc\\slave_level_models\\slave_convex_vtest3\\')
            from nwk_choice_4.cvx_prog_run_nwk_4 import cvx_prog_run_nwk_4
            obj_value, results, results_y = cvx_prog_run_nwk_4(parallel_thread_num, bilinear_pieces, solver_choice)
            return_data['obj_value_' + str(i)] = obj_value 
            return_data['results_' + str(i)] = results
            return_data['results_y_' + str(i)] = results_y
    
    return return_data

##This function runs the extraction process in parallel
def run_extract_parallel (dim_sol_file, sol_file, cores_used, main_working_folder_loc, time_steps, iteration_id): 
    
    import multiprocessing as mp
    import numpy as np
    import pandas as pd
    
    ##dim_sol_file --- the dimensions of the solution file 
    ##cores_used --- the number of cores to be used
    
    ##Creating input list for the parallel process
    num_iterations = []
    for i in range (0, dim_sol_file[0]):
        num_iterations.append(i)

    ##Determining the number of cores to be used 
    if (cores_used < mp.cpu_count()) and (cores_used >= 1):
        
        p = mp.Pool(cores_used)
        ret_values = p.map(execute_parallel_worker_function, num_iterations)
        p.close()
        p.join()
        ret_values = np.array(ret_values)
        
    else:
        p = mp.Pool()
        ret_values = p.map(execute_parallel_worker_function, num_iterations)
        p.close()
        p.join()
        ret_values = np.array(ret_values)    
    
    ##All the return values will just be in the from of numbers without the headers and indices
    just_values = process_variables_1d (sol_file)
    df_columns, mdv_per_ts = create_df_columns (main_working_folder_loc, time_steps, iteration_id, just_values)
    
    ##Initiating an empty dataframe 
    all_var_values = pd.DataFrame(columns = df_columns)
    
    for i in range (0, dim_sol_file[0]):
        temp_df = pd.DataFrame(data = [ret_values[i, :]], columns = df_columns)
        all_var_values = all_var_values.append(temp_df, ignore_index = True)        
    
    return all_var_values

##This function executes the parallel procesing calculations 
def execute_parallel_worker_function (iteration_number):
    
    import numpy as np 
    
    ##iteration_number --- the associated key for data extraction 
    
    main_working_folder_loc = 'C:\\Optimization_zlc\\control_center\\single_chiller_single_demand_run\\'
    time_steps = 2
    
    data_loc = 'C:\\Optimization_zlc\\control_center\\single_chiller_single_demand_run\\ga_results_current_store\\test_run\\best_obj_per_gen.csv'
    data_file = np.genfromtxt(data_loc, delimiter=',')
    dim_data_file = data_file.shape
    
    ##Process the files, removing the index and the objective function values
    just_values = process_variables_1d (data_file) 
    thread_input_values = just_values[iteration_number, :]
    
    dim_just_values = just_values.shape
    mdv_per_ts = dim_just_values[1] / time_steps
    
    ##Getting the slave values based on the master values
    slave_values = ga_scsd_run_ea_extract_values (thread_input_values, iteration_number)
    
    
    temp_data = []
    
    ##Populating the return array 
    current_mdv_index = 0
        
    for i in range (0, time_steps):
        ##Appending master decision variable values
        for j in range (0, int(mdv_per_ts)):
            temp_data.append(thread_input_values[current_mdv_index])
            current_mdv_index = current_mdv_index + 1
        ##Appending slave decision variable values
        dim_cont_var = slave_values['results_' + str(i)].shape
        for j in range (0, dim_cont_var[0]):
            temp_data.append(slave_values['results_' + str(i)]['Values'][j])
        dim_bin_var = slave_values['results_y_' + str(i)].shape
        for j in range (0, dim_bin_var[0]):
            temp_data.append(slave_values['results_y_' + str(i)]['Values'][j])
        ##Appending the objective function value for particular time step 
        temp_data.append(slave_values['obj_value_' + str(i)])
    ##Appending the final objective function 
    temp_data.append(data_file[iteration_number, dim_data_file[1] - 1])
    
    return temp_data
 

##This function runs the extraction process in series 
def run_extract_series (sol_file, time_steps, iteration_id, main_working_folder_loc):
    
    import pandas as pd 
        
    ##sol_file --- the solution file, first column is index, last is the objective function value 
    ##time_steps --- the number of time steps 
    ##iteration_id --- the corresponding iteration id to keep operations specific 
    ##main_working_folder_loc --- the main folder working location in the control center
    
    ##Preprocess the solution file 
    dim_sol_file = sol_file.shape

    ##Process the files, removing the index and the objective function values
    just_values = process_variables_1d (sol_file)
    
    df_columns, mdv_per_ts = create_df_columns (main_working_folder_loc, time_steps, iteration_id, just_values)

    ##Create a dataframe to store all the return values 
    all_var_values = pd.DataFrame(columns = df_columns)
    
    for i in range (0, dim_sol_file[0]):
        current_mdv = just_values[i, :]
        current_slv = ga_scsd_run_ea_extract_values (current_mdv, iteration_id)
        
        temp_data = []
        ##Populating the return dataframe  
        current_mdv_index = 0
        for j in range (0, time_steps):
            ##Appending master decision variable values
            for k in range (0, int(mdv_per_ts)):
                temp_data.append(current_mdv[current_mdv_index])
                current_mdv_index = current_mdv_index + 1
            ##Appending slave decision variable values
            dim_cont_var = current_slv['results_' + str(j)].shape
            for k in range (0, dim_cont_var[0]):
                temp_data.append(current_slv['results_' + str(j)]['Values'][k])
            dim_bin_var = current_slv['results_y_' + str(j)].shape
            for k in range (0, dim_bin_var[0]):
                temp_data.append(current_slv['results_y_' + str(j)]['Values'][k])
            ##Appending the objective function value for particular time step 
            temp_data.append(current_slv['obj_value_' + str(j)])
        ##Appending the final objective function 
        temp_data.append(sol_file[i, dim_sol_file[1] - 1])
        
        ##Appending the dataframe 
        temp_df = pd.DataFrame(data = [temp_data], columns = df_columns)
        all_var_values = all_var_values.append(temp_df, ignore_index = True)
        
    return all_var_values

##This function processes the variables into the 1d array from 
def process_variables_1d (sol_file):

    import numpy as np
    
    ##sol_file --- the solution file 
    
    dim_sol_file = sol_file.shape
    
    ##Initialize a new numpy array for holding the solution values 
    ret_array = np.copy(sol_file)
    
    ret_array = np.delete(ret_array, dim_sol_file[1] - 1, 1)
    ret_array = np.delete(ret_array, 0, 1)
            
    return ret_array 

##This function gets the names of the master decision variables 
def get_mdv_names (main_working_folder_loc, time_steps):
    
    import sys 
    sys.path.append(main_working_folder_loc)
    from ga_mono_simple_setup import variable_def
    
    ##main_working_folder_loc --- the location of the main working folder
    
    ##Dataframe containing all the information for the master decision variables 
    variable_list, initial_variable_values = variable_def (time_steps)

    dim_variable_list = variable_list.shape

    return_mdv_names = []
    
    for i in range(0, dim_variable_list[0]):
        return_mdv_names.append(variable_list['Name'][i])
    
    ##Determining the number of master decision variables per time step 
    mdv_per_ts = dim_variable_list[0] / time_steps
    
    return return_mdv_names, mdv_per_ts

##This function gets the names of the slave decision variables 
def get_sdv_names (sample_mdv_values, iteration_id, time_steps):
    
    ##sample_mdv_values --- a feasible set of values from the master decision variables
    ##iteration_id --- the corresponding iteration id to keep operations specific 
    ##time_steps --- the number of time steps 
    
    current_return_data = ga_scsd_run_ea_extract_values (sample_mdv_values, iteration_id)
    slave_names_ret = []
    
    for i in range (0, time_steps):
        dim_cont_var = current_return_data['results_' + str(i)].shape
        dim_bin_var = current_return_data['results_y_' + str(i)].shape
        
        for j in range (0, dim_cont_var[0]):
            slave_names_ret.append(current_return_data['results_' + str(i)]['Name'][j] + '_time_step_' + str(i))
        for j in range (0, dim_bin_var[0]):
            slave_names_ret.append(current_return_data['results_y_' + str(i)]['Name'][j] + '_time_step_' + str(i))            
            
    slv_per_ts = (dim_cont_var[0] + dim_bin_var[0])
    
    return slave_names_ret, slv_per_ts

##This function gets places the objective function values properly 
def create_df_columns (main_working_folder_loc, time_steps, iteration_id, just_values):
    
    import pandas as pd
    
    ##main_working_folder_loc --- the location of the main working folder
    ##time_steps --- the number of time steps 
    ##iteration_id --- the corresponding iteration id to keep operations specific 
    ##just_values --- the input values from the master to slave     
    
    ##Get the master decision variable names 
    mdv_names, mdv_per_ts = get_mdv_names (main_working_folder_loc, time_steps)
     
    ##Get the slave decision variable names 
    slv_names, slv_per_ts = get_sdv_names (just_values[0, :], iteration_id, time_steps)
    
    return_names = []
    
    current_mdv_index = 0
    current_slv_index = 0
    
    for i in range (0, time_steps):
        ##Handing master decision variables first
        for j in range (0, int(mdv_per_ts)):
            return_names.append(mdv_names[current_mdv_index])
            current_mdv_index = current_mdv_index + 1
        ##Handling slave decision variables next
        for j in range (0, int(slv_per_ts)):
            return_names.append(slv_names[current_slv_index])
            current_slv_index = current_slv_index + 1
        ##Appending the objective function value column for each time-step 
        return_names.append('Obj_Value_time_step_' + str(i))
    
    ##Overall objective function
    return_names.append('Obj_Value_Overall')
    
    return return_names, mdv_per_ts

#########################################################################################################################################################################
##Running the extraction algorithm  
if __name__ == '__main__':
    process_extract_best_slave()



