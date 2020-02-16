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
    

