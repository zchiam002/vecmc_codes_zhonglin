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

def ga_mono_simple_setup():   
    
    from datetime import datetime   
    startTime = datetime.now()
    import pandas as pd 
    import numpy as np
    from ga_mono_main import ga_mono_main
    
    ##Initializing the variable_list dataframe 
    variable_list = pd.DataFrame(columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec','Steps'])
    
    
    #Population size 
    population = 200
    
    ##Generations
    generations = 20
    ##Selection choice
        ##roulette_wheel 
        ##tournament_selection
    selection_choice = 'tournament_selection'
    selection_choice_data = {}
    selection_choice_data['tournament_size'] = 20        ##Tournament size should not exceed half of the population size
    
    
    ##Crossover pool percentage (size of the parent_pool) (best to keep above 0.2 and less than 0.6)
    crossover_perc = 0.3
    
    ##Mutation percentage (variation, not corrpution, best to keep between 0.05 and 0.1)
    mutation_perc = 0.1
    
    ##Variable input 
    variable = {}
    variable['Name'] = 'x1_value' 
    variable['Type'] = 'continuous'
    variable['Lower_bound'] = -100
    variable['Upper_bound'] = 100
    variable['Bin_dec_prec'] = 3
    variable['Steps'] = '-'
    
    temp_data = [variable['Name'], variable['Type'], variable['Lower_bound'], variable['Upper_bound'], variable['Bin_dec_prec'], variable['Steps']]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec','Steps'])
    variable_list = variable_list.append(temp_df, ignore_index = True)
    
    variable = {}
    variable['Name'] = 'x2_value' 
    variable['Type'] = 'continuous'
    variable['Lower_bound'] = -100
    variable['Upper_bound'] = 100
    variable['Bin_dec_prec'] = 3
    variable['Steps'] = '-'
    
    temp_data = [variable['Name'], variable['Type'], variable['Lower_bound'], variable['Upper_bound'], variable['Bin_dec_prec'], variable['Steps']]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec','Steps'])
    variable_list = variable_list.append(temp_df, ignore_index = True)
    
    variable = {}
    variable['Name'] = 'x3_value' 
    variable['Type'] = 'continuous'
    variable['Lower_bound'] = -100
    variable['Upper_bound'] = 100
    variable['Bin_dec_prec'] = 3
    variable['Steps'] = '-'
    
    temp_data = [variable['Name'], variable['Type'], variable['Lower_bound'], variable['Upper_bound'], variable['Bin_dec_prec'], variable['Steps']]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec','Steps'])
    variable_list = variable_list.append(temp_df, ignore_index = True)
    
    variable = {}
    variable['Name'] = 'x4_value' 
    variable['Type'] = 'continuous'
    variable['Lower_bound'] = -100
    variable['Upper_bound'] = 100
    variable['Bin_dec_prec'] = 3
    variable['Steps'] = '-'
    
    temp_data = [variable['Name'], variable['Type'], variable['Lower_bound'], variable['Upper_bound'], variable['Bin_dec_prec'], variable['Steps']]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec','Steps'])
    variable_list = variable_list.append(temp_df, ignore_index = True)
    
    ##Initial variables
    
    ##The number of seeds
    num_seeds = 0
    num_variables = 4
    initial_variable_values = np.zeros((num_seeds, num_variables))
    
#    initial_variable_values[0,:] = [0, 0, 0, 0]
#    initial_variable_values[1,:] = [850, 236, 1, 500]
    
    ##Parallel processing
    ##yes or no
    parallel_process = 'yes'
   
    ##Objective function plot
    ##yes or no
    obj_func_plot = 'yes'
    
    ##Number of cores to be used (1 - max_cpu_core_count)
    cores_used = 8
    
    ##Calling the mono objective genetic algorithm
    ga_mono_main(population, generations, selection_choice, selection_choice_data, crossover_perc, mutation_perc, variable_list, initial_variable_values, parallel_process, obj_func_plot, cores_used)

    print(datetime.now() - startTime)

    return
    
if __name__ == '__main__':
    ga_mono_simple_setup()
    
 