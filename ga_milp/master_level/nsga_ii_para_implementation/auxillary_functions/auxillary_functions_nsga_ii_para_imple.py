##This script contains auxillary functions required for the parallel implementation of nsga_II

##This function converts the variables into the form processible by the nsga_ii original implementation 
def reconfigure_hyper_params (population, generations, num_obj_func, selection_choice_data, crossover_perc, mutation_distribution_index, variable_list, 
                              initial_variable_values, parallel_process, obj_func_plot, cores_used, crossover_distribution_index, mutation_perc):
    
    ##population --- the number of agents in a given population 
    ##generations --- the number of generations to run the algorithm for
    ##num_obj_func --- the number of objective functions 
    ##selection_choice_data --- the additional hyperparameters pertaining to the chosen selection_choice 
    ##crossover_perc --- the percentage of the initial population to select as parents to generate child agents 
    ##mutation_distribution_index --- a probability figure for the individual undergoing mutation
    ##crossover_distribution_index --- a probability figure for the individual undergoing crossover
    ##mutation_perc --- the probability the individual undergoes mutation 
    ##variable_list --- a dataframe of variables and their corresponding attributes 
    ##initial_variable_values --- the initial seeds for the initial population 
    ##parallel_process --- yes/no
    ##obj_func_plot --- a dynamic graph of objective function values 
    ##cores_used --- the number of cores used
    
    ##Initialize dictionary to hold the values 
    input_v = {}
    
    ##Appending the hyper parameters for the nsga_II algoirthm 
    input_v['population'] = population
    input_v['generations'] = generations
    input_v['num_obj_func'] = num_obj_func    
    input_v['selection_choice_data'] = selection_choice_data
    input_v['crossover_perc'] = crossover_perc
    input_v['mutation_distribution_index'] = mutation_distribution_index
    input_v['mutation_perc'] = mutation_perc
    input_v['crossover_distribution_index'] = crossover_distribution_index    
    input_v['variable_list'] = variable_list
    input_v['initial_variable_values'] = initial_variable_values
    input_v['parallel_process'] = parallel_process
    input_v['obj_func_plot'] = obj_func_plot
    input_v['cores_used'] = cores_used        
    
    return input_v


##This is a sort function, it takes in the column number to be sorted by and returns the index of the sorting order 
##index refers to the initial row number before sorting 
def index_sort_by_column(matrix, column_num):
    import numpy as np
    
    dim = matrix.shape 
    sorted_m = np.zeros((dim[0], dim[1]+1))
    
    for i in range (0, dim[0]):
        for j in range (0, dim[1]):
            sorted_m[i,j] = matrix[i,j]
        sorted_m[i,dim[1]] = i
    
    sorted_m = sorted_m[np.argsort(sorted_m[:, column_num])]
    index = sorted_m[:, dim[1]]
    
    return index

##This is a sub function to determine if a parsed 1D array contains a given value 
def contains_value(array, value):
    return_value = 0
    dim_array = len(array)
    for i in range (0, dim_array-1):
        if array[i] == value:
            return_value = 1
            break
    
    return return_value

##This is a sub function which returns the position of the minimum value in the given array of values 
def find_min_max_pos(min_max, array):
    dim_array = len(array)
    dup = []
    
    if min_max == 'min':
        for i in range (0, dim_array):          ##Finding the minimum vale 
            if i < 1:
                min_val = array[i]
                min_pos = i
            else:
                if array[i] < min_val:
                    min_val = array[i]
                    min_pos = i
        dup.append(min_pos)
        
        for i in range (0, dim_array):          ##Adding values for duplidates 
            if i != min_pos:
                if array[i] == min_val:
                    dup.append(i)
                    
    if min_max == 'max':
        for i in range (0, dim_array):          ##Finding the maximum vale 
            if i < 1:
                max_val = array[i]
                max_pos = i
            else:
                if array[i] > max_val:
                    max_val = array[i]
                    max_pos = i
        dup.append(max_pos)
        
        for i in range (0, dim_array):          ##Adding values for duplidates 
            if i != max_pos:
                if array[i] == max_val:
                    dup.append(i)        
    
    return dup

##This is a sub function which will compare 2 1D arrays and return a value if they are exactly identical 

def identical_array (array1, array2):
    
    dim_array1 = len(array1)
    dim_array2 = len(array2)
    
    count = 0
    if dim_array1 == dim_array2:
        for i in range (0, dim_array1):
            if array1[i] == array2[i]:
                count = count + 1
        if count == dim_array1:
            value = 1
        else:
            value = 0
    else:
        value = 0

    return value 

##This sub function finds the maximum index of an element in a matrix when the given condition is true 

def find_max_index (matrix, column, value):
    import numpy as np
    dim_matrix = matrix.shape 
    placeholder = np.zeros((1,2))
    
    for i in range (0, dim_matrix[0]):
        if matrix[i,column] == value:
            if (placeholder[0,0] == 0) and (placeholder[0,1] == 0):
                placeholder[0,0] = matrix[i, column]
                placeholder[0,1] = i
            else:
                temp = [matrix[i, column], i]
                placeholder = np.concatenate((placeholder, [temp]), axis=0)
    
    dim_placeholder = placeholder.shape
    pos = []
    for i in range (0, dim_placeholder[0]):
        pos.append(placeholder[i,1])
        
    max_pos = max(pos)
    
    return max_pos 

    