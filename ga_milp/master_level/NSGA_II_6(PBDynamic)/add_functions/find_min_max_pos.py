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
