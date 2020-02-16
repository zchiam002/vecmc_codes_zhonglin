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
    
    import sys
    sys.path.append('C:\\Optimization_zlc\\master_level\\modular_simple_ga\\')
    from datetime import datetime   
    startTime = datetime.now()
    import pandas as pd 
    import numpy as np
    from ga_mono_main import ga_mono_main
    
    #Population size 
    population = 100
    
    ##Generations
    generations = 30
    ##Selection choice
        ##roulette_wheel 
        ##tournament_selection
    selection_choice = 'tournament_selection'
    selection_choice_data = {}
    selection_choice_data['tournament_size'] = 30    ##Tournament size should not exceed half of the population size
    
    
    ##Crossover pool percentage (size of the parent_pool) (best to keep above 0.2 and less than 0.6)
    crossover_perc = 0.4
    
    ##Mutation percentage (variation, not corrpution, best to keep between 0.05 and 0.1)
    mutation_perc = 0.1
        
    ##Parallel processing
    ##yes or no
    parallel_process = 'yes'
   
    ##Objective function plot
    ##yes or no
    obj_func_plot = 'yes'
    
    ##Number of cores to be used (1 - max_cpu_core_count)
    cores_used = 4
    
    ##Problem specific
    time_steps = 1
    
    ##Preparing the variables 
    variable_list, initial_variable_values = variable_def (time_steps)
    
    ##Calling the mono objective genetic algorithm
    ga_mono_main(population, generations, selection_choice, selection_choice_data, crossover_perc, mutation_perc, variable_list, initial_variable_values, parallel_process, obj_func_plot, cores_used)

    print(datetime.now() - startTime)

    return

#########################################################################################################################################################################
##Additional functions 

def variable_def (time_steps):
    
    import pandas as pd 
    import numpy as np
    
    #time_steps --- the number of time steps for the associated problem 
    
    ##Initializing the variable_list dataframe 
    variable_list = pd.DataFrame(columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec','Steps'])
    
    for i in range (0, time_steps):
        
        variable = {}
        variable['Name'] = 'chiller_evap_return_temp_time_step_' + str(i)
        variable['Type'] = 'continuous'
        variable['Lower_bound'] = 275.16
        variable['Upper_bound'] = 288.15
        variable['Bin_dec_prec'] = 2
        variable['Steps'] = '-'
        
        temp_data = [variable['Name'], variable['Type'], variable['Lower_bound'], variable['Upper_bound'], variable['Bin_dec_prec'], variable['Steps']]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec','Steps'])
        variable_list = variable_list.append(temp_df, ignore_index = True)  
        
        variable = {}
        variable['Name'] = 'total_evap_nwk_flowrate_time_step_' + str(i) 
        variable['Type'] = 'continuous'
        variable['Lower_bound'] = 0.01
        variable['Upper_bound'] = 1860.00
        variable['Bin_dec_prec'] = 2
        variable['Steps'] = '-'
        
        temp_data = [variable['Name'], variable['Type'], variable['Lower_bound'], variable['Upper_bound'], variable['Bin_dec_prec'], variable['Steps']]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec','Steps'])
        variable_list = variable_list.append(temp_df, ignore_index = True)  
        
#        variable = {}
#        variable['Name'] = 'dummy' + str(i) 
#        variable['Type'] = 'binary'
#        variable['Lower_bound'] = 0
#        variable['Upper_bound'] = 0
#        variable['Bin_dec_prec'] = 0
#        variable['Steps'] = 0
#        
#        temp_data = [variable['Name'], variable['Type'], variable['Lower_bound'], variable['Upper_bound'], variable['Bin_dec_prec'], variable['Steps']]
#        temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec','Steps'])
#        variable_list = variable_list.append(temp_df, ignore_index = True)        
        
        ##Initial variables
        
        ##The number of seeds
        num_seeds = 1
        num_variables = 2 * time_steps
        initial_variable_values = np.zeros((num_seeds, num_variables))
        
        ##Importing seeding values 
        seeds = pd.read_csv('C:\\Optimization_zlc\\control_center\\conference_chiller_only\\seeding_values_hl.csv')
        
        allocated_hour = 11
        
        s1 = round(seeds['T_evap_in'][allocated_hour], 2)        
        s2 = round(seeds['evap_flow'][allocated_hour], 2)
        #s3 = int(1.0)        

        initial_variable_values[0,:] = [s1, s2]#, s3]

    return variable_list, initial_variable_values



#########################################################################################################################################################################
##Running the optimization    
if __name__ == '__main__':
    ga_mono_simple_setup()
    
 