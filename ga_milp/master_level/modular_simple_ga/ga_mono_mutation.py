##This function performs the mutation of the newly generated pool 

def ga_mono_mutation (parent_pool, child_pool, mutation_perc, mutation_prob):
    
    import numpy as np
    import math
    
    ##parent_pool --- the pool of original selected parents
    ##child_pool --- the offsprings of the parents 
    ##mutation_perc --- the percentage of the total bits which will be switched
    ##mutation_prob --- the probability of bits mutation
    
    ##Combining the parent and child pools 
    combined_pool = np.concatenate((parent_pool, child_pool), axis = 0)
    
    ##Determining the total number of bits
    dim_combined_pool = combined_pool.shape 
    bit_len = dim_combined_pool[1] - 2                  ##The last 2 columns are for the objective function and the fitness respectively 
    total_bits = bit_len * dim_combined_pool[0]
    
    bits_to_mutate = math.ceil(mutation_perc * total_bits)
    
    ##Making a copy of the combined_pool
    combined_pool_copy = np.copy(combined_pool)
    
    for i in range (0, bits_to_mutate):
       row = np.random.choice(range(dim_combined_pool[0]))
       column = np.random.choice(range(dim_combined_pool[1] - 2), p = mutation_prob)
       if int(combined_pool_copy[row, column]) == 0:
           combined_pool_copy[row, column] = 1
       else:
           combined_pool_copy[row, column] = 0

    return combined_pool_copy