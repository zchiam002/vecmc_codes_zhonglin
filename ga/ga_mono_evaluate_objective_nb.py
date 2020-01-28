##This function evaluates the objective of the related problem 
##This is also ths script which the problem definition should be placed.

def ga_mono_evaluate_objective_nb (variable_values, iteration_number):
    
    import os 
    function_path = os.path.dirname(os.path.abspath(__file__))[:-42] + '\\'    
    import sys
    sys.path.append(function_path + 'control_center\\chiller_optimization_dist_nwk_ga_nb\\')
    from ga_scsd_run_ea_nb import ga_scsd_run_ea_nb
    
    objective_value = ga_scsd_run_ea_nb (variable_values, iteration_number)

    return objective_value

