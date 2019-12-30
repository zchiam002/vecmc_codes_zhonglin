##This function takes in dataframes and solve the mono-time problem using gurobipy

def solve_mono_time_problem_gurobipy (input_dataframes, utilitylist, processlist, layerslist, parallel_thread_num, obj_func, bilinear_pieces, show_optimal_solution, write_lp_file):

    from datetime import datetime
    startTime = datetime.now()
    import gurobipy as grb
    import sys 
    sys.path.append('C:\\Optimization_zlc\\slave_convex_handlers\\solve_mono_time_problem_gurobipy_addons\\')
    from smtpgpy_add_variables import smtpgpy_add_variables
    from smtpgpy_add_objective_function import smtpgpy_add_objective_function
    from smtpgpy_add_constraints import smtpgpy_add_constraints
    
    
    ##Legend of the inputs
    
    ##input_dataframes = {}                                     --- it is a dictionary of dataframes
    ##input_dataframes['utilitylist_bilinear']                  --- list of bilinear utilities 
    ##input_dataframes['processlist_bilinear']                  --- list of bilinear processes
    ##input_dataframes['streams_bilinear']                      --- list of bilinear streams 
    ##input_dataframes['cons_eqns_terms_bilinear']              --- list of bilinear cons_eqns_terms
    ##input_dataframes['utilitylist_linear']                    --- linear utility list 
    ##input_dataframes['processlist_linear']                    --- linear process list 
    ##input_dataframes['streams_linear']                        --- linear streams list 
    ##input_dataframes['cons_eqns_terms_linear']                --- linear cons_eqns_terms 
    ##input_dataframes['cons_eqns_all']                         --- all cons_eqns
    
    ##utilitylist --- the list of all the utilities
    ##processlist --- the list of all the processes
    ##layerslist --- the list of layers 
    ##parallel_thread_num --- the number to append for the directory to be unique 
    ##obj_func --- the objective function, it can be of 4 types 
    ##bilinear_pieces --- the number of bilinear pieces    
    
    ##Create a gurobi MILP new model 
    model = grb.Model('milp_model_id_' + str(parallel_thread_num))
    model.setParam('OutputFlag', 0)
    
    ##Input variables 
    model, var_continuous_dict, var_binary_dict = smtpgpy_add_variables (model, input_dataframes, utilitylist, processlist)  
    ##Input objective fuctions
    model = smtpgpy_add_objective_function (model, input_dataframes, utilitylist, processlist, obj_func, var_continuous_dict, var_binary_dict)
    ##Input constraints 
    model = smtpgpy_add_constraints (model, input_dataframes, utilitylist, processlist, layerslist, bilinear_pieces, var_continuous_dict, var_binary_dict)     
    ##Writing lp file for debugging
    if write_lp_file == 'yes':
        model.write('C:\\Optimization_zlc\\slave_convex_handlers\\gurobi_user\\model.lp')
        
    ##Optimizing the model
    model.optimize()
    
    #Print the feasible solution if optimal.
    if model.status == grb.GRB.Status.OPTIMAL:
        obj_value = model.objVal
        if show_optimal_solution == 'yes':
            import pandas as pd 
            result_dataframe = pd.DataFrame(columns = ['Name', 'Value'])
            for v in model.getVars():
                temp_name = v.varName
                temp_value = v.x
                temp_data = [temp_name, temp_value]
                temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value'])
                result_dataframe = result_dataframe.append(temp_df, ignore_index = True)
            from extract_and_process_values import convert_back_to_original  
            results, results_y = convert_back_to_original (result_dataframe, utilitylist, processlist, bilinear_pieces)
        else:
            results = 'not_shown'
            results_y = 'not_shown'            
    else:
        obj_value = 'na'
        results = 'na'
        results_y = 'na'    
    
    print(datetime.now() - startTime)    
    return obj_value, results, results_y





