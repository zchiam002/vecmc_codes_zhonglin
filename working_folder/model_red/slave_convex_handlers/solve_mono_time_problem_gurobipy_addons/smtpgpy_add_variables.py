##This function adds variables to the gurobipy model 
def smtpgpy_add_variables (grb_model, input_dataframes, utilitylist, processlist):

    import gurobipy as grb    
    
    ##grb_model --- the gurobipy model
    ##input_dataframes, utilitylist, processlist --- list of processed data 
    
    ##Initializing dictionary for the involved variables 
    grb_var_dict_continuous = {}
    grb_var_dict_binary = {}
    
    ##Handling continuous variables first 
        ##Utilities
    dim_utilities_linear = input_dataframes['utilitylist_linear'].shape
    dim_utilities_bilinear = input_dataframes['utilitylist_bilinear'].shape
    
    for i in range (0, dim_utilities_linear[0]):
        temp_name = input_dataframes['utilitylist_linear']['Parent'][i] + '_' + input_dataframes['utilitylist_linear']['Name'][i]      
        temp_var = grb_model.addVar(vtype=grb.GRB.CONTINUOUS, name=temp_name)
        grb_var_dict_continuous[temp_name] = temp_var

    
    for i in range (0, dim_utilities_bilinear[0]):
        temp_name = input_dataframes['utilitylist_bilinear']['Name'][i]     
        temp_var = grb_model.addVar(vtype=grb.GRB.CONTINUOUS, name=temp_name)
        grb_var_dict_continuous[temp_name] = temp_var
        
        ##Processes 
    dim_processes_linear = input_dataframes['processlist_linear'].shape
    dim_processes_bilinear = input_dataframes['processlist_bilinear'].shape
    
    for i in range (0, dim_processes_linear[0]):
        temp_name = input_dataframes['processlist_linear']['Parent'][i] + '_' + input_dataframes['processlist_linear']['Name'][i]   
        temp_var = grb_model.addVar(vtype=grb.GRB.CONTINUOUS, name=temp_name) 
        grb_var_dict_continuous[temp_name] = temp_var
        
    for i in range (0, dim_processes_bilinear[0]):
        temp_name = input_dataframes['processlist_bilinear']['Name'][i]    
        temp_var = grb_model.addVar(vtype=grb.GRB.CONTINUOUS, name=temp_name)      
        grb_var_dict_continuous[temp_name] = temp_var        

            
    ##Handling binary variables
        ##Utilities
    dim_utilitylist = utilitylist.shape
    
    for i in range (0, dim_utilitylist[0]):
        temp_name = utilitylist['Name'][i] + '_y'
        temp_var = grb_model.addVar(vtype=grb.GRB.BINARY, name=temp_name)
        grb_var_dict_binary[temp_name] = temp_var         
        
    for i in range (0, dim_utilities_bilinear[0]):
        temp_name = input_dataframes['utilitylist_bilinear']['Name'][i] + '_y'  
        temp_var = grb_model.addVar(vtype=grb.GRB.BINARY, name=temp_name)
        grb_var_dict_binary[temp_name] = temp_var     
        
        ##Processes
    dim_processlist = processlist.shape

    for i in range (0, dim_processlist[0]):                                                     ##This ensures that the processes are always on.
        temp_name = processlist['Name'][i] + '_y'
        temp_var = grb_model.addVar(vtype=grb.GRB.BINARY, name=temp_name)
        grb_var_dict_binary[temp_name] = temp_var          
        
    for i in range (0, dim_processes_bilinear[0]):
        temp_name = input_dataframes['processlist_bilinear']['Name'][i] + '_y'
        temp_var = grb_model.addVar(vtype=grb.GRB.BINARY, name=temp_name)
        grb_var_dict_binary[temp_name] = temp_var           
        
    return grb_model, grb_var_dict_continuous, grb_var_dict_binary