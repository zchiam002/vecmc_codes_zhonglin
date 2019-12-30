##This function uses parameters to fix constraints for the models 

def para_master_var(all_temp, allm_var_ts, time_step, multi_time):
    import pandas as pd
    ##time_step refers to the current time step which the optimization is at currently 
    
    allm_var_1 = pd.DataFrame(columns = ['Name', 'Value', 'Unit', 'LB', 'UB', 'Type'])
    
    key1 = 'ct_t_out'

    dim_allm_var = allm_var_ts.shape     
    
    if multi_time == 0:
        ##Creating the constraints for the ct_t_out and chiller_ret_etret
        for i in range (0, dim_allm_var[0]):
            if key1 in allm_var_ts['Name'][i]:
                if all_temp['T_WB'][time_step] > (273.15 + 22):                                             ##A conditional check such that the condenser temperature does not plunge too low 
                    x = all_temp['T_WB'][time_step]                                                         ##The lower bound of the cooling tower exit temperature is the wet bulb temperature
                    y = all_temp['T_WB'][time_step] + 10                                                    ##The maximum delta t of the cooling tower is 10 degrees
                else:
                    x = 273.15 + 22
                    y = 273.15 + 22 + 10
    
                values = [allm_var_ts['Name'][i], allm_var_ts['Value'][i], allm_var_ts['Unit'][i], x, y, allm_var_ts['Type'][i]]
                input_df = pd.DataFrame(data = [values], columns = ['Name', 'Value', 'Unit', 'LB', 'UB', 'Type'])
                allm_var_1 = allm_var_1.append(input_df, ignore_index=True)
                
            else:
                values = [allm_var_ts['Name'][i], allm_var_ts['Value'][i], allm_var_ts['Unit'][i], allm_var_ts['LB'][i], allm_var_ts['UB'][i], allm_var_ts['Type'][i]]
                input_df = pd.DataFrame(data = [values], columns = ['Name', 'Value', 'Unit', 'LB', 'UB', 'Type'])
                allm_var_1 = allm_var_1.append(input_df, ignore_index=True)
    
        return allm_var_1
        
    elif multi_time == 1:
        sub_script = '_' + str(time_step)
        for i in range (0, dim_allm_var[0]):
            if key1 in allm_var_ts['Name'][i]:              
                if all_temp['T_WB'][time_step] > (273.15 + 22):                                             ##A conditional check so that the condenser temperature does not plunge too low
                    x = all_temp['T_WB'][time_step]                                                         ##The lower bound of the cooling tower exit temperature is the wet bulb temperature
                    y = all_temp['T_WB'][time_step] + 10                                                    ##The maximum delta t of the cooling tower is 10 degrees
                else:
                    x = 273.15 + 22
                    y = 273.15 + 22 + 10
                    
                name =  allm_var_ts['Name'][i] + sub_script
                values = [name, allm_var_ts['Value'][i], allm_var_ts['Unit'][i], x, y, allm_var_ts['Type'][i]]
                input_df = pd.DataFrame(data = [values], columns = ['Name', 'Value', 'Unit', 'LB', 'UB', 'Type'])
                allm_var_1 = allm_var_1.append(input_df, ignore_index=True)
                
            else:
                name =  allm_var_ts['Name'][i] + sub_script 
                values = [name, allm_var_ts['Value'][i], allm_var_ts['Unit'][i], allm_var_ts['LB'][i], allm_var_ts['UB'][i], allm_var_ts['Type'][i]]
                input_df = pd.DataFrame(data = [values], columns = ['Name', 'Value', 'Unit', 'LB', 'UB', 'Type'])
                allm_var_1 = allm_var_1.append(input_df, ignore_index=True)
        
        
        return allm_var_1
        
