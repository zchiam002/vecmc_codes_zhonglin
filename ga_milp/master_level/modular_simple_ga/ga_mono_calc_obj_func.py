##This function evaluates the objective function for each individual mutated binary list in series 
def ga_mono_calc_obj_func_series(mutated_pool, bin_info_variable_list, iteration):
    
    import numpy as np
    from ga_mono_evaluate_objective import ga_mono_evaluate_objective 
    
    ##mutated_pool --- the binary equivalent and the additional columns for objective function and fitness values
    ##bin_info_variable_list --- the list of variables and their corresponding attributes 
    ##iteration --- the associated parallel processing code, for series = 1
    
    dim_mutated_pool = mutated_pool.shape
    total_bin_len = dim_mutated_pool[1] - 2
    dim_bin_info_variable_list = bin_info_variable_list.shape
    num_var = dim_bin_info_variable_list[0]
    
    ##Evaluatiing the objective function for each agent 
        ##Creating a copy of the binary inputs for manipulation purposes, leaving out the column for fitness values 
    ret_values = np.copy(mutated_pool)
    ret_values = np.delete(ret_values, dim_mutated_pool[1] - 1, 1)
    
        ##Creating an array to copy the decimal values and objective function
    ret_values_dec = np.zeros((dim_mutated_pool[0], num_var + 1))
    
    for i in range (0, dim_mutated_pool[0]):
        
        ##Convert the binary combination into decimal equivalent
        bin_list = ret_values[i, :]
        dec_vals = conv_from_binary_gmcof (bin_info_variable_list, bin_list, num_var)
        obj_func = ga_mono_evaluate_objective(dec_vals, iteration) 
        ret_values[i, total_bin_len] = obj_func
        
        ret_values_dec_temp = dec_vals
        ret_values_dec_temp.append(obj_func)
        ret_values_dec[i, :] = ret_values_dec_temp
    
    return ret_values, ret_values_dec

##This function evaluates the objective function for each individual mutated binary list in parallel
def ga_mono_calc_obj_func_parallel(mutated_pool, bin_info_variable_list, cores_used):
    import multiprocessing as mp
    import numpy as np
    
    ##mutated_pool --- the binary equivalent and the additional columns for objective function and fitness values
    ##bin_info_variable_list --- the list of variables and their corresponding attributes 
    
    dim_mutated_pool = mutated_pool.shape
    total_bin_len = dim_mutated_pool[1] - 2
    dim_bin_info_variable_list = bin_info_variable_list.shape
    num_var = dim_bin_info_variable_list[0]
    
    parallel_array = parallel_process_prep_gmcof (mutated_pool, bin_info_variable_list)

    ##Determining the number of cores to be used 
    if (cores_used < mp.cpu_count()) and (cores_used >= 1):
        p = mp.Pool(cores_used)
        ret_values = p.map(parallel_process_eval_obj_func_mutated_pool, parallel_array)
        p.close()
        p.join()
        
        ret_values = np.array(ret_values)
        
    else:
        p = mp.Pool()
        ret_values = p.map(parallel_process_eval_obj_func_mutated_pool, parallel_array)
        p.close()
        p.join()
        
        ret_values = np.array(ret_values)

    ##Series testing 
#    ret_values = np.zeros((dim_mutated_pool[0], total_bin_len + 1 + num_var + 1)) 
#    
#    for i in range (0, dim_mutated_pool[0]):
#        ret_values[i,:] = parallel_process_eval_obj_func_mutated_pool(parallel_array[i])
        
    ##Copying the binary part of the return_values 
    ret_values_bin = ret_values[:, 0:total_bin_len + 1]
    start_dec = total_bin_len + 1
    end_dec = start_dec + num_var + 1
    ret_values_dec = ret_values[:, start_dec:end_dec]

    return ret_values_bin, ret_values_dec

#######################################################################################################################################################
##Additional functions 

##The preperation function for parallel processing 
def parallel_process_prep_gmcof (mutated_pool, bin_info_variable_list):
    
    import numpy as np 
    
    ##mutated_pool --- the binary equivalent and the additional columns for objective function and fitness values
    ##bin_info_variable_list --- the list of variables and their corresponding attributes 
    
    dim_mutated_pool = mutated_pool.shape
    
    ##Storing the information in common location so that all the parallel processes can access it 
    filename_loc = 'C:\\Optimization_zlc\\master_level\\modular_simple_ga\\parallel_process_temp_storage\\initialize_agents\\bin_info_variable_list_gmcof.csv'
    bin_info_variable_list.to_csv(filename_loc)
    
    ##Saving the mutated pool in a common location so that all the parallel processes can access it 
    filename_loc1 = 'C:\\Optimization_zlc\\master_level\\modular_simple_ga\\parallel_process_temp_storage\\initialize_agents\\mutated_pool.csv'
    np.savetxt(filename_loc1, mutated_pool, delimiter = ',')    
    
    ##Establishing an array for the input to the parallel processes
    ret_array = []
    for i in range (0, dim_mutated_pool[0]):
        ret_array.append(i)
        
    return ret_array

##A function for evaluating the objective function in parallel for each agent
def parallel_process_eval_obj_func_mutated_pool (iteration):
    
    import numpy as np
    import pandas as pd 
    from ga_mono_evaluate_objective import ga_mono_evaluate_objective    
    
    ##iteration --- the code for accessing the right value 
    
    ##Loading the information about the bin_info_variable_list
    ##Extracting variable information 
    filename_loc = 'C:\\Optimization_zlc\\master_level\\modular_simple_ga\\parallel_process_temp_storage\\initialize_agents\\bin_info_variable_list_gmcof.csv'
    bin_info_variable_list = pd.read_csv(filename_loc)
    dim_bin_info_variable_list = bin_info_variable_list.shape
    num_var = dim_bin_info_variable_list[0]
    
    ##Extracting the information about the mutated pool
    filename_loc1 = 'C:\\Optimization_zlc\\master_level\\modular_simple_ga\\parallel_process_temp_storage\\initialize_agents\\mutated_pool.csv'    
    mutated_pool = np.genfromtxt(filename_loc1, delimiter=',')
    
    ##Extracting the exact binary combination to evaluate
    dim_mutated_pool = mutated_pool.shape
    selected_agent = []
    
    ##For now leave out the objective function and the fitness value
    for i in range (0, dim_mutated_pool[1] - 2):
        selected_agent.append(mutated_pool[iteration, i])
    
    dec_vals = conv_from_binary_gmcof (bin_info_variable_list, selected_agent, num_var)
    obj_val = ga_mono_evaluate_objective(dec_vals, iteration)
    
    selected_agent.append(obj_val)
    
    ##Appending the decimal values behind the objective function for storage purposes
    for i in range (0, num_var):
        selected_agent.append(dec_vals[i])
    
    ##Appending the objective function again for easier processing 
    selected_agent.append(obj_val)

    return selected_agent
    
##Convert the variable in binary form to decimal form for function evluation 
def conv_from_binary_gmcof (bin_info_variable_list, bin_list, num_var):
    
    ##bin_info_variable_list --- the list of variables and its corresponding attributes, with binary attributes
    ##bin_list --- a array with a binary string and an empty column for the objective function 
    ##num_var --- the number of variables 
    
    ##Creating a temporary array to hold the return values
    ret_dec_vals = []
    
    ##Determining the values variables
    current_position = 0
    for i in range (0, num_var):
        
        if bin_info_variable_list['Type'][i] == 'continuous':
            lb_bits = current_position
            ub_bits = current_position + bin_info_variable_list['Bits'][i]
            
            ##Initialize an empty string to hold the values 
            string_bits = ''
            string_ul = ''              ##The upperlimit on the strings 
            
            for j in range (lb_bits, ub_bits):
                string_bits = string_bits + str(int(bin_list[j]))
                string_ul = string_ul + str(1)
                
            ##Converting the strings to decimal 
            temp_value = int(string_bits, 2)
            max_value = int(string_ul, 2) 
            ##The ratio of the max and min  
            temp_upper_bound = float(bin_info_variable_list['Upper_bound'][i])            
            temp_lower_bound = float(bin_info_variable_list['Lower_bound'][i])           
            dec_value = ((temp_value / (max_value-1)) * (temp_upper_bound - temp_lower_bound)) + temp_lower_bound
            ##Appending the final return list 
            ret_dec_vals.append(dec_value)
            ##Updating the current_value
            current_position = ub_bits
    
        elif bin_info_variable_list['Type'][i] == 'binary':
            ret_dec_vals.append(bin_list[current_position])
            current_position = current_position + 1
            
        elif bin_info_variable_list['Type'][i] == 'discrete':
            
            ##Establishing the number of bins
            num_bins = int(bin_info_variable_list['Steps'][i])
            ##Establishing the bin size 
            bin_sz = float(bin_info_variable_list['Bin_sz'][i])
            
            ##Determining the value of the binary choice 
            lb_bits = current_position 
            ub_bits = current_position + bin_info_variable_list['Bits'][i]

            ##Initialize an empty string to hold the values 
            string_bits = ''
            
            for j in range (lb_bits, ub_bits):
                string_bits = string_bits + str(int(bin_list[j]))
                
            ##Converting the strings to decimal 
            temp_value = int(string_bits, 2)     
            
            ##Establishing which bin the number is allocated to 
            for j in range (0, num_bins):
                bin_lb = j * bin_sz
                bin_ub = (j + 1) * bin_sz
                if (temp_value >= bin_lb) and (temp_value <= bin_ub):
                    allocated_bin = j
                    break
                
            temp_upper_bound = float(bin_info_variable_list['Upper_bound'][i])            
            temp_lower_bound = float(bin_info_variable_list['Lower_bound'][i])   
                
            dec_value = ((allocated_bin / (num_bins-1)) * (temp_upper_bound - temp_lower_bound)) + temp_lower_bound

            ret_dec_vals.append(dec_value)
            ##Updating the current_value
            current_position = ub_bits 
            
    return ret_dec_vals



