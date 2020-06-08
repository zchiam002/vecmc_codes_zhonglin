##Function to evaluate the objective functions for the given input vector x. x is an array of decision variables 
##and f(1), f(2), etc are the objective functions. The algorithm always minimizes the objective function hence if 
##you would like to maximize the function then multiply the function by negative one.

def nsga_ii_para_imple_evaluate_objective (variable_values, num_obj_func, iteration_number):

    ##variable_values       --- the array of variable values to be evaluated 
    ##num_obj_func          --- the nuber of objective functions to evaluate 
    ##iteration_number      --- a unique number so that saving the file name will be unique
    
    import numpy as np
    
    ##Creating a numpy array to store the objective function values 
    objective_values = np.zeros((1, num_obj_func))
    
    ##Iterating based on the number of objective functions to be evaluated 
    for i in range (0, num_obj_func):
        objective_values[0,i] = kursawe_function_moo (variable_values, i)
        
    return objective_values

######################################################################################################################################################################################
##Test functions 
       
##This is the kursawe test function 
       ## -5 <= x_i <= 5
       ## 1 <= i <= 3
       ## num_obj_func = 2
       
def kursawe_function_moo (x, obj_to_evaluate):
    
    ##x --- the list of variable values 
    ##obj_to_evaluate --- the objective function to evaluate 
    
    import math 
    
    ##Determining the number of variables to be evaluated
    num_var = len(x)
    
    ##Determining which objective function to evaluate 
    if obj_to_evaluate == 0:
        ret_obj = 0
        for i in range (0, num_var-1):
            v1 = x[i]
            v2 = x[i+1]
            ret_obj = ret_obj + (-10 * math.exp(-0.2 * math.sqrt(pow(v1, 2) + pow(v2, 2))))
            
    elif obj_to_evaluate == 1:
        ret_obj = 0
        for i in range (0, num_var):
            v1 = x[i]
            if v1 < 0:
                ret_obj = ret_obj + (pow(-v1, 0.8) + (5 * math.sin(pow(v1, 3))))
            else:
                ret_obj = ret_obj + (pow(v1, 0.8) + (5 * math.sin(pow(v1, 3))))    

    return ret_obj
                                         
 