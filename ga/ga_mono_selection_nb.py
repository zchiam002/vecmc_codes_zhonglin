##This script contains functions to perform the selection process

def ga_mono_selection_nb (agents_obj_val_fitness, num_var_per_agent, selection_choice, selection_choice_data, crossover_perc):
    
    ##agents_obj_val_fitness --- values of x, obj_values and fitness values
    ##num_var_per_agent --- the number of variables per agent 
    ##selection_choice --- the mode of selecting the better agents
    ##selection_choice_data --- a dictionary containing data needed for various selection choices
    ##crossover_perc --- the percentage of the population to form the parent pool for crossovers
    
    if selection_choice == 'roulette_wheel':
        parent_pool, crossover_duty = ga_mono_roulette_wheel_nb (agents_obj_val_fitness, num_var_per_agent, crossover_perc)
    elif selection_choice == 'tournament_selection':
        parent_pool, crossover_duty = ga_mono_tournament_selection_nb (agents_obj_val_fitness, num_var_per_agent, crossover_perc, selection_choice_data)

    return parent_pool, crossover_duty

#######################################################################################################################################
##Additional functions 

##This is the roulette wheel function 
def ga_mono_roulette_wheel_nb (agents_obj_val_fitness, num_var_per_agent, crossover_perc):
    
    import numpy as np

    ##agents_obj_val_fitness --- values of x, obj_values and fitness values, sorted by decreasing fitness values 
    ##num_var_per_agent --- the number of variables per agent 
    ##crossover_perc --- the percentage of the population to form the parent pool for crossovers

    dim_agents_obj_val_fitness = agents_obj_val_fitness.shape 
    
    ##Determining the parent pool size 
    orginal_pop_size = dim_agents_obj_val_fitness[0]
    selected_parent_size = int(crossover_perc * orginal_pop_size)
    
    ##Determining the number of child agents which the crossover function has to fulfil 
    crossover_duty = orginal_pop_size - selected_parent_size
    
    ##Creating a copy for deletion purposes, so that the same parent is not selected twice    
    copied_agents_obj_val_fitness = np.copy(agents_obj_val_fitness)
    ##Initializing an empty parent pool
    parent_pool = np.zeros((selected_parent_size, dim_agents_obj_val_fitness[1]))
    
    ##This process will be very slow if the num_var_per_agent is too long 
    
    for i in range (0, selected_parent_size):
        ##Determining the size of the current numpy array 
        dim_copied_agents_obj_val_fitness = copied_agents_obj_val_fitness.shape
        ##Creating a probability_reference list 
        probability_reference = copied_agents_obj_val_fitness[:, num_var_per_agent + 1]
        ##Normalize probability_reference, making sure that their sum is equals to 1
        probability_reference = [float(j)/sum(probability_reference) for j in probability_reference]
        chosen_value = np.random.choice(np.arange(0, dim_copied_agents_obj_val_fitness[0]), p = probability_reference)
        ##Appending the parent pool
        parent_pool[i, :] = copied_agents_obj_val_fitness[chosen_value, :]
        ##Deleting the row from the copied array 
        copied_agents_obj_val_fitness = np.delete(copied_agents_obj_val_fitness, chosen_value, 0)
        
    return parent_pool, crossover_duty

##This is the tournament selection function
def ga_mono_tournament_selection_nb (agents_obj_val_fitness, num_var_per_agent, crossover_perc, selection_choice_data):
    
    import numpy as np 
    
    ##agents_obj_val_fitness --- values of x, obj_values and fitness values, sorted by decreasing fitness values 
    ##num_var_per_agent --- the number of variables per agent 
    ##crossover_perc --- the percentage of the population to form the parent pool for crossovers
    ##selection_choice_data --- a dictionary containing data needed for various selection choices

    dim_agents_obj_val_fitness = agents_obj_val_fitness.shape 
    
    ##Determining the parent pool size 
    orginal_pop_size = dim_agents_obj_val_fitness[0]
    selected_parent_size = int(crossover_perc * orginal_pop_size)
    
    ##Determining the number of child agents which the crossover function has to fulfil 
    crossover_duty = orginal_pop_size - selected_parent_size
    
    ##Creating a copy for deletion purposes, so that the same parent is not selected twice    
    copied_agents_obj_val_fitness = np.copy(agents_obj_val_fitness) 
    ##Initializing an empty parent pool
    parent_pool = np.zeros((selected_parent_size, dim_agents_obj_val_fitness[1]))    
    tournament_size = int(selection_choice_data['tournament_size'])
    for i in range (0, selected_parent_size):
        
        ##Determining the size of the copied_pool
        dim_copied_agents_obj_val_fitness = copied_agents_obj_val_fitness.shape
        ##This is the current population size
        curr_pop_size = dim_copied_agents_obj_val_fitness[0]
        ##Selecting the required number of agents at random for tournament selection 
        selection_range = range(curr_pop_size)
        selected_agents_for_tournament = np.random.choice(selection_range, tournament_size, replace=False)
        ##Indexing the current array 
        copied1_array = np.copy(copied_agents_obj_val_fitness)
        selection_range_nparray = np.zeros((dim_copied_agents_obj_val_fitness[0], 1))
        
        for j in range(0, dim_copied_agents_obj_val_fitness[0]):
            selection_range_nparray[j,0] = j
            
        copied1_array = np.concatenate((copied1_array, selection_range_nparray), axis = 1)
        
        ##Forming a numpy array for the selected agents
        dim_copied1_array = copied1_array.shape
        selected_agents_data = np.zeros((tournament_size, dim_copied1_array[1]))

        ##Copying the data over 
        for j in range (0, tournament_size):
            index = selected_agents_for_tournament[j]
            selected_agents_data[j,:] = copied1_array[index, :]
        
        ##Sort this temporary matrix according to the objective function values 
        sorted_selected_agents = selected_agents_data[np.argsort(selected_agents_data[:,dim_copied1_array[1]-3])]
        best_selected_agent_index = int(sorted_selected_agents[0, dim_copied1_array[1]-1])
        
        ##Appending the selected values to the parent_pool
        parent_pool[i, :] = copied_agents_obj_val_fitness[best_selected_agent_index, :]

        ##Deleting the selected row from the 
        copied_agents_obj_val_fitness = np.delete(copied_agents_obj_val_fitness, best_selected_agent_index, 0)
    
    return parent_pool, crossover_duty


    


