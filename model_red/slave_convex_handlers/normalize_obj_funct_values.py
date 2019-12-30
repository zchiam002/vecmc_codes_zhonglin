##This function is introducted to normalize the objective function values. It does place the values exactly within the bounds of 0 and 1, but introduces a scale factor such that the objectives 
##are similar in magnitude

def normalize_obj_funct_values (utilitylist, storagelist, processlist, obj_func, obj_weights, time_steps):
    
    import pandas as pd 
    
    ##utilitylist --- the list of all utilities 
    ##storagelist --- the list of all the storages 
    ##processlist --- the list of all the processes
    ##obj_func --- the list of all the objective functions 
    ##obj_weights --- the list of all the associated weights 
    ##time_steps --- the number of time steps
    
    ##Normalize the required objective functions
        ##To do that, the max and min of each are required 
    
    dim_utilitylist = utilitylist.shape 
    dim_storagelist = storagelist.shape
    dim_processlist = processlist.shape
    
    ##Lists to store the min and max values of each objective function across the time horizon
    obj_min = []
    obj_max = []

    for i in range (0, len(obj_func)):
        obj_min.append(0)
        obj_max.append(0)
        
    ##Determine a list of scale factors 
    scale_list = []
    for i in range (0, len(obj_func)):
        scale_list.append(0)    
    
    ##Determine the access codes to the dataframe of information 
    keys = []
    
    for i in range(0, len(obj_func)):
        keys.append(obj_function_detect_nofv (obj_func[i]))
    
    for i in range (0, len(obj_func)):
        
        curr_key = keys[i]
        
        for j in range (0, dim_utilitylist[0]):
            if utilitylist['Variable2'][j] != '-':
                obj_min[i] = obj_min[i] + (utilitylist[curr_key + '_v1_2'][j] * pow(utilitylist['Fmin_v1'][j], 2))
                obj_min[i] = obj_min[i] + (utilitylist[curr_key + '_v1_1'][j] * utilitylist['Fmin_v1'][j])
                obj_min[i] = obj_min[i] + (utilitylist[curr_key + '_v2_2'][j] * pow(utilitylist['Fmin_v2'][j], 2))
                obj_min[i] = obj_min[i] + (utilitylist[curr_key + '_v2_1'][j] * utilitylist['Fmin_v2'][j])
                obj_min[i] = obj_min[i] + (utilitylist[curr_key + '_v1_v2'][j] * (utilitylist['Fmin_v1'][j] * utilitylist['Fmin_v2'][j])) 
                obj_min[i] = obj_min[i] + utilitylist[curr_key + '_cst'][j] 
                
                obj_max[i] = obj_max[i] + (utilitylist[curr_key + '_v1_2'][j] * pow(utilitylist['Fmax_v1'][j], 2))
                obj_max[i] = obj_max[i] + (utilitylist[curr_key + '_v1_1'][j] * utilitylist['Fmax_v1'][j])
                obj_max[i] = obj_max[i] + (utilitylist[curr_key + '_v2_2'][j] * pow(utilitylist['Fmax_v2'][j], 2))
                obj_max[i] = obj_max[i] + (utilitylist[curr_key + '_v2_1'][j] * utilitylist['Fmax_v2'][j])
                obj_max[i] = obj_max[i] + (utilitylist[curr_key + '_v1_v2'][j] * (utilitylist['Fmax_v1'][j] * utilitylist['Fmax_v2'][j])) 
                obj_max[i] = obj_max[i] + utilitylist[curr_key + '_cst'][j]                
                
                
            else:
                obj_min[i] = obj_min[i] + (utilitylist[curr_key + '_v1_2'][j] * pow(utilitylist['Fmin_v1'][j], 2))
                obj_min[i] = obj_min[i] + (utilitylist[curr_key + '_v1_1'][j] * utilitylist['Fmin_v1'][j])                
                obj_min[i] = obj_min[i] + utilitylist[curr_key + '_cst'][j]         

                obj_max[i] = obj_max[i] + (utilitylist[curr_key + '_v1_2'][j] * pow(utilitylist['Fmax_v1'][j], 2))
                obj_max[i] = obj_max[i] + (utilitylist[curr_key + '_v1_1'][j] * utilitylist['Fmax_v1'][j])                
                obj_max[i] = obj_max[i] + utilitylist[curr_key + '_cst'][j]  
        
        for j in range (0, dim_storagelist[0]):
            if storagelist['Variable2'][j] != '-':
                obj_min[i] = obj_min[i] + (storagelist[curr_key + '_v1_2'][j] * pow(storagelist['Fmin_v1'][j], 2))
                obj_min[i] = obj_min[i] + (storagelist[curr_key + '_v1_1'][j] * storagelist['Fmin_v1'][j])
                obj_min[i] = obj_min[i] + (storagelist[curr_key + '_v2_2'][j] * pow(storagelist['Fmin_v2'][j], 2))
                obj_min[i] = obj_min[i] + (storagelist[curr_key + '_v2_1'][j] * storagelist['Fmin_v2'][j])
                obj_min[i] = obj_min[i] + (storagelist[curr_key + '_v1_v2'][j] * (storagelist['Fmin_v1'][j] * storagelist['Fmin_v2'][j])) 
                obj_min[i] = obj_min[i] + storagelist[curr_key + '_cst'][j] 
                
                obj_max[i] = obj_max[i] + (storagelist[curr_key + '_v1_2'][j] * pow(storagelist['Fmax_v1'][j], 2))
                obj_max[i] = obj_max[i] + (storagelist[curr_key + '_v1_1'][j] * storagelist['Fmax_v1'][j])
                obj_max[i] = obj_max[i] + (storagelist[curr_key + '_v2_2'][j] * pow(storagelist['Fmax_v2'][j], 2))
                obj_max[i] = obj_max[i] + (storagelist[curr_key + '_v2_1'][j] * storagelist['Fmax_v2'][j])
                obj_max[i] = obj_max[i] + (storagelist[curr_key + '_v1_v2'][j] * (storagelist['Fmax_v1'][j] * storagelist['Fmax_v2'][j])) 
                obj_max[i] = obj_max[i] + storagelist[curr_key + '_cst'][j]                
                
                
            else:
                obj_min[i] = obj_min[i] + (storagelist[curr_key + '_v1_2'][j] * pow(storagelist['Fmin_v1'][j], 2))
                obj_min[i] = obj_min[i] + (storagelist[curr_key + '_v1_1'][j] * storagelist['Fmin_v1'][j])                
                obj_min[i] = obj_min[i] + storagelist[curr_key + '_cst'][j]         

                obj_max[i] = obj_max[i] + (storagelist[curr_key + '_v1_2'][j] * pow(storagelist['Fmax_v1'][j], 2))
                obj_max[i] = obj_max[i] + (storagelist[curr_key + '_v1_1'][j] * storagelist['Fmax_v1'][j])                
                obj_max[i] = obj_max[i] + storagelist[curr_key + '_cst'][j]  
                

        for j in range (0, dim_processlist[0]):
            if processlist['Variable2'][j] != '-':
                obj_min[i] = obj_min[i] + (processlist[curr_key + '_v1_2'][j] * pow(processlist['Fmin_v1'][j], 2))
                obj_min[i] = obj_min[i] + (processlist[curr_key + '_v1_1'][j] * processlist['Fmin_v1'][j])
                obj_min[i] = obj_min[i] + (processlist[curr_key + '_v2_2'][j] * pow(processlist['Fmin_v2'][j], 2))
                obj_min[i] = obj_min[i] + (processlist[curr_key + '_v2_1'][j] * processlist['Fmin_v2'][j])
                obj_min[i] = obj_min[i] + (processlist[curr_key + '_v1_v2'][j] * (processlist['Fmin_v1'][j] * processlist['Fmin_v2'][j])) 
                obj_min[i] = obj_min[i] + processlist[curr_key + '_cst'][j] 
                
                obj_max[i] = obj_max[i] + (processlist[curr_key + '_v1_2'][j] * pow(processlist['Fmax_v1'][j], 2))
                obj_max[i] = obj_max[i] + (processlist[curr_key + '_v1_1'][j] * processlist['Fmax_v1'][j])
                obj_max[i] = obj_max[i] + (processlist[curr_key + '_v2_2'][j] * pow(processlist['Fmax_v2'][j], 2))
                obj_max[i] = obj_max[i] + (processlist[curr_key + '_v2_1'][j] * processlist['Fmax_v2'][j])
                obj_max[i] = obj_max[i] + (processlist[curr_key + '_v1_v2'][j] * (processlist['Fmax_v1'][j] * processlist['Fmax_v2'][j])) 
                obj_max[i] = obj_max[i] + processlist[curr_key + '_cst'][j]                
                
                
            else:
                obj_min[i] = obj_min[i] + (processlist[curr_key + '_v1_2'][j] * pow(processlist['Fmin_v1'][j], 2))
                obj_min[i] = obj_min[i] + (processlist[curr_key + '_v1_1'][j] * processlist['Fmin_v1'][j])                
                obj_min[i] = obj_min[i] + processlist[curr_key + '_cst'][j]         

                obj_max[i] = obj_max[i] + (processlist[curr_key + '_v1_2'][j] * pow(processlist['Fmax_v1'][j], 2))
                obj_max[i] = obj_max[i] + (processlist[curr_key + '_v1_1'][j] * processlist['Fmax_v1'][j])                
                obj_max[i] = obj_max[i] + processlist[curr_key + '_cst'][j]    
                
    
    ##For now the scaling is done using only the maximum values 
    smallest_max_obj_value = min(obj_max)
    
    for i in range (0, len(obj_func)):
        scale_list[i] = smallest_max_obj_value / obj_max[i]               

    return scale_list

#######################################################################################################################################################################################################

##This function just returns the appropriate key to seach based on the entered objective function for the slave
def obj_function_detect_nofv (obj_func_select):
    
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