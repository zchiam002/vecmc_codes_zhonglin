##This function adds the constraints to the model 
def smtpgpy_add_constraints (grb_model, input_dataframes, utilitylist, processlist, layerslist, bilinear_pieces, var_continuous_dict, var_binary_dict):
    
    import gurobipy as grb 
    import sys 
    sys.path.append('C:\\Optimization_zlc\\slave_convex_handlers\\solve_mono_time_problem_gurobipy_addons\\additional_functions\\')
    from check_if_item_in_list_smtpgpy import check_if_item_in_list_smtpgpy
    from append_constraint_based_on_sign_smtpgpy import append_constraint_based_on_sign_smtpgpy
    
    ##grb_model --- the gurobipy model 
    ##input_dataframes, utilitylist, processlist, layerslist --- list of processed data
    ##bilinearpieces --- the number of bilinear pieces
    ##var_continuous_dict --- dictionary of all gurobipy continuous variables 
    ##var_binary_dict --- dictionary of all gurobipy binary variables
    
    ##Index tracker 
    current_index = 0
    
    ##Fmin and Fmax constraints for utilities and processes
        ##Utilities
        ##Utilities linear
    dim_utilitieslinear = input_dataframes['utilitylist_linear'].shape
    
    for i in range (0, dim_utilitieslinear[0]):
        var_name_temp = input_dataframes['utilitylist_linear']['Parent'][i] + '_' + input_dataframes['utilitylist_linear']['Name'][i]
        var_name_temp_y = input_dataframes['utilitylist_linear']['Parent'][i] + '_y'
        fmin_temp = input_dataframes['utilitylist_linear']['Fmin'][i]
        fmax_temp = input_dataframes['utilitylist_linear']['Fmax'][i]        
        
        ##Appending the Fmin constraint 
        curr_constraint = 0
        curr_constraint = curr_constraint + (fmin_temp * var_binary_dict[var_name_temp_y]) - (var_continuous_dict[var_name_temp])
        grb_model.addConstr(curr_constraint <= 0, 'c' + str(current_index))
        current_index = current_index + 1
        
        ##Appending the Fmax constraint 
        curr_constraint = 0
        curr_constraint = curr_constraint + (var_continuous_dict[var_name_temp]) - (fmax_temp * var_binary_dict[var_name_temp_y]) 
        grb_model.addConstr(curr_constraint <= 0, 'c' + str(current_index))
        current_index = current_index + 1
        
        ##Utilities bilinear
    dim_utilitiesbilinear = input_dataframes['utilitylist_bilinear'].shape
    
    for i in range (0, dim_utilitiesbilinear[0]):
        var_name_temp = input_dataframes['utilitylist_bilinear']['Name'][i]
        var_name_temp_y = var_name_temp + '_y'
        fmin_temp = input_dataframes['utilitylist_bilinear']['Fmin'][i]
        fmax_temp = input_dataframes['utilitylist_bilinear']['Fmax'][i]

        ##Appending the Fmin constraint 
        curr_constraint = 0
        curr_constraint = curr_constraint + (fmin_temp * var_binary_dict[var_name_temp_y]) - (var_continuous_dict[var_name_temp])
        grb_model.addConstr(curr_constraint <= 0, 'c' + str(current_index))
        current_index = current_index + 1
        
        ##Appending the Fmax constraint 
        curr_constraint = 0
        curr_constraint = curr_constraint + (var_continuous_dict[var_name_temp]) - (fmax_temp * var_binary_dict[var_name_temp_y]) 
        grb_model.addConstr(curr_constraint <= 0, 'c' + str(current_index))
        current_index = current_index + 1

        ##Fmin and Fmax conatraint in relation to x and y for utilities
    dim_utilitylist = utilitylist.shape 
    
    check_list = input_dataframes['utilitylist_bilinear']['Parent'][:]
    
    for i in range (0, dim_utilitylist[0]):
        check_value = check_if_item_in_list_smtpgpy (check_list, utilitylist['Name'][i])                    ##The variable is affected by RLT
        if  check_value == 1:            
            base_parent_name_onoff = utilitylist['Name'][i] + '_y'
            
            x_fmin_value = utilitylist['Fmin_v1'][i] * 2
            x_fmax_value = utilitylist['Fmax_v1'][i] * 2
            y_fmin_value = utilitylist['Fmin_v2'][i] * 2
            y_fmax_value = utilitylist['Fmax_v2'][i] * 2
            
            u_term_temp = 0
            v_term_temp = 0
            
            for j in range (0, bilinear_pieces):
                base_name_u = utilitylist['Name'][i] + '_u' + str(j)
                base_name_v = utilitylist['Name'][i] + '_v' + str(j)          
                
                u_term_temp = u_term_temp + var_continuous_dict[base_name_u]
                v_term_temp = v_term_temp + var_continuous_dict[base_name_v]

            
            ##Appending the Fmin of 2x = u + v
            curr_constraint = 0
            curr_constraint = curr_constraint + (x_fmin_value * var_binary_dict[base_parent_name_onoff]) - (u_term_temp) - (v_term_temp)
            grb_model.addConstr(curr_constraint <= 0, 'c' + str(current_index))  
            current_index = current_index + 1  
            
            ##Appending the Fmax of 2x = u + v 
            curr_constraint = 0
            curr_constraint = curr_constraint + (u_term_temp) + (v_term_temp) - (x_fmax_value * var_binary_dict[base_parent_name_onoff])
            grb_model.addConstr(curr_constraint <= 0, 'c' + str(current_index))  
            current_index = current_index + 1             
            
            ##Appending the Fmin of 2y = u - v
            curr_constraint = 0
            curr_constraint = curr_constraint + (y_fmin_value * var_binary_dict[base_parent_name_onoff]) - (u_term_temp) + (v_term_temp)
            grb_model.addConstr(curr_constraint <= 0, 'c' + str(current_index))  
            current_index = current_index + 1  
            
            ##Appending the Fmax of 2y = u - v
            curr_constraint = 0
            curr_constraint = curr_constraint + (u_term_temp) - (v_term_temp) - (y_fmax_value * var_binary_dict[base_parent_name_onoff])
            grb_model.addConstr(curr_constraint <= 0, 'c' + str(current_index))  
            current_index = current_index + 1              
            
        ##Processes
        ##Process linear
    dim_processeslinear = input_dataframes['processlist_linear'].shape
    
    for i in range (0, dim_processeslinear[0]):
        var_name_temp = input_dataframes['processlist_linear']['Parent'][i] + '_' + input_dataframes['processlist_linear']['Name'][i]
        var_name_temp_y = input_dataframes['processlist_linear']['Parent'][i] + '_y'
        fmax_temp = input_dataframes['processlist_linear']['Fmax'][i]        
        
        ##Appending the 'Fmin' constraint to ensure that it is always at the maximum value 
        curr_constraint = 0
        curr_constraint = curr_constraint + (var_continuous_dict[var_name_temp])
        grb_model.addConstr(curr_constraint == fmax_temp, 'c' + str(current_index))
        current_index = current_index + 1
        
        ##Appending the constraint which ensures that the binary variable is always on 
        curr_constraint = 0
        curr_constraint = curr_constraint + (var_binary_dict[var_name_temp_y]) 
        grb_model.addConstr(curr_constraint == 1, 'c' + str(current_index))
        current_index = current_index + 1
        
        ##Processes bilinear
    dim_processesbilinear = input_dataframes['processlist_bilinear'].shape
    
    for i in range (0, dim_processesbilinear[0]):
        var_name_temp = input_dataframes['processlist_bilinear']['Name'][i]
        var_name_temp_y = var_name_temp + '_y'
        fmin_temp = input_dataframes['processlist_bilinear']['Fmin'][i]
        fmax_temp = input_dataframes['processlist_bilinear']['Fmax'][i]

        ##Appending the Fmin constraint 
        curr_constraint = 0
        curr_constraint = curr_constraint + (fmin_temp * var_binary_dict[var_name_temp_y]) - (var_continuous_dict[var_name_temp])
        grb_model.addConstr(curr_constraint <= 0, 'c' + str(current_index))
        current_index = current_index + 1
        
        ##Appending the Fmax constraint 
        curr_constraint = 0
        curr_constraint = curr_constraint + (var_continuous_dict[var_name_temp]) - (fmax_temp * var_binary_dict[var_name_temp_y]) 
        grb_model.addConstr(curr_constraint <= 0, 'c' + str(current_index))
        current_index = current_index + 1

        ##Fmin and Fmax conatraint in relation to x and y for processes
    dim_processlist = processlist.shape 
    
    check_list = input_dataframes['processlist_bilinear']['Parent'][:]
    
    for i in range (0, dim_processlist[0]):
        check_value = check_if_item_in_list_smtpgpy (check_list, processlist['Name'][i])                    ##The variable is affected by RLT
        if  check_value == 1:            
            base_parent_name_onoff = processlist['Name'][i] + '_y'
            
            x_fmin_value = processlist['Fmin_v1'][i] * 2
            x_fmax_value = processlist['Fmax_v1'][i] * 2
            y_fmin_value = processlist['Fmin_v2'][i] * 2
            y_fmax_value = processlist['Fmax_v2'][i] * 2
            
            u_term_temp = 0
            v_term_temp = 0
            
            for j in range (0, bilinear_pieces):
                base_name_u = processlist['Name'][i] + '_u' + str(j)
                base_name_v = processlist['Name'][i] + '_v' + str(j)          
                
                u_term_temp = u_term_temp + var_continuous_dict[base_name_u]
                v_term_temp = v_term_temp + var_continuous_dict[base_name_v]

            
            ##Appending the Fmin of 2x = u + v
            curr_constraint = 0
            curr_constraint = curr_constraint + (u_term_temp) + (v_term_temp)
            grb_model.addConstr(curr_constraint >= x_fmin_value, 'c' + str(current_index))  
            current_index = current_index + 1  
            
            ##Appending the Fmax of 2x = u + v 
            curr_constraint = 0
            curr_constraint = curr_constraint + (u_term_temp) + (v_term_temp) 
            grb_model.addConstr(curr_constraint >= x_fmax_value, 'c' + str(current_index))  
            current_index = current_index + 1             
            
            ##Appending the Fmin of 2y = u - v
            curr_constraint = 0
            curr_constraint = curr_constraint + (u_term_temp) - (v_term_temp)
            grb_model.addConstr(curr_constraint >= y_fmin_value, 'c' + str(current_index))  
            current_index = current_index + 1  
            
            ##Appending the Fmax of 2y = u - v
            curr_constraint = 0
            curr_constraint = curr_constraint + (u_term_temp) - (v_term_temp)
            grb_model.addConstr(curr_constraint <= y_fmax_value, 'c' + str(current_index))  
            current_index = current_index + 1    
            
    ##Stream constraints 
    dim_layerslist = layerslist.shape 
    dim_streams_linear = input_dataframes['streams_linear'].shape
    dim_streams_bilinear = input_dataframes['streams_bilinear'].shape
    
    for i in range (0, dim_layerslist[0]):
        current_layer = layerslist['Name'][i]
        ##Differentiating by type  
        if layerslist['Type'][i] == 'balancing_only':    
            ##Initiating a variable to hold the in and out values 
            temp_in = 0
            temp_out = 0
            
            ##Scanning through the linear stream list 
            for j in range (0, dim_streams_linear[0]):
                if input_dataframes['streams_linear']['Layer'][j] == current_layer:
                    if input_dataframes['streams_linear']['InOut'][j] == 'in':            
                        var_name_temp = input_dataframes['streams_linear']['Parent'][j] + '_' + input_dataframes['streams_linear']['Variable'][j]
                        temp_in = temp_in + (input_dataframes['streams_linear']['Flow_grad'][j] * var_continuous_dict[var_name_temp])
                        temp_in = temp_in + (input_dataframes['streams_linear']['Flow_min'][j] * var_binary_dict[input_dataframes['streams_linear']['Parent'][j] + '_y'])
                    elif input_dataframes['streams_linear']['InOut'][j] == 'out':
                        var_name_temp = input_dataframes['streams_linear']['Parent'][j] + '_' + input_dataframes['streams_linear']['Variable'][j]
                        temp_out = temp_out + (input_dataframes['streams_linear']['Flow_grad'][j] * var_continuous_dict[var_name_temp])
                        temp_out = temp_out + (input_dataframes['streams_linear']['Flow_min'][j] * var_binary_dict[input_dataframes['streams_linear']['Parent'][j] + '_y'])
            
            ##Scanning through the bilinear stream list 
            for j in range (0, dim_streams_bilinear[0]):
                if input_dataframes['streams_bilinear']['Layer'][j] == current_layer:                
                    if input_dataframes['streams_bilinear']['InOut'][j] == 'in':
                        var_name_temp = input_dataframes['streams_bilinear']['Variable'][j]            
                        temp_in = temp_in + (input_dataframes['streams_bilinear']['Flow_grad'][j] * var_continuous_dict[var_name_temp])
                        temp_in = temp_in + (input_dataframes['streams_bilinear']['Flow_min'][j] * var_binary_dict[var_name_temp + '_y'])   
                    elif input_dataframes['streams_bilinear']['InOut'][j] == 'out':
                        var_name_temp = input_dataframes['streams_bilinear']['Variable'][j]   
                        temp_out = temp_out + (input_dataframes['streams_bilinear']['Flow_grad'][j] * var_continuous_dict[var_name_temp])
                        temp_out = temp_out + (input_dataframes['streams_bilinear']['Flow_min'][j] * var_binary_dict[var_name_temp + '_y'])
                        
            ##Appending the constraint 
            curr_constraint = 0
            curr_constraint = temp_in - temp_out
            grb_model.addConstr(curr_constraint == 0, 'c' + str(current_index))  
            current_index = current_index + 1         
            
        elif (layerslist['Type'][i] == 'temp_chil') or (layerslist['Type'][i] == 'pressure') or (layerslist['Type'][i] == 'energy_reverse') or (layerslist['Type'][i] == 'flow_reverse'):                        
            ##Initiating a variable to hold the in and out values 
            temp_in = 0
            temp_out = 0
            
            ##Scanning through the linear stream list 
            for j in range (0, dim_streams_linear[0]):
                if input_dataframes['streams_linear']['Layer'][j] == current_layer:
                    if input_dataframes['streams_linear']['InOut'][j] == 'in':            
                        var_name_temp = input_dataframes['streams_linear']['Parent'][j] + '_' + input_dataframes['streams_linear']['Variable'][j]
                        temp_in = temp_in + (input_dataframes['streams_linear']['Flow_grad'][j] * var_continuous_dict[var_name_temp])
                        temp_in = temp_in + (input_dataframes['streams_linear']['Flow_min'][j] * var_binary_dict[input_dataframes['streams_linear']['Parent'][j] + '_y'])
                    elif input_dataframes['streams_linear']['InOut'][j] == 'out':
                        var_name_temp = input_dataframes['streams_linear']['Parent'][j] + '_' + input_dataframes['streams_linear']['Variable'][j]
                        temp_out = temp_out + (input_dataframes['streams_linear']['Flow_grad'][j] * var_continuous_dict[var_name_temp])
                        temp_out = temp_out + (input_dataframes['streams_linear']['Flow_min'][j] * var_binary_dict[input_dataframes['streams_linear']['Parent'][j] + '_y'])
            
            ##Scanning through the bilinear stream list 
            for j in range (0, dim_streams_bilinear[0]):
                if input_dataframes['streams_bilinear']['Layer'][j] == current_layer:                
                    if input_dataframes['streams_bilinear']['InOut'][j] == 'in':
                        var_name_temp = input_dataframes['streams_bilinear']['Variable'][j]            
                        temp_in = temp_in + (input_dataframes['streams_bilinear']['Flow_grad'][j] * var_continuous_dict[var_name_temp])
                        temp_in = temp_in + (input_dataframes['streams_bilinear']['Flow_min'][j] * var_binary_dict[var_name_temp + '_y'])   
                    elif input_dataframes['streams_bilinear']['InOut'][j] == 'out':
                        var_name_temp = input_dataframes['streams_bilinear']['Variable'][j]   
                        temp_out = temp_out + (input_dataframes['streams_bilinear']['Flow_grad'][j] * var_continuous_dict[var_name_temp])
                        temp_out = temp_out + (input_dataframes['streams_bilinear']['Flow_min'][j] * var_binary_dict[var_name_temp + '_y'])            

            ##Appending the constraint 
            curr_constraint = 0
            curr_constraint = temp_in - temp_out
            grb_model.addConstr(curr_constraint >= 0, 'c' + str(current_index))  
            current_index = current_index + 1    

        elif (layerslist['Type'][i] == 'flow') or (layerslist['Type'][i] == 'energy'):
            ##Initiating a variable to hold the in and out values 
            temp_in = 0
            temp_out = 0
            
            ##Scanning through the linear stream list 
            for j in range (0, dim_streams_linear[0]):
                if input_dataframes['streams_linear']['Layer'][j] == current_layer:
                    if input_dataframes['streams_linear']['InOut'][j] == 'in':            
                        var_name_temp = input_dataframes['streams_linear']['Parent'][j] + '_' + input_dataframes['streams_linear']['Variable'][j]
                        temp_in = temp_in + (input_dataframes['streams_linear']['Flow_grad'][j] * var_continuous_dict[var_name_temp])
                        temp_in = temp_in + (input_dataframes['streams_linear']['Flow_min'][j] * var_binary_dict[input_dataframes['streams_linear']['Parent'][j] + '_y'])
                    elif input_dataframes['streams_linear']['InOut'][j] == 'out':
                        var_name_temp = input_dataframes['streams_linear']['Parent'][j] + '_' + input_dataframes['streams_linear']['Variable'][j]
                        temp_out = temp_out + (input_dataframes['streams_linear']['Flow_grad'][j] * var_continuous_dict[var_name_temp])
                        temp_out = temp_out + (input_dataframes['streams_linear']['Flow_min'][j] * var_binary_dict[input_dataframes['streams_linear']['Parent'][j] + '_y'])
            
            ##Scanning through the bilinear stream list 
            for j in range (0, dim_streams_bilinear[0]):
                if input_dataframes['streams_bilinear']['Layer'][j] == current_layer:                
                    if input_dataframes['streams_bilinear']['InOut'][j] == 'in':
                        var_name_temp = input_dataframes['streams_bilinear']['Variable'][j]            
                        temp_in = temp_in + (input_dataframes['streams_bilinear']['Flow_grad'][j] * var_continuous_dict[var_name_temp])
                        temp_in = temp_in + (input_dataframes['streams_bilinear']['Flow_min'][j] * var_binary_dict[var_name_temp + '_y'])   
                    elif input_dataframes['streams_bilinear']['InOut'][j] == 'out':
                        var_name_temp = input_dataframes['streams_bilinear']['Variable'][j]   
                        temp_out = temp_out + (input_dataframes['streams_bilinear']['Flow_grad'][j] * var_continuous_dict[var_name_temp])
                        temp_out = temp_out + (input_dataframes['streams_bilinear']['Flow_min'][j] * var_binary_dict[var_name_temp + '_y'])            

            ##Appending the constraint 
            curr_constraint = 0
            curr_constraint = temp_in - temp_out
            grb_model.addConstr(curr_constraint <= 0, 'c' + str(current_index))  
            current_index = current_index + 1 
    
    ##Additional constraints
    
    dim_cons_eqns_all = input_dataframes['cons_eqns_all'].shape
    dim_cons_eqns_terms_linear = input_dataframes['cons_eqns_terms_linear'].shape
    dim_cons_eqns_terms_bilinear = input_dataframes['cons_eqns_terms_bilinear'].shape
    
    ##Appending the unit binary constraints 
    for i in range (0, dim_cons_eqns_all[0]):
        if input_dataframes['cons_eqns_all']['Type'][i] == 'unit_binary':    
            eqn_name_temp = input_dataframes['cons_eqns_all']['Name'][i]
            sign_temp = input_dataframes['cons_eqns_all']['Sign'][i]
            rhs_value = input_dataframes['cons_eqns_all']['RHS_value'][i]
            lhs_value = 0            
            ##Scanning through the linear list first
            for j in range (0, dim_cons_eqns_terms_linear[0]):
                if input_dataframes['cons_eqns_terms_linear']['Parent_eqn'][j] == eqn_name_temp:
                    var_temp_name = input_dataframes['cons_eqns_terms_linear']['Parent_unit'][j] + '_y'
                    lhs_value = lhs_value + (input_dataframes['cons_eqns_terms_linear']['Coefficient'][j] * var_binary_dict[var_temp_name])
            ##Scanning through the bilinear list next 
            for j in range (0, dim_cons_eqns_terms_bilinear[0]):
                if input_dataframes['cons_eqns_terms_bilinear']['Parent_eqn'][j] == eqn_name_temp:                
                    var_temp_name = input_dataframes['cons_eqns_terms_bilinear']['Variable'][j] + '_y'                    
                    lhs_value = lhs_value + (input_dataframes['cons_eqns_terms_bilinear']['Coefficient'][j] * var_binary_dict[var_temp_name])    
            ##Appending the constraint
            grb_model, current_index = append_constraint_based_on_sign_smtpgpy (grb_model, lhs_value, rhs_value, sign_temp, current_index)
    
    ##Appending the unit binary equality constraint 
    for i in range (0, dim_cons_eqns_all[0]):
        if input_dataframes['cons_eqns_all']['Type'][i] == 'unit_binary_equality':
            eqn_name_temp = input_dataframes['cons_eqns_all']['Name'][i]
            sign_temp = input_dataframes['cons_eqns_all']['Sign'][i]
            rhs_value = input_dataframes['cons_eqns_all']['RHS_value'][i]
            lhs_value = 0
            ##Scanning through the linear list first
            for j in range (0, dim_cons_eqns_terms_linear[0]):
                if input_dataframes['cons_eqns_terms_linear']['Parent_eqn'][j] == eqn_name_temp:
                    var_temp_name = input_dataframes['cons_eqns_terms_linear']['Parent_unit'][j] + '_y'
                    lhs_value = lhs_value + (input_dataframes['cons_eqns_terms_linear']['Coefficient'][j] * var_binary_dict[var_temp_name])
            ##Scanning through the bilinear list next 
            for j in range (0, dim_cons_eqns_terms_bilinear[0]):
                if input_dataframes['cons_eqns_terms_bilinear']['Parent_eqn'][j] == eqn_name_temp:                
                    var_temp_name = input_dataframes['cons_eqns_terms_bilinear']['Variable'][j] + '_y'                    
                    lhs_value = lhs_value + (input_dataframes['cons_eqns_terms_bilinear']['Coefficient'][j] * var_binary_dict[var_temp_name])    
            ##Appending the constraint
            grb_model, current_index = append_constraint_based_on_sign_smtpgpy (grb_model, lhs_value, rhs_value, sign_temp, current_index)            
            
    ##Appending the stream_limit_modified constraints 
    for i in range (0, dim_cons_eqns_all[0]):                    
        if input_dataframes['cons_eqns_all']['Type'][i] == 'stream_limit_modified':
            eqn_name_temp = input_dataframes['cons_eqns_all']['Name'][i]            
            sign_temp = input_dataframes['cons_eqns_all']['Sign'][i]            
            rhs_value = input_dataframes['cons_eqns_all']['RHS_value'][i]
            lhs_value = 0         
            ##Scanning through the linear list first
            for j in range (0, dim_cons_eqns_terms_linear[0]):
                if input_dataframes['cons_eqns_terms_linear']['Parent_eqn'][j] == eqn_name_temp:
                    var_temp_name = input_dataframes['cons_eqns_terms_linear']['Parent_unit'][j] + '_' + input_dataframes['cons_eqns_terms_linear']['Variable'][j]
                    var_temp_name_y = input_dataframes['cons_eqns_terms_linear']['Parent_unit'][j] + '_y'
                    lhs_value = lhs_value + (input_dataframes['cons_eqns_terms_linear']['Grad'][j] * var_continuous_dict[var_temp_name])
                    lhs_value = lhs_value + (input_dataframes['cons_eqns_terms_linear']['Cst'][j] * var_binary_dict[var_temp_name_y])
            ##Scanning through the bilinear list next 
            for j in range (0, dim_cons_eqns_terms_bilinear[0]):
                if input_dataframes['cons_eqns_terms_bilinear']['Parent_eqn'][j] == eqn_name_temp:                
                    var_temp_name = input_dataframes['cons_eqns_terms_bilinear']['Variable'][j]
                    var_temp_name_y = var_temp_name + '_y'
                    lhs_value = lhs_value + (input_dataframes['cons_eqns_terms_bilinear']['Grad'][j] * var_continuous_dict[var_temp_name])
                    lhs_value = lhs_value + (input_dataframes['cons_eqns_terms_bilinear']['Cst'][j] * var_binary_dict[var_temp_name_y])     
            ##Appending the constraint 
            grb_model, current_index = append_constraint_based_on_sign_smtpgpy (grb_model, lhs_value, rhs_value, sign_temp, current_index)        
    
    ##Appending the bilinear_limits_fmin_util constraints, only affects cons_eqns_terms_bilinear
    for i in range (0, dim_cons_eqns_all[0]):                         
        if input_dataframes['cons_eqns_all']['Type'][i] == 'bilinear_limits_fmin_util':  
            eqn_name_temp = input_dataframes['cons_eqns_all']['Name'][i]                        
            parent_coeff = input_dataframes['cons_eqns_all']['RHS_value'][i]
            lhs_value = 0            
            ##Scanning through the bilinear list 
            for j in range (0, dim_cons_eqns_terms_bilinear[0]):
                if input_dataframes['cons_eqns_terms_bilinear']['Parent_eqn'][j] == eqn_name_temp:                
                    var_temp_name = input_dataframes['cons_eqns_terms_bilinear']['Variable'][j]
                    var_temp_name_y = var_temp_name + '_y'
                    lhs_value = lhs_value + (input_dataframes['cons_eqns_terms_bilinear']['Grad'][j] * var_continuous_dict[var_temp_name])
                    lhs_value = lhs_value + (input_dataframes['cons_eqns_terms_bilinear']['Cst'][j] * var_binary_dict[var_temp_name_y])
            ##Appending the constraint
            parent_binary = eqn_name_temp.replace('_bilin_cons_fmin', '_y')            
            lhs_value = lhs_value - (parent_coeff * var_binary_dict[parent_binary])
            grb_model, current_index = append_constraint_based_on_sign_smtpgpy (grb_model, lhs_value, 0, 'greater_than_equal_to', current_index)

    ##Appending the bilinear_limits_fmax_util constraints, only affects cons_eqns_terms_bilinear                          
    for i in range (0, dim_cons_eqns_all[0]):                         
        if input_dataframes['cons_eqns_all']['Type'][i] == 'bilinear_limits_fmax_util':  
            eqn_name_temp = input_dataframes['cons_eqns_all']['Name'][i]                       
            parent_coeff = input_dataframes['cons_eqns_all']['RHS_value'][i]
            lhs_value = 0              
            ##Scanning through the bilinear list 
            for j in range (0, dim_cons_eqns_terms_bilinear[0]):
                if input_dataframes['cons_eqns_terms_bilinear']['Parent_eqn'][j] == eqn_name_temp:                
                    var_temp_name = input_dataframes['cons_eqns_terms_bilinear']['Variable'][j]
                    var_temp_name_y = var_temp_name + '_y'
                    lhs_value = lhs_value + (input_dataframes['cons_eqns_terms_bilinear']['Grad'][j] * var_continuous_dict[var_temp_name])
                    lhs_value = lhs_value + (input_dataframes['cons_eqns_terms_bilinear']['Cst'][j] * var_binary_dict[var_temp_name_y])
            ##Appending the constraint 
            parent_binary = eqn_name_temp.replace('_bilin_cons_fmax', '_y')            
            lhs_value = lhs_value - (parent_coeff * var_binary_dict[parent_binary])
            grb_model, current_index = append_constraint_based_on_sign_smtpgpy (grb_model, lhs_value, 0, 'less_than_equal_to', current_index)  

    ##Appending the bilinear_limits_fmax_proc constraints, only affects cons_eqns_terms_bilinear, only fmax is needed for processes as it is an equality    
    for i in range (0, dim_cons_eqns_all[0]):                         
        if input_dataframes['cons_eqns_all']['Type'][i] == 'bilinear_limits_fmax_proc':  
            eqn_name_temp = input_dataframes['cons_eqns_all']['Name'][i]                       
            rhs_value = input_dataframes['cons_eqns_all']['RHS_value'][i]
            lhs_value = 0                            
            ##Scanning through the bilinear list 
            for j in range (0, dim_cons_eqns_terms_bilinear[0]):
                if input_dataframes['cons_eqns_terms_bilinear']['Parent_eqn'][j] == eqn_name_temp:                
                    var_temp_name = input_dataframes['cons_eqns_terms_bilinear']['Variable'][j]
                    var_temp_name_y = var_temp_name + '_y'
                    lhs_value = lhs_value + (input_dataframes['cons_eqns_terms_bilinear']['Grad'][j] * var_continuous_dict[var_temp_name])
                    lhs_value = lhs_value + (input_dataframes['cons_eqns_terms_bilinear']['Cst'][j] * var_binary_dict[var_temp_name_y])  
            ##Appending the constraints 
            parent_binary = eqn_name_temp.replace('_bilin_cons_fmax', '_y')
            grb_model, current_index = append_constraint_based_on_sign_smtpgpy (grb_model, lhs_value, rhs_value, 'equal_to', current_index)
            grb_model, current_index = append_constraint_based_on_sign_smtpgpy (grb_model, parent_binary, 1, 'equal_to', current_index)  
                    
    return grb_model
