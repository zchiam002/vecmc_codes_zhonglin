##This function handles master-level variables for the linear program 

def process_master_var (modelname, parallel_thread_num):         #modelname is a string which contains the model name  
    
    import pandas as pd
    master_var = pd.read_csv('C:\\Optimization_zlc\\slave_convex_handlers\\master_values\\master_slave_var_list_' + str(parallel_thread_num) + '.csv')
    
    rows=len(master_var.index)                      #Parsing the master decision variables as parameters for the linear program 
    model_mvar = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])    
    
    for i in range (0,rows):
        if modelname in master_var['Name'][i]:
            value = [master_var['Name'][i], master_var['Value'][i], master_var['Unit'][i]]
            temp = pd.DataFrame(data = [value], columns = ['Name', 'Value', 'Unit'])
            model_mvar = model_mvar.append(temp, ignore_index=True)
    
    
    return model_mvar

##This is function for multi-time processing
def process_master_var_v2 (modelname, parallel_thread_num, curr_time_step):         #modelname is a string which contains the model name  
    
    import pandas as pd
    
    master_var = pd.read_csv('C:\\Optimization_zlc\\slave_convex_handlers\\master_values\\master_slave_var_list_' + str(parallel_thread_num) + '.csv')
    
    rows=len(master_var.index)                      #Parsing the master decision variables as parameters for the linear program 
    model_mvar = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])    
    
    for i in range (0,rows):
        if modelname in master_var['Name'][i]:
            value = [master_var['Name'][i], master_var['Value_' + str(curr_time_step)][i], master_var['Unit'][i]]
            temp = pd.DataFrame(data = [value], columns = ['Name', 'Value', 'Unit'])
            model_mvar = model_mvar.append(temp, ignore_index=True)
    
    
    return model_mvar
       