##This is the interface for defining the input and output to the master decision variable file

def multi_objective_master_backend (multi_time, mdv, wd, dd):
    import sys
    sys.path.append('C:\\Optimization_zlc\\master_level\\auxillary')
    sys.path.append('C:\\Optimization_zlc\\slave_level_models\\glpk_v1\\')
    sys.path.append('C:\\Optimization_zlc\\master_level\\NSGA_II')
    from input_data_process import extract_temp
    from input_data_process import extract_demand
    from master_decision_variables import master_decision_variables
    from parameters_to_dv import para_master_var
    from MOOSetUp import MOOSetUp
    import pandas as pd 
    
###############################################################################################################################################################
###############################################################################################################################################################

    ##Processing input data
    all_temp = extract_temp(wd)
    all_demand = extract_demand(dd)
    allm_var = master_decision_variables(mdv)
    
    if multi_time == 0:
        time_step = 0
        allm_var_ts = allm_var 
        allm_var_ts = para_master_var(all_temp, allm_var_ts, time_step, multi_time)
        
    elif multi_time != 0:
        time_step = 0 
        dim_all_demand = all_demand.shape
        num_time_steps = dim_all_demand[0]
     

        ##This may be different for different problems 
        allm_var_ts = pd.DataFrame(columns = ['Name', 'Value', 'Unit', 'LB', 'UB', 'Type'])
        
        
        for i in range (0, num_time_steps):
            allm_var_ts1 = allm_var  
            allm_var_ts1 = para_master_var(all_temp, allm_var_ts1, time_step, multi_time)
            allm_var_ts = allm_var_ts.append(allm_var_ts1, ignore_index=True)
            time_step = time_step + 1 

    
    print('Starting Optimization...')
    MOOSetUp(allm_var_ts)


        
    #print(all_temp)
    #print(all_demand)
    #print(allm_var)
    
    
###############################################################################################################################################################
    
    ##Create the csv file for master decision variables to act as slave parameters

    #master_slave_var = master_dv_2_slave_param(allm_var)
    #master_slave_var.to_csv('C:\\Optimization_zlc\\master_level\\master-slave_var.csv', encoding='utf-8')
    #allm_var_ts.to_csv('C:\\Optimization_zlc\\master_level\\allm_var_ts.csv', encoding='utf-8')  
###############################################################################################################################################################    
    
    ##Adding up and evaluating the values from both sides 
    
    return

