##This is the main script of the mono objective genetic algorithm

def ga_mono_main (population, generations, selection_choice, selection_choice_data, crossover_perc, mutation_perc, variable_list, initial_variable_values, parallel_process, obj_func_plot, cores_used):
    
    import numpy as np
    import matplotlib.pyplot as plt
    from ga_mono_binary_conv_info import ga_mono_binary_conv_info
    from ga_mono_initialize_agents import ga_mono_initialize_agents
    from ga_mono_fitness_function import ga_mono_fitness_function
    
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
    
    ##The first step is to convert the entire list of variables into a string of binary numbers based on specification 
    bin_info_variable_list =  ga_mono_binary_conv_info(variable_list)
    total_binary_len = sum(bin_info_variable_list['Bits'][:])
    
    ##The next step is to create the initial population in binary 
        ##The last column of the initial_population variable contains the evaluated objective function value in decimal 
    initial_population, initial_population_dec = ga_mono_initialize_agents(population, bin_info_variable_list, initial_variable_values, parallel_process, cores_used)
    
    ##Storing important information about the initial_population 
    storage = ga_mono_data_store (storage, initial_population_dec, '-')
    
    ##Generating probability reference for the mutation process
    mutation_prob = ga_mono_agent_mutation_probability (bin_info_variable_list, total_binary_len)
    
    if parallel_process == 'no':
        iteration = 1
        storage = ga_mono_run_serial(initial_population, num_var, total_binary_len, generations, selection_choice, selection_choice_data, crossover_perc, mutation_perc, bin_info_variable_list, storage, mutation_prob, obj_func_plot, iteration)
    
    elif parallel_process == 'yes':
        storage = ga_mono_run_parallel(initial_population, num_var, total_binary_len, generations, selection_choice, selection_choice_data, crossover_perc, mutation_perc, bin_info_variable_list, cores_used, storage, mutation_prob, obj_func_plot)
    
    ##Storing the relevant data in csv format 
    results_loc_all_eval_pop = 'C:\\Optimization_zlc\\master_level\\modular_simple_ga\\ga_mono_results\\all_eval_pop.csv'
    results_loc_best_obj_per_gen = 'C:\\Optimization_zlc\\master_level\\modular_simple_ga\\ga_mono_results\\best_obj_per_gen.csv'
    results_loc_best_agent = 'C:\\Optimization_zlc\\master_level\\modular_simple_ga\\ga_mono_results\\best_agent_movement.csv'
    np.savetxt(results_loc_all_eval_pop, storage['all_eval_pop'], delimiter = ',')
    np.savetxt(results_loc_best_obj_per_gen, storage['best_obj_per_gen'], delimiter = ',')
    np.savetxt(results_loc_best_agent, storage['best_agent_movement'], delimiter = ',')    
    
    return

##################################################################################################################################################
##Additional functions 

##This function runs the genetic algorithm generation loop in series
def ga_mono_run_serial(initial_population, num_var, total_binary_len, generations, selection_choice, selection_choice_data, crossover_perc, mutation_perc, bin_info_variable_list, storage, mutation_prob, obj_func_plot, iteration):
    
    import numpy as np
    import matplotlib.pyplot as plt 
    import time
    from ga_mono_fitness_function import ga_mono_fitness_function
    from ga_mono_selection import ga_mono_selection
    from ga_mono_crossover import ga_mono_crossover
    from ga_mono_mutation import ga_mono_mutation
    from ga_mono_calc_obj_func import ga_mono_calc_obj_func_series
    
    ##initial_population --- the initial population to begin the genetic algorithm
    ##num_var --- the number of variables 
    ##generations --- the number of generations to run the function for
    ##selection_choice --- the selection method to be employed 
    ##selection_choice_data --- a dictionary containing data needed for various selection choices
    ##crossover_perc --- the percentage of the original population selected for crossover 
    ##mutation_perc --- the percentage of the total number of bits which will be mutated
    ##bin_info_variable_list --- the list of variables and its corresponding attributes, with binary attributes
    ##storage --- a dictionary containing the important result records
    ##mutation_prob --- the probability of bits mutation 
    ##obj_func_plot --- instructions to plot graphs 
    ##iteration --- the associated code for parallel processing, for series = 1
    
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
        agents_obj_val_fitness =  ga_mono_fitness_function(current_population, total_binary_len) 
        ##Performing the selection process
        parent_pool, crossover_duty = ga_mono_selection(agents_obj_val_fitness, total_binary_len, selection_choice, selection_choice_data, crossover_perc)
        ##Performing the crossover process
        child_pool = ga_mono_crossover(parent_pool, crossover_duty)
        ##Performing the mutation process
        mutated_pool = ga_mono_mutation(parent_pool, child_pool, mutation_perc, mutation_prob)
        ##Evaluating the objective function 
        new_population , new_population_dec = ga_mono_calc_obj_func_series(mutated_pool, bin_info_variable_list, iteration)
        #Storing information about the current population 
        storage = ga_mono_data_store (storage, new_population_dec, i)
    
        curr_best_obj = min(current_population[:,total_binary_len])
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

##This function runs the genetic algorithm generation loop using parallel pools 
def ga_mono_run_parallel(initial_population, num_var, total_binary_len, generations, selection_choice, selection_choice_data, crossover_perc, mutation_perc, bin_info_variable_list, cores_used, storage, mutation_prob, obj_func_plot):
    
    import numpy as np
    import matplotlib.pyplot as plt 
    import time
    from ga_mono_fitness_function import ga_mono_fitness_function
    from ga_mono_selection import ga_mono_selection
    from ga_mono_crossover import ga_mono_crossover
    from ga_mono_mutation import ga_mono_mutation
    from ga_mono_calc_obj_func import ga_mono_calc_obj_func_parallel
    
    ##initial_population --- the initial population to begin the genetic algorithm
    ##num_var --- the number of variables 
    ##total_binary_len --- total length of binary bits for all represented variables
    ##generations --- the number of generations to run the function for
    ##selection_choice --- the selection method to be employed 
    ##selection_choice_data --- a dictionary containing data needed for various selection choices
    ##crossover_perc --- the percentage of the original population selected for crossover 
    ##mutation_perc --- the percentage of the total number of bits which will be mutated
    ##bin_info_variable_list --- the list of variables and its corresponding attributes, with binary attributes
    ##storage --- a dictionary containing the important result records
    ##mutation_prob --- the probability of bits mutation 
    ##obj_func_plot --- instructions to plot graphs 
    
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
        agents_obj_val_fitness =  ga_mono_fitness_function(current_population, total_binary_len) 
        ##Performing the selection process
        parent_pool, crossover_duty = ga_mono_selection(agents_obj_val_fitness, total_binary_len, selection_choice, selection_choice_data, crossover_perc)
        ##Performing the crossover process
        child_pool = ga_mono_crossover(parent_pool, crossover_duty)
        ##Performing the mutation process
        mutated_pool = ga_mono_mutation(parent_pool, child_pool, mutation_perc, mutation_prob)
        ##Evaluating the objective function 
        new_population , new_population_dec = ga_mono_calc_obj_func_parallel(mutated_pool, bin_info_variable_list, cores_used)
        #Storing information about the current population 
        storage = ga_mono_data_store (storage, new_population_dec, i)
        
        curr_best_obj = min(current_population[:,total_binary_len])
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

def ga_mono_data_store (storage, population, generation):
    
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
 
##This function generates the reference matrix of probabilities of selecting bits for mutation. 

def ga_mono_agent_mutation_probability (bin_info_variable_list, total_binary_len):
    
    ##bin_info_variable_list --- the list of variables and its corresponding attributes, with binary attributes    
    ##total_binary_len --- total length of binary bits for all represented variables 
    
    
    dim_bin_info_variable_list = bin_info_variable_list.shape
    
    ##Ensuring that each variable has an equal chance of being mutated 
    num_var = dim_bin_info_variable_list[0]
    var_prob = 1 / num_var 
    
    ind_var_prob = []
    
    for i in range (0, num_var):
        ##Performing linear ranking
        prob = range(1, bin_info_variable_list['Bits'][i] + 1)
        denom = sum(prob)
        for j in range (0, bin_info_variable_list['Bits'][i]):
            bit_prob = (prob[j] / denom) * var_prob
            ind_var_prob.append(bit_prob)
            
    return ind_var_prob