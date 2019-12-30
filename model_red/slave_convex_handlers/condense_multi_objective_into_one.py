##This function condenses the objective function into a single one, with the consideration of weights 
##After this process, all objective functions will be 'investment_cost' or 'Cinv'

def condense_multi_objective_into_one (utilitylist, storagelist, processlist, obj_func, obj_weights, obj_func_scale_list):
    
    import pandas as pd 
    
    ##utilitylist --- the list of all utilities and the associate attributes
    ##storagelist --- the list of all storages and the associate attributes
    ##processlist --- the list of all process and the associate attributes
    ##obj_func --- the list of objective functions selected 
    ##obj_weights --- the associated weights of each objective function 
    ##obj_func_scale_list --- the list of scaling so that no objective function will dominate the other
    
    ##Determining the number of objective functions
    num_obj = len(obj_func)
    keys = []
    ##Determinig the associated keys for accessing the values in the objective function table 
    for i in range (0, num_obj):
        key_curr = obj_function_detect_cmoio (obj_func[i])
        keys.append(key_curr)
        
    ##Arbiturarily determining a representative objective function 
    rep_obj_func = 'investment_cost'
    
    ##Column labels for return dataframes 
    column_labels = ['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 
                     'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2', 'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 
                     'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2', 'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst']
    
    
    ##Handling utilitylist 
        ##new dataframe for utilities 
        
    util_new = pd.DataFrame(columns = column_labels)
    
    dim_utilitylist = utilitylist.shape
    
    for i in range (0, dim_utilitylist[0]):
        
        obj_v1_2 = 0
        obj_v1_1 = 0
        obj_v2_2 = 0
        obj_v2_1 = 0
        obj_v1_v2 = 0
        obj_cst = 0
        
        ##Combining the objective functions 
        for j in range (0, num_obj):
            obj_v1_2 = obj_v1_2 + (utilitylist[keys[j] + '_v1_2'][i] * obj_weights[j] * obj_func_scale_list[j]) 
            obj_v1_1 = obj_v1_1 + (utilitylist[keys[j] + '_v1_1'][i] * obj_weights[j] * obj_func_scale_list[j])
            obj_v2_2 = obj_v2_2 + (utilitylist[keys[j] + '_v2_2'][i] * obj_weights[j] * obj_func_scale_list[j])
            obj_v2_1 = obj_v2_1 + (utilitylist[keys[j] + '_v2_1'][i] * obj_weights[j] * obj_func_scale_list[j])
            obj_v1_v2 = obj_v1_v2 + (utilitylist[keys[j] + '_v1_v2'][i] * obj_weights[j] * obj_func_scale_list[j]) 
            obj_cst = obj_cst + (utilitylist[keys[j] + '_cst'][i] * obj_weights[j] * obj_func_scale_list[j])
            
        temp_data = [utilitylist['Name'][i], utilitylist['Variable1'][i], utilitylist['Variable2'][i], utilitylist['Fmin_v1'][i], utilitylist['Fmax_v1'][i], utilitylist['Fmin_v2'][i],
                     utilitylist['Fmax_v2'][i], utilitylist['Coeff_v1_2'][i], utilitylist['Coeff_v1_1'][i], utilitylist['Coeff_v2_2'][i], utilitylist['Coeff_v2_1'][i], 
                     utilitylist['Coeff_v1_v2'][i], utilitylist['Coeff_cst'][i], utilitylist['Fmin'][i], utilitylist['Fmax'][i], 0, 0, 0, 0, 0, 0, obj_v1_2, obj_v1_1, obj_v2_2, obj_v2_1, 
                     obj_v1_v2, obj_cst, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        temp_df = pd.DataFrame(data = [temp_data], columns = column_labels)
        util_new = util_new.append(temp_df, ignore_index = True)
        
    ##Handling storagelist 
        ##new dataframe for storages
        
    sto_new = pd.DataFrame(columns = column_labels)
    
    dim_storagelist = storagelist.shape
    
    for i in range (0, dim_storagelist[0]):
        
        obj_v1_2 = 0
        obj_v1_1 = 0
        obj_v2_2 = 0
        obj_v2_1 = 0
        obj_v1_v2 = 0
        obj_cst = 0
        
        ##Combining the objective functions 
        for j in range (0, num_obj):
            obj_v1_2 = obj_v1_2 + (storagelist[keys[j] + '_v1_2'][i] * obj_weights[j] * obj_func_scale_list[j])
            obj_v1_1 = obj_v1_1 + (storagelist[keys[j] + '_v1_1'][i] * obj_weights[j] * obj_func_scale_list[j])
            obj_v2_2 = obj_v2_2 + (storagelist[keys[j] + '_v2_2'][i] * obj_weights[j] * obj_func_scale_list[j])
            obj_v2_1 = obj_v2_1 + (storagelist[keys[j] + '_v2_1'][i] * obj_weights[j] * obj_func_scale_list[j])
            obj_v1_v2 = obj_v1_v2 + (storagelist[keys[j] + '_v1_v2'][i] * obj_weights[j] * obj_func_scale_list[j]) 
            obj_cst = obj_cst + (storagelist[keys[j] + '_cst'][i] * obj_weights[j] * obj_func_scale_list[j])
            
        temp_data = [storagelist['Name'][i], storagelist['Variable1'][i], storagelist['Variable2'][i], storagelist['Fmin_v1'][i], storagelist['Fmax_v1'][i], storagelist['Fmin_v2'][i],
                     storagelist['Fmax_v2'][i], storagelist['Coeff_v1_2'][i], storagelist['Coeff_v1_1'][i], storagelist['Coeff_v2_2'][i], storagelist['Coeff_v2_1'][i], 
                     storagelist['Coeff_v1_v2'][i], storagelist['Coeff_cst'][i], storagelist['Fmin'][i], storagelist['Fmax'][i], 0, 0, 0, 0, 0, 0, obj_v1_2, obj_v1_1, obj_v2_2, obj_v2_1, 
                     obj_v1_v2, obj_cst, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        temp_df = pd.DataFrame(data = [temp_data], columns = column_labels)
        sto_new = sto_new.append(temp_df, ignore_index = True)    

    ##Handling processlist 
        ##new dataframe for processes
        
    pro_new = pd.DataFrame(columns = column_labels)
    
    dim_processlist = processlist.shape
    
    for i in range (0, dim_processlist[0]):
        
        obj_v1_2 = 0
        obj_v1_1 = 0
        obj_v2_2 = 0
        obj_v2_1 = 0
        obj_v1_v2 = 0
        obj_cst = 0
        
        ##Combining the objective functions 
        for j in range (0, num_obj):
            obj_v1_2 = obj_v1_2 + (processlist[keys[j] + '_v1_2'][i] * obj_weights[j] * obj_func_scale_list[j])
            obj_v1_1 = obj_v1_1 + (processlist[keys[j] + '_v1_1'][i] * obj_weights[j] * obj_func_scale_list[j])
            obj_v2_2 = obj_v2_2 + (processlist[keys[j] + '_v2_2'][i] * obj_weights[j] * obj_func_scale_list[j])
            obj_v2_1 = obj_v2_1 + (processlist[keys[j] + '_v2_1'][i] * obj_weights[j] * obj_func_scale_list[j])
            obj_v1_v2 = obj_v1_v2 + (processlist[keys[j] + '_v1_v2'][i] * obj_weights[j] * obj_func_scale_list[j]) 
            obj_cst = obj_cst + (processlist[keys[j] + '_cst'][i] * obj_weights[j] * obj_func_scale_list[j])
            
        temp_data = [processlist['Name'][i], processlist['Variable1'][i], processlist['Variable2'][i], processlist['Fmin_v1'][i], processlist['Fmax_v1'][i], processlist['Fmin_v2'][i],
                     processlist['Fmax_v2'][i], processlist['Coeff_v1_2'][i], processlist['Coeff_v1_1'][i], processlist['Coeff_v2_2'][i], processlist['Coeff_v2_1'][i], 
                     processlist['Coeff_v1_v2'][i], processlist['Coeff_cst'][i], processlist['Fmin'][i], processlist['Fmax'][i], 0, 0, 0, 0, 0, 0, obj_v1_2, obj_v1_1, obj_v2_2, obj_v2_1, 
                     obj_v1_v2, obj_cst, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        temp_df = pd.DataFrame(data = [temp_data], columns = column_labels)
        pro_new = pro_new.append(temp_df, ignore_index = True)        
    
    return util_new, sto_new, pro_new, rep_obj_func

#######################################################################################################################################################################################################

##This function just returns the appropriate key to seach based on the entered objective function for the slave
def obj_function_detect_cmoio (obj_func_select):
    
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