##This script contains functions to perform the crossover process

def ga_mono_crossover(parent_pool, crossover_duty):
    import numpy as np 
    import copy 
    
    ##parent_pool --- the selected chromosomes for crossover purposes, by standard convention 
        ##last column --- fitness value 
        ##2nd last column --- objective function 
    ##crossover duty --- the number of child chromosomes needed 
    
    dim_parent_pool = parent_pool.shape
    ##Determine the total number of combinations possible 
    total_binary_len = dim_parent_pool[1] - 2
    ##Initialize an array containing a list of parents
    parents_array = []
    for i in range (0, dim_parent_pool[0]):
        parents_array.append(i)
    ##Initialize an array for the possible split points 
    split = []
    for i in range (1, total_binary_len - 1):
        split.append(i)
    
    ##Initialize a numpy array to store the child values 
    child_ret = np.zeros((crossover_duty, dim_parent_pool[1]))

    ##Performing the crossover 
    for i in range (0, crossover_duty):
        ##Copying the array for manipulations
        parents_array_copied = copy.copy(parents_array)
        
        ##Selecting parent 1 
        parent1_index = np.random.choice(parents_array_copied)
        ##Removing parent 1 index from the choices 
        parents_array_copied.remove(parents_array_copied[parent1_index])
        ##Selecting parent 2
        parent2_index = np.random.choice(parents_array_copied)
        
        ##Selecting the crossover point 
        crossover_point = np.random.choice(split)
        
        ##Copying the parents array 
        parent1 = parent_pool[parent1_index, :-2]
        parent2 = parent_pool[parent2_index, :-2]
        
        ##Forming the child arrays 
        child_p1 = parent1[0:crossover_point]
        child_p2 = parent2[crossover_point:total_binary_len]
        
        child = np.append(child_p1, child_p2)
        ##Empty columns for the fitness values and the objective function
        child = np.append(child, [0, 0])        
        child_ret[i, :] = child    

    return child_ret