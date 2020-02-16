
def genscript_lp_format (input_dataframes, utilitylist, processlist, layerslist, parallel_thread_num, obj_func, bilinear_pieces):

    import os
    import sys
    import shutil
    import pandas as pd
    sys.path.append('C:\\Optimization_zlc\\slave_convex_handlers\\auxillary\\')
    from single_sign_string import single_sign_string
    
    ##Dealing with the storage directory for this script 
    ##Setting the path directory 
    master_folder = 'C:\\Optimization_zlc\\slave_convex_handlers\\solver_lp_format_holder\\'
    sub_folder = 'thread_' + str(parallel_thread_num) + '\\'
    script = 'script_' + str(parallel_thread_num) + '.lp'
    
    ##First check if the sub folder directory exists, if it does, delete it 
    sub_folder_path = master_folder + sub_folder 
    if os.path.exists(sub_folder_path):
        shutil.rmtree(sub_folder_path)
    
    ##Now, create the sub folder directory for storing the lp format script for the specific thread
    if not os.path.exists(sub_folder_path):
        os.makedirs(sub_folder_path)
        
    ##The final file location should be 
    script_loc = sub_folder_path + script 
    
###############################################################################################################################################################################################
###############################################################################################################################################################################################
###############################################################################################################################################################################################
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
    
###############################################################################################################################################################################################
###############################################################################################################################################################################################
###############################################################################################################################################################################################
    ##Problem definition section
    f_data_set = open(script_loc, 'w')
    
###############################################################################################################################################################################################
###############################################################################################################################################################################################
###############################################################################################################################################################################################    
    ##Objective function section 

    f_data_set.write('\\\\ Objective function for all utilities and processes \n \n')

    f_data_set.write('Minimize \n')
    f_data_set.write('\n')     

    ##Determining the type of objective function 
    key = obj_function_detect_genlp(obj_func)
    
    ##The overall string to contain all the objective function values 
    obj_function_input = ''

    ##Writing the utility terms in the objective function for strictly linear terms
    dim_utilitylist_linear = input_dataframes['utilitylist_linear'].shape
   
    for i in range (0, dim_utilitylist_linear[0]):
        var_name_temp = input_dataframes['utilitylist_linear']['Parent'][i] + '_' + input_dataframes['utilitylist_linear']['Name'][i]
        var_name_temp_y = input_dataframes['utilitylist_linear']['Parent'][i] + '_y'
        grad_temp = input_dataframes['utilitylist_linear'][key + '1'][i]
        int_temp = input_dataframes['utilitylist_linear'][key + '2'][i]
       
        check_empty = check_empty_string(obj_function_input)
       
        if check_empty == 1:
            temp_term = ''
            temp_term = temp_term + str(grad_temp) + ' ' + var_name_temp
            temp_term = temp_term + single_sign_string(int_temp, '+') + ' ' + var_name_temp_y
            obj_function_input = obj_function_input + temp_term
        else:
            temp_term = ''
            temp_term = temp_term + single_sign_string(grad_temp, '+') + ' ' + var_name_temp
            temp_term = temp_term + single_sign_string(int_temp, '+') + ' ' + var_name_temp_y
            obj_function_input = obj_function_input + temp_term

    ##Writing the utility terms in the objective function for relaxed bilinear terms 
    dim_utilitylist_bilinear = input_dataframes['utilitylist_bilinear'].shape

    for i in range (0, dim_utilitylist_bilinear[0]):           
        var_name_temp = input_dataframes['utilitylist_bilinear']['Name'][i]
        var_name_temp_y = var_name_temp + '_y'
        grad_temp = input_dataframes['utilitylist_bilinear'][key + '1'][i]
        int_temp = input_dataframes['utilitylist_bilinear'][key + '2'][i]       
   
        check_empty = check_empty_string(obj_function_input)   

        if check_empty == 1:
            temp_term = ''
            temp_term = temp_term + str(grad_temp) + ' ' + var_name_temp
            temp_term = temp_term + single_sign_string(int_temp, '+') + ' ' + var_name_temp_y
            obj_function_input = obj_function_input + temp_term
        else:
            temp_term = ''
            temp_term = temp_term + single_sign_string(grad_temp, '+') + ' ' + var_name_temp
            temp_term = temp_term + single_sign_string(int_temp, '+') + ' ' + var_name_temp_y
            obj_function_input = obj_function_input + temp_term
    
    ##Writing the process terms in the objective function for strictly linear terms
    dim_processlist_linear = input_dataframes['processlist_linear'].shape
    
    for i in range (0, dim_processlist_linear[0]):
        var_name_temp = input_dataframes['processlist_linear']['Parent'][i] + '_' + input_dataframes['processlist_linear']['Name'][i]
        var_name_temp_y = input_dataframes['processlist_linear']['Parent'][i] + '_y'
        grad_temp = input_dataframes['processlist_linear'][key + '1'][i]
        int_temp = input_dataframes['processlist_linear'][key + '2'][i]
       
        check_empty = check_empty_string(obj_function_input)
       
        if check_empty == 1:
            temp_term = ''
            temp_term = temp_term + str(grad_temp) + ' ' + var_name_temp
            temp_term = temp_term + single_sign_string(int_temp, '+') + ' ' + var_name_temp_y
            obj_function_input = obj_function_input + temp_term
        else:
            temp_term = ''
            temp_term = temp_term + single_sign_string(grad_temp, '+') + ' ' + var_name_temp
            temp_term = temp_term + single_sign_string(int_temp, '+') + ' ' + var_name_temp_y
            obj_function_input = obj_function_input + temp_term
           
    ##Writing the process terms in the objective function for relaxed bilinear terms 
    dim_processlist_bilinear = input_dataframes['processlist_bilinear'].shape

    for i in range (0, dim_processlist_bilinear[0]):           
        var_name_temp = input_dataframes['processlist_bilinear']['Name'][i]
        var_name_temp_y = var_name_temp + '_y'
        grad_temp = input_dataframes['processlist_bilinear'][key + '1'][i]
        int_temp = input_dataframes['processlist_bilinear'][key + '2'][i]       
   
        check_empty = check_empty_string(obj_function_input)   

        if check_empty == 1:
            temp_term = ''
            temp_term = temp_term + str(grad_temp) + ' ' + var_name_temp
            temp_term = temp_term + single_sign_string(int_temp, '+') + ' ' + var_name_temp_y
            obj_function_input = obj_function_input + temp_term
        else:
            temp_term = ''
            temp_term = temp_term + single_sign_string(grad_temp, '+') + ' ' + var_name_temp
            temp_term = temp_term + single_sign_string(int_temp, '+') + ' ' + var_name_temp_y
            obj_function_input = obj_function_input + temp_term
    
    f_data_set.write('obj: ' + obj_function_input) 
    f_data_set.write('\n \n')          
  
###############################################################################################################################################################################################    
###############################################################################################################################################################################################
###############################################################################################################################################################################################
    ##Constraint section 
    f_data_set.write('Subject To \n \n')

    current_index = 0
###############################################################################################################################################################################################    

    ##Writing Fmin, Fmax constraints for utilities linear 
    f_data_set.write('\\\\Writing Fmin, Fmax constraints for utilities linear \n \n')
    
    for i in range (0, dim_utilitylist_linear[0]):
        var_name_temp = input_dataframes['utilitylist_linear']['Parent'][i] + '_' + input_dataframes['utilitylist_linear']['Name'][i]
        var_name_temp_y = input_dataframes['utilitylist_linear']['Parent'][i] + '_y'
        fmin_temp = input_dataframes['utilitylist_linear']['Fmin'][i]
        fmax_temp = input_dataframes['utilitylist_linear']['Fmax'][i]
        
        ##Writing Fmin first 
        current_index = current_index + 1
        temp_term = ''
        temp_term = temp_term + 'c' + str(current_index) + ': '
        temp_term = temp_term + str(fmin_temp) + ' ' + var_name_temp_y
        temp_term = temp_term + ' - ' + var_name_temp + ' <= 0'
        f_data_set.write(temp_term + '\n')
        
        ##Writing the Fmax next 
        current_index = current_index + 1
        temp_term = ''
        temp_term = temp_term + 'c' + str(current_index) + ': '
        temp_term = temp_term + var_name_temp
        temp_term = temp_term + single_sign_string(fmax_temp, '-') + ' ' + var_name_temp_y + ' <= 0'
        f_data_set.write(temp_term + '\n')   
    
    f_data_set.write('\n')
    
    ##Writing Fmin, Fmax constraints for utilities bilinear 
    f_data_set.write('\\\\Writing Fmin, Fmax constraints for utilities bilinear \n \n')
    
    for i in range (0, dim_utilitylist_bilinear[0]):
        var_name_temp = input_dataframes['utilitylist_bilinear']['Name'][i]
        var_name_temp_y = var_name_temp + '_y'
        fmin_temp = input_dataframes['utilitylist_bilinear']['Fmin'][i]
        fmax_temp = input_dataframes['utilitylist_bilinear']['Fmax'][i]
        
        ##Writing Fmin first 
        current_index = current_index + 1
        temp_term = ''
        temp_term = temp_term + 'c' + str(current_index) + ': '
        temp_term = temp_term + str(fmin_temp) + ' ' + var_name_temp_y
        temp_term = temp_term + ' - ' + var_name_temp + ' <= 0'
        f_data_set.write(temp_term + '\n')
        
        ##Writing the Fmax next 
        current_index = current_index + 1
        temp_term = ''
        temp_term = temp_term + 'c' + str(current_index) + ': '
        temp_term = temp_term + var_name_temp
        temp_term = temp_term + single_sign_string(fmax_temp, '-') + ' ' + var_name_temp_y + ' <= 0'
        f_data_set.write(temp_term + '\n')

    f_data_set.write('\n') 
        
    ##Writing the fmin and fmax constraint in relation to x and y for utilities 
    f_data_set.write('\\\\Writing the fmin and fmax constraint in relation to x and y for utilities \n \n')
    dim_utilitylist = utilitylist.shape
    
    check_list = input_dataframes['utilitylist_bilinear']['Parent'][:]
    
    for i in range (0, dim_utilitylist[0]):
        check_value = check_if_item_in_list (check_list, utilitylist['Name'][i])
        if  check_value == 1:            
            base_parent_name_onoff = utilitylist['Name'][i] + '_y'
            
            x_fmin_value = utilitylist['Fmin_v1'][i] * 2
            x_fmax_value = utilitylist['Fmax_v1'][i] * 2
            y_fmin_value = utilitylist['Fmin_v2'][i] * 2
            y_fmax_value = utilitylist['Fmax_v2'][i] * 2
            
            u_term_temp_pos = ''
            v_term_temp_pos = ''
            u_term_temp_neg = ''
            v_term_temp_neg = ''
            
            for j in range (0, bilinear_pieces):
                base_name_u = utilitylist['Name'][i] + '_u' + str(j)
                base_name_v = utilitylist['Name'][i] + '_v' + str(j)  
                
                if (check_empty_string(u_term_temp_pos) == 1):
                    u_term_temp_pos = u_term_temp_pos + base_name_u
                else:
                    u_term_temp_pos = u_term_temp_pos + ' + ' + base_name_u
                
                if (check_empty_string(v_term_temp_pos) == 1):
                    v_term_temp_pos = v_term_temp_pos + base_name_v
                else:
                    v_term_temp_pos = v_term_temp_pos + ' + ' + base_name_v                

                if (check_empty_string(u_term_temp_neg) == 1):
                    u_term_temp_neg = u_term_temp_neg + base_name_u
                else:
                    u_term_temp_neg = u_term_temp_neg + ' - ' + base_name_u

                if (check_empty_string(v_term_temp_neg) == 1):
                    v_term_temp_neg = v_term_temp_neg + base_name_v
                else:
                    v_term_temp_neg = v_term_temp_neg + ' - ' + base_name_v 
                
            ##Writing the Fmin of 2x = u + v
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + str(x_fmin_value) + ' ' + base_parent_name_onoff 
            temp_term = temp_term + ' - ' + u_term_temp_neg + ' - ' + v_term_temp_neg + ' <= 0'
            f_data_set.write(temp_term + '\n')
            
            ##Writing the Fmax of 2x = u + v                
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + u_term_temp_pos + ' + ' + v_term_temp_pos
            temp_term = temp_term + single_sign_string(x_fmax_value , '-') + ' ' + base_parent_name_onoff
            temp_term = temp_term + ' <= 0'
            f_data_set.write(temp_term + '\n')                
            
            ##Writing the Fmin of the 2y = u - v
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '  
            temp_term = temp_term + str(y_fmin_value) + ' ' + base_parent_name_onoff 
            temp_term = temp_term + ' - ' + u_term_temp_neg + ' + ' + v_term_temp_pos + ' <= 0'
            f_data_set.write(temp_term + '\n')

            ##Writing the Fmax of the 2y = u - v       
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + u_term_temp_pos + ' - ' + v_term_temp_neg
            temp_term = temp_term + single_sign_string(y_fmax_value , '-') + ' ' + base_parent_name_onoff
            temp_term = temp_term + ' <= 0'
            f_data_set.write(temp_term + '\n')      
        
    f_data_set.write('\n') 
    
    ##Writing Fmin, Fmax constraints for process linear 
    f_data_set.write('\\\\Writing Fmin, Fmax constraints for process linear \n \n')
    
    for i in range (0, dim_processlist_linear[0]):
        var_name_temp = input_dataframes['processlist_linear']['Parent'][i] + '_' + input_dataframes['processlist_linear']['Name'][i]
        var_name_temp_y = input_dataframes['processlist_linear']['Parent'][i] + '_y'
        fmax_temp = input_dataframes['processlist_linear']['Fmax'][i]
        
        ##Writing 'Fmin' first 
        current_index = current_index + 1
        temp_term = ''
        temp_term = temp_term + 'c' + str(current_index) + ': '
        temp_term = temp_term +  var_name_temp
        temp_term = temp_term + ' = ' + str(fmax_temp)
        f_data_set.write(temp_term + '\n')

        ##Writing 'Fmin' first for the binary variable making sure it is always turn on
        current_index = current_index + 1
        temp_term = ''
        temp_term = temp_term + 'c' + str(current_index) + ': '
        temp_term = temp_term +  input_dataframes['processlist_linear']['Parent'][i]  + '_y'
        temp_term = temp_term + ' = ' + str(1.0)
        f_data_set.write(temp_term + '\n')
        
    f_data_set.write('\n')        
    
    ##Writing Fmin, Fmax constraints for processes bilinear 
    f_data_set.write('\\\\Writing Fmin, Fmax constraints for process bilinear \n \n')
    
    for i in range (0, dim_processlist_bilinear[0]):
        var_name_temp = input_dataframes['processlist_bilinear']['Name'][i]
        var_name_temp_y = var_name_temp + '_y'
        fmin_temp = input_dataframes['processlist_bilinear']['Fmin'][i]
        fmax_temp = input_dataframes['processlist_bilinear']['Fmax'][i]
        
        ##Writing Fmin first 
        current_index = current_index + 1
        temp_term = ''
        temp_term = temp_term + 'c' + str(current_index) + ': '
        temp_term = temp_term + str(fmin_temp) + ' ' + var_name_temp_y
        temp_term = temp_term + ' - ' + var_name_temp + ' <= 0'
        f_data_set.write(temp_term + '\n')
        
        ##Writing the Fmax next 
        current_index = current_index + 1
        temp_term = ''
        temp_term = temp_term + 'c' + str(current_index) + ': '
        temp_term = temp_term + var_name_temp
        temp_term = temp_term + single_sign_string(fmax_temp, '-') + ' ' + var_name_temp_y + ' <= 0'
        f_data_set.write(temp_term + '\n') 
        
    f_data_set.write('\n') 

    ##Writing the fmin and fmax constraint in relation to x and y for processes
    f_data_set.write('\\\\Writing the fmin and fmax constraint in relation to x and y for processes \n \n')
    dim_processlist = processlist.shape
    
    check_list = input_dataframes['processlist_bilinear']['Parent'][:]
    
    for i in range (0, dim_processlist[0]):
        check_value = check_if_item_in_list (check_list, processlist['Name'][i])
        if  check_value == 1:
            base_parent_name_onoff = processlist['Name'][i] + '_y'
            
            x_fmin_value = processlist['Fmin_v1'][i] * 2
            x_fmax_value = processlist['Fmax_v1'][i] * 2
            y_fmin_value = processlist['Fmin_v2'][i] * 2
            y_fmax_value = processlist['Fmax_v2'][i] * 2
            
            u_term_temp_pos = ''
            v_term_temp_pos = ''
            u_term_temp_neg = ''
            v_term_temp_neg = ''
            
            for j in range (0, bilinear_pieces):
                base_name_u = processlist['Name'][i] + '_u' + str(j)
                base_name_v = processlist['Name'][i] + '_v' + str(j)
                
                if (check_empty_string(u_term_temp_pos) == 1):
                    u_term_temp_pos = u_term_temp_pos + base_name_u
                else:
                    u_term_temp_pos = u_term_temp_pos + ' + ' + base_name_u
                
                if (check_empty_string(v_term_temp_pos) == 1):
                    v_term_temp_pos = v_term_temp_pos + base_name_v
                else:
                    v_term_temp_pos = v_term_temp_pos + ' + ' + base_name_v
                
                if (check_empty_string(u_term_temp_neg) == 1):
                    u_term_temp_neg = u_term_temp_neg + base_name_u
                else:
                    u_term_temp_neg = u_term_temp_neg + ' - ' + base_name_u

                if (check_empty_string(v_term_temp_neg) == 1):
                    v_term_temp_neg = v_term_temp_neg + base_name_v
                else:
                    v_term_temp_neg = v_term_temp_neg + ' - ' + base_name_v 

            
            ##Writing the Fmin of 2x = u + v
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + u_term_temp_pos + ' + ' + v_term_temp_pos + ' >= ' + str(x_fmin_value)
            f_data_set.write(temp_term + '\n')
            
            ##Writing the Fmax of 2x = u + v                
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + u_term_temp_pos + ' + ' + v_term_temp_pos
            temp_term = temp_term + ' <= ' + str(x_fmax_value)
            f_data_set.write(temp_term + '\n')                
            
            ##Writing the Fmin of the 2y = u - v
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '  
            temp_term = temp_term + u_term_temp_pos + ' - ' + v_term_temp_neg + ' >= ' + str(y_fmin_value)
            f_data_set.write(temp_term + '\n')

            ##Writing the Fmax of the 2y = u - v       
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + u_term_temp_pos + ' - ' + v_term_temp_neg + ' <= ' + str(y_fmax_value)
            f_data_set.write(temp_term + '\n')  
        
    f_data_set.write('\n')         
    
    ##Writing the stream constraints
    f_data_set.write('\\\\Writing stream constraints \n \n')
    dim_layerslist = layerslist.shape 
    dim_streams_linear = input_dataframes['streams_linear'].shape
    dim_streams_bilinear = input_dataframes['streams_bilinear'].shape

    for i in range (0, dim_layerslist[0]):
        current_layer = layerslist['Name'][i]
        ##Differentiating by type  
        if layerslist['Type'][i] == 'balancing_only':
            ##Initiating a string to hold the in and out values 
            temp_in = ''
            temp_out = ''
            
            ##Scanning through the linear stream list 
            for j in range (0, dim_streams_linear[0]):
                if input_dataframes['streams_linear']['Layer'][j] == current_layer:
                    if input_dataframes['streams_linear']['InOut'][j] == 'in':
                        var_name_temp = input_dataframes['streams_linear']['Parent'][j] + '_' + input_dataframes['streams_linear']['Variable'][j]
                        check_empty = check_empty_string(temp_in)
                        if check_empty == 1:
                            temp_in = temp_in + str(input_dataframes['streams_linear']['Flow_grad'][j]) + ' ' + var_name_temp
                            temp_in = temp_in + single_sign_string(input_dataframes['streams_linear']['Flow_min'][j], '+') + ' ' + input_dataframes['streams_linear']['Parent'][j] + '_y'
                        else:
                            temp_in = temp_in + single_sign_string(input_dataframes['streams_linear']['Flow_grad'][j], '+') + ' ' + var_name_temp
                            temp_in = temp_in + single_sign_string(input_dataframes['streams_linear']['Flow_min'][j], '+') + ' ' + input_dataframes['streams_linear']['Parent'][j] + '_y'                          
                    elif input_dataframes['streams_linear']['InOut'][j] == 'out':
                        var_name_temp = input_dataframes['streams_linear']['Parent'][j] + '_' + input_dataframes['streams_linear']['Variable'][j]
                        temp_out = temp_out + single_sign_string(input_dataframes['streams_linear']['Flow_grad'][j], '-') + ' ' + var_name_temp
                        temp_out = temp_out + single_sign_string(input_dataframes['streams_linear']['Flow_min'][j], '-') + ' ' + input_dataframes['streams_linear']['Parent'][j] + '_y'  
          
            #Scanning through the bilinear stream list 
            for j in range (0, dim_streams_bilinear[0]):
                if input_dataframes['streams_bilinear']['Layer'][j] == current_layer:                
                    if input_dataframes['streams_bilinear']['InOut'][j] == 'in':
                        var_name_temp = input_dataframes['streams_bilinear']['Variable'][j]
                        check_empty = check_empty_string(temp_in)
                        if check_empty == 1:
                            temp_in = temp_in + str(input_dataframes['streams_bilinear']['Flow_grad'][j]) + ' ' + var_name_temp
                            temp_in = temp_in + single_sign_string(input_dataframes['streams_bilinear']['Flow_min'][j], '+') + ' ' + var_name_temp + '_y'
                        else:
                            temp_in = temp_in + single_sign_string(input_dataframes['streams_bilinear']['Flow_grad'][j], '+') + ' ' + var_name_temp
                            temp_in = temp_in + single_sign_string(input_dataframes['streams_bilinear']['Flow_min'][j], '+') + ' ' + var_name_temp + '_y'                          
                    elif input_dataframes['streams_bilinear']['InOut'][j] == 'out':
                        var_name_temp = input_dataframes['streams_bilinear']['Variable'][j]
                        temp_out = temp_out + single_sign_string(input_dataframes['streams_bilinear']['Flow_grad'][j], '-') + ' ' + var_name_temp
                        temp_out = temp_out + single_sign_string(input_dataframes['streams_bilinear']['Flow_min'][j], '-') + ' ' + var_name_temp + '_y'
        
            ##Writing the constraints 
            temp_InOut = temp_in + temp_out
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + temp_InOut + ' = 0'
            f_data_set.write(temp_term + '\n')  
            
        elif (layerslist['Type'][i] == 'temp_chil') or (layerslist['Type'][i] == 'pressure') or (layerslist['Type'][i] == 'energy_reverse') or (layerslist['Type'][i] == 'flow_reverse'):
            ##Initiating a string to hold the in and out values 
            temp_in = ''
            temp_out = ''
            
            ##Scanning through the linear stream list 
            for j in range (0, dim_streams_linear[0]):
                if input_dataframes['streams_linear']['Layer'][j] == current_layer:
                    if input_dataframes['streams_linear']['InOut'][j] == 'in':
                        var_name_temp = input_dataframes['streams_linear']['Parent'][j] + '_' + input_dataframes['streams_linear']['Variable'][j]
                        check_empty = check_empty_string(temp_in)
                        if check_empty == 1:
                            temp_in = temp_in + str(input_dataframes['streams_linear']['Flow_grad'][j]) + ' ' + var_name_temp
                            temp_in = temp_in + single_sign_string(input_dataframes['streams_linear']['Flow_min'][j], '+') + ' ' + input_dataframes['streams_linear']['Parent'][j] + '_y'
                        else:
                            temp_in = temp_in + single_sign_string(input_dataframes['streams_linear']['Flow_grad'][j], '+') + ' ' + var_name_temp
                            temp_in = temp_in + single_sign_string(input_dataframes['streams_linear']['Flow_min'][j], '+') + ' ' + input_dataframes['streams_linear']['Parent'][j] + '_y'                          
                    elif input_dataframes['streams_linear']['InOut'][j] == 'out':
                        var_name_temp = input_dataframes['streams_linear']['Parent'][j] + '_' + input_dataframes['streams_linear']['Variable'][j]
                        temp_out = temp_out + single_sign_string(input_dataframes['streams_linear']['Flow_grad'][j], '-') + ' ' + var_name_temp
                        temp_out = temp_out + single_sign_string(input_dataframes['streams_linear']['Flow_min'][j], '-') + ' ' + input_dataframes['streams_linear']['Parent'][j] + '_y'  
          
            #Scanning through the bilinear stream list 
            for j in range (0, dim_streams_bilinear[0]):
                if input_dataframes['streams_bilinear']['Layer'][j] == current_layer:                
                    if input_dataframes['streams_bilinear']['InOut'][j] == 'in':
                        var_name_temp = input_dataframes['streams_bilinear']['Variable'][j]
                        check_empty = check_empty_string(temp_in)
                        if check_empty == 1:
                            temp_in = temp_in + str(input_dataframes['streams_bilinear']['Flow_grad'][j]) + ' ' + var_name_temp
                            temp_in = temp_in + single_sign_string(input_dataframes['streams_bilinear']['Flow_min'][j], '+') + ' ' + var_name_temp + '_y'
                        else:
                            temp_in = temp_in + single_sign_string(input_dataframes['streams_bilinear']['Flow_grad'][j], '+') + ' ' + var_name_temp
                            temp_in = temp_in + single_sign_string(input_dataframes['streams_bilinear']['Flow_min'][j], '+') + ' ' + var_name_temp + '_y'                          
                    elif input_dataframes['streams_bilinear']['InOut'][j] == 'out':
                        var_name_temp = input_dataframes['streams_bilinear']['Variable'][j]
                        temp_out = temp_out + single_sign_string(input_dataframes['streams_bilinear']['Flow_grad'][j], '-') + ' ' + var_name_temp
                        temp_out = temp_out + single_sign_string(input_dataframes['streams_bilinear']['Flow_min'][j], '-') + ' ' + var_name_temp + '_y'
        
            ##Writing the constraints 
            temp_InOut = temp_in + temp_out
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + temp_InOut + ' >= 0'
            f_data_set.write(temp_term + '\n')
            
        elif (layerslist['Type'][i] == 'flow') or (layerslist['Type'][i] == 'energy'):
            ##Initiating a string to hold the in and out values 
            temp_in = ''
            temp_out = ''
            
            ##Scanning through the linear stream list 
            for j in range (0, dim_streams_linear[0]):
                if input_dataframes['streams_linear']['Layer'][j] == current_layer:
                    if input_dataframes['streams_linear']['InOut'][j] == 'in':
                        var_name_temp = input_dataframes['streams_linear']['Parent'][j] + '_' + input_dataframes['streams_linear']['Variable'][j]
                        check_empty = check_empty_string(temp_in)
                        if check_empty == 1:
                            temp_in = temp_in + str(input_dataframes['streams_linear']['Flow_grad'][j]) + ' ' + var_name_temp
                            temp_in = temp_in + single_sign_string(input_dataframes['streams_linear']['Flow_min'][j], '+') + ' ' + input_dataframes['streams_linear']['Parent'][j] + '_y'
                        else:
                            temp_in = temp_in + single_sign_string(input_dataframes['streams_linear']['Flow_grad'][j], '+') + ' ' + var_name_temp
                            temp_in = temp_in + single_sign_string(input_dataframes['streams_linear']['Flow_min'][j], '+') + ' ' + input_dataframes['streams_linear']['Parent'][j] + '_y'                          
                    elif input_dataframes['streams_linear']['InOut'][j] == 'out':
                        var_name_temp = input_dataframes['streams_linear']['Parent'][j] + '_' + input_dataframes['streams_linear']['Variable'][j]
                        temp_out = temp_out + single_sign_string(input_dataframes['streams_linear']['Flow_grad'][j], '-') + ' ' + var_name_temp
                        temp_out = temp_out + single_sign_string(input_dataframes['streams_linear']['Flow_min'][j], '-') + ' ' + input_dataframes['streams_linear']['Parent'][j] + '_y'  
          
            #Scanning through the bilinear stream list 
            for j in range (0, dim_streams_bilinear[0]):
                if input_dataframes['streams_bilinear']['Layer'][j] == current_layer:                
                    if input_dataframes['streams_bilinear']['InOut'][j] == 'in':
                        var_name_temp = input_dataframes['streams_bilinear']['Variable'][j]
                        check_empty = check_empty_string(temp_in)
                        if check_empty == 1:
                            temp_in = temp_in + str(input_dataframes['streams_bilinear']['Flow_grad'][j]) + ' ' + var_name_temp
                            temp_in = temp_in + single_sign_string(input_dataframes['streams_bilinear']['Flow_min'][j], '+') + ' ' + var_name_temp + '_y'
                        else:
                            temp_in = temp_in + single_sign_string(input_dataframes['streams_bilinear']['Flow_grad'][j], '+') + ' ' + var_name_temp
                            temp_in = temp_in + single_sign_string(input_dataframes['streams_bilinear']['Flow_min'][j], '+') + ' ' + var_name_temp + '_y'                          
                    elif input_dataframes['streams_bilinear']['InOut'][j] == 'out':
                        var_name_temp = input_dataframes['streams_bilinear']['Variable'][j]
                        temp_out = temp_out + single_sign_string(input_dataframes['streams_bilinear']['Flow_grad'][j], '-') + ' ' + var_name_temp
                        temp_out = temp_out + single_sign_string(input_dataframes['streams_bilinear']['Flow_min'][j], '-') + ' ' + var_name_temp + '_y'
        
            ##Writing the constraints 
            temp_InOut = temp_in + temp_out
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + temp_InOut + ' <= 0'
            f_data_set.write(temp_term + '\n')
        
    f_data_set.write('\n')

    ##Writing the additional constraints
    f_data_set.write('\\\\Writing additional constraints \n \n')
    
    dim_cons_eqns_all = input_dataframes['cons_eqns_all'].shape
    dim_cons_eqns_terms_linear = input_dataframes['cons_eqns_terms_linear'].shape
    dim_cons_eqns_terms_bilinear = input_dataframes['cons_eqns_terms_bilinear'].shape
    
    ##Writing the unit binary constraints 
    f_data_set.write('\\\\Writing additional constraints: unit_binary \n \n')    
    
    for i in range (0, dim_cons_eqns_all[0]):
        if input_dataframes['cons_eqns_all']['Type'][i] == 'unit_binary':
            eqn_name_temp = input_dataframes['cons_eqns_all']['Name'][i]
            sign_temp = determine_sign (input_dataframes['cons_eqns_all']['Sign'][i])
            rhs_value = str(input_dataframes['cons_eqns_all']['RHS_value'][i])
            temp_lhs = ''
            ##Scanning through the linear list first
            for j in range (0, dim_cons_eqns_terms_linear[0]):
                if input_dataframes['cons_eqns_terms_linear']['Parent_eqn'][j] == eqn_name_temp:
                    var_temp_name = input_dataframes['cons_eqns_terms_linear']['Parent_unit'][j] + '_y'
                    check_empty = check_empty_string (temp_lhs)
                    if check_empty == 1:
                        temp_lhs = temp_lhs + str(input_dataframes['cons_eqns_terms_linear']['Coefficient'][j]) + ' ' + var_temp_name
                    else:
                        temp_lhs = temp_lhs + single_sign_string(input_dataframes['cons_eqns_terms_linear']['Coefficient'][j], '+') + ' ' + var_temp_name
            ##Scanning through the bilinear list next 
            for j in range (0, dim_cons_eqns_terms_bilinear[0]):
                if input_dataframes['cons_eqns_terms_bilinear']['Parent_eqn'][j] == eqn_name_temp:                
                    var_temp_name = input_dataframes['cons_eqns_terms_bilinear']['Variable'][j] + '_y'
                    check_empty = check_empty_string (temp_lhs)
                    if check_empty == 1:
                        temp_lhs = temp_lhs + str(input_dataframes['cons_eqns_terms_bilinear']['Coefficient'][j]) + ' ' + var_temp_name
                    else:
                        temp_lhs = temp_lhs + single_sign_string(input_dataframes['cons_eqns_terms_bilinear']['Coefficient'][j], '+') + ' ' + var_temp_name
            
            ##Writing the constraint
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + temp_lhs + sign_temp + rhs_value
            f_data_set.write(temp_term + '\n')                     

    f_data_set.write('\n')
    
    ##Writing the unit binary equality constraints 
    f_data_set.write('\\\\Writing additional constraints: unit_binary_equality \n \n')    
    
    for i in range (0, dim_cons_eqns_all[0]):
        if input_dataframes['cons_eqns_all']['Type'][i] == 'unit_binary_equality':
            eqn_name_temp = input_dataframes['cons_eqns_all']['Name'][i]
            sign_temp = determine_sign (input_dataframes['cons_eqns_all']['Sign'][i])
            rhs_value = str(input_dataframes['cons_eqns_all']['RHS_value'][i])
            temp_lhs = ''
            ##Scanning through the linear list first
            for j in range (0, dim_cons_eqns_terms_linear[0]):
                if input_dataframes['cons_eqns_terms_linear']['Parent_eqn'][j] == eqn_name_temp:
                    var_temp_name = input_dataframes['cons_eqns_terms_linear']['Parent_unit'][j] + '_y'
                    check_empty = check_empty_string (temp_lhs)
                    if check_empty == 1:
                        temp_lhs = temp_lhs + str(input_dataframes['cons_eqns_terms_linear']['Coefficient'][j]) + ' ' + var_temp_name
                    else:
                        temp_lhs = temp_lhs + single_sign_string(input_dataframes['cons_eqns_terms_linear']['Coefficient'][j], '+') + ' ' + var_temp_name
            ##Scanning through the bilinear list next 
            for j in range (0, dim_cons_eqns_terms_bilinear[0]):
                if input_dataframes['cons_eqns_terms_bilinear']['Parent_eqn'][j] == eqn_name_temp:                
                    var_temp_name = input_dataframes['cons_eqns_terms_bilinear']['Variable'][j] + '_y'
                    check_empty = check_empty_string (temp_lhs)
                    if check_empty == 1:
                        temp_lhs = temp_lhs + str(input_dataframes['cons_eqns_terms_bilinear']['Coefficient'][j]) + ' ' + var_temp_name
                    else:
                        temp_lhs = temp_lhs + single_sign_string(input_dataframes['cons_eqns_terms_bilinear']['Coefficient'][j], '+') + ' ' + var_temp_name
            
            ##Writing the constraint
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + temp_lhs + sign_temp + rhs_value
            f_data_set.write(temp_term + '\n')                     

    f_data_set.write('\n')
    
    ##Writing the stream_limit_modified constraints 
    f_data_set.write('\\\\Writing additional constraints: stream_limit_modified \n \n')                     
    for i in range (0, dim_cons_eqns_all[0]):                    
        if input_dataframes['cons_eqns_all']['Type'][i] == 'stream_limit_modified':
            eqn_name_temp = input_dataframes['cons_eqns_all']['Name'][i]            
            sign_temp = determine_sign (input_dataframes['cons_eqns_all']['Sign'][i])            
            rhs_value = str(input_dataframes['cons_eqns_all']['RHS_value'][i])
            temp_lhs = ''
            ##Scanning through the linear list first
            for j in range (0, dim_cons_eqns_terms_linear[0]):
                if input_dataframes['cons_eqns_terms_linear']['Parent_eqn'][j] == eqn_name_temp:
                    var_temp_name = input_dataframes['cons_eqns_terms_linear']['Parent_unit'][j] + '_' + input_dataframes['cons_eqns_terms_linear']['Variable'][j]
                    var_temp_name_y = input_dataframes['cons_eqns_terms_linear']['Parent_unit'][j] + '_y'
                    check_empty = check_empty_string (temp_lhs)
                    if check_empty == 1:
                        temp_lhs = temp_lhs + str(input_dataframes['cons_eqns_terms_linear']['Grad'][j]) + ' ' + var_temp_name
                        temp_lhs = temp_lhs + single_sign_string(input_dataframes['cons_eqns_terms_linear']['Cst'][j], '+') + ' ' + var_temp_name_y
                    else:
                        temp_lhs = temp_lhs + single_sign_string(input_dataframes['cons_eqns_terms_linear']['Grad'][j], '+') + ' ' + var_temp_name
                        temp_lhs = temp_lhs + single_sign_string(input_dataframes['cons_eqns_terms_linear']['Cst'][j], '+') + ' ' + var_temp_name_y   
                        
            ##Scanning through the bilinear list next 
            for j in range (0, dim_cons_eqns_terms_bilinear[0]):
                if input_dataframes['cons_eqns_terms_bilinear']['Parent_eqn'][j] == eqn_name_temp:                
                    var_temp_name = input_dataframes['cons_eqns_terms_bilinear']['Variable'][j]
                    var_temp_name_y = var_temp_name + '_y'
                    check_empty = check_empty_string (temp_lhs)
                    if check_empty == 1:
                        temp_lhs = temp_lhs + str(input_dataframes['cons_eqns_terms_bilinear']['Grad'][j]) + ' ' + var_temp_name
                        temp_lhs = temp_lhs + single_sign_string(input_dataframes['cons_eqns_terms_bilinear']['Cst'][j], '+') + ' ' + var_temp_name_y
                    else:
                        temp_lhs = temp_lhs + single_sign_string(input_dataframes['cons_eqns_terms_bilinear']['Grad'][j], '+') + ' ' + var_temp_name
                        temp_lhs = temp_lhs + single_sign_string(input_dataframes['cons_eqns_terms_bilinear']['Cst'][j], '+') + ' ' + var_temp_name_y   
                        
            ##Writing the constraint
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + temp_lhs + sign_temp + rhs_value
            f_data_set.write(temp_term + '\n')    

    f_data_set.write('\n')

    ##Writing the bilinear_limits_fmin_util constraints, only affects cons_eqns_terms_bilinear
    f_data_set.write('\\\\Writing additional constraints: bilinear_limits_fmin_util \n \n') 
    for i in range (0, dim_cons_eqns_all[0]):                         
        if input_dataframes['cons_eqns_all']['Type'][i] == 'bilinear_limits_fmin_util':  
            eqn_name_temp = input_dataframes['cons_eqns_all']['Name'][i]                        
            rhs_value = str(input_dataframes['cons_eqns_all']['RHS_value'][i])
            temp_lhs = ''            
            ##Scanning through the bilinear list 
            for j in range (0, dim_cons_eqns_terms_bilinear[0]):
                if input_dataframes['cons_eqns_terms_bilinear']['Parent_eqn'][j] == eqn_name_temp:                
                    var_temp_name = input_dataframes['cons_eqns_terms_bilinear']['Variable'][j]
                    var_temp_name_y = var_temp_name + '_y'
                    check_empty = check_empty_string (temp_lhs)
                    ##All values need to be negative
                    if check_empty == 1:
                        temp_lhs = temp_lhs + str(input_dataframes['cons_eqns_terms_bilinear']['Grad'][j]) + ' ' + var_temp_name
                        temp_lhs = temp_lhs + single_sign_string(input_dataframes['cons_eqns_terms_bilinear']['Cst'][j], '+') + ' ' + var_temp_name_y
                    else:
                        temp_lhs = temp_lhs + single_sign_string(input_dataframes['cons_eqns_terms_bilinear']['Grad'][j], '+') + ' ' + var_temp_name
                        temp_lhs = temp_lhs + single_sign_string(input_dataframes['cons_eqns_terms_bilinear']['Cst'][j], '+') + ' ' + var_temp_name_y    
                        
            ##Writing the constraint
            parent_binary = eqn_name_temp.replace('_bilin_cons_fmin', '_y')
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + temp_lhs + ' ' + single_sign_string(input_dataframes['cons_eqns_all']['RHS_value'][i], '-') + ' ' + parent_binary
            temp_term = temp_term + ' >= 0'
            f_data_set.write(temp_term + '\n')    

    f_data_set.write('\n')

    ##Writing the bilinear_limits_fmax_util constraints, only affects cons_eqns_terms_bilinear    
    f_data_set.write('\\\\Writing additional constraints: bilinear_limits_fmax_util \n \n') 
    for i in range (0, dim_cons_eqns_all[0]):                         
        if input_dataframes['cons_eqns_all']['Type'][i] == 'bilinear_limits_fmax_util':  
            eqn_name_temp = input_dataframes['cons_eqns_all']['Name'][i]                       
            rhs_value = str(input_dataframes['cons_eqns_all']['RHS_value'][i])
            temp_lhs = ''            
            ##Scanning through the bilinear list 
            for j in range (0, dim_cons_eqns_terms_bilinear[0]):
                if input_dataframes['cons_eqns_terms_bilinear']['Parent_eqn'][j] == eqn_name_temp:                
                    var_temp_name = input_dataframes['cons_eqns_terms_bilinear']['Variable'][j]
                    var_temp_name_y = var_temp_name + '_y'
                    check_empty = check_empty_string (temp_lhs)
                    ##All values need to be positive
                    if check_empty == 1:
                        temp_lhs = temp_lhs + str(input_dataframes['cons_eqns_terms_bilinear']['Grad'][j]) + ' ' + var_temp_name
                        temp_lhs = temp_lhs + single_sign_string(input_dataframes['cons_eqns_terms_bilinear']['Cst'][j], '+') + ' ' + var_temp_name_y
                    else:
                        temp_lhs = temp_lhs + single_sign_string(input_dataframes['cons_eqns_terms_bilinear']['Grad'][j], '+') + ' ' + var_temp_name
                        temp_lhs = temp_lhs + single_sign_string(input_dataframes['cons_eqns_terms_bilinear']['Cst'][j], '+') + ' ' + var_temp_name_y    
                        
            ##Writing the constraint
            parent_binary = eqn_name_temp.replace('_bilin_cons_fmax', '_y')
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + temp_lhs + ' - ' + rhs_value + ' ' + parent_binary + ' <= 0'
            f_data_set.write(temp_term + '\n')    

    f_data_set.write('\n')

    ##Writing the bilinear_limits_fmax_proc constraints, only affects cons_eqns_terms_bilinear, only fmax is needed for processes as it is an equality    
    f_data_set.write('\\\\Writing additional constraints: bilinear_limits_fmax_proc, equality \n \n') 
    for i in range (0, dim_cons_eqns_all[0]):                         
        if input_dataframes['cons_eqns_all']['Type'][i] == 'bilinear_limits_fmax_proc':  
            eqn_name_temp = input_dataframes['cons_eqns_all']['Name'][i]                       
            rhs_value = str(input_dataframes['cons_eqns_all']['RHS_value'][i])
            temp_lhs = ''            
            ##Scanning through the bilinear list 
            for j in range (0, dim_cons_eqns_terms_bilinear[0]):
                if input_dataframes['cons_eqns_terms_bilinear']['Parent_eqn'][j] == eqn_name_temp:                
                    var_temp_name = input_dataframes['cons_eqns_terms_bilinear']['Variable'][j]
                    var_temp_name_y = var_temp_name + '_y'
                    check_empty = check_empty_string (temp_lhs)
                    ##All values need to be positive
                    if check_empty == 1:
                        temp_lhs = temp_lhs + str(input_dataframes['cons_eqns_terms_bilinear']['Grad'][j]) + ' ' + var_temp_name
                        temp_lhs = temp_lhs + single_sign_string(input_dataframes['cons_eqns_terms_bilinear']['Cst'][j], '+') + ' ' + var_temp_name_y
                    else:
                        temp_lhs = temp_lhs + single_sign_string(input_dataframes['cons_eqns_terms_bilinear']['Grad'][j], '+') + ' ' + var_temp_name
                        temp_lhs = temp_lhs + single_sign_string(input_dataframes['cons_eqns_terms_bilinear']['Cst'][j], '+') + ' ' + var_temp_name_y    
                        
            ##Writing the constraint
            parent_binary = eqn_name_temp.replace('_bilin_cons_fmax', '_y')
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + temp_lhs + ' = ' + rhs_value
            f_data_set.write(temp_term + '\n')    
            
            ##Writing the constraint
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + parent_binary + ' = ' + str(1.0)
            f_data_set.write(temp_term + '\n') 
            


    f_data_set.write('\n')                           
###############################################################################################################################################################################################    
###############################################################################################################################################################################################
###############################################################################################################################################################################################
    ##Bounds section 

    ##Writing the binary variables 
    f_data_set.write('Binary \n \n')  
    
    ##Writing the binary variables for all the parent utilities

    for i in range (0, dim_utilitylist[0]):
        temp_term = ''
        temp_term = utilitylist['Name'][i] + '_y'
        f_data_set.write(temp_term + '\n')          

    for i in range (0, dim_utilitylist_bilinear[0]):
        temp_term = ''
        temp_term = input_dataframes['utilitylist_bilinear']['Name'][i] + '_y'
        f_data_set.write(temp_term + '\n')    

    f_data_set.write('\n')   
###############################################################################################################################################################################################    
###############################################################################################################################################################################################
###############################################################################################################################################################################################

    ##Wrapping up 
    f_data_set.write('End \n')    
    f_data_set.close
    return 
    
###############################################################################################################################################################################################
###############################################################################################################################################################################################
###############################################################################################################################################################################################

##Additional functions 

##This function returns the key to access the correct dataframe columns 
def obj_function_detect_genlp (obj_func):
    ##obj_func --- a string of values
    
    if obj_func == 'investment_cost':
        key = 'Cinv'
    elif obj_func == 'operation_cost':
        key = 'Cost'
    elif obj_func == 'power':
        key = 'Power'
    elif obj_func == 'impact':
        key = 'Impact'
        
    return key

##This function determines if a string is empty or not 
def check_empty_string (string):
    ##string --- a string of something 
    
    if not string:
        ret_val = 1
    else:
        ret_val = 0
    
    return ret_val

##This function determines the sign of the constraint
def determine_sign (sign_string):
    ##sign_string --- the string of the associated sign 
    
    if sign_string == 'less_than_equal_to': 
        ret_sign = ' <= '
    elif sign_string == 'equal_to': 
        ret_sign = ' = '
    elif sign_string == 'greater_than_equal_to':
        ret_sign = ' >= '
    return ret_sign

##This function checks if a value exists in the list 
def check_if_item_in_list (check_list, item):
    ##check_list --- the list where the item is to be checked against 
    ##item --- the item to be checked 
    
    dim_check_list = len(check_list)
    
    ret_value = 0
    for i in range (0, dim_check_list):
        if check_list[i] == item:
            ret_value = 1
            break
            
    return ret_value


    