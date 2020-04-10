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

def ga_mono_simple_setup_nb():   
    
    import os
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'            ##Incase of the need to use relative directory
    import sys
    sys.path.append(current_path + '')
    from datetime import datetime   
    startTime = datetime.now()
    import pandas as pd
    from ga_mono_main_nb import ga_mono_main_nb
    
    #Population size 
    population = 20
    
    ##Generations
    generations = 3
    ##Selection choice
        ##roulette_wheel 
        ##tournament_selection
    selection_choice = 'tournament_selection'
    selection_choice_data = {}
    selection_choice_data['tournament_size'] = 0.2 * population     ##Tournament size should not exceed half of the population size
    
    
    ##Crossover pool percentage (size of the parent_pool) (best to keep above 0.2 and less than 0.6)
    crossover_perc = 0.4
    
    ##Mutation percentage (variation, not corrpution, best to keep between 0.05 and 0.1)
    mutation_perc = 0.1
        
    ##Parallel processing
    ##yes or no
    parallel_process = 'yes'
   
    ##Objective function plot (dynamic)
    ##yes or no
    obj_func_plot = 'yes'
    
    ##Number of cores to be used (1 - max_cpu_core_count)
    cores_used = 8
    
    ##Number of time steps (problem specific), if this value is more than 1, defined will be generated as many times as the number of time steps defined.
    ##variable names will also be augmented with the specific time step which they are associated with. 
    time_steps = 1
    
    ##Preparing the variables 
    variable_list, initial_variable_values = variable_def (time_steps)
    
    ##Calling the mono objective genetic algorithm
    ga_mono_main_nb(population, generations, selection_choice, selection_choice_data, crossover_perc, mutation_perc, variable_list, initial_variable_values, parallel_process, obj_func_plot, cores_used)

    print(datetime.now() - startTime)

    return (datetime.now() - startTime)

#########################################################################################################################################################################
##Additional functions 

def variable_def (time_steps):
    
    import pandas as pd 
    import numpy as np    
    import os
    
    #time_steps --- the number of time steps for the associated problem 
    
    ##Initializing the variable_list dataframe 
    variable_list = pd.DataFrame(columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Dec_prec','Steps'])
    
    for i in range (0, time_steps):
        
        variable = {}
        variable['Name'] = 'v0'                     ##Name of the variable 
        variable['Type'] = 'continuous'             ##Type, continuous, binary, discrete
        variable['Lower_bound'] = -5.12             ##Lower bound 
        variable['Upper_bound'] = 5.12              ##Upper bound
        variable['Dec_prec'] = 2                    ##Decimal precision if the variable type is continuous  
        variable['Steps'] = '-'                     ##Number of steps if the variable type is discrete
        
        temp_data = [variable['Name'], variable['Type'], variable['Lower_bound'], variable['Upper_bound'], variable['Dec_prec'], variable['Steps']]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Dec_prec','Steps'])
        variable_list = variable_list.append(temp_df, ignore_index = True)  
        
        variable = {}
        variable['Name'] = 'v1'
        variable['Type'] = 'continuous'
        variable['Lower_bound'] = -5.12
        variable['Upper_bound'] = 5.12
        variable['Dec_prec'] = 2
        variable['Steps'] = '-'
        
        temp_data = [variable['Name'], variable['Type'], variable['Lower_bound'], variable['Upper_bound'], variable['Dec_prec'], variable['Steps']]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Dec_prec','Steps'])
        variable_list = variable_list.append(temp_df, ignore_index = True)
        
        variable = {}
        variable['Name'] = 'v2'
        variable['Type'] = 'continuous'
        variable['Lower_bound'] = -5.12
        variable['Upper_bound'] = 5.12
        variable['Dec_prec'] = 2
        variable['Steps'] = '-'
        
        temp_data = [variable['Name'], variable['Type'], variable['Lower_bound'], variable['Upper_bound'], variable['Dec_prec'], variable['Steps']]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Dec_prec','Steps'])
        variable_list = variable_list.append(temp_df, ignore_index = True)

        variable = {}
        variable['Name'] = 'v3'
        variable['Type'] = 'continuous'
        variable['Lower_bound'] = -5.12
        variable['Upper_bound'] = 5.12
        variable['Dec_prec'] = 2
        variable['Steps'] = '-'
        
        temp_data = [variable['Name'], variable['Type'], variable['Lower_bound'], variable['Upper_bound'], variable['Dec_prec'], variable['Steps']]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Dec_prec','Steps'])
        variable_list = variable_list.append(temp_df, ignore_index = True)

    ##Initial variable values (seeds)
        ##The number of seeds
    num_seeds = 1                                                                           ##The number of seeds
    num_variables = variable_list.shape[0] 
    initial_variable_values = np.zeros((num_seeds, num_variables)) 
    
    initial_variable_values[0,:] = [-5.044431644, 0.899512478, 3.028129792, 0.01297007]     ##Input each seed in the form of an array.

    return variable_list, initial_variable_values



