##This is the main script of the mono objective genetic algorithm, which is handled at the digit level 

def ga_mono_main_nb (population, generations, selection_choice, selection_choice_data, crossover_perc, mutation_perc, variable_list, initial_variable_values, parallel_process, obj_func_plot, cores_used):

    ##population --- the population size
    ##generations --- the number of reproduction generations 
    ##selection_choice --- the selection method which is to be employed
    ##selection_choice_data --- a dictionary containing data needed for various selection choices
    ##crossover_perc --- the percentage of the original population used for mating
    ##mutation_perc --- the percentage of population subjected to random mutation
    ##variable_list --- Dataframe of variable attributes 
    ##initial_variable_values --- starting points, used to seed the initial population 
    ##parallel_process --- to parallel process or not to boolean yes or no
    ##obj_func_plot --- dynamic graph of the objective function value
    
    import os
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'            ##Incase of the need to use relative directory
    import sys
    sys.path.append(current_path)    
    import numpy as np
    from ga_mono_nb_conv_info import ga_mono_nb_conv_info
    from ga_mono_initialize_agents_nb import ga_mono_initialize_agents_nb
    
    print('Starting Up... ...')

    dim_variable_list = variable_list.shape
    num_var = dim_variable_list[0]

    ##Storing the data 
    storage = {}
    ##Initiate a matrix to hold the following:
        ##All evaluated agents
    storage['all_eval_pop'] = np.zeros((0, num_var + 2))           ##The extra columns are for the objective function and generation
        ##The best agent per generation 
    storage['best_obj_per_gen'] = np.zeros((0, num_var + 2))
        ##The overall best agent movement
    storage['best_agent_movement'] = np.zeros((0, num_var + 1))
    
    ##The first step is to convert the entire list of variables into an list of numbers based on the specification 
    dec_info_variable_list = ga_mono_nb_conv_info(variable_list)
    
    ##The next step is to create the initial population 
        ##The last column of the initial_population placeholder contains the evaluated objective function value 
    initial_population_int, initial_population_actual = ga_mono_initialize_agents_nb(population, dec_info_variable_list, initial_variable_values, parallel_process, cores_used)
 
    ##Storing important information about the initial_population 
    storage = ga_mono_data_store_nb (storage, initial_population_actual, '-')
        
    if parallel_process == 'no':
        iteration = 1
        storage = ga_mono_run_serial_nb(initial_population_int, num_var, generations, selection_choice, selection_choice_data, crossover_perc, mutation_perc, dec_info_variable_list, storage, obj_func_plot, iteration)
    
    elif parallel_process == 'yes':
        storage = ga_mono_run_parallel_nb(initial_population_int, num_var, generations, selection_choice, selection_choice_data, crossover_perc, mutation_perc, dec_info_variable_list, cores_used, storage, obj_func_plot)
    
    ##Storing the relevant data in csv format 
    results_loc_all_eval_pop = current_path + 'ga_mono_results\\all_eval_pop.csv'
    results_loc_best_obj_per_gen = current_path + 'ga_mono_results\\best_obj_per_gen.csv'
    results_loc_best_agent = current_path + 'ga_mono_results\\best_agent_movement.csv'
    np.savetxt(results_loc_all_eval_pop, storage['all_eval_pop'], delimiter = ',')
    np.savetxt(results_loc_best_obj_per_gen, storage['best_obj_per_gen'], delimiter = ',')
    np.savetxt(results_loc_best_agent, storage['best_agent_movement'], delimiter = ',')    
    
    return

##################################################################################################################################################
##Additional functions 

##This function runs the genetic algorithm generation loop in series
def ga_mono_run_serial_nb(initial_population, num_var, generations, selection_choice, selection_choice_data, crossover_perc, mutation_perc, dec_info_variable_list, storage, obj_func_plot, iteration):

    import numpy as np
    import matplotlib.pyplot as plt 
    import time
    from ga_mono_fitness_function_nb import ga_mono_fitness_function_nb
    from ga_mono_selection_nb import ga_mono_selection_nb
    from ga_mono_crossover_nb import ga_mono_crossover_nb
    from ga_mono_mutation_nb import ga_mono_mutation_nb
    from ga_mono_calc_obj_func_nb import ga_mono_calc_obj_func_series_nb
    
    ##initial_population --- the initial population to begin the genetic algorithm in the interval form
    ##num_var --- the number of variables 
    ##generations --- the number of generations to run the function for
    ##selection_choice --- the selection method to be employed 
    ##selection_choice_data --- a dictionary containing data needed for various selection choices
    ##crossover_perc --- the percentage of the original population selected for crossover 
    ##mutation_perc --- the percentage of the total number of bits which will be mutated
    ##dec_info_variable_list --- the list of variables and its corresponding attributes, with binary attributes
    ##storage --- a dictionary containing the important result records
    ##obj_func_plot --- instructions to plot graphs 
    ##iteration --- the associated code for parallel processing, for series = 1
    
    ##Determining the number of variables per agent 
    dim_dec_info_variable_list = dec_info_variable_list.shape
    num_var_per_agent = dim_dec_info_variable_list[0]
    
    current_population = np.copy(initial_population)
    
    ##Starting the evolution process
    print('Starting evolution process... ...')
    
    if obj_func_plot == 'yes':
        ##Setting up the dynamic graph 
        x_gen = []
        y_gen = []
        plt.show()
        axes = plt.gca()
    
    for i in range (0, generations):
        
        print('Evaluating generation ' + str(i) + ' ... ...')        
        ##Generating calculating the fitness values, sorting them in decreasing fitness values order 
        agents_obj_val_fitness =  ga_mono_fitness_function_nb(current_population) 
        ##Performing the selection process
        parent_pool, crossover_duty = ga_mono_selection_nb(agents_obj_val_fitness, num_var_per_agent, selection_choice, selection_choice_data, crossover_perc)
        ##Performing the crossover process
        child_pool = ga_mono_crossover_nb(parent_pool, crossover_duty)
        ##Performing the mutation process
        mutated_pool = ga_mono_mutation_nb(parent_pool, child_pool, mutation_perc, dec_info_variable_list)
        ##Evaluating the objective function 
        new_population_int , new_population_actual = ga_mono_calc_obj_func_series_nb(mutated_pool, dec_info_variable_list, iteration)
        #Storing information about the current population 
        storage = ga_mono_data_store_nb (storage, new_population_actual, i)
        
        curr_best_obj = min(current_population[:,num_var_per_agent])
        if i == 0:
            overall_best_obj = curr_best_obj
        else:
            if overall_best_obj > curr_best_obj:
                overall_best_obj = curr_best_obj
                
        print('Current Best Objective: ' + str(curr_best_obj))
        print('Overall Best Objective: ' + str(overall_best_obj))

        ##Letting the current_population be the new_population
        current_population = new_population_int       
        
        if obj_func_plot == 'yes':
            ##Dynamic plotting
            x_gen.append(i)
            y_gen.append(overall_best_obj)
            ##Dynamic axes
            axes.clear()
            line, = axes.plot(x_gen, y_gen, 'b*')
            plt.title('Objective Function Movement')
            plt.xlabel('Generations')
            plt.ylabel('Minimum Objective Function Value')            
            axes.set_xlim(0, i + 1)
            axes.set_ylim(0.9 * min(storage['best_agent_movement'][:, num_var]), 1.1 * max(storage['best_agent_movement'][:, num_var]))    
            line.set_xdata(x_gen)
            line.set_ydata(y_gen)
            curr_msg = 'Current Best Objective Function: \n' + str(overall_best_obj)
            plt.text(0.7, 0.9, curr_msg, horizontalalignment='center', verticalalignment='center', transform = axes.transAxes)
            plt.draw()
            plt.pause(1e-17)
            time.sleep(0.1)
    
    if obj_func_plot == 'yes':
        plt.show()
    return storage

##This function runs the genetic algorithm generation loop using parallel pools 
def ga_mono_run_parallel_nb(initial_population, num_var, generations, selection_choice, selection_choice_data, crossover_perc, mutation_perc, dec_info_variable_list, cores_used, storage, obj_func_plot):
    
    import numpy as np
    import matplotlib.pyplot as plt 
    import time
    from ga_mono_fitness_function_nb import ga_mono_fitness_function_nb
    from ga_mono_selection_nb import ga_mono_selection_nb
    from ga_mono_crossover_nb import ga_mono_crossover_nb
    from ga_mono_mutation_nb import ga_mono_mutation_nb
    from ga_mono_calc_obj_func_nb import ga_mono_calc_obj_func_parallel_nb
    
    ##initial_population --- the initial population to begin the genetic algorithm
    ##num_var --- the number of variables 
    ##generations --- the number of generations to run the function for
    ##selection_choice --- the selection method to be employed 
    ##selection_choice_data --- a dictionary containing data needed for various selection choices
    ##crossover_perc --- the percentage of the original population selected for crossover 
    ##mutation_perc --- the percentage of the total number of bits which will be mutated
    ##dec_info_variable_list --- the list of variables and its corresponding attributes, with binary attributes
    ##storage --- a dictionary containing the important result records
    ##obj_func_plot --- instructions to plot graphs 

    ##Determining the number of variables per agent 
    dim_dec_info_variable_list = dec_info_variable_list.shape
    num_var_per_agent = dim_dec_info_variable_list[0]
    
    current_population = np.copy(initial_population)
    
    ##Starting the evolution process
    print('Starting evolution process... ...')
    
    if obj_func_plot == 'yes':
        ##Setting up the dynamic graph 
        x_gen = []
        y_gen = []
        plt.show()
        axes = plt.gca()
    
    for i in range (0, generations):
        
        print('Evaluating generation ' + str(i) + ' ... ...')        
        ##Generating calculating the fitness values, sorting them in decreasing fitness values order 
        agents_obj_val_fitness =  ga_mono_fitness_function_nb(current_population) 
        ##Performing the selection process
        parent_pool, crossover_duty = ga_mono_selection_nb(agents_obj_val_fitness, num_var_per_agent, selection_choice, selection_choice_data, crossover_perc)
        ##Performing the crossover process
        child_pool = ga_mono_crossover_nb(parent_pool, crossover_duty)
        ##Performing the mutation process
        mutated_pool = ga_mono_mutation_nb(parent_pool, child_pool, mutation_perc, dec_info_variable_list)
        ##Evaluating the objective function 
        new_population , new_population_dec = ga_mono_calc_obj_func_parallel_nb(mutated_pool, dec_info_variable_list, cores_used)
        #Storing information about the current population 
        storage = ga_mono_data_store_nb (storage, new_population_dec, i)
        
        curr_best_obj = min(current_population[:,num_var_per_agent])
        if i == 0:
            overall_best_obj = curr_best_obj
        else:
            if overall_best_obj > curr_best_obj:
                overall_best_obj = curr_best_obj
                
        print('Current Best Objective: ' + str(curr_best_obj))
        print('Overall Best Objective: ' + str(overall_best_obj))
        
        ##Letting the current_population be the new_population
        current_population = new_population
        
        if obj_func_plot == 'yes':
            ##Dynamic plotting
            x_gen.append(i)
            y_gen.append(overall_best_obj)
            ##Dynamic axes
            axes.clear()
            line, = axes.plot(x_gen, y_gen, 'b*')
            plt.title('Objective Function Movement')
            plt.xlabel('Generations')
            plt.ylabel('Minimum Objective Function Value')            
            axes.set_xlim(0, i + 1)
            axes.set_ylim(0.9 * min(storage['best_agent_movement'][:, num_var]), 1.1 * max(storage['best_agent_movement'][:, num_var]))    
            line.set_xdata(x_gen)
            line.set_ydata(y_gen)
            curr_msg = 'Current Best Objective Function: \n' + str(overall_best_obj)
            plt.text(0.7, 0.9, curr_msg, horizontalalignment='center', verticalalignment='center', transform = axes.transAxes)
            plt.draw()
            plt.pause(1e-17)
            time.sleep(0.1)
     
    if obj_func_plot == 'yes':
        plt.show()
    
    return storage

##This is the function which intakes numpy arrays and appends them 

def ga_mono_data_store_nb (storage, population, generation):
    
    import numpy as np 
    
    ##storage = {}
    ##storage['all_eval_pop'] --- data pertaining to all evaluated populations in decimal 
    ##storage['best_obj_per_gen'] --- data pertaining to the best agent per generation in decimal 
    ##storage['best_agent'] --- data pertaining to the best overall agent in decimal 
    
    ##population --- the population to be stored and evaluated
    ##generation --- the current index for prefixing
    
    dim_population = population.shape
    
    ##Creating the prefix and the array 
    prefix = np.zeros((dim_population[0] ,1))
    if generation == '-':
        gen_index = 0
    else:
        gen_index = generation + 1
    prefix[:,0] = gen_index
    
    ##Storing storage['all_eval_pop'] data
    storage_all_eval_pop = np.concatenate((prefix, population), axis = 1)
    storage['all_eval_pop'] = np.concatenate((storage['all_eval_pop'], storage_all_eval_pop), axis = 0)
    
    sorted_by_obj_func = population[np.argsort(population[:,dim_population[1] - 1])]
    pop_best_agent = np.zeros((1, dim_population[1]))
    pop_best_agent[0,:] = sorted_by_obj_func[0,:]
    gen_index_np = np.zeros((1,1))
    gen_index_np[0,0] = gen_index
    pop_best_agent_with_gen = np.concatenate((gen_index_np, pop_best_agent), axis = 1)
    storage['best_obj_per_gen'] = np.concatenate((storage['best_obj_per_gen'], pop_best_agent_with_gen), axis = 0)
    
    dim_storage_best_agent_movement = storage['best_agent_movement'].shape
    row = dim_storage_best_agent_movement[0] - 1
    if dim_storage_best_agent_movement[0] == 0:
        storage['best_agent_movement'] = pop_best_agent
    else:
        if storage['best_agent_movement'][row, dim_population[1]-1] > pop_best_agent[0, dim_population[1]-1]:
            storage['best_agent_movement'] = np.concatenate((storage['best_agent_movement'], pop_best_agent), axis = 0)    
        else:
            existing_best = np.zeros((1, dim_storage_best_agent_movement[1]))
            existing_best[0, :] = storage['best_agent_movement'][row, :]
            storage['best_agent_movement'] = np.concatenate((storage['best_agent_movement'], existing_best), axis = 0)
    
    return storage
 
