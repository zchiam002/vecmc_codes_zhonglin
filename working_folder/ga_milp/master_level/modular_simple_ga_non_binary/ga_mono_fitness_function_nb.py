##This function is used to calculate the fitness function values of the given population 

def ga_mono_fitness_function_nb (agents_and_obj_vals):
    
   import numpy as np

   ##agents_and_obj_vals --- a numpy array with the values of variables and objective function values
       ##the objective function values are stored in the final columns of the numpy array 
       
   ##This method of defining the fitness values is relative to each population.
   ##The highest fitness values are always given to the agents with the lowest objective function values 
   ##As population size is usually not that large, there is no need for parallel computation here.
   
   dim_agents_and_obj_vals = agents_and_obj_vals.shape
   
   ##Initializing a return array to avoid making changes to original array 
   ret_values = agents_and_obj_vals
   
   ##Sorting the matrices based on the objective function values 
   sorted_ret_values = ret_values[np.argsort(ret_values[:,dim_agents_and_obj_vals[1]-1])]   
      
   ##Initializing a temporary matrix to hold the fitness values assigned based on maximization method 
   max_format_fitness = []
   ##Calculating the sum of all of the objective function values for the given population
   sum_obj_func_values = sum(sorted_ret_values[:, dim_agents_and_obj_vals[1]-1])
   
   for i in range (0, dim_agents_and_obj_vals[0]):
       temp_fitness = sorted_ret_values[i, dim_agents_and_obj_vals[1]-1] / sum_obj_func_values
       max_format_fitness.append(temp_fitness)
       
   ##Creating a new matrix to store return values 
   ##Additional column is for the fitness values
   ret_vals_with_fitness = np.zeros((dim_agents_and_obj_vals[0], dim_agents_and_obj_vals[1] + 1))
   ret_vals_with_fitness[:, :-1] = sorted_ret_values
   
   ##Filling in the fitness values in reverse order
   for i in range (0, dim_agents_and_obj_vals[0]):
       ret_vals_with_fitness[i, dim_agents_and_obj_vals[1]] = max_format_fitness[dim_agents_and_obj_vals[0] - (1 + i)]
    
   return ret_vals_with_fitness