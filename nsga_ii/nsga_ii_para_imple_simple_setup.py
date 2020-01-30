##IMPORTANT NOTICE
##PARALLEL COMPUTATION DOES NOT WORK WELL WITH IPYTHON CONSOLE, USE SEPARATE PYTHON CONSOLE, WELL SOMETIMES

##This is the interface for the modular genetic algorithm
##This genetic algorithm MINIMIZES the value for a given problem 
##Data needs to be entered in the specific format shown below
##variable
    ##Name --- description 
    ##Type --- one of the 3 types (continuous, discrete, binary)
    ##Lower_bound --- applicable for continuous and discrete only 
    ##Upper_bound --- applicable for continuous and discrete only 
    ##Steps --- applicable for discrete only 

def nsga_ii_para_imple_simple_setup():   
    
    import os
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'            ##Incase relative directories are needed
    import sys 
    sys.path.append(current_path + 'auxillary_functions\\')
    from datetime import datetime   
    startTime = datetime.now()
    from auxillary_functions_nsga_ii_para_imple import reconfigure_hyper_params
    from nsga_ii_para_imple_main import nsga_ii_para_imple_main
    
    ##Number of objective function 
    num_obj_func = 2
    
    #Population size 
    population = 150
    
    ##Generations
    generations = 50
    
    ##Tournament_selection data
    selection_choice_data = {}
    selection_choice_data['tournament_size'] = 2     ##For multi-objective, binary tournament size is reccomended
    
    ##Crossover pool percentage (size of the parent_pool) (best to keep above 0.2 and less than 0.6)
    crossover_perc = 0.5
    
    ##mutation percentage 
    mutation_perc = 0.1
    
    ##Crossover distribution index
    crossover_distribution_index = 20
    
    ##Mutation distribution index
    mutation_distribution_index = 20
        
    ##Parallel processing
    ##yes or no
    parallel_process = 'no'
   
    ##Objective function plot
    ##yes or no
    obj_func_plot = 'yes'
    
    ##Number of cores to be used (1 - max_cpu_core_count)
    cores_used = 4
    
    ##Problem specific
    time_steps = 1
    
    ##Preparing the variables 
    variable_list, initial_variable_values = variable_def (time_steps)
    
    ##Reconfiguring the format of the input hyper parameters 
    input_v = reconfigure_hyper_params (population, generations, num_obj_func, selection_choice_data, crossover_perc, mutation_distribution_index, variable_list, initial_variable_values, 
                                        parallel_process, obj_func_plot, cores_used, crossover_distribution_index, mutation_perc)
    
    ##Calling the mono objective genetic algorithm
    nsga_ii_para_imple_main(input_v)

    print(datetime.now() - startTime)

    return

#########################################################################################################################################################################
##Additional functions 

##Definition of the variables 
def variable_def (time_steps):
    
    import pandas as pd 
    import numpy as np
    
    #time_steps --- the number of time steps for the associated problem 
    
    ##Initializing the variable_list dataframe 
    variable_list = pd.DataFrame(columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Dec_prec','Steps'])
    
    for i in range (0, time_steps):
        
        variable = {}
        variable['Name'] = 'v0' + str(i)
        variable['Type'] = 'continuous'
        variable['Lower_bound'] = -5.00
        variable['Upper_bound'] = 5.00
        variable['Dec_prec'] = 2
        variable['Steps'] = '-'
        
        temp_data = [variable['Name'], variable['Type'], variable['Lower_bound'], variable['Upper_bound'], variable['Dec_prec'], variable['Steps']]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Dec_prec','Steps'])
        variable_list = variable_list.append(temp_df, ignore_index = True)  
        
        variable = {}
        variable['Name'] = 'v1' + str(i) 
        variable['Type'] = 'continuous'
        variable['Lower_bound'] = -5.00
        variable['Upper_bound'] = 5.00
        variable['Dec_prec'] = 2
        variable['Steps'] = '-'
        
        temp_data = [variable['Name'], variable['Type'], variable['Lower_bound'], variable['Upper_bound'], variable['Dec_prec'], variable['Steps']]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Dec_prec','Steps'])
        variable_list = variable_list.append(temp_df, ignore_index = True)

        variable = {}
        variable['Name'] = 'v2' + str(i) 
        variable['Type'] = 'continuous'
        variable['Lower_bound'] = -5.00
        variable['Upper_bound'] = 5.00
        variable['Dec_prec'] = 2
        variable['Steps'] = '-'
        
        temp_data = [variable['Name'], variable['Type'], variable['Lower_bound'], variable['Upper_bound'], variable['Dec_prec'], variable['Steps']]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Dec_prec','Steps'])
        variable_list = variable_list.append(temp_df, ignore_index = True)

        
        ##Initial variables
        
        ##The number of seeds
        num_seeds = 1
        num_variables = 4 * time_steps
        initial_variable_values = np.zeros((num_seeds, num_variables))
        
        initial_variable_values[0,:] = [5.12, -5.12, 5.12, -5.12]


    return variable_list, initial_variable_values

#########################################################################################################################################################################
#########################################################################################################################################################################
#########################################################################################################################################################################
##Running the optimization    
if __name__ == '__main__':
    nsga_ii_para_imple_simple_setup()
    
 