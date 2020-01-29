##This function evaluates the objective function for each individual mutated binary list in series 
def ga_mono_calc_obj_func_series_nb(mutated_pool, dec_info_variable_list, iteration):
    
    import numpy as np
    from ga_mono_evaluate_objective_nb import ga_mono_evaluate_objective_nb 
    
    ##mutated_pool --- the binary equivalent and the additional columns for objective function and fitness values
    ##dec_info_variable_list --- the list of variables and their corresponding attributes 
    ##iteration --- the associated parallel processing code, for series = 1
    
    dim_mutated_pool = mutated_pool.shape
    num_var_per_agent = dim_mutated_pool[1] - 2
    
    ##Evaluating the objective function for each agent 
        ##Creating a copy of the interval inputs for manipulation purposes, leaving out the column for fitness values 
    ret_values_int = np.copy(mutated_pool)
    ret_values_int = np.delete(ret_values_int, dim_mutated_pool[1] - 1, 1)
    
        ##Creating an array to copy the actual values and objective function
    ret_values_actual = np.zeros((dim_mutated_pool[0], num_var_per_agent + 1))
    
    for i in range (0, dim_mutated_pool[0]):
        
        ##Convert the interval into actual values
        int_list = ret_values_int[i, :]
        actual_vals = conv_from_interval_gmcof (dec_info_variable_list, int_list, num_var_per_agent)
        
        obj_func = ga_mono_evaluate_objective_nb(actual_vals, iteration) 
        ret_values_int[i, num_var_per_agent] = obj_func
        
        ret_values_actual_temp = actual_vals
        ret_values_actual_temp.append(obj_func)
        ret_values_actual[i, :] = ret_values_actual_temp
    
    return ret_values_int, ret_values_actual

##This function evaluates the objective function for each individual mutated binary list in parallel
def ga_mono_calc_obj_func_parallel_nb(mutated_pool, dec_info_variable_list, cores_used):
    import multiprocessing as mp
    import numpy as np
    
    ##mutated_pool --- the interval equivalent and the additional columns for objective function and fitness values
    ##dec_info_variable_list --- the list of variables and their corresponding attributes 
    
    dim_mutated_pool = mutated_pool.shape
    num_var_per_agent = dim_mutated_pool[1] - 2
    
    parallel_array = parallel_process_prep_gmcof_nb (mutated_pool, dec_info_variable_list)

    ##Determining the number of cores to be used 
    if (cores_used < mp.cpu_count()) and (cores_used >= 1):
        p = mp.Pool(cores_used)
        ret_values = p.map(parallel_process_eval_obj_func_mutated_pool_np, parallel_array)
        p.close()
        p.join()
        
        ret_values = np.array(ret_values)
        
    else:
        p = mp.Pool()
        ret_values = p.map(parallel_process_eval_obj_func_mutated_pool_np, parallel_array)
        p.close()
        p.join()
        
        ret_values = np.array(ret_values)
        
    ##Copying the interval part of the return_values 
    ret_values_bin = ret_values[:, 0:num_var_per_agent + 1]
    start_dec = num_var_per_agent + 1
    end_dec = start_dec + num_var_per_agent + 1
    ret_values_dec = ret_values[:, start_dec:end_dec]

    return ret_values_bin, ret_values_dec

#######################################################################################################################################################
##Additional functions 

##The preperation function for parallel processing 
def parallel_process_prep_gmcof_nb (mutated_pool, dec_info_variable_list):
    
    import numpy as np 
    import os
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'            ##Incase of the need to use relative directory
        
    ##mutated_pool --- the interval equivalent and the additional columns for objective function and fitness values
    ##dec_info_variable_list --- the list of variables and their corresponding attributes 
    
    dim_mutated_pool = mutated_pool.shape
    
    ##Storing the information in common location so that all the parallel processes can access it 
    filename_loc = current_path + 'parallel_process_temp_storage\\initialize_agents\\dec_info_variable_list_gmcof.csv'
    dec_info_variable_list.to_csv(filename_loc)
    
    ##Saving the mutated pool in a common location so that all the parallel processes can access it 
    filename_loc1 = current_path + 'parallel_process_temp_storage\\initialize_agents\\mutated_pool.csv'
    np.savetxt(filename_loc1, mutated_pool, delimiter = ',')    
    
    ##Establishing an array for the input to the parallel processes
    ret_array = []
    for i in range (0, dim_mutated_pool[0]):
        ret_array.append(i)
        
    return ret_array

##A function for evaluating the objective function in parallel for each agent
def parallel_process_eval_obj_func_mutated_pool_np (iteration):
    
    import numpy as np
    import pandas as pd 
    from ga_mono_evaluate_objective_nb import ga_mono_evaluate_objective_nb    
    import os
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'            ##Incase of the need to use relative directory
    
    ##iteration --- the code for accessing the right value 
    
    ##Loading the information about the dec_info_variable_list
    ##Extracting variable information 
    filename_loc = current_path + 'parallel_process_temp_storage\\initialize_agents\\dec_info_variable_list_gmcof.csv'
    dec_info_variable_list = pd.read_csv(filename_loc)
    dim_dec_info_variable_list = dec_info_variable_list.shape
    num_var = dim_dec_info_variable_list[0]
    
    ##Extracting the information about the mutated pool
    filename_loc1 = current_path + 'parallel_process_temp_storage\\initialize_agents\\mutated_pool.csv'    
    mutated_pool = np.genfromtxt(filename_loc1, delimiter=',')
    
    ##Extracting the exact binary combination to evaluate
    dim_mutated_pool = mutated_pool.shape
    selected_agent = []
    
    ##For now leave out the objective function and the fitness value
    for i in range (0, dim_mutated_pool[1] - 2):
        selected_agent.append(mutated_pool[iteration, i])
    
    actual_vals = conv_from_interval_gmcof (dec_info_variable_list, selected_agent, num_var)
    obj_val = ga_mono_evaluate_objective_nb(actual_vals, iteration)
    
    selected_agent.append(obj_val)
    
    ##Appending the actual values behind the objective function for storage purposes
    for i in range (0, num_var):
        selected_agent.append(actual_vals[i])
    
    ##Appending the objective function again for easier processing 
    selected_agent.append(obj_val)

    return selected_agent

##Defining a function to convert the interval values into actual values for the evaluate function 
def conv_from_interval_gmcof (dec_info_variable_list, interval_and_empty_obj_func, num_var):
    
    ##dec_info_variable_list --- the list of variables and its corresponding attributes, with interval attributes
    ##interval_and_empty_obj_func --- a array with the intervals and an empty column for the objective function 
    ##num_var --- the number of variables 
    
    ##Creating a temporary array to hold the return values
    ret_dec_vals = []
    
    ##Determining the actual values of the variables 
    for i in range (0, num_var):
        ##Determining the ratio
        max_interval = dec_info_variable_list['Interval'][i]
        chosen_number = interval_and_empty_obj_func[i]
        ratio = chosen_number / max_interval 
        actual_value = ratio * (dec_info_variable_list['Upper_bound'][i] - dec_info_variable_list['Lower_bound'][i]) + dec_info_variable_list['Lower_bound'][i]
        
        if dec_info_variable_list['Type'][i] == 'continuous':
            actual_value = round(actual_value, int(dec_info_variable_list['Dec_prec'][i]))
        else:
            actual_value = int(round(actual_value))
        
        ##Appending the return list 
        ret_dec_vals.append(actual_value)
            
    return ret_dec_vals











