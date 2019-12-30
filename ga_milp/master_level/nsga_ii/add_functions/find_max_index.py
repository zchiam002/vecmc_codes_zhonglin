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
