##This is the evaluate objective function for the slave formulation 

def ga_scsd_run_ea (variables, iteration):
    
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level\\reinforcement_learning\\state_independent\\')
    from rl_evaluate_objective import test_function_Rastrigin
    
    ##Preparing values 
    pseudo_state = [1]
    return_value = test_function_Rastrigin(pseudo_state, variables)
    
    print('input', variables)
    print('obj_funct', return_value)
    
    return return_value