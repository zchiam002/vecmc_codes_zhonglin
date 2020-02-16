##This function performs the mutation of the newly generated pool 

def ga_mono_mutation_nb (parent_pool, child_pool, mutation_perc, dec_info_variable_list):
    
    import numpy as np
    import math
    import random
    
    ##parent_pool --- the pool of original selected parents
    ##child_pool --- the offsprings of the parents 
    ##mutation_perc --- the percentage of the total variables which will be switched
    ##dec_info_variable_list --- information about the variable type as well as the upper and lower bounds
    
    ##Combining the parent and child pools 
    combined_pool = np.concatenate((parent_pool, child_pool), axis = 0)
    
    ##Determining the total number of variables in the pool
    dim_combined_pool = combined_pool.shape 
    number_of_variables_per_agent = dim_combined_pool[1] - 2                  ##The last 2 columns are for the objective function and the fitness respectively 
    total_variables = number_of_variables_per_agent * dim_combined_pool[0]
    
    variables_to_mutate = math.ceil(mutation_perc * total_variables)
    
    ##Making a copy of the combined_pool
    combined_pool_copy = np.copy(combined_pool)
    
    for i in range (0, variables_to_mutate):
       row = np.random.choice(range(dim_combined_pool[0]))
       column = np.random.choice(range(dim_combined_pool[1] - 2))
       
       ##Determining the information about the randomly selected variable, still working with intervals only 
       variable_interval = dec_info_variable_list['Interval'][column]       
       randomly_mutated_variable = random.randint(0, variable_interval)
       
       combined_pool_copy[row, column] = randomly_mutated_variable
      

    return combined_pool_copy