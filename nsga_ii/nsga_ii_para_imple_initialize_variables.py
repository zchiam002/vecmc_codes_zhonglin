##This function creates the initial population

def nsga_ii_para_imple_initialize_variables (input_v):

    ##input_v['population']                     ---     population
    ##input_v['generations']                    ---     generations
    ##input_v['num_obj_func']                   ---     num_obj_func    
    ##input_v['selection_choice_data']          ---     selection_choice_data
    ##input_v['crossover_perc']                 ---     crossover_perc
    ##input_v['mutation_distribution_index']    ---     mutation_distribution_index
    ##input_v['mutation_perc']                  ---     mutation_perc
    ##input_v['crossover_distribution_index']   ---     crossover_distribution_index    
    ##input_v['variable_list']                  ---     variable_list
    ##input_v['initial_variable_values']        ---     initial_variable_values
    ##input_v['parallel_process']               ---     parallel_process
    ##input_v['obj_func_plot']                  ---     obj_func_plot
    ##input_v['cores_used']                     ---     cores_used   
    ##input_v['objAll']                         ---     []
    ##input_v['xAll']                           ---     []
    ##input_v['M']                              ---     number of objective functions
    ##input_v['V']                              ---     number of decision variables      
    ##input_v['variable_list_conv_info']        ---     a dataframe of the intervals based on each variable type 
    
    import numpy as np
    
    ##Printing a message 
    print('Initializing population')
    
    ##Determining the number of function evaluations to perform 
    dim_initial_variable_values = input_v['initial_variable_values'].shape
    num_seeds = dim_initial_variable_values[0]
    num_rand_agents = input_v['population'] - num_seeds
    
    
    ##Evaluating the number of randomly determined objective function values 
    ##Checking if parallel processing is used
    if input_v['parallel_process'] == 'no':
        iteration_num = 10001
        f_x, f_obj = serial_initialize_variables(input_v, num_rand_agents, iteration_num)
    
    else:
        ##Preparing the associated data in array form for parallel pool processing 
        num_calc_list = prepare_parallel_process_info (input_v['variable_list_conv_info'], num_rand_agents, input_v['V'], input_v['M'])
        
        import multiprocessing as mp
        ##Determining the number of cores to be used 
        if (input_v['cores_used'] < mp.cpu_count()) and (input_v['cores_used'] >= 1):
    
            p = mp.Pool(input_v['cores_used'])
            ret_values_all = p.map(calc_indiv_value_parallel, num_calc_list)
            p.close()
            p.join()
        
            ret_values_all = np.array(ret_values_all)    
    
        else:
            p = mp.Pool()
            ret_values_all = p.map(calc_indiv_value_parallel, num_calc_list)
            p.close()
            p.join()
        
            ret_values_all = np.array(ret_values_all)           
        
        ##Post processing of all the outputs from the parallel pools 
        f_x, f_obj = post_process_parallel_process_output (ret_values_all, input_v['M'])
    
    ##Evaluating the objective function values of the seeded values
    f_x_seeds, f_obj_seeds = calc_value_seeds (input_v['variable_list_conv_info'], input_v['initial_variable_values'], input_v['M'])
    
    ##Concatenating the initial population and the calculated values of the seeds 
    f_x_all = np.concatenate((f_x, f_x_seeds), axis = 0)
    f_obj_all = np.concatenate((f_obj, f_obj_seeds), axis = 0)
    
    
    input_v['objAll'] = f_obj_all
    input_v['xAll'] = f_x_all

    f_all = np.concatenate((f_x_all, f_obj_all), axis=1)       
    
    return f_all, input_v

###################################################################################################################################################################################
##Auxillary functions

##This function calculates the value of the seeds
def calc_value_seeds (variable_list_conv_info, initial_variable_values, num_obj_func):
    
    ##variable_list_conv_info   ---     a dataframe of the intervals based on each variable type 
    ##initial_variable_values   ---     a numpy array of initial seed values 
    ##num_obj_func              ---     the number of objective functions 
    
    import numpy as np
    from nsga_ii_para_imple_evaluate_objective import nsga_ii_para_imple_evaluate_objective
    
    ##Setting an arbitrarily determined iteration number 
    iteration_num = 100002 
    
    ##Determining the number of initial seeds 
    dim_initial_variable_values = initial_variable_values.shape 
    num_initial_seeds = dim_initial_variable_values[0]
    
    ##Determining the number of variables 
    dim_variable_list_conv_info = variable_list_conv_info.shape 
    num_var = dim_variable_list_conv_info[0]
    
    ##Initializing the return values 
    f_obj = np.zeros((num_initial_seeds, num_obj_func))             ##To only contain objective function values 
    f_x = np.zeros((num_initial_seeds, num_var))               ##To contain only variables     
    
    ##Preparing the initial seeds and also calculating the corresponding objective function 
    for i in range (0, num_initial_seeds):
        
        ##First preparing the seeds for type consistency 
        for j in range (0, num_var):
            ##Determining the value of the current variable
            curr_var = initial_variable_values[i,j]
            ##Determining the type of the current variable
            var_type = variable_list_conv_info['Type'][j]
            ##Rounding off, etc as necessary to make the type consistent
            if var_type == 'continuous':
                curr_var = round(curr_var, int(variable_list_conv_info['Dec_prec'][j]))
            else:
                curr_var = int(round(curr_var))
            ##Updating the numpy array 
            f_x[i,j] = curr_var
            
        ##Now calculating the objective function values 
        f_obj[i,:] = nsga_ii_para_imple_evaluate_objective (f_x[i,:], num_obj_func, iteration_num)
    
    return f_x, f_obj

##This function is the parallel process function, which only works after prepare_parallel_process_info has been executed
def calc_indiv_value_parallel (iteration_num):
    
    ##iteration_num     ---     an arbitrarily selected number for making the saving file names unique if needed
    
    import numpy as np 
    import pandas as pd 
    from nsga_ii_para_imple_evaluate_objective import nsga_ii_para_imple_evaluate_objective
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'             ##Incase relative directories are needed
    
    ##The idea of having iteration_num is to firstly extract the right variable values as well as to make sure each save file is unique
    
    ##Extracting the allocated random values 
    filename_loc = current_path + 'parallel_process_temp_storage\\common_access_init_agents.csv'
    random_generated_variable_values = np.genfromtxt(filename_loc, delimiter=',')    
    specific_allocated_values = random_generated_variable_values[iteration_num, :]
    
    ##Extracting information about the number of objective functions
    num_obj_func_df = pd.read_csv(current_path + 'parallel_process_temp_storage\\obj_func_df.csv')
    num_obj_func = num_obj_func_df['num_obj_func'][0]

    ##Calculating the objective function 
    obj_func_val = nsga_ii_para_imple_evaluate_objective(specific_allocated_values, num_obj_func, iteration_num)
    
    ##Creating a list to append the return values 
    return_vals = []
    
    ##Determining the number of decision variables 
    dim_random_generated_variable_values = random_generated_variable_values.shape
    num_dv = dim_random_generated_variable_values[1]
    
    ##Appending the actual values
    for i in range (0, num_dv):
        return_vals.append(specific_allocated_values[i])
    
    ##Appending the objective function values 
    for i in range (0, num_obj_func):
        return_vals.append(obj_func_val[0,i])
        
    return return_vals

##Function for initializing variables in a serial manner 
def serial_initialize_variables (input_v, num_rand_agents, iteration_num):
    
    ##input_v['population']                 ---     population
    ##input_v['generations']                ---     generations
    ##input_v['num_obj_func']               ---     num_obj_func    
    ##input_v['selection_choice']           ---     selection_choice
    ##input_v['selection_choice_data']      ---     selection_choice_data
    ##input_v['crossover_perc']             ---     crossover_perc
    ##input_v['mutation_perc']              ---     mutation_perc
    ##input_v['variable_list']              ---     variable_list
    ##input_v['initial_variable_values']    ---     initial_variable_values
    ##input_v['parallel_process']           ---     parallel_process
    ##input_v['obj_func_plot']              ---     obj_func_plot
    ##input_v['cores_used']                 ---     cores_used  
    ##input_v['objAll']                     ---     []
    ##input_v['xAll']                       ---     []
    ##input_v['M']                          ---     number of objective functions
    ##input_v['V']                          ---     number of decision variables      
    ##input_v['variable_list_conv_info']    ---     a dataframe of the intervals based on each variable type 
    
    
    ##num_rand_agents                       ---     the number of random runction evaluations to perform
    ##iteration_num                         ---     an arbitrarily selected number for making the saving file names unique if needed

    from nsga_ii_para_imple_evaluate_objective import nsga_ii_para_imple_evaluate_objective 
    import numpy as np    
    
    M = input_v['M']
    V = input_v['V']
    
    ##Initialize each return value
    f_obj = np.zeros((num_rand_agents,M))             ##To only contain objective function values 
    f_x = np.zeros((num_rand_agents,V))               ##To contain only variables     
    
    for i in range (0, num_rand_agents):
        ##Initialize the decision variables based on the minimum and the maximum possible values.
        ##V is the number of decision variables. A random number is picked between the minimum and 
        ##maximum possible values for each decision variable.
            
        for j in range (0, V):
            randomly_selected_val = choose_random_value_based_on_type (input_v['variable_list_conv_info'], j)
            f_x[i,j] = randomly_selected_val
        
        ##For ease of computation and handling data the chromosome also has the value of the objective
        ##function concatenated at the end. The elements V + 1 to K has the objective function values.
        ##The function evaluate_objective takes one chromosome at a time, infact only the decision variables 
        ##are passed to the function along with information about the number of objective functions which are 
        ##processed and returns the value for the objective functions. These values are now stored at the end 
        ##of the chromosome itself.
        f_obj[i,:] = nsga_ii_para_imple_evaluate_objective (f_x[i,:], M, iteration_num)

    return f_x, f_obj

##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
##Additional functions 
    
##This function post processes the parallel processing outputs into the suitable format 
def post_process_parallel_process_output (parallel_process_output, num_obj_func):
    
    ##parallel_process_output   ---     a numpy array of outputs containing variable and objective function values 
    ##num_obj_func              ---     the number of objectives 
    
    ##Determining the dimensions of the output data from the parallel process
    dim_parallel_process_output  = parallel_process_output.shape 
    num_cols = dim_parallel_process_output[1]
    
    ##Determining the last variable columns
    end_var_col = num_cols - num_obj_func
    
    f_x = parallel_process_output[:, 0:end_var_col]
    f_obj = parallel_process_output[:, end_var_col:num_cols]
    
    return f_x, f_obj

##This function prepares the values in the suitable format for parallel processing 
def prepare_parallel_process_info (variable_list_conv_info, num_rand_agents, num_dv, num_obj_func):
    
    ##variable_list_conv_info   ---     a dataframe of the intervals based on each variable type 
    ##num_rand_agents           ---     the number of random runction evaluations to perform
    ##num_dv                    ---     the number of decision variables 
    ##num_obj_func              ---     the number of objective functions 

    import numpy as np
    import pandas as pd 
    import os
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'             ##Incase relative directories are needed
    
    ##Determining a save path for the storage of common references 
    save_dir = current_path + 'parallel_process_temp_storage\\'
    
    ##Saving variable_list_conv_info 
    variable_list_conv_info.to_csv(save_dir + 'variable_list_conv_info_initialize_agents.csv')
    
    ##Preparing the numpy array of randomly initialized values
    common_access = np.zeros((num_rand_agents, num_dv))
    
    for i in range (0, num_rand_agents):
        for j in range (0, num_dv):
            curr_value = choose_random_value_based_on_type (variable_list_conv_info, j)
            common_access[i,j] = curr_value
            
    ##Storing the numpy array in a temporary location for access by all parallel processes
    file_save_loc = save_dir + 'common_access_init_agents.csv'
    np.savetxt(file_save_loc, common_access, delimiter=',')
    
    ##Saving the number of objective functions 
    obj_func_df = pd.DataFrame(data = [num_obj_func], columns = ['num_obj_func'])
    obj_func_df.to_csv(save_dir + 'obj_func_df.csv')
    
    ##Creating a reference list for all parallel process workers to reference from 
    num_calc_list = []
    for i in range (0, num_rand_agents):
        num_calc_list.append(i)
    
    return num_calc_list 

##This function chooses a random number within the interval and calculates the actual return value  
def choose_random_value_based_on_type (variable_list_conv_info, var_num):
    
    ##variable_list_conv_info   ---     a dataframe of the intervals based on each variable type 
    ##var_num                   ---     the variable number    
    
    import random
    
    ##The interval the is dealt with currently 
    curr_interval = variable_list_conv_info['Interval'][var_num]
    ##The value of the randomly chosen number      
    curr_value = random.randint(0, curr_interval)
    ##Converting that number back to the actual form so that it can be used for evaluating the objective function 
    ratio = curr_value / curr_interval 
    actual_value = (ratio * (variable_list_conv_info['Upper_bound'][var_num] - variable_list_conv_info['Lower_bound'][var_num])) +  variable_list_conv_info['Lower_bound'][var_num]
    ##Determining the nature of the variable type and processing accoridingly 
    var_type = variable_list_conv_info['Type'][var_num] 
    if var_type == 'continuous':
        actual_value = round(actual_value, int(variable_list_conv_info['Dec_prec'][var_num]))
    else:
        actual_value = int(round(actual_value))    
    
    return actual_value

##Copyright (c) 2009, Aravind Seshadri
##All rights reserved.

##Redistribution and use in source and binary forms, with or without  modification, are permitted provided that the following 
##conditions are met:

##   * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer 
##     in the documentation and/or other materials provided with the distribution
##     
##THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT 
##NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL 
##THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
##(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
##HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
##ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.