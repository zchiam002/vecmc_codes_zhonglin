##This function handles all the backend operation for communicating with GLPK involving multi-objective 

def slave_convex_backend_v3 (files, multi_time, obj_func, package_name, parallel_thread_num, slave_models_location, bilinear_pieces, solver_choice, obj_weights, time_steps): 

    ##Setting hyper parameters for gurobipy
    save_file = 'no'                    ##To export csv files for debugging purposes
    show_optimal_solution = 'yes'           ##To view the optimal values
    write_lp_file = 'no'                   ##To export the LP file of the model   
    
    ##First check if earlier versions can do the job
    if solver_choice != 'gurobipy':
        if multi_time == 0:
            obj_value, results, results_y = scbv3_earlier_editions (files, multi_time, obj_func, package_name, parallel_thread_num, slave_models_location, bilinear_pieces, solver_choice, obj_weights, time_steps)
            return obj_value, results, results_y
        else:
            obj_value, results, results_y, ind_obj_value, obj_func_table_dict = scbv3_earlier_editions (files, multi_time, obj_func, package_name, parallel_thread_num, slave_models_location, bilinear_pieces, solver_choice, obj_weights, time_steps)
            return obj_value, results, results_y, ind_obj_value, obj_func_table_dict
    
    ##Else use the python interface
    elif solver_choice == 'gurobipy':
        if multi_time == 0:
            obj_value, results, results_y = gurobipy_mono_time_backened (files, multi_time, obj_func, package_name, parallel_thread_num, slave_models_location, bilinear_pieces, solver_choice, save_file, show_optimal_solution, write_lp_file)
            return obj_value, results, results_y
        else:
            print('not ready')
        
        
    
    
                
    return obj_value, results, results_y, ind_obj_value, obj_func_table_dict
        
        
        
####################################################################################################################################################################################
##Additional functions 

##This function exists to determine type of problem and allocate it to earlier backend versions to handle 
def scbv3_earlier_editions (files, multi_time, obj_func, package_name, parallel_thread_num, slave_models_location, bilinear_pieces, solver_choice, obj_weights, time_steps):
    
    import sys
    sys.path.append('C:\\Optimization_zlc\\slave_convex_handlers\\')
    
    ##Not a multi-time problem and 
    if multi_time == 0:
        from slave_convex_backend import slave_convex_backend
        
        obj_value, results, results_y = slave_convex_backend (files, multi_time, obj_func, package_name, parallel_thread_num, slave_models_location, bilinear_pieces, solver_choice)
        
        return obj_value, results, results_y
    
    else:
        from slave_convex_backend_v2 import slave_convex_backend_v2
        
        obj_value, results, results_y, ind_obj_value, obj_func_table_dict = slave_convex_backend_v2 (files, multi_time, obj_func, package_name, parallel_thread_num, slave_models_location, bilinear_pieces, solver_choice, obj_weights, time_steps)                
        
        return obj_value, results, results_y, ind_obj_value, obj_func_table_dict

##This function handles mono_time 
def gurobipy_mono_time_backened (files, multi_time, obj_func, package_name, parallel_thread_num, slave_models_location, bilinear_pieces, solver_choice, save_file, show_optimal_solution, write_lp_file):

    ##Not a multi-time problem
    import pandas as pd
    import sys
    sys.path.append('C:\\Optimization_zlc\\slave_convex_handlers\\auxillary')                       ##Add directories to working directories 
    from get_values_models import get_values_models
    sys.path.append('C:\\Optimization_zlc\\slave_convex_handlers')
    sys.path.append(slave_models_location)
    from sorting_linear_and_bilinear_terms import sorting_linear_and_bilinear_terms
    from genscript_lp_format import genscript_lp_format
    from lpsolver_runscript import lpsolver_runscript
    from extract_and_process_values import extract_and_process_values
    from slave_convex_backend import save_function
    from solve_mono_time_problem_gurobipy import solve_mono_time_problem_gurobipy
    
    ##Getting the values from the models
    layerslist, utilitylist, processlist, streams, cons_eqns, cons_eqns_terms = get_values_models(files, package_name, parallel_thread_num, slave_models_location) 
    
    ##Linearizing the bilinear terms 
    ret_dataframes, affected_list = sorting_linear_and_bilinear_terms (layerslist, utilitylist, processlist, streams, cons_eqns, cons_eqns_terms, obj_func, bilinear_pieces)

    ##Save function for debug
    save_function (ret_dataframes, layerslist, utilitylist, processlist, streams, cons_eqns, cons_eqns_terms, save_file)
    
    ##Running and solving the optimization problem with gurobipy
    obj_value, results, results_y = solve_mono_time_problem_gurobipy (ret_dataframes, utilitylist, processlist, layerslist, parallel_thread_num, obj_func, bilinear_pieces, show_optimal_solution, write_lp_file)
    
    return obj_value, results, results_y