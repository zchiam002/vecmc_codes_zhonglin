##This is a sub function to determine if a parsed 1D array contains a given value 

def contains_value(array, value):
    return_value = 0
    dim_array = len(array)
    for i in range (0, dim_array-1):
        if array[i] == value:
            return_value = 1
            break
    
    return return_value
    

