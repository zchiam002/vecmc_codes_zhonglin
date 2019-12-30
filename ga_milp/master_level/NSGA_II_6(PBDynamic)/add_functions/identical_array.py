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