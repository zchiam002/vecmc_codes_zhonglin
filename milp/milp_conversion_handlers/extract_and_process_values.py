##This function extracts the values of the objective functions and converts the bilinear values back to the original values 

def extract_and_process_values (ret_dataframes, utility_list, process_list, bilinear_pieces, solver_choice, parallel_thread_num, affected_list):

    ##ret_dataframes                                          --- it is a dictionary of dataframes
    ##ret_dataframes['utilitylist_bilinear']                  --- list of bilinear utilities 
    ##ret_dataframes['processlist_bilinear']                  --- list of bilinear processes
    ##ret_dataframes['streams_bilinear']                      --- list of bilinear streams 
    ##ret_dataframes['cons_eqns_terms_bilinear']              --- list of bilinear cons_eqns_terms
    ##ret_dataframes['utilitylist_linear']                    --- linear utility list 
    ##ret_dataframes['processlist_linear']                    --- linear process list 
    ##ret_dataframes['streams_linear']                        --- linear streams list 
    ##ret_dataframes['cons_eqns_terms_linear']                --- linear cons_eqns_terms 
    ##ret_dataframes['cons_eqns_all']                         --- all cons_eqns
    
    ##utility_list --- the list of all utilities 
    ##process_list --- the list of all processes
    ##bilinear_pieces --- the number of bilinear pieces
    ##solver_choice --- the choice of solvers 
    ##parallel_thread_num --- the associated parallel thread number
    ##affected_list --- the list of all the variables affected by bilinear constraints
        
    if solver_choice == 'glpk':
        obj_value, results, results_y = extract_glpk_results (ret_dataframes, utility_list, process_list, bilinear_pieces, parallel_thread_num, affected_list)
        
    
    return obj_value, results, results_y

############################################################################################################################################################################
##Additional functions

def extract_glpk_results (ret_dataframes, utility_list, process_list, bilinear_pieces, parallel_thread_num, affected_list):
    
    import os 
    current_path = os.path.dirname(__file__)[:-25] + '/' 
    import pandas as pd
    
    ##ret_dataframes                                          --- it is a dictionary of dataframes 
    ##ret_dataframes['utilitylist_bilinear']                  --- list of bilinear utilities 
    ##ret_dataframes['processlist_bilinear']                  --- list of bilinear processes
    ##ret_dataframes['streams_bilinear']                      --- list of bilinear streams 
    ##ret_dataframes['cons_eqns_terms_bilinear']              --- list of bilinear cons_eqns_terms
    ##ret_dataframes['utilitylist_linear']                    --- linear utility list 
    ##ret_dataframes['processlist_linear']                    --- linear process list 
    ##ret_dataframes['streams_linear']                        --- linear streams list 
    ##ret_dataframes['cons_eqns_terms_linear']                --- linear cons_eqns_terms 
    ##ret_dataframes['cons_eqns_all']                         --- all cons_eqns
    
    ##utility_list --- the list of all utilities 
    ##process_list --- the list of all processes
    ##bilinear_pieces --- the number of bilinear pieces
    ##solver_choice --- the choice of solvers 
    ##parallel_thread_num --- the associated parallel thread number
    ##affected_list --- the list of all the variables affected by bilinear constraints
    
    ##Result file location 
    result_file = current_path + 'milp_conversion_handlers\\solver_lp_format_holder\\' + r'\t' + 'hread_' + str(parallel_thread_num) + '\\out.txt'

    ##Extracting the objective function 
    with open(result_file) as fo:
        for rec in fo:
            if 'Objective:  ' in rec:
                obj = rec.split(' ')
                break
    obj_value = float(obj[4])
    
    ##Establishing a list of all variables and the total count
    data_needed = {}
    data_needed['utilitylist_bilinear'] = ret_dataframes['utilitylist_bilinear']
    data_needed['processlist_bilinear'] = ret_dataframes['processlist_bilinear']
    data_needed['utilitylist_linear'] = ret_dataframes['utilitylist_linear'] 
    data_needed['processlist_linear'] = ret_dataframes['processlist_linear'] 
    data_needed['affected_list'] = affected_list
    
    parent_all_list, total_num_var = determine_all_possible_variables(data_needed)
    
    ##Dataframe for storing the values of the results 
    result_dataframe = pd.DataFrame(columns = ['Name', 'Value'])
    starting_line = 0
    variable_count = 0
    
    ##To determine the last line in the records
    last_line = 0
    
    #Extracting the rest of the values 
    with open(result_file) as fo:
        for rec in fo:
            
            if last_line == 1:
                break
            else:
                check_split = rec.split()
                if check_split:
                    if starting_line < 2:
                        if len(check_split) != 0:
                            if str.isdigit(check_split[0]) == True:
                                if int(check_split[0]) == 1:
                                    starting_line = starting_line + 1
                    ##This is where the records should start
                    if starting_line == 2:
                        if variable_count < total_num_var:
                            if (str.isdigit(check_split[1]) == False) and (len(check_split[1]) > 12): 
                                temp_name = check_split[1]
                                check_split2 = next(fo).split()
                                ##Checking if the variable is binary
                                chk_val = check_if_binary(temp_name)
                                if chk_val == 0:
                                    temp_value = float(check_split2[0])
                                else:
                                    ##Checking if it is a utility or process binary variable 
                                    check_proc_util_bin_val = check_if_proc_binary_var (temp_name, process_list)
                                    if check_proc_util_bin_val == 0: 
                                        temp_value = float(check_split2[1])
                                    else:
                                        temp_value = float(check_split2[0])                               
                                temp_values = [temp_name, temp_value]
                                temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value'])
                                result_dataframe = result_dataframe.append(temp_df, ignore_index = True)
                                variable_count = variable_count + 1
                                
                            elif (str.isdigit(check_split[1]) == False):
                                if check_split[1] == 'feasibility':
                                    last_line = 1
                                    break
                                else:
                                    temp_name = check_split[1]
                                    chk_val = check_if_binary(temp_name)
                                    if chk_val == 0:
                                        temp_value = float(check_split[2])
                                    else:
                                        ##Checking if it is a utility or process binary variable 
                                        check_proc_util_bin_val = check_if_proc_binary_var (temp_name, process_list)
                                        if check_proc_util_bin_val == 0: 
                                            temp_value = float(check_split[3])
                                        else:
                                            temp_value = float(check_split[2])  
                                    temp_values = [temp_name, temp_value]
                                    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value'])
                                    result_dataframe = result_dataframe.append(temp_df, ignore_index = True)
                                    variable_count = variable_count + 1

    final_dataframe, final_dataframe_y = convert_back_to_original (result_dataframe, utility_list, process_list, bilinear_pieces)
        
    return obj_value, final_dataframe, final_dataframe_y

##This function converts to original variable name and sorts the continuous and binary variables separately  
def convert_back_to_original (result_dataframe, utility_list, process_list, bilinear_pieces):
    
    ##result_dataframe      --- the dataframe containing the results from the solver 
    ##utility_list          --- the dataframe containing information abourt the utilities 
    ##process_list          --- the dataframe containing information about the processes 
    ##bilinear_pieces       --- the number of bilinear pieces
    
    import pandas as pd
    
    ##Processing the bilinear and linear variable values 
    final_dataframe = pd.DataFrame(columns = ['Name', 'Values'])
    final_dataframe_y = pd.DataFrame(columns = ['Name', 'Values']) 
    
    dim_result_dataframe = result_dataframe.shape 
    
    u_value = 0
    v_value = 0
    bilin_count = 0
    
    for i in range (0, dim_result_dataframe[0]):
        
        ##Determining the length of the name
        temp_name = result_dataframe['Name'][i]
        temp_name_len = len(temp_name)
        temp_value = result_dataframe['Value'][i]
        
        ##Regular binary variable
        check_if_bilin_binary = check_if_binary_bilinear_affected_variable (temp_name, bilinear_pieces)
        chk_value, chk_value_type = check_if_cont_bilinear_affected_variable (temp_name, bilinear_pieces)
        if (temp_name[temp_name_len - 2] == '_') and (temp_name[temp_name_len - 1] == 'y') and (check_if_bilin_binary == 0):
            temp_data = [temp_name, temp_value]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Values'])
            final_dataframe_y = final_dataframe_y.append(temp_df, ignore_index = True)
        
        ##Regular continuous variable
        elif (temp_name[temp_name_len - 2] != '_') and (temp_name[temp_name_len - 1] != 'y') and (str.isdigit(temp_name[temp_name_len - 1]) == False):
            temp_data = [temp_name, temp_value]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Values'])
            final_dataframe = final_dataframe.append(temp_df, ignore_index = True)
            
        ##Handling Bilinear variables        
        elif (chk_value_type == 'u') and (chk_value == 1) and (bilin_count < 2 * bilinear_pieces):
            u_value = u_value + temp_value
            bilin_count = bilin_count + 1

        elif (chk_value_type == 'v') and (chk_value == 1) and (bilin_count < 2 * bilinear_pieces):
            v_value = v_value + temp_value
            bilin_count = bilin_count + 1
        
        ##The value has been added up
        if (bilin_count == 2 * bilinear_pieces):
            x_value_true = (u_value + v_value) / 2
            y_value_true = (u_value - v_value) / 2
            ##Finding the parent name
            parent_name_actual = temp_name.replace('_v' + str(bilinear_pieces - 1), '')
            ##Determining the variable names of the original parents 
            var1_name, var2_name = find_variable_names(parent_name_actual, utility_list, process_list)
            ##Determining the actual names of the variables 
            var1_name_actual = parent_name_actual + '_' + var1_name 
            var2_name_actual = parent_name_actual + '_' + var2_name
            ##Adding the values to the return dataframes 
            temp_data = [var1_name_actual, x_value_true]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Values'])
            final_dataframe = final_dataframe.append(temp_df, ignore_index = True)
            temp_data = [var2_name_actual, y_value_true]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Values'])
            final_dataframe = final_dataframe.append(temp_df, ignore_index = True)            
                            
            u_value = 0
            v_value = 0
            bilin_count = 0
            
    return final_dataframe, final_dataframe_y

##This is a function to check if 2 variable names, given a parent unit name 
def find_variable_names (parent_name, utilitylist, processlist):
    
    ##parent_name --- a given name 
    ##utilitylist --- the complete list of utilities 
    ##processlist --- the complete list of processes
    
    dim_utilitylist = utilitylist.shape
    dim_processlist = processlist.shape 
    
    check = 0
    for i in range (0, dim_utilitylist[0]):
        if utilitylist['Name'][i] == parent_name:
            var1_name = utilitylist['Variable1'][i]
            var2_name = utilitylist['Variable2'][i]
            check = 1
            break 
    
    if check == 0:
        for i in range (0, dim_processlist[0]):
            if processlist['Name'][i] == parent_name:
                var1_name = processlist['Variable1'][i]
                var2_name = processlist['Variable2'][i]
                check = 1
                break  
            
    return var1_name, var2_name

##This function returns a list of all the variables (continuous and binary) and the total count 
def determine_all_possible_variables(data_required):
    
    ##data_required     --- dictionary of values
    ##data_required['utilitylist_bilinear']
    ##data_required['processlist_bilinear']
    ##data_required['utilitylist_linear']
    ##data_required['processlist_linear'] 
    ##data_required['affected_list']
    
    ##Determining all the variables possible 
    dim_utilitylist_bilinear = data_required['utilitylist_bilinear'].shape
    dim_processlist_bilinear = data_required['processlist_bilinear'].shape
    dim_utilitylist_linear = data_required['utilitylist_linear'].shape
    dim_processlist_linear = data_required['processlist_linear'].shape
    dim_affected_list = data_required['affected_list'].shape
    
    parent_all_list = []

    ##Appending the list of all the names 
    
    for i in range(0, dim_utilitylist_bilinear[0]):
        parent_all_list.append(data_required['utilitylist_bilinear']['Name'][i])
        parent_all_list.append(data_required['utilitylist_bilinear']['Name'][i] + '_y')        

    for i in range(0, dim_processlist_bilinear[0]):
        parent_all_list.append(data_required['processlist_bilinear']['Name'][i])
        parent_all_list.append(data_required['processlist_bilinear']['Name'][i] + '_y')
          
    for i in range(0, dim_utilitylist_linear[0]):
        parent_all_list.append(data_required['utilitylist_linear']['Parent'][i] + '_' + data_required['utilitylist_linear']['Name'][i])
        parent_all_list.append(data_required['utilitylist_linear']['Parent'][i] + '_' + data_required['utilitylist_linear']['Name'][i] + '_y')

    for i in range(0, dim_processlist_linear[0]):
        parent_all_list.append(data_required['processlist_linear']['Parent'][i] + '_' + data_required['processlist_linear']['Name'][i])
        parent_all_list.append(data_required['processlist_linear']['Parent'][i] + '_' + data_required['processlist_linear']['Name'][i] + '_y')
        
    for i in range(0, dim_affected_list[0]):
        parent_all_list.append(data_required['affected_list']['Names'][i] + '_y')        
    
    ##Finding the total number of variables 
    total_num_var = len(parent_all_list)
    
    return parent_all_list, total_num_var 

##This function checks if a variable is binary or not 
def check_if_binary (var_name):
    
    ##var_name --- the name of the variable 
    
    ret_val = 0
    len_var = len(var_name)
    
    if (var_name[len_var - 2] == '_') and (var_name[len_var - 1] == 'y'):
        ret_val = 1
    
    return ret_val

##This function checks if the variable is a regular one or not 
def check_if_binary_bilinear_affected_variable (variable_name, bilinear_pieces):
    
    ##variable_name --- the variable_name to be checked 
    ##bilinear_pieces --- the number of bilinear_pieces
    
    max_len = len(str(bilinear_pieces - 1))
    
    ret_value = 0
    for i in range (0, max_len):
        if (variable_name[len(variable_name) - 4 - i] == 'u') and (str.isdigit(variable_name[len(variable_name) - 3 - i]) == True):
            ret_value = 1
            break
        elif (variable_name[len(variable_name) - 4 - i] == 'v') and (str.isdigit(variable_name[len(variable_name) - 3 - i]) == True):
            ret_value = 1
            break

    return ret_value

##This function checks if the variable is a continuous bilinear one or not 
def check_if_cont_bilinear_affected_variable (variable_name, bilinear_pieces):
    
    ##variable_name --- the variable_name to be checked 
    ##bilinear_pieces --- the number of bilinear_pieces
    
    max_len = len(str(bilinear_pieces - 1))
    
    ret_value = 0
    ret_type = ''
    for i in range (0, max_len):
        if (variable_name[len(variable_name) - 2 - i] == 'u') and (str.isdigit(variable_name[len(variable_name) - 1 - i]) == True):
            ret_value = 1
            ret_type = 'u'
            break
        elif (variable_name[len(variable_name) - 2 - i] == 'v') and (str.isdigit(variable_name[len(variable_name) - 1 - i]) == True):
            ret_value = 1
            ret_type = 'v'
            break

    return ret_value, ret_type

##This function checks if it is a process binary variable 
def check_if_proc_binary_var (name, processlist_original):
    
    ##name                  --- the vale of the variable 
    ##processlist_original  --- the original proceslist 
    
    checklist = processlist_original['Name'][:]
    iterations = len(checklist)
    
    ret_value = 0
    for i in range (0, iterations):
        if checklist[i] in name:
            ret_value = 1
            break
    
    return ret_value
