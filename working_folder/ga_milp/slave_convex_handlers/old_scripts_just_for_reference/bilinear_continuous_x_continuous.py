
def bilinear_continuous_x_continuous (continuous_x_continuous_terms, bilinear_pieces):
    
    import pandas as pd
    
    ##continuous_x_continuous_terms['objective_function_utility_bilinear']
    ##continuous_x_continuous_terms['dual_variable_constraint_utility_bilinear']
    ##continuous_x_continuous_terms['objective_function_process_bilinear']
    ##continuous_x_continuous_terms['dual_variable_constraint_process_bilinear'] 
    ##continuous_x_continuous_terms['streams_bilinear']
    ##continuous_x_continuous_terms['cons_eqn_terms_bilinear']  
    
    ##bilinear_pieces --- the number of bilinear splits 
    ##obj_func --- helps to deal with the associated objective function to perform the spilt
    
    ##General approach 
    ##1. Find the original limits of x+y and x-y
    ##2. Determine the number of pieces 
    ##3. Find the individual limits 
    ##4. Find the new coefficients 
    ##5. Write the new constraints of each piece, attack the constants

#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################

    ##Handling objective_function_utility_bilinear
    dim_objective_function_utility_bilinear = continuous_x_continuous_terms['objective_function_utility_bilinear'].shape
    
    ##Packaging the new details into a DataFrame in the separated units form for each linearized piece  
    obj_func_u_bilin_new = pd.DataFrame(columns = ['Name_parent', 'Variable1_parent', 'Variable2_parent', 'Name', 'Variable', 'Fmin_v1', 'Fmax_v1', 'Coeff', 'Intercept'])
        
    for i in range (0, dim_objective_function_utility_bilinear[0]):
        ##Determine limts for x+y and x-y 
        l_lim1 = continuous_x_continuous_terms['objective_function_utility_bilinear']['Fmin_v1'][i]
        u_lim1 = continuous_x_continuous_terms['objective_function_utility_bilinear']['Fmax_v1'][i]
        l_lim2 = continuous_x_continuous_terms['objective_function_utility_bilinear']['Fmin_v2'][i]
        u_lim2 = continuous_x_continuous_terms['objective_function_utility_bilinear']['Fmax_v2'][i]
        
        ##Determining the limits for x + y
        l_lim_func1 = l_lim1 + l_lim2
        u_lim_func1 = u_lim1 + u_lim2
        
        ##Derermining the limits for x - y
        l_lim_func2 = l_lim1 - u_lim2
        u_lim_func2 = u_lim1 - l_lim2
        
        ##Determining the individual coefficients for each of the limits 
        lim_func1_steps = (u_lim_func1 - l_lim_func1) / bilinear_pieces
        lim_func2_steps = (u_lim_func2 - l_lim_func2) / bilinear_pieces
        
        for j in range (0, bilinear_pieces):
            l_lim_func1_temp = l_lim_func1 + j*lim_func1_steps
            u_lim_func1_temp = l_lim_func1 + (j+1)*lim_func1_steps
            l_lim_func2_temp = l_lim_func2 + j*lim_func2_steps
            u_lim_func2_temp = l_lim_func2 + (j+1)*lim_func2_steps

            ##Finding the linear coefficients to the piecewise quadratic parts, reason is 0.5(u2 - v2) = xy 
            l_lim_func12_temp = 0.5 * pow(l_lim_func1_temp, 2)
            u_lim_func12_temp = 0.5 * pow(u_lim_func1_temp, 2)
            
            if (u_lim_func1_temp - l_lim_func1_temp) == 0:
                coeff_func1 = 0
                cst_func1 = 0
            else:
                coeff_func1 = (u_lim_func12_temp - l_lim_func12_temp) / (u_lim_func1_temp - l_lim_func1_temp)
                cst_func1 = u_lim_func12_temp - coeff_func1*u_lim_func1_temp
                
            l_lim_func22_temp = 0.5 * pow(l_lim_func2_temp, 2)
            u_lim_func22_temp = 0.5 * pow(u_lim_func2_temp, 2)
            
            if (u_lim_func2_temp - l_lim_func2_temp) == 0:
                coeff_func2 = 0
                cst_func2 = 0
            else:
                coeff_func2 = (u_lim_func22_temp - l_lim_func22_temp) / (u_lim_func2_temp - l_lim_func2_temp)
                cst_func2 = u_lim_func22_temp - coeff_func2*u_lim_func2_temp
            
            ##Appending sub_unit u
            sub_unit_name = continuous_x_continuous_terms['objective_function_utility_bilinear']['Name'][i] + 'bl_u' + str(j)
            variable = 'u'
            temp_data = [continuous_x_continuous_terms['objective_function_utility_bilinear']['Name'][i], continuous_x_continuous_terms['objective_function_utility_bilinear']['Variable1'][i],
                         continuous_x_continuous_terms['objective_function_utility_bilinear']['Variable2'][i], sub_unit_name, variable, l_lim_func1_temp, u_lim_func1_temp, coeff_func1, cst_func1]
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['Name_parent', 'Variable1_parent', 'Variable2_parent', 'Name', 'Variable', 'Fmin_v1', 'Fmax_v1', 'Coeff', 'Intercept'])
            obj_func_u_bilin_new = obj_func_u_bilin_new.append(temp_data_df, ignore_index = True)
            
            ##Appending sub_unit v
            sub_unit_name = continuous_x_continuous_terms['objective_function_utility_bilinear']['Name'][i] + 'bl_v' + str(j)
            variable = 'v'
            temp_data = [continuous_x_continuous_terms['objective_function_utility_bilinear']['Name'][i], continuous_x_continuous_terms['objective_function_utility_bilinear']['Variable1'][i],
                         continuous_x_continuous_terms['objective_function_utility_bilinear']['Variable2'][i], sub_unit_name, variable, l_lim_func2_temp, u_lim_func2_temp, coeff_func2, cst_func2]
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['Name_parent', 'Variable1_parent', 'Variable2_parent', 'Name', 'Variable', 'Fmin_v1', 'Fmax_v1', 'Coeff', 'Intercept'])
            obj_func_u_bilin_new = obj_func_u_bilin_new.append(temp_data_df, ignore_index = True)            
                
#############################################################################################################################################################################################
############################################################################################################################################################################################
############################################################################################################################################################################################

    ##Handing the dual_variable_constraint_utility_bilinear
    dim_dual_variable_constraint_utility_bilinear = continuous_x_continuous_terms['dual_variable_constraint_utility_bilinear'].shape    

    ##Packaging the new details into a DataFrame in the separated units form for each linearized piece  
    dual_v_c_util_bilin_new = pd.DataFrame(columns = ['Name_parent', 'Variable1_parent', 'Variable2_parent', 'Name', 'Variable', 'Fmin_v1', 'Fmax_v1', 'Coeff', 'Intercept'])                
    
    for i in range (0, dim_dual_variable_constraint_utility_bilinear[0]):
        ##Determine limts for x+y and x-y 
        l_lim1 = continuous_x_continuous_terms['dual_variable_constraint_utility_bilinear']['Fmin_v1'][i]
        u_lim1 = continuous_x_continuous_terms['dual_variable_constraint_utility_bilinear']['Fmax_v1'][i]
        l_lim2 = continuous_x_continuous_terms['dual_variable_constraint_utility_bilinear']['Fmin_v2'][i]
        u_lim2 = continuous_x_continuous_terms['dual_variable_constraint_utility_bilinear']['Fmax_v2'][i]
        
        ##Determining the limits for x + y
        l_lim_func1 = l_lim1 + l_lim2
        u_lim_func1 = u_lim1 + u_lim2
        
        ##Derermining the limits for x - y
        l_lim_func2 = l_lim1 - u_lim2
        u_lim_func2 = u_lim1 - l_lim2
        
        ##Determining the individual coefficients for each of the limits 
        lim_func1_steps = (u_lim_func1 - l_lim_func1) / bilinear_pieces
        lim_func2_steps = (u_lim_func2 - l_lim_func2) / bilinear_pieces
        
        for j in range (0, bilinear_pieces):
            l_lim_func1_temp = l_lim_func1 + j*lim_func1_steps
            u_lim_func1_temp = l_lim_func1 + (j+1)*lim_func1_steps
            l_lim_func2_temp = l_lim_func2 + j*lim_func2_steps
            u_lim_func2_temp = l_lim_func2 + (j+1)*lim_func2_steps

            ##Finding the linear coefficients to the piecewise quadratic parts, reason is 0.5(u2 - v2) = xy  
            l_lim_func12_temp = 0.5 * pow(l_lim_func1_temp, 2)
            u_lim_func12_temp = 0.5 * pow(u_lim_func1_temp, 2)
            
            if (u_lim_func1_temp - l_lim_func1_temp) == 0:
                coeff_func1 = 0
                cst_func1 = 0
            else:
                coeff_func1 = (u_lim_func12_temp - l_lim_func12_temp) / (u_lim_func1_temp - l_lim_func1_temp)
                cst_func1 = u_lim_func12_temp - coeff_func1*u_lim_func1_temp
                
            l_lim_func22_temp = 0.5 * pow(l_lim_func2_temp, 2)
            u_lim_func22_temp = 0.5 * pow(u_lim_func2_temp, 2)
            
            if (u_lim_func2_temp - l_lim_func2_temp) == 0:
                coeff_func2 = 0
                cst_func2 = 0
            else:
                coeff_func2 = (u_lim_func22_temp - l_lim_func22_temp) / (u_lim_func2_temp - l_lim_func2_temp)
                cst_func2 = u_lim_func22_temp - coeff_func2*u_lim_func2_temp
            
            ##Appending sub_unit u
            sub_unit_name = continuous_x_continuous_terms['dual_variable_constraint_utility_bilinear']['Name'][i] + 'bl_u' + str(j)
            variable = 'u'
            temp_data = [continuous_x_continuous_terms['dual_variable_constraint_utility_bilinear']['Name'][i], continuous_x_continuous_terms['dual_variable_constraint_utility_bilinear']['Variable1'][i],
                         continuous_x_continuous_terms['dual_variable_constraint_utility_bilinear']['Variable2'][i], sub_unit_name, variable, l_lim_func1_temp, u_lim_func1_temp, coeff_func1, cst_func1]
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['Name_parent', 'Variable1_parent', 'Variable2_parent', 'Name', 'Variable', 'Fmin_v1', 'Fmax_v1', 'Coeff', 'Intercept'])
            dual_v_c_util_bilin_new = dual_v_c_util_bilin_new.append(temp_data_df, ignore_index = True)
            
            ##Appending sub_unit v
            sub_unit_name = continuous_x_continuous_terms['dual_variable_constraint_utility_bilinear']['Name'][i] + 'bl_v' + str(j)
            variable = 'v'
            temp_data = [continuous_x_continuous_terms['dual_variable_constraint_utility_bilinear']['Name'][i], continuous_x_continuous_terms['dual_variable_constraint_utility_bilinear']['Variable1'][i],
                         continuous_x_continuous_terms['dual_variable_constraint_utility_bilinear']['Variable2'][i], sub_unit_name, variable, l_lim_func2_temp, u_lim_func2_temp, coeff_func2, cst_func2]
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['Name_parent', 'Variable1_parent', 'Variable2_parent', 'Name', 'Variable', 'Fmin_v1', 'Fmax_v1', 'Coeff', 'Intercept'])
            dual_v_c_util_bilin_new = dual_v_c_util_bilin_new.append(temp_data_df, ignore_index = True)   
            
############################################################################################################################################################################################
############################################################################################################################################################################################
############################################################################################################################################################################################

    ##Handling objective_function_process_bilinear
    dim_objective_function_process_bilinear = continuous_x_continuous_terms['objective_function_process_bilinear'].shape 

    ##Packaging the new details into a DataFrame in the separated units form for each linearized piece  
    obj_func_p_bilin_new = pd.DataFrame(columns = ['Name_parent', 'Variable1_parent', 'Variable2_parent', 'Name', 'Variable', 'Fmin_v1', 'Fmax_v1', 'Coeff', 'Intercept'])  
    
    for i in range (0, dim_objective_function_process_bilinear[0]):
        ##Determine limts for x+y and x-y 
        l_lim1 = continuous_x_continuous_terms['objective_function_process_bilinear']['Fmin_v1'][i]
        u_lim1 = continuous_x_continuous_terms['objective_function_process_bilinear']['Fmax_v1'][i]
        l_lim2 = continuous_x_continuous_terms['objective_function_process_bilinear']['Fmin_v2'][i]
        u_lim2 = continuous_x_continuous_terms['objective_function_process_bilinear']['Fmax_v2'][i]
        
        ##Determining the limits for x + y
        l_lim_func1 = l_lim1 + l_lim2
        u_lim_func1 = u_lim1 + u_lim2
        
        ##Derermining the limits for x - y
        l_lim_func2 = l_lim1 - u_lim2
        u_lim_func2 = u_lim1 - l_lim2
        
        ##Determining the individual coefficients for each of the limits 
        lim_func1_steps = (u_lim_func1 - l_lim_func1) / bilinear_pieces
        lim_func2_steps = (u_lim_func2 - l_lim_func2) / bilinear_pieces
        
        for j in range (0, bilinear_pieces):
            l_lim_func1_temp = l_lim_func1 + j*lim_func1_steps
            u_lim_func1_temp = l_lim_func1 + (j+1)*lim_func1_steps
            l_lim_func2_temp = l_lim_func2 + j*lim_func2_steps
            u_lim_func2_temp = l_lim_func2 + (j+1)*lim_func2_steps

            ##Finding the linear coefficients to the piecewise quadratic parts, reason is 0.5(u2 - v2) = xy  
            l_lim_func12_temp = 0.5 * pow(l_lim_func1_temp, 2)
            u_lim_func12_temp = 0.5 * pow(u_lim_func1_temp, 2)
            
            if (u_lim_func1_temp - l_lim_func1_temp) == 0:
                coeff_func1 = 0
                cst_func1 = 0
            else:
                coeff_func1 = (u_lim_func12_temp - l_lim_func12_temp) / (u_lim_func1_temp - l_lim_func1_temp)
                cst_func1 = u_lim_func12_temp - coeff_func1*u_lim_func1_temp
                
            l_lim_func22_temp = 0.5 * pow(l_lim_func2_temp, 2)
            u_lim_func22_temp = 0.5 * pow(u_lim_func2_temp, 2)
            
            if (u_lim_func2_temp - l_lim_func2_temp) == 0:
                coeff_func2 = 0
                cst_func2 = 0
            else:
                coeff_func2 = (u_lim_func22_temp - l_lim_func22_temp) / (u_lim_func2_temp - l_lim_func2_temp)
                cst_func2 = u_lim_func22_temp - coeff_func2*u_lim_func2_temp
            
            ##Appending sub_unit u
            sub_unit_name = continuous_x_continuous_terms['objective_function_process_bilinear']['Name'][i] + 'bl_u' + str(j)
            variable = 'u'
            temp_data = [continuous_x_continuous_terms['objective_function_process_bilinear']['Name'][i], continuous_x_continuous_terms['objective_function_process_bilinear']['Variable1'][i],
                         continuous_x_continuous_terms['objective_function_process_bilinear']['Variable2'][i], sub_unit_name, variable, l_lim_func1_temp, u_lim_func1_temp, coeff_func1, cst_func1]
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['Name_parent', 'Variable1_parent', 'Variable2_parent', 'Name', 'Variable', 'Fmin_v1', 'Fmax_v1', 'Coeff', 'Intercept'])
            obj_func_p_bilin_new = obj_func_p_bilin_new.append(temp_data_df, ignore_index = True)
            
            ##Appending sub_unit v
            sub_unit_name = continuous_x_continuous_terms['objective_function_process_bilinear']['Name'][i] + 'bl_v' + str(j)
            variable = 'v'
            temp_data = [continuous_x_continuous_terms['objective_function_process_bilinear']['Name'][i], continuous_x_continuous_terms['objective_function_process_bilinear']['Variable1'][i],
                         continuous_x_continuous_terms['objective_function_process_bilinear']['Variable2'][i], sub_unit_name, variable, l_lim_func2_temp, u_lim_func2_temp, coeff_func2, cst_func2]
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['Name_parent', 'Variable1_parent', 'Variable2_parent', 'Name', 'Variable', 'Fmin_v1', 'Fmax_v1', 'Coeff', 'Intercept'])
            obj_func_p_bilin_new =  obj_func_p_bilin_new.append(temp_data_df, ignore_index = True)      
             
############################################################################################################################################################################################
############################################################################################################################################################################################
############################################################################################################################################################################################

    ##Handling dual_variable_constraint_process_bilinear
    dim_dual_variable_constraint_process_bilinear = continuous_x_continuous_terms['dual_variable_constraint_process_bilinear'].shape 

    ##Packaging the new details into a DataFrame in the separated units form for each linearized piece  
    dual_v_c_proc_bilin_new = pd.DataFrame(columns = ['Name_parent', 'Variable1_parent', 'Variable2_parent', 'Name', 'Variable', 'Fmin_v1', 'Fmax_v1', 'Coeff', 'Intercept'])    
    
    for i in range (0, dim_dual_variable_constraint_process_bilinear[0]):
        ##Determine limts for x+y and x-y 
        l_lim1 = continuous_x_continuous_terms['dual_variable_constraint_process_bilinear']['Fmin_v1'][i]
        u_lim1 = continuous_x_continuous_terms['dual_variable_constraint_process_bilinear']['Fmax_v1'][i]
        l_lim2 = continuous_x_continuous_terms['dual_variable_constraint_process_bilinear']['Fmin_v2'][i]
        u_lim2 = continuous_x_continuous_terms['dual_variable_constraint_process_bilinear']['Fmax_v2'][i]
        
        ##Determining the limits for x + y
        l_lim_func1 = l_lim1 + l_lim2
        u_lim_func1 = u_lim1 + u_lim2
        
        ##Derermining the limits for x - y
        l_lim_func2 = l_lim1 - u_lim2
        u_lim_func2 = u_lim1 - l_lim2
        
        ##Determining the individual coefficients for each of the limits 
        lim_func1_steps = (u_lim_func1 - l_lim_func1) / bilinear_pieces
        lim_func2_steps = (u_lim_func2 - l_lim_func2) / bilinear_pieces
        
        for j in range (0, bilinear_pieces):
            l_lim_func1_temp = l_lim_func1 + j*lim_func1_steps
            u_lim_func1_temp = l_lim_func1 + (j+1)*lim_func1_steps
            l_lim_func2_temp = l_lim_func2 + j*lim_func2_steps
            u_lim_func2_temp = l_lim_func2 + (j+1)*lim_func2_steps

            ##Finding the linear coefficients to the piecewise quadratic parts, reason is 0.5(u2 - v2) = xy  
            l_lim_func12_temp = 0.5 * pow(l_lim_func1_temp, 2)
            u_lim_func12_temp = 0.5 * pow(u_lim_func1_temp, 2)
            
            if (u_lim_func1_temp - l_lim_func1_temp) == 0:
                coeff_func1 = 0
                cst_func1 = 0
            else:
                coeff_func1 = (u_lim_func12_temp - l_lim_func12_temp) / (u_lim_func1_temp - l_lim_func1_temp)
                cst_func1 = u_lim_func12_temp - coeff_func1*u_lim_func1_temp
                
            l_lim_func22_temp = 0.5 * pow(l_lim_func2_temp, 2)
            u_lim_func22_temp = 0.5 * pow(u_lim_func2_temp, 2)
            
            if (u_lim_func2_temp - l_lim_func2_temp) == 0:
                coeff_func2 = 0
                cst_func2 = 0
            else:
                coeff_func2 = (u_lim_func22_temp - l_lim_func22_temp) / (u_lim_func2_temp - l_lim_func2_temp)
                cst_func2 = u_lim_func22_temp - coeff_func2*u_lim_func2_temp
            
            ##Appending sub_unit u
            sub_unit_name = continuous_x_continuous_terms['dual_variable_constraint_process_bilinear']['Name'][i] + 'bl_u' + str(j)
            variable = 'u'
            temp_data = [continuous_x_continuous_terms['dual_variable_constraint_process_bilinear']['Name'][i], continuous_x_continuous_terms['dual_variable_constraint_process_bilinear']['Variable1'][i],
                         continuous_x_continuous_terms['dual_variable_constraint_process_bilinear']['Variable2'][i], sub_unit_name, variable, l_lim_func1_temp, u_lim_func1_temp, coeff_func1, cst_func1]
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['Name_parent', 'Variable1_parent', 'Variable2_parent', 'Name', 'Variable', 'Fmin_v1', 'Fmax_v1', 'Coeff', 'Intercept'])
            dual_v_c_proc_bilin_new = dual_v_c_proc_bilin_new.append(temp_data_df, ignore_index = True)
            
            ##Appending sub_unit v
            sub_unit_name = continuous_x_continuous_terms['dual_variable_constraint_process_bilinear']['Name'][i] + 'bl_v' + str(j)
            variable = 'v'
            temp_data = [continuous_x_continuous_terms['dual_variable_constraint_process_bilinear']['Name'][i], continuous_x_continuous_terms['dual_variable_constraint_process_bilinear']['Variable1'][i],
                         continuous_x_continuous_terms['dual_variable_constraint_process_bilinear']['Variable2'][i], sub_unit_name, variable, l_lim_func2_temp, u_lim_func2_temp, coeff_func2, cst_func2]
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['Name_parent', 'Variable1_parent', 'Variable2_parent', 'Name', 'Variable', 'Fmin_v1', 'Fmax_v1', 'Coeff', 'Intercept'])
            dual_v_c_proc_bilin_new = dual_v_c_proc_bilin_new.append(temp_data_df, ignore_index = True)   
            
############################################################################################################################################################################################
############################################################################################################################################################################################
############################################################################################################################################################################################

    ##Handling streams_bilinear
    dim_streams_bilinear = continuous_x_continuous_terms['streams_bilinear'].shape 

    ##Packaging the new details into a DataFrame in the separated units form for each linearized piece  
    streams_bilin_new = pd.DataFrame(columns = ['Name_parent', 'Variable1_parent', 'Variable2_parent', 'Name', 'Variable', 'Fmin_v1', 'Fmax_v1', 'Coeff', 'Intercept'])

    for i in range (0, dim_streams_bilinear[0]):
        ##Determine limts for x+y and x-y 
        l_lim1 = continuous_x_continuous_terms['streams_bilinear']['Fmin_v1'][i]
        u_lim1 = continuous_x_continuous_terms['streams_bilinear']['Fmax_v1'][i]
        l_lim2 = continuous_x_continuous_terms['streams_bilinear']['Fmin_v2'][i]
        u_lim2 = continuous_x_continuous_terms['streams_bilinear']['Fmax_v2'][i]
        
        ##Determining the limits for x + y
        l_lim_func1 = l_lim1 + l_lim2
        u_lim_func1 = u_lim1 + u_lim2
        
        ##Derermining the limits for x - y
        l_lim_func2 = l_lim1 - u_lim2
        u_lim_func2 = u_lim1 - l_lim2
        
        ##Determining the individual coefficients for each of the limits 
        lim_func1_steps = (u_lim_func1 - l_lim_func1) / bilinear_pieces
        lim_func2_steps = (u_lim_func2 - l_lim_func2) / bilinear_pieces
        
        for j in range (0, bilinear_pieces):
            l_lim_func1_temp = l_lim_func1 + j*lim_func1_steps
            u_lim_func1_temp = l_lim_func1 + (j+1)*lim_func1_steps
            l_lim_func2_temp = l_lim_func2 + j*lim_func2_steps
            u_lim_func2_temp = l_lim_func2 + (j+1)*lim_func2_steps

            ##Finding the linear coefficients to the piecewise quadratic parts, reason is 0.5(u2 - v2) = xy  
            l_lim_func12_temp = 0.5 * pow(l_lim_func1_temp, 2)
            u_lim_func12_temp = 0.5 * pow(u_lim_func1_temp, 2)
            
            if (u_lim_func1_temp - l_lim_func1_temp) == 0:
                coeff_func1 = 0
                cst_func1 = 0
            else:
                coeff_func1 = (u_lim_func12_temp - l_lim_func12_temp) / (u_lim_func1_temp - l_lim_func1_temp)
                cst_func1 = u_lim_func12_temp - coeff_func1*u_lim_func1_temp
                
            l_lim_func22_temp = 0.5 * pow(l_lim_func2_temp, 2)
            u_lim_func22_temp = 0.5 * pow(u_lim_func2_temp, 2)
            
            if (u_lim_func2_temp - l_lim_func2_temp) == 0:
                coeff_func2 = 0
                cst_func2 = 0
            else:
                coeff_func2 = (u_lim_func22_temp - l_lim_func22_temp) / (u_lim_func2_temp - l_lim_func2_temp)
                cst_func2 = u_lim_func22_temp - coeff_func2*u_lim_func2_temp
            
            ##Appending sub_unit u
            sub_unit_name = continuous_x_continuous_terms['streams_bilinear']['Parent'][i] + 'bl_u' + str(j)
            variable = 'u'
            temp_data = [continuous_x_continuous_terms['streams_bilinear']['Name'][i], continuous_x_continuous_terms['streams_bilinear']['Parent_v1_name'][i],
                         continuous_x_continuous_terms['streams_bilinear']['Parent_v2_name'][i], sub_unit_name, variable, l_lim_func1_temp, u_lim_func1_temp, coeff_func1, cst_func1]
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['Name_parent', 'Variable1_parent', 'Variable2_parent', 'Name', 'Variable', 'Fmin_v1', 'Fmax_v1', 'Coeff', 'Intercept'])
            streams_bilin_new = streams_bilin_new.append(temp_data_df, ignore_index = True)
            
            ##Appending sub_unit v
            sub_unit_name = continuous_x_continuous_terms['streams_bilinear']['Parent'][i] + 'bl_v' + str(j)
            variable = 'v'
            temp_data = [continuous_x_continuous_terms['streams_bilinear']['Name'][i], continuous_x_continuous_terms['streams_bilinear']['Parent_v1_name'][i],
                         continuous_x_continuous_terms['streams_bilinear']['Parent_v2_name'][i], sub_unit_name, variable, l_lim_func2_temp, u_lim_func2_temp, coeff_func2, cst_func2]
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['Name_parent', 'Variable1_parent', 'Variable2_parent', 'Name', 'Variable', 'Fmin_v1', 'Fmax_v1', 'Coeff', 'Intercept'])
            streams_bilin_new = streams_bilin_new.append(temp_data_df, ignore_index = True)   

############################################################################################################################################################################################
############################################################################################################################################################################################
############################################################################################################################################################################################

    ##Handling cons_eqn_terms_bilinear
    dim_cons_eqn_terms_bilinear = continuous_x_continuous_terms['cons_eqn_terms_bilinear'].shape    

    ##Packaging the new details into a DataFrame in the separated units form for each linearized piece  
    cons_eqn_terms_bilin_new = pd.DataFrame(columns = ['Name_parent', 'Variable1_parent', 'Variable2_parent', 'Name', 'Variable', 'Fmin_v1', 'Fmax_v1', 'Coeff', 'Intercept'])
    
    for i in range (0, dim_cons_eqn_terms_bilinear[0]):
        ##Determine limts for x+y and x-y 
        l_lim1 = continuous_x_continuous_terms['cons_eqn_terms_bilinear']['Fmin_v1'][i]
        u_lim1 = continuous_x_continuous_terms['cons_eqn_terms_bilinear']['Fmax_v1'][i]
        l_lim2 = continuous_x_continuous_terms['cons_eqn_terms_bilinear']['Fmin_v2'][i]
        u_lim2 = continuous_x_continuous_terms['cons_eqn_terms_bilinear']['Fmax_v2'][i]
        
        ##Determining the limits for x + y
        l_lim_func1 = l_lim1 + l_lim2
        u_lim_func1 = u_lim1 + u_lim2
        
        ##Derermining the limits for x - y
        l_lim_func2 = l_lim1 - u_lim2
        u_lim_func2 = u_lim1 - l_lim2
        
        ##Determining the individual coefficients for each of the limits 
        lim_func1_steps = (u_lim_func1 - l_lim_func1) / bilinear_pieces
        lim_func2_steps = (u_lim_func2 - l_lim_func2) / bilinear_pieces
        
        for j in range (0, bilinear_pieces):
            l_lim_func1_temp = l_lim_func1 + j*lim_func1_steps
            u_lim_func1_temp = l_lim_func1 + (j+1)*lim_func1_steps
            l_lim_func2_temp = l_lim_func2 + j*lim_func2_steps
            u_lim_func2_temp = l_lim_func2 + (j+1)*lim_func2_steps

            ##Finding the linear coefficients to the piecewise quadratic parts, reason is 0.5(u2 - v2) = xy  
            l_lim_func12_temp = 0.5 * pow(l_lim_func1_temp, 2)
            u_lim_func12_temp = 0.5 * pow(u_lim_func1_temp, 2)
            
            if (u_lim_func1_temp - l_lim_func1_temp) == 0:
                coeff_func1 = 0
                cst_func1 = 0
            else:
                coeff_func1 = (u_lim_func12_temp - l_lim_func12_temp) / (u_lim_func1_temp - l_lim_func1_temp)
                cst_func1 = u_lim_func12_temp - coeff_func1*u_lim_func1_temp
                
            l_lim_func22_temp = 0.5 * pow(l_lim_func2_temp, 2)
            u_lim_func22_temp = 0.5 * pow(u_lim_func2_temp, 2)
            
            if (u_lim_func2_temp - l_lim_func2_temp) == 0:
                coeff_func2 = 0
                cst_func2 = 0
            else:
                coeff_func2 = (u_lim_func22_temp - l_lim_func22_temp) / (u_lim_func2_temp - l_lim_func2_temp)
                cst_func2 = u_lim_func22_temp - coeff_func2*u_lim_func2_temp
            
            ##Appending sub_unit u
            sub_unit_name = continuous_x_continuous_terms['cons_eqn_terms_bilinear']['Parent_unit'][i] + 'bl_u' + str(j)
            variable = 'u'
            temp_data = [continuous_x_continuous_terms['cons_eqn_terms_bilinear']['Parent_unit'][i], continuous_x_continuous_terms['cons_eqn_terms_bilinear']['Parent_v1_name'][i],
                         continuous_x_continuous_terms['cons_eqn_terms_bilinear']['Parent_v2_name'][i], sub_unit_name, variable, l_lim_func1_temp, u_lim_func1_temp, coeff_func1, cst_func1]
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['Name_parent', 'Variable1_parent', 'Variable2_parent', 'Name', 'Variable', 'Fmin_v1', 'Fmax_v1', 'Coeff', 'Intercept'])
            cons_eqn_terms_bilin_new = cons_eqn_terms_bilin_new.append(temp_data_df, ignore_index = True)
            
            ##Appending sub_unit v
            sub_unit_name = continuous_x_continuous_terms['cons_eqn_terms_bilinear']['Parent_unit'][i] + 'bl_v' + str(j)
            variable = 'v'
            temp_data = [continuous_x_continuous_terms['cons_eqn_terms_bilinear']['Parent_unit'][i], continuous_x_continuous_terms['cons_eqn_terms_bilinear']['Parent_v1_name'][i],
                         continuous_x_continuous_terms['cons_eqn_terms_bilinear']['Parent_v2_name'][i], sub_unit_name, variable, l_lim_func2_temp, u_lim_func2_temp, coeff_func2, cst_func2]
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['Name_parent', 'Variable1_parent', 'Variable2_parent', 'Name', 'Variable', 'Fmin_v1', 'Fmax_v1', 'Coeff', 'Intercept'])
            cons_eqn_terms_bilin_new = cons_eqn_terms_bilin_new.append(temp_data_df, ignore_index = True)      
            
############################################################################################################################################################################################
############################################################################################################################################################################################
############################################################################################################################################################################################

     ##Consolidating the data and returning the dataframes 
    linearized_list = {}
    linearized_list['obj_func_u_bilin_new'] = obj_func_u_bilin_new
    linearized_list['dual_v_c_util_bilin_new'] = dual_v_c_util_bilin_new
    linearized_list['obj_func_p_bilin_new'] = obj_func_p_bilin_new
    linearized_list['dual_v_c_proc_bilin_new'] = dual_v_c_proc_bilin_new
    linearized_list['streams_bilin_new'] = streams_bilin_new    
    linearized_list['cons_eqn_terms_bilin_new'] = cons_eqn_terms_bilin_new    
           
    return linearized_list