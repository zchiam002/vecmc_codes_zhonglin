##This function is used to create the initial population 

def ga_mono_initialize_agents_nb (population, dec_info_variable_list, initial_variable_values, parallel_process, cores_used):
    
    import numpy as np 
    
    ##population --- the population size 
    ##dec_info_variable_list --- the list of variables and its corresponding attributes, with the interval attributes
    ##initial_variable_values --- starting values to seed the initial population 
    ##parallel_process --- boolean yes or no
    
    ##Determining the number of initial seeds 
    num_init_vals = len(initial_variable_values)

    ##Fist dealing with generating a randomly initialized population 
    if parallel_process == 'no':
        ##Determining the number of calculations
        num_calculations = population - num_init_vals
        ##Calculating the randomy generated agents 
        iteration = 1
        ret_values_int, ret_values_actual = calc_indiv_value_series_nb(dec_info_variable_list, initial_variable_values, num_calculations, iteration)

    if parallel_process == 'yes':
        ##Preparing the associated data in array from for parallel pool processing 
        num_calc_list = conv_df_to_arrays_parallel_nb (dec_info_variable_list, population, num_init_vals)
        
        import multiprocessing as mp        
        ##Determining the number of cores to be used 
        if (cores_used < mp.cpu_count()) and (cores_used >= 1):
    
            p = mp.Pool(cores_used)
            ret_values_all = p.map(calc_indiv_value_parallel_nb, num_calc_list)
            p.close()
            p.join()
        
            ret_values_all = np.array(ret_values_all)    
    
        else:
            p = mp.Pool()
            ret_values_all = p.map(calc_indiv_value_parallel_nb, num_calc_list)
            p.close()
            p.join()
        
            ret_values_all = np.array(ret_values_all)    
    
        ##Determining the number of variables per agent 
        dim_dec_info_variable_list = dec_info_variable_list.shape 
        num_var_per_agent = dim_dec_info_variable_list[0]
    
        ##Separating the interval and actual parts 
        ret_values_int = ret_values_all[:, 0:num_var_per_agent+1]
        start_actual = num_var_per_agent + 1
        end_actual = start_actual + num_var_per_agent + 1
        ret_values_actual = ret_values_all[:, start_actual:end_actual]
    
    
    ##Calculating the values of the initial seeds
        ##Determining the interval equivalent of the initial seeds, note that the last column is left empty for the objective function 
    init_seeds_interval_value_wo_obj_func = conv_seed_to_interval (dec_info_variable_list, initial_variable_values)
        ##Now we want to fill in the objective function value 
    iteration_seeds = 1001
    init_seeds_int_filled, init_seeds_actual_filled = calc_obj_func_seeds_nb(dec_info_variable_list, init_seeds_interval_value_wo_obj_func, iteration_seeds)
        ##Combine the 2
    ret_all_combined = np.concatenate((ret_values_int, init_seeds_int_filled), axis = 0)
    ret_all_combined_actual = np.concatenate((ret_values_actual, init_seeds_actual_filled), axis = 0)

    return ret_all_combined, ret_all_combined_actual
    
##################################################################################################################################################
##################################################################################################################################################
##Additional functions 

##Defining a function to convert the DataFrame into array form 
def conv_df_to_arrays_parallel_nb (dec_info_variable_list, population, num_init_vals):
    
    import random
    import numpy as np
    import os
    current_path = os.path.dirname(os.path.abspath(__file__))[:-42] + '\\'
    
    ##dec_info_variable_list --- the list of variables and their corresponding attributes 
    ##population --- the stipulated population size 
    ##num_initial_values --- the number of sets of initial values
    
    ##Saving the dataframe to a temporary location for access by all the parallel processes
    filename_loc = current_path + 'master_level\\modular_simple_ga_non_binary\\parallel_process_temp_storage\\initialize_agents\\dec_info_variable_list.csv'
    dec_info_variable_list.to_csv(filename_loc)
    
    ##Determining the number of calculations to be performed
    num_calculations = population - num_init_vals
    
    ##Generating a return numpy array to hold the values 
    dim_dec_info_variable_list = dec_info_variable_list.shape
    num_var_per_agent = dim_dec_info_variable_list[0]
    common_access = np.zeros((num_calculations, num_var_per_agent))
    
    for i in range (0, num_calculations):
        for j in range (0, num_var_per_agent):
            curr_interval = dec_info_variable_list['Interval'][j]
            curr_value = random.randint(0, curr_interval)
            common_access[i,j] = curr_value
            
    ##Storging it in a temporary location for access by all parallel processes
    filename_loc1 = current_path + 'master_level\\modular_simple_ga_non_binary\\parallel_process_temp_storage\\initialize_agents\\chosen_values.csv'        
    np.savetxt(filename_loc1, common_access, delimiter=',')    
    
    ##A reference list for all parallel process workers to reference from 
    num_calc_list = []
    for i in range (0, num_calculations):
        num_calc_list.append(i)
    return num_calc_list    

##Defining a function calculate individual values and the resultant objective function value of the individual in parallel
def calc_indiv_value_parallel_nb (iteration_number):
   
    import numpy as np
    import pandas as pd
    from ga_mono_evaluate_objective_nb import ga_mono_evaluate_objective_nb
    import os
    current_path = os.path.dirname(os.path.abspath(__file__))[:-42] + '\\' 
    
    ##The initial train of thought for the iterantion_number is that it can make each file unique    
       
    ##Extracting variable information 
    filename_loc = current_path + 'master_level\\modular_simple_ga_non_binary\\parallel_process_temp_storage\\initialize_agents\\dec_info_variable_list.csv'
    dec_info_variable_list = pd.read_csv(filename_loc)
    dim_dec_info_variable_list = dec_info_variable_list.shape
    num_var_per_agent = dim_dec_info_variable_list[0]
    
    ##Extracting the allocated random values
    filename_loc1 = current_path + 'master_level\\modular_simple_ga_non_binary\\parallel_process_temp_storage\\initialize_agents\\chosen_values.csv'     
    random_generated_variable_values = np.genfromtxt(filename_loc1, delimiter=',')
    specific_allocated_values = random_generated_variable_values[iteration_number, :]
    
    ##Converting the intervals into actual values so that it can be used to evaluate the objective function 
        ##Function returns a list of actual values 
    actual_values = conv_from_interval (dec_info_variable_list, specific_allocated_values, num_var_per_agent)
        ##Calculating the objective function 
    obj_func_val = ga_mono_evaluate_objective_nb(actual_values, iteration_number)
        ##Appending it to the end of the list
    actual_values.append(obj_func_val)
    
    ##Creating a numpy array to return both the interval values as well as the actual calculated values 
    return_values = []
    ##Appending the interval values and objective function first 
    for i in range (0, num_var_per_agent):
        return_values.append(specific_allocated_values[i])
    return_values.append(obj_func_val)
    ##Appending the actual values next 
    for i in range (0, len(actual_values)):
        return_values.append(actual_values[i])
    
    return return_values
    
##Defining a function to calculate individual values and the resultant objective function of the individual in series
def calc_indiv_value_series_nb (dec_info_variable_list, initial_variable_values, num_calcs, iteration):
    
    import numpy as np
    import random
    from ga_mono_evaluate_objective_nb import ga_mono_evaluate_objective_nb
    ##dec_info_variable_list --- the list of variables and its corresponding attributes, with interval attributes
    ##initial_variable_values --- the initial values for seeding purposes
    ##num_calcs --- the number of calculations to be performed 
    ##iteration--- associate parallel processing code = 1 for series 
    
    ##Determining the number of variables per agent  
    dim_variable_list = dec_info_variable_list.shape
    num_var_per_agent = dim_variable_list[0]
    
    
    ##The last row will host the objective function value
        ##Only in terms of the interval 
    ret_values_int = np.zeros((num_calcs, num_var_per_agent + 1))
        ##With the lower and upper bounds computed 
    ret_values_actual = np.zeros((num_calcs, num_var_per_agent + 1))
    
    ##Generating random agents 
    for i in range (0, num_calcs):
        for j in range (0, num_var_per_agent):
            ##Generating a random number based on the bounds of the interval 
            curr_interval = dec_info_variable_list['Interval'][j]
            curr_value = random.randint(0, curr_interval)
            ret_values_int[i,j] = curr_value
    
    ##Converting the intervals into actual values so that it can be used to evaluate the objective function 
    for i in range (0, num_calcs):
        
        ##Preparing the array of interest 
        curr_var_list = ret_values_int[i,:]
        ##Function returns a list of actual values 
        actual_values = conv_from_interval (dec_info_variable_list, curr_var_list, num_var_per_agent)
        ##Calculating the objective function 
        obj_func_val = ga_mono_evaluate_objective_nb(actual_values, iteration)
        ##Appending it to the end of the list
        actual_values.append(obj_func_val)
        ##Appending the numpy array of actual return values 
        ret_values_actual[i, :] = actual_values
        ##Appending the numpy array of the interval values
        ret_values_int[i, num_var_per_agent] = obj_func_val
        
    return ret_values_int, ret_values_actual

##Defining a function to convert the interval values into actual values for the evaluate function 
def conv_from_interval (dec_info_variable_list, interval_and_empty_obj_func, num_var):
    
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

##Defining a function to convert the seeded values into their respective interval values 
def conv_seed_to_interval (dec_info_variable_list, initial_variable_values):
    
    import sys 
    import numpy as np
    
    ##dec_info_variable_list --- the list of variables and its corresponding attributes, with interval attributes
    ##initial_variable_values --- starting values to seed the initial population

    ##Determine the number of variables 
    dim_dec_info_variable_list = dec_info_variable_list.shape
    dim_initial_variable_values = initial_variable_values.shape     

    ##Checking if the seeded values are of the same order 
    if dim_dec_info_variable_list[0] != dim_initial_variable_values[1]:
        print('Error in seeding entries')
        sys.exit()
        
    ##Establishing the return value numpy array, with the last column slated for storing the objective function
    ret_int_values = np.zeros((dim_initial_variable_values[0], dim_dec_info_variable_list[0] + 1))

    ##Determining the closest interval representation of the seeded variables 
    
    ##The ith variable handles each set of seeded variables 
    for i in range (0, dim_initial_variable_values[0]):
        ##the jth variable handles the processes with each set of variables 
        for j in range (0, dim_dec_info_variable_list[0]):
            curr_lower_bound = dec_info_variable_list['Lower_bound'][j]
            curr_interval = initial_variable_values[i,j] - curr_lower_bound
            ##Checking if the variables are properly input 
            if curr_interval < 0:
                print(curr_interval, j)
                print('Error in seeding entries range row X col:', i, j)
                sys.exit()                
            
            ##Processing the interval so that it is in sync with the rest of the format 
            if dec_info_variable_list['Type'][i] == 'continuous':
                curr_interval = round(curr_interval, dec_info_variable_list['Dec_prec'][i])
            else:
                curr_interval = int(round(curr_interval))     
            
            ret_int_values[i,j] = curr_interval
        
    return ret_int_values

##Defining a function to calculate the values of the objective function from their initial seeds in their binary forms
def calc_obj_func_seeds_nb(dec_info_variable_list, init_seeds_int_wo_obj_func, iteration):
    
    import numpy as np
    import copy
    from ga_mono_evaluate_objective_nb import ga_mono_evaluate_objective_nb
    
    ##dec _info_variable_list --- the list of variables and its corresponding attributes, with interval attributes
    ##init_seeds_bin_wo_obj_func --- numpy array of the initial seeds in interval form, last column is empty for the objective function 
    ##iteration --- associated code for parallel processing, if in series == 1
    
    ##Making a copy of the input list
    copy_list = np.copy(init_seeds_int_wo_obj_func)
    
    ##Determining the number of variables 
    dim_dec_info_variable_list = dec_info_variable_list.shape
    num_var_per_agent = dim_dec_info_variable_list[0]
    
    ##Determining the number of initial seeds
    dim_init_seeds_int_wo_obj_func = init_seeds_int_wo_obj_func.shape
    num_initial_seeds = dim_init_seeds_int_wo_obj_func[0]
    
    ##Initializing a numpy array for holding the decimal return values 
    ret_vals_actual = np.zeros((num_initial_seeds, num_var_per_agent + 1))
   
    for i in range (0, num_initial_seeds):
        temp_array = copy_list[i, :]
        array_actual_input = conv_from_interval(dec_info_variable_list, temp_array, num_var_per_agent)
        obj_val = ga_mono_evaluate_objective_nb(array_actual_input, iteration)
        ##Appending the interval array
        copy_list[i,dim_init_seeds_int_wo_obj_func[1] - 1] = obj_val
        
        temp_ret_vals_actual = copy.copy(array_actual_input)
        temp_ret_vals_actual.append(obj_val)
        ##Appending the actual array 
        ret_vals_actual[i, :] = temp_ret_vals_actual
    
    return copy_list, ret_vals_actual