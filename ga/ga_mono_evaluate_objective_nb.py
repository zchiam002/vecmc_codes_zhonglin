##This function evaluates the objective of the related problem 
##This is also the script which the problem definition should be placed.

def ga_mono_evaluate_objective_nb (variable_values, iteration_number):
    
    ##variable_values           --- the values of the decision variables stored in a list 
    ##iteration_number          --- unique ID number for parallel processing purposes (if needed)
    
    import os 
    function_path = os.path.dirname(os.path.abspath(__file__)) + '\\'           ##Incase of the need to use relative directory
    import sys
    sys.path.append(function_path + '')
    
    objective_value = original_test_func (variable_values)

    return objective_value

#########################################################################################################################################################################
#########################################################################################################################################################################
##This is a test function to test the GA
    ##Rastrigin function -5.12 <= x_i <= 5.12
def original_test_func (variable_values):
    
    import math
    ##There are only 4 inputs to the variable_values
    ##The input to this function has to be in the form of a list
    x = variable_values
    objective_value = (10*len(x)) 
    
    for i in range (0, len(x)):
        temp = pow(x[i], 2) - (10*math.cos(2 * 3.142 * x[i]))
        objective_value = objective_value + temp
    
    return objective_value

#if __name__ == '__main__':
#    variable_values = [-5.344431644,0.899512478,3.028129792,0.01297007]
#    objective_value = original_test_func (variable_values)
#    print(objective_value)