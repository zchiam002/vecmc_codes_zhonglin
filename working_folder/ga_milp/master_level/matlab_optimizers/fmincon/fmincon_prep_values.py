##This function prepares the starting point, lower and upper bound information which is then to be utilized by matlab optimizers

def fmincon_prep_values (multi_time, mdv, wd, dd):
    import sys
    sys.path.append('C:\\Optimization_zlc\\master_level\\')
    sys.path.append('C:\\Optimization_zlc\\master_level\\auxillary')
    sys.path.append('C:\\Optimization_zlc\\master_level\\NSGA_II')
    from input_data_process import extract_temp
    from input_data_process import extract_demand
    from master_decision_variables import master_decision_variables
    from parameters_to_dv import para_master_var
    import pandas as pd 
    import numpy as np
    
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
        
    ##Preparing the values for optimization
    dim_allm_var_ts = allm_var_ts.shape
    sp = ''
    lb = ''
    ub = ''
    for i in range (0, dim_allm_var_ts[0]):
        sp = sp + str(allm_var_ts['Value'][i]) + ', '
        lb = lb + str(allm_var_ts['LB'][i]) + ', '
        ub = ub + str(allm_var_ts['UB'][i]) + ', '
    
    sp_data_value = open('C:\\Optimization_zlc\\master_level\\Matlab_Optimizers\\Fmincon\\values_for_matlab_manual\\sp.txt','w')
    sp_data_value.write(sp)
    sp_data_value.close
    
    lb_data_value = open('C:\\Optimization_zlc\\master_level\\Matlab_Optimizers\\Fmincon\\values_for_matlab_manual\\lb.txt','w')
    lb_data_value.write(lb)
    lb_data_value.close   
    
    ub_data_value = open('C:\\Optimization_zlc\\master_level\\Matlab_Optimizers\\Fmincon\\values_for_matlab_manual\\ub.txt','w')
    ub_data_value.write(ub)
    ub_data_value.close
            
    print('Preparation done...')

        
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

