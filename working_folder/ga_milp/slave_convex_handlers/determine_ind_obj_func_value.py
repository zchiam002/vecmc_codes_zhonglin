##This function calculates the actual values of each objective function 

def determine_ind_obj_func_value (utilitylist, storagelist, processlist, obj_func, obj_weights, obj_value, results, results_y):
    
    import pandas as pd 
    
    ##utilitylist --- the list of all utilities 
    ##storagelist --- the list of all storages 
    ##processlist --- the list of all processes
    ##obj_func --- a list of objective functions 
    ##obj_weights --- the associated weights of the objective function 
    ##obj_value --- the combined value of the objective function (factoring it weights)
    ##results --- the continuous variable values 
    ##results_y --- the binary variable values 
    
    dim_utilitylist = utilitylist.shape
    dim_storagelist = storagelist.shape
    dim_processlist = processlist.shape
    
    dim_obj_func = len(obj_func)
    
    ##Determining the objective function key
    keys = []
    
    for i in range (0, dim_obj_func):
        keys.append(obj_function_detect_diofv (obj_func[i]))
        
    ##Creating a dataframe for returning the individual objective function values 
    ind_obj_value = pd.DataFrame(columns = ['Objective', 'Value', 'Weight'])
    
    ##Creating a dataframe to check the multiplication done in order to determine the final objective function value 
    obj_func_table_dict = {}
    
    for i in range (0, dim_obj_func):
        curr_obj_name = obj_func[i]
        obj_func_table_dict[curr_obj_name] = pd.DataFrame(columns = ['Unit_name', 'v1_name', 'v2_name', 'v1_value', 'v2_value', 'y_value', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2', 
                                             'Coeff_cst', 'obj_contri'])
    

    
    ##Calculating the individual objective functions
    for i in range (0, dim_obj_func):
        
        x_value_index = 0
        y_value_index = 0
        
        curr_obj_func = obj_func[i]
        curr_obj_func_value = 0
        
        ##Current obj function key 
        curr_key = keys[i]
        
        ##Handling utilitylist first 
        for j in range (0, dim_utilitylist[0]):
            
            obj_contri_util = 0
            
            if utilitylist['Variable2'][j] != '-':
                v2_name = utilitylist['Variable2'][j]
            else:
                v2_name = '-'
            
            if v2_name == '-':                                                  ##That means only 1 variable exists
                v1_value = results['Values'][x_value_index]
                v2_value = 0                                                    ##Letting the 2nd variable take on 0 value
                x_value_index = x_value_index + 1
            else:                                                               ##There exists 2 variables for the unit
                v1_value = results['Values'][x_value_index]
                v2_value = results['Values'][x_value_index + 1]                
                x_value_index = x_value_index + 2
            
            y_value = results_y['Values'][y_value_index]
            y_value_index = y_value_index + 1
            
            ##Calculating the contribution to the objective function 
            obj_contri_util = obj_contri_util + (utilitylist[curr_key + '_v1_2'][j] * pow(v1_value, 2))
            obj_contri_util = obj_contri_util + (utilitylist[curr_key + '_v1_1'][j] * v1_value)
            obj_contri_util = obj_contri_util + (utilitylist[curr_key + '_v2_2'][j] * pow(v2_value, 2))
            obj_contri_util = obj_contri_util + (utilitylist[curr_key + '_v2_1'][j] * v2_value)
            obj_contri_util = obj_contri_util + (utilitylist[curr_key + '_v1_v2'][j] * v1_value * v2_value)
            obj_contri_util = obj_contri_util + (utilitylist[curr_key + '_cst'][j] * y_value)
            
            temp_data = [utilitylist['Name'][j], utilitylist['Variable1'][j], v2_name, v1_value, v2_value, y_value, utilitylist[curr_key + '_v1_2'][j], utilitylist[curr_key + '_v1_1'][j], utilitylist[curr_key + '_v2_2'][j],
                         utilitylist[curr_key + '_v2_1'][j], utilitylist[curr_key + '_v1_v2'][j], utilitylist[curr_key + '_cst'][j], obj_contri_util]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Unit_name', 'v1_name', 'v2_name', 'v1_value', 'v2_value', 'y_value', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2', 
                                                                  'Coeff_cst', 'obj_contri'])
            obj_func_table_dict[curr_obj_func] = obj_func_table_dict[curr_obj_func].append(temp_df, ignore_index = True)
            
            ##Updating the objective function value
            curr_obj_func_value = curr_obj_func_value + obj_contri_util
            
        ##Handling the storagelist next 
        for j in range (0, dim_storagelist[0]):
            
            obj_contri_sto = 0
            
            if storagelist['Variable2'][j] != '-':
                v2_name = storagelist['Variable2'][j]
            else:
                v2_name = '-'
            
            if v2_name == '-':                                                  ##That means only 1 variable exists
                v1_value = results['Values'][x_value_index]
                v2_value = 0                                                    ##Letting the 2nd variable take on 0 value
                x_value_index = x_value_index + 1
            else:                                                               ##There exists 2 variables for the unit
                v1_value = results['Values'][x_value_index]
                v2_value = results['Values'][x_value_index + 1]
                x_value_index = x_value_index + 2
            
            y_value = results_y['Values'][y_value_index]
            y_value_index = y_value_index + 1
            
            ##Calculating the contribution to the objective function 
            obj_contri_sto = obj_contri_sto + (storagelist[curr_key + '_v1_2'][j] * pow(v1_value, 2))
            obj_contri_sto = obj_contri_sto + (storagelist[curr_key + '_v1_1'][j] * v1_value)
            obj_contri_sto = obj_contri_sto + (storagelist[curr_key + '_v2_2'][j] * pow(v2_value, 2))
            obj_contri_sto = obj_contri_sto + (storagelist[curr_key + '_v2_1'][j] * v2_value)
            obj_contri_sto = obj_contri_sto + (storagelist[curr_key + '_v1_v2'][j] * v1_value * v2_value)
            obj_contri_sto = obj_contri_sto + (storagelist[curr_key + '_cst'][j] * y_value)
            
            temp_data = [storagelist['Name'][j], storagelist['Variable1'][j], v2_name, v1_value, v2_value, y_value, storagelist[curr_key + '_v1_2'][j], storagelist[curr_key + '_v1_1'][j], storagelist[curr_key + '_v2_2'][j],
                         storagelist[curr_key + '_v2_1'][j], storagelist[curr_key + '_v1_v2'][j], storagelist[curr_key + '_cst'][j], obj_contri_sto]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Unit_name', 'v1_name', 'v2_name', 'v1_value', 'v2_value', 'y_value', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2', 
                                                                  'Coeff_cst', 'obj_contri'])
            obj_func_table_dict[curr_obj_func] = obj_func_table_dict[curr_obj_func].append(temp_df, ignore_index = True)
            
            ##Updating the objective function value
            curr_obj_func_value = curr_obj_func_value + obj_contri_sto            
            
        ##Handling the processlist last 
        for j in range (0, dim_processlist[0]):
            
            obj_contri_pro = 0
            
            if processlist['Variable2'][j] != '-':
                v2_name = processlist['Variable2'][j]
            else:
                v2_name = '-'
            
            if v2_name == '-':                                                  ##That means only 1 variable exists
                v1_value = results['Values'][x_value_index]
                v2_value = 0                                                    ##Letting the 2nd variable take on 0 value
                x_value_index = x_value_index + 1
            else:                                                               ##There exists 2 variables for the unit
                v1_value = results['Values'][x_value_index]
                v2_value = results['Values'][x_value_index + 1]
                x_value_index = x_value_index + 2
            
            y_value = results_y['Values'][y_value_index]
            y_value_index = y_value_index + 1
            
            ##Calculating the contribution to the objective function 
            obj_contri_pro = obj_contri_pro + (processlist[curr_key + '_v1_2'][j] * pow(v1_value, 2))
            obj_contri_pro = obj_contri_pro + (processlist[curr_key + '_v1_1'][j] * v1_value)
            obj_contri_pro = obj_contri_pro + (processlist[curr_key + '_v2_2'][j] * pow(v2_value, 2))
            obj_contri_pro = obj_contri_pro + (processlist[curr_key + '_v2_1'][j] * v2_value)
            obj_contri_pro = obj_contri_pro + (processlist[curr_key + '_v1_v2'][j] * v1_value * v2_value)
            obj_contri_pro = obj_contri_pro + (processlist[curr_key + '_cst'][j] * y_value)
            
            temp_data = [processlist['Name'][j], processlist['Variable1'][j], v2_name, v1_value, v2_value, y_value, processlist[curr_key + '_v1_2'][j], processlist[curr_key + '_v1_1'][j], processlist[curr_key + '_v2_2'][j],
                         processlist[curr_key + '_v2_1'][j], processlist[curr_key + '_v1_v2'][j], processlist[curr_key + '_cst'][j], obj_contri_pro]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Unit_name', 'v1_name', 'v2_name', 'v1_value', 'v2_value', 'y_value', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2', 
                                                                  'Coeff_cst', 'obj_contri'])
            obj_func_table_dict[curr_obj_func] = obj_func_table_dict[curr_obj_func].append(temp_df, ignore_index = True)
            
            ##Updating the objective function value
            curr_obj_func_value = curr_obj_func_value + obj_contri_pro
    
        temp_data_curr_obj_func = [curr_obj_func, curr_obj_func_value, obj_weights[i]]
        temp_df_curr_obj_func = pd.DataFrame(data = [temp_data_curr_obj_func], columns = ['Objective', 'Value', 'Weight'])
        ind_obj_value = ind_obj_value.append(temp_df_curr_obj_func, ignore_index = True)
        
    
    return obj_func_table_dict, ind_obj_value

#######################################################################################################################################################################################################

##This function just returns the appropriate key to seach based on the entered objective function for the slave
def obj_function_detect_diofv (obj_func_select):
    
    ##obj_func --- a string of values
    
    if obj_func_select == 'investment_cost':
        key = 'Cinv'
    elif obj_func_select == 'operation_cost':
        key = 'Cost'
    elif obj_func_select == 'power':
        key = 'Power'
    elif obj_func_select == 'impact':
        key = 'Impact'
        
    return key


