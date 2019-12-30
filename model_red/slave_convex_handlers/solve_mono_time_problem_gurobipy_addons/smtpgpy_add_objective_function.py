##This function adds terms to the objective function 
def smtpgpy_add_objective_function (grb_model, input_dataframes, utilitylist, processlist, obj_func, var_continuous_dict, var_binary_dict):
    
    import gurobipy as grb
    import sys 
    sys.path.append('C:\\Optimization_zlc\\slave_convex_handlers\\solve_mono_time_problem_gurobipy_addons\\additional_functions\\')
    from obj_function_detect_smtpgpy import obj_function_detect_smtpgpy
    
    ##grb_model --- the gurobipy model 
    ##input_dataframes, utilitylist, processlist --- list of processed data
    ##obj_func --- the associated objective function 
    ##var_continuous_dict --- dictionary of all gurobipy continuous variables 
    ##var_binary_dict --- dictionary of all gurobipy binary variables
    
    ##Determining the objective function key 
    key = obj_function_detect_smtpgpy (obj_func)
    
    ##Initializing an empty placeholder for the objective function 
    cum_obj_func = 0
    
    ##Appending the objective function list for the strictly linear terms
        ##Handling utilities 
    dim_utilitylist_linear = input_dataframes['utilitylist_linear'].shape
    dim_utilitylist_bilinear = input_dataframes['utilitylist_bilinear'].shape
    
        ##Utilities linear terms
    prev_name_y = ''                                                              ##So that there is no double entry of binary variables 
    for i in range (0, dim_utilitylist_linear[0]):
        temp_name = input_dataframes['utilitylist_linear']['Parent'][i] + '_' + input_dataframes['utilitylist_linear']['Name'][i] 
        temp_name_y = input_dataframes['utilitylist_linear']['Parent'][i] + '_y'
        temp_var = var_continuous_dict[temp_name]
        temp_var_y = var_binary_dict[temp_name_y]
        temp_grad = input_dataframes['utilitylist_linear'][key + '1'][i]
        temp_int = input_dataframes['utilitylist_linear'][key + '2'][i]
    
        if temp_name_y != prev_name_y:
            cum_obj_func = cum_obj_func + (temp_var * temp_grad)
            cum_obj_func = cum_obj_func + (temp_var_y * temp_int)
            prev_name_y = temp_name_y                
        else:
            cum_obj_func = cum_obj_func + (temp_var * temp_grad)

        ##Utilities bilinear terms 
    for i in range (0, dim_utilitylist_bilinear[0]):
        temp_name = input_dataframes['utilitylist_bilinear']['Name'][i]
        temp_name_y = temp_name + '_y'
        temp_var = var_continuous_dict[temp_name]
        temp_var_y = var_binary_dict[temp_name_y]
        temp_grad = input_dataframes['utilitylist_bilinear'][key + '1'][i]
        temp_int = input_dataframes['utilitylist_bilinear'][key + '2'][i]
        
        cum_obj_func = cum_obj_func + (temp_var * temp_grad)
        cum_obj_func = cum_obj_func + (temp_var_y * temp_int)                        


        ##Handling processes 
    dim_processlist_linear = input_dataframes['processlist_linear'].shape
    dim_processlist_bilinear = input_dataframes['processlist_bilinear'].shape
    
        ##Processes linear terms
    prev_name_y = ''                                                              ##So that there is no double entry of binary variables 
    for i in range (0, dim_processlist_linear[0]):
        temp_name = input_dataframes['processlist_linear']['Parent'][i] + '_' + input_dataframes['processlist_linear']['Name'][i] 
        temp_name_y = input_dataframes['processlist_linear']['Parent'][i] + '_y'
        temp_var = var_continuous_dict[temp_name]
        temp_var_y = var_binary_dict[temp_name_y]
        temp_grad = input_dataframes['processlist_linear'][key + '1'][i]
        temp_int = input_dataframes['processlist_linear'][key + '2'][i]
        
        if temp_name_y != prev_name_y:
            cum_obj_func = cum_obj_func + (temp_var * temp_grad)
            cum_obj_func = cum_obj_func + (temp_var_y * temp_int)
            prev_name_y = temp_name_y                
        else:
            cum_obj_func = cum_obj_func + (temp_var * temp_grad) 

        ##Process bilinear terms 
    for i in range (0, dim_processlist_bilinear[0]):
        temp_name = input_dataframes['processlist_bilinear']['Name'][i]
        temp_name_y = temp_name + '_y'
        temp_var = var_continuous_dict[temp_name]
        temp_var_y = var_binary_dict[temp_name_y]
        temp_grad = input_dataframes['processlist_bilinear'][key + '1'][i]
        temp_int = input_dataframes['processlist_bilinear'][key + '2'][i]

        cum_obj_func = cum_obj_func + (temp_var * temp_grad)
        cum_obj_func = cum_obj_func + (temp_var_y * temp_int)  
        
    ##Adding the objective function into the model 
    grb_model.setObjective(cum_obj_func, grb.GRB.MINIMIZE)        

    return grb_model