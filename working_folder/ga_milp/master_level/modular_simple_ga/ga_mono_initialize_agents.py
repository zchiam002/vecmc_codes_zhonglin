##This function is used to create the initial population 

def ga_mono_initialize_agents (population, bin_info_variable_list, initial_variable_values, parallel_process, cores_used):
    
    import numpy as np 
    
    ##population --- the population size 
    ##bin_info_variable_list --- the list of variables and its corresponding attributes, with binary attributes
    ##initial_variable_values --- starting values to seed the initial population 
    ##parallel_process --- boolean yes or no
    
    ##Determining the number of variables 
    dim_initial_variable_values = len(initial_variable_values) 
    num_init_vals = dim_initial_variable_values                  ##This is the number of initial values for the variables 
    total_bin_len = sum(bin_info_variable_list['Bits'][:])
    dim_bin_info_variable_list = bin_info_variable_list.shape
    num_var = dim_bin_info_variable_list[0]
    
    if parallel_process == 'no':
        ##Determining the number of calculations 
        num_calculations = population - num_init_vals
        ##Calculating the randomly generated strings
        iteration = 1
        ret_values, ret_values_dec = calc_indiv_value_series(bin_info_variable_list, initial_variable_values, num_calculations, iteration)
        
    if parallel_process == 'yes':
        ##Preparing the associated data in array form for parallel pool processing 
        num_calc_list = conv_df_to_arrays_parallel (bin_info_variable_list, population, num_init_vals)

        import multiprocessing as mp        
        ##Determining the number of cores to be used 
        if (cores_used < mp.cpu_count()) and (cores_used >= 1):
            
            p = mp.Pool(cores_used)
            ret_values_bin_dec = p.map(calc_indiv_value_parallel, num_calc_list)
            p.close()
            p.join()
        
            ret_values_bin_dec = np.array(ret_values_bin_dec)
            
        else:
            p = mp.Pool()
            ret_values_bin_dec = p.map(calc_indiv_value_parallel, num_calc_list)
            p.close()
            p.join()
        
            ret_values_bin_dec = np.array(ret_values_bin_dec)
        
#        ret_values_bin_dec = np.zeros((len(num_calc_list), total_bin_len + 1 + num_var + 1))
#        for i in range (0, len(num_calc_list)):
#            ret_values_temp = calc_indiv_value_parallel(num_calc_list[i])
#            ret_values_bin_dec[i, :] = ret_values_temp

        ##Copying the binary part of the return_values 
        ret_values = ret_values_bin_dec[:, 0:total_bin_len + 1]
        start_dec = total_bin_len + 1
        end_dec = start_dec + num_var + 1
        ret_values_dec = ret_values_bin_dec[:, start_dec:end_dec]
        
    ##Calculating the values of the initial seeds
        ##Determing the binary equivalent of the initial seeds, note that the last columns is left empty for the objective function 
    init_seeds_bin_wo_obj_func = conv_seed_to_bin (bin_info_variable_list, initial_variable_values)
        ##now we want to fill in the columns with the objective function 
    iteration_seeds = 1001
    init_seeds_bin_filled, init_seeds_bin_filled_dec = calc_obj_func_seeds(bin_info_variable_list, init_seeds_bin_wo_obj_func, iteration_seeds)
        ##Combine the 2 
    ret_all_combined = np.concatenate((ret_values, init_seeds_bin_filled), axis = 0)
    ret_all_combined_dec = np.concatenate((ret_values_dec, init_seeds_bin_filled_dec), axis = 0)

    return ret_all_combined, ret_all_combined_dec
    
##################################################################################################################################################
##################################################################################################################################################
##Additional functions 

##Defining a function to convert the DataFrame into array form 
def conv_df_to_arrays_parallel (bin_info_variable_list, population, num_init_vals):
    
    import random
    import numpy as np
    
    ##bin_info_variable_list --- the list of variables and their corresponding attributes 
    ##population --- the stipulated population size 
    ##num_initial_values --- the number of sets of initial values
    
    ##Saving the dataframe to a temporary location for access by all the parallel processes
    filename_loc = 'C:\\Optimization_zlc\\master_level\\modular_simple_ga\\parallel_process_temp_storage\\initialize_agents\\bin_info_variable_list.csv'
    bin_info_variable_list.to_csv(filename_loc)
    num_calculations = population - num_init_vals
    
    ##As we want binary without replacements 
    ##Generating the binary string needed for randomization of the initial values 
    total_bin_str_len = sum(bin_info_variable_list['Bits'][:])
    
    ##The total number of possible combinations based on string length 
    total_comb = pow(2, total_bin_str_len)

    ##Generating random integer numbers between 0, total_comb - 1, as many times as required
    ##This function ensures no duplicates
    if total_bin_str_len <= 64:
        random_num_list = random.sample(range(total_comb), num_calculations)
    ##Too many integers to handle, it is difficult for the program
    else:
        random_num_list = []
        for i in range (0, num_calculations):
            temp_select = int((random.uniform(0,1)) * total_comb)
            random_num_list.append(temp_select)

    ##Storing it in a temporary loaction for access by all the parallel processes
    filename_loc1 = 'C:\\Optimization_zlc\\master_level\\modular_simple_ga\\parallel_process_temp_storage\\initialize_agents\\chosen_value.csv'        
    np.savetxt(filename_loc1, random_num_list)
    
    num_calc_list = []
    for i in range (0, num_calculations):
        num_calc_list.append(i)
    return num_calc_list

##Defining a function calculate individual values and the resultant objective function value of the individual in parallel
def calc_indiv_value_parallel (iteration_number):
    ##The initial train of thought for the iterantion_number is that it can make each file unique
    
    import numpy as np
    import pandas as pd
    from ga_mono_evaluate_objective import ga_mono_evaluate_objective
    
    ##Extracting variable information 
    filename_loc = 'C:\\Optimization_zlc\\master_level\\modular_simple_ga\\parallel_process_temp_storage\\initialize_agents\\bin_info_variable_list.csv'
    bin_info_variable_list = pd.read_csv(filename_loc)
    dim_bin_info_variable_list = bin_info_variable_list.shape
    num_var = dim_bin_info_variable_list[0]
    
    ##Extracting the allocated random number 
    filename_loc1 = 'C:\\Optimization_zlc\\master_level\\modular_simple_ga\\parallel_process_temp_storage\\initialize_agents\\chosen_value.csv'     
    allocated_random_num = np.genfromtxt(filename_loc1, delimiter=',')
    specific_allocated_num = allocated_random_num[iteration_number]
    
    ##Initializing the return array
    ret_values = []
    total_bin_str_len = sum(bin_info_variable_list['Bits'][:])
    
    ##Converting the selected values into binary 
    bin_temp_str = "{0:b}".format(int(specific_allocated_num))
    len_bin_temp_str = len(bin_temp_str)
    preceeding_zeros = total_bin_str_len - len_bin_temp_str
    
    ##Filling up the preceeding zeros 
    for i in range (0, preceeding_zeros):
        ret_values.append(0)
    ##Filling upthe binary values 
    for i in range (0, len_bin_temp_str):
        ret_values.append(int(bin_temp_str[i]))
        
    ##Converting the selected values for objective function evaluation 
    dec_vals = conv_from_binary (bin_info_variable_list, ret_values, num_var)
    obj_val = ga_mono_evaluate_objective(dec_vals, iteration_number)
    
    ##Placing return values into an array  
    ret_values.append(obj_val)
    
    ##Placing the decimal values behind the binary ones 
    for i in range(0, num_var):
        ret_values.append(dec_vals[i])
        
    ret_values.append(obj_val)
    
    return ret_values
    
##Defining a function to calculate individual values and the resultant objective function of the individual in series
def calc_indiv_value_series (bin_info_variable_list, initial_variable_values, num_calcs, iteration):
    
    import numpy as np
    import copy
    import random
    from ga_mono_evaluate_objective import ga_mono_evaluate_objective
    ##bin_info_variable_list --- the list of variables and its corresponding attributes, with binary attributes
    ##initial_variable_values --- the initial values for seeding purposes
    ##num_calcs --- the number of calculations to be performed 
    ##iteration--- associate parallel processing code = 1 for series 
    
    dim_variable_list = bin_info_variable_list.shape
    total_bin_str_len = sum(bin_info_variable_list['Bits'][:])
    
    ##The last row will host the objective function value
    ret_values_bin = np.zeros((num_calcs, total_bin_str_len + 1))
    ret_values_dec = np.zeros((num_calcs, dim_variable_list[0] + 1))
    
    
    ##The total number of possible combinations based on string length 
    total_comb = pow(2, total_bin_str_len)
    
    ##Generating random integer numbers between 0, total_comb - 1, as many times as required
    ##This function ensures no duplicates
    if total_bin_str_len <= 64:
        random_num_list = random.sample(range(total_comb), num_calcs)
    ##Too many integers to handle, it is difficult for the program
    else:
        random_num_list = []
        for i in range (0, num_calcs):
            temp_select = int((random.uniform(0,1)) * total_comb)
            random_num_list.append(temp_select)
            
    ##Converting to the corresponding binary string 
    
    for i in range(0, num_calcs):
        bin_temp_str = "{0:b}".format(random_num_list[i])
        ##Determining the length of the string 
        len_bin_temp_str = len(bin_temp_str)
        ##Finding the number of 0s preceeding the real values 
        preceding_zeros = total_bin_str_len - len_bin_temp_str
        
        ##Filling up the return array
        
        ##Filling up the zeros first
        current_index = 0
        for j in range (0, preceding_zeros):
            ret_values_bin[i, j] = 0
            current_index = current_index + 1
            
        ##Filling up the values of the strings
        for k in range (0, len_bin_temp_str):
            ret_values_bin[i, current_index] = int(bin_temp_str[k])
            current_index = current_index + 1
            
        ##Now that the strings are filled with binary, it is time to process the values as input values (decimal)
            ##To do that it is important to know the length of the string 
        
        ##Setting up a temporary array to deal with the function 
        bin_and_empty_obj_func = ret_values_bin[i, :] 
        
        ##Converting the randomly chosen binary values to decimal         
        dec_values = conv_from_binary (bin_info_variable_list, bin_and_empty_obj_func, dim_variable_list[0])
        
        ##For filling up the return decimal values 
        temp_ret_values_dec = copy.copy(dec_values)
         
        ##Calculating the objective function value
        obj_func_val = ga_mono_evaluate_objective(dec_values, iteration)
        temp_ret_values_dec.append(obj_func_val)
        
        ret_values_bin[i, total_bin_str_len] = obj_func_val
        ret_values_dec[i, :] = temp_ret_values_dec
        
    return ret_values_bin, ret_values_dec

##Defining a function to convert the binary string into values for the evaluate function 
def conv_from_binary (bin_info_variable_list, bin_and_empty_obj_func, num_var):
    
    ##bin_info_variable_list --- the list of variables and its corresponding attributes, with binary attributes
    ##bin_and_empty_obj_func --- a array with a binary string and an empty column for the objective function 
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
                string_bits = string_bits + str(int(bin_and_empty_obj_func[j]))
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
            ret_dec_vals.append(bin_and_empty_obj_func[current_position])
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
                string_bits = string_bits + str(int(bin_and_empty_obj_func[j]))
                
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

##Defining a function to convert the seeded values to the best optimal value precision

def conv_seed_to_bin (bin_info_variable_list, initial_variable_values):
    
    import sys 
    import numpy as np
    import math
    
    ##bin_info_variable_list --- the list of variables and its corresponding attributes, with binary attributes
    ##initial_variable_values --- starting values to seed the initial population

    ##Determine the number of variables 
    dim_bin_info_variable_list = bin_info_variable_list.shape
    dim_initial_variable_values = initial_variable_values.shape 
    
    ##Checking if the seeded values are of the same order
    if dim_bin_info_variable_list[0] != dim_initial_variable_values[1]:
        print('Error in seeding entries')
        sys.exit()
    
    ##Establishing the return value array 
    total_bits = sum(bin_info_variable_list['Bits'][:])
    ##The addition of an additional column is for the storage of the objective function 
    ret_vals = np.zeros((dim_initial_variable_values[0], total_bits + 1))
    
    ##Determining the closest binary representation of the seeded variables
    
    ##i variable handles each set of seeded variables 
    for i in range (0, dim_initial_variable_values[0]):
        ##j variable handles the processes within each set of variables
        ##This array index is to handle the input column of the return numpy array 
        array_index = 0
        for j in range (0, dim_bin_info_variable_list[0]):
            if (bin_info_variable_list['Type'][j] == 'continuous'):
                ##The binary representation is just a ratio of the min and max within the range 
                lb_dec = bin_info_variable_list['Lower_bound'][j]
                ub_dec = bin_info_variable_list['Upper_bound'][j]
                seed_val = initial_variable_values[i,j]
                ub_binary_in_dec = pow(2, bin_info_variable_list['Bits'][j]) - 1
                frac_rep_dec = (seed_val - lb_dec) / (ub_dec - lb_dec)
                seed_val_bin_in_dec = frac_rep_dec * ub_binary_in_dec
                ##We need a whole number, so round it off to the nearest approximation 
                seed_val_bin_in_dec = int(round(seed_val_bin_in_dec))
                ##Converting the number to binary form 
                bin_form_str = "{0:b}".format(seed_val_bin_in_dec)
                ##Checking for the length of the returned string 
                len_value_bits = len(bin_form_str)
                ##Calculating the number of preceding zeros 
                len_preceding_zeros = bin_info_variable_list['Bits'][j] - len_value_bits
                ##Populating the return numpy array 
                for k in range (0, len_preceding_zeros):
                    ret_vals[i,array_index] = 0
                    array_index = array_index + 1
                ##Populating the return array with the bits 
                for k in range (0, len_value_bits):
                    ret_vals[i, array_index] = bin_form_str[k]
                    array_index = array_index + 1
            
            elif bin_info_variable_list['Type'][j] == 'binary':
                ##This is straightforaward, just fill in the values
                ret_vals[i, array_index] = initial_variable_values[i,j]
                array_index = array_index + 1
                
            elif (bin_info_variable_list['Type'][j] == 'discrete'):
                ##The binary representation is just a ratio of the min and max within the range 
                lb_dec = bin_info_variable_list['Lower_bound'][j]
                ub_dec = bin_info_variable_list['Upper_bound'][j]
                seed_val = initial_variable_values[i,j]
                ub_binary_in_dec = pow(2, bin_info_variable_list['Bits'][j]) - 1
                frac_rep_dec = (seed_val - lb_dec) / (ub_dec - lb_dec)
                seed_val_bin_in_dec = frac_rep_dec * ub_binary_in_dec
                ##We need a whole number, so round it off to the nearest approximation 
                seed_val_bin_in_dec = int(math.ceil(seed_val_bin_in_dec))
                ##Converting the number to binary form 
                bin_form_str = "{0:b}".format(seed_val_bin_in_dec)
                ##Checking for the length of the returned string 
                len_value_bits = len(bin_form_str)
                ##Calculating the number of preceding zeros 
                len_preceding_zeros = bin_info_variable_list['Bits'][j] - len_value_bits
                ##Populating the return numpy array 
                for k in range (0, len_preceding_zeros):
                    ret_vals[i,array_index] = 0
                    array_index = array_index + 1
                ##Populating the return array with the bits 
                for k in range (0, len_value_bits):
                    ret_vals[i, array_index] = bin_form_str[k]
                    array_index = array_index + 1
        
    return ret_vals

##Defining a function to calculate the values of the objective function from their initial seeds in their binary forms
def calc_obj_func_seeds(bin_info_variable_list, init_seeds_bin_wo_obj_func, iteration):
    
    import numpy as np
    import copy
    from ga_mono_evaluate_objective import ga_mono_evaluate_objective
    
    ##bin_info_variable_list --- the list of variables and its corresponding attributes, with binary attributes
    ##init_seeds_bin_wo_obj_func --- numpy array of the initial seeds in binary form, last column is empty for the objective function 
    ##iteration --- associated code for parallel processing, if in series == 1
    
    ##Making a copy of the input list
    copy_list = np.copy(init_seeds_bin_wo_obj_func)
    
    ##Determining the number of variables 
    dim_bin_info_variable_list = bin_info_variable_list.shape
    num_var = dim_bin_info_variable_list[0]
    
    ##Determining the number of initial seeds
    dim_init_seeds_bin_wo_obj_func = init_seeds_bin_wo_obj_func.shape
    num_initial_seeds = dim_init_seeds_bin_wo_obj_func[0]
    
    ##Initializing a numpy array for holding the decimal return values 
    ret_vals_dec = np.zeros((num_initial_seeds, num_var + 1))
   
    for i in range (0, num_initial_seeds):
        temp_array = copy_list[i, :]
        array_dec_input = conv_from_binary (bin_info_variable_list, temp_array, num_var)
        obj_val = ga_mono_evaluate_objective(array_dec_input, iteration)
        copy_list[i,dim_init_seeds_bin_wo_obj_func[1] - 1] = obj_val
        
        temp_ret_vals_dec = copy.copy(array_dec_input)
        temp_ret_vals_dec.append(obj_val)
        ret_vals_dec[i, :] = temp_ret_vals_dec
    
    return copy_list, ret_vals_dec