##This script takes in input values and run the decidated python function once, returning an output value in an easily accessible format for matlab to read and use 

def fmincon_run_function():
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\nsgaII_glpk_v1\\')
    from overall_exe import ecoenergies_opt
    import numpy as np
    
    ##Reading values from temperory csv file, these values should come from the matlab optimizer 
    x = np.genfromtxt('C:\\Optimization_zlc\\master_level\\Matlab_Optimizers\\Fmincon\\temp_value_storage\\test_value_in.csv', delimiter = ',')
    
    ##Preparing the values in the format for the python function 
    num_variables = len(x) / 24
    return_value = ecoenergies_opt(x, num_variables)
    #print(return_value)
    
    ##Writing the return values into csv file format to ensure that matlab can access it 
    output_data_value = open('C:\\Optimization_zlc\\master_level\\Matlab_Optimizers\\Fmincon\\temp_value_storage\\test_value_out.csv','w')
    output_data_value.write(str(return_value)+ ' ')
    output_data_value.close
    
    return