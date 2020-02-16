##This function evaluates the objective of the related problem 
##This is also ths script which the problem definition should be placed.

def ga_mono_evaluate_objective (variable_values, iteration_number):
    
    import sys 
    sys.path.append('C:\\Optimization_zlc\\control_center\\paper_ga_only_case\\')
    from ga_scsd_run_ea import ga_scsd_run_ea
    
    objective_value = ga_scsd_run_ea (variable_values, iteration_number)

    return objective_value

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