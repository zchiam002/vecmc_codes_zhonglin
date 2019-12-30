###This function reverses the process of piecewise linearization 

def reverse_pwl (dt):
    
    import numpy as np 
    import pandas as pd 
    
    linear_pieces = 4
    
    ##Loading the results 
    results_loc = 'C:\\Optimization_zlc\\control_center\\paper_qe_testcase\\optimization_results\\opti_' + dt + '\\'
    data_name = dt + '_compute.csv'
    
    solved_results = pd.read_csv(results_loc + data_name)    
    dim_solved_results = solved_results.shape
    
    ##Dealing with the names of distribution pumps 
    dist_pumps_data = ['dist_np_4nc_combi_', 'm_flow', 'delp']
    num_pumps = 7
    
    ##Creating dist_pumps dataframe 
    dist_pump_df = pd.DataFrame(columns = ['Unit', 'v1', 'v2'])
    
    for i in range (0, num_pumps):
        name = dist_pumps_data[0] + str(i) + '_'
        temp_data = [name, dist_pumps_data[1], dist_pumps_data[2]]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['Unit', 'v1', 'v2'])
        dist_pump_df = dist_pump_df.append(temp_df, ignore_index = True)
        
    ##Creating chiller data
    chiller1_evap_data = ['ch1_4nc', '_evap', 'm_perc', 't_out']
    chiller2_evap_data = ['ch2_4nc', '_evap', 'm_perc', 't_out']
    chiller3_evap_data = ['ch3_4nc', '_evap', 'm_perc', 't_out']    
    
    
    not_affected_variables = pd.read_csv('C:\\Optimization_zlc\\slave_level_models\\paper_qe_testcase_slave_convex\\var_not_aff_pwl.csv')
    affected_variables = pd.read_csv('C:\\Optimization_zlc\\slave_level_models\\paper_qe_testcase_slave_convex\\var_aff_pwl.csv')
    
    ##Determining the number of variables 
    var_list = []
    
    ##Chiller evap first
    var_list.append(chiller1_evap_data[0] + chiller1_evap_data[1] + '_' + chiller1_evap_data[2])
    var_list.append(chiller1_evap_data[0] + chiller1_evap_data[1] + '_' + chiller1_evap_data[3])
    var_list.append(chiller2_evap_data[0] + chiller2_evap_data[1] + '_' + chiller2_evap_data[2])
    var_list.append(chiller2_evap_data[0] + chiller2_evap_data[1] + '_' + chiller2_evap_data[3])
    var_list.append(chiller3_evap_data[0] + chiller3_evap_data[1] + '_' + chiller3_evap_data[2])
    var_list.append(chiller3_evap_data[0] + chiller3_evap_data[1] + '_' + chiller3_evap_data[3])
        
    dim_dist_pump_df = dist_pump_df.shape
    for i in range (0, dim_dist_pump_df[0]):    
        var_list.append(dist_pump_df['Unit'][i] + dist_pump_df['v1'][i])
        var_list.append(dist_pump_df['Unit'][i] + dist_pump_df['v2'][i])    
        
    dim_not_affected_variables = not_affected_variables.shape
    for i in range (0, dim_not_affected_variables[0]):
        var_list.append(not_affected_variables['Name'][i] + '_' + not_affected_variables['v1'][i])
        if not_affected_variables['v2'][i] != '-':
            var_list.append(not_affected_variables['Name'][i] + '_' + not_affected_variables['v2'][i])            
    
    dim_affected_variables = affected_variables.shape
    for i in range (0, dim_affected_variables[0]):
        var_list.append(affected_variables['Name'][i] + affected_variables['v1'][i])
        if affected_variables['v2'][i] != '-':
            var_list.append(affected_variables['Name'][i] + affected_variables['v2'][i])     
    
    var_list.append('Obj_func')
    ##Creating the return dataframe 
    
    return_values_df = pd.DataFrame(columns = var_list)    
    num_ts = dim_solved_results[0]
    
    for i in range (0, num_ts):
        
        return_data = []
    
        ##Writing chiller values
        temp_value1 = 0
        temp_value2 = 0        
        temp_value3 = 0
        temp_value4 = 0  
        temp_value5 = 0
        temp_value6 = 0          
        for j in range (1, linear_pieces+1):
            code = chiller1_evap_data[0] + '_' + str(j) + chiller1_evap_data[1] + '_' + chiller1_evap_data[2]
            temp_value1 = temp_value1 + solved_results[code][i]
            
            code = chiller1_evap_data[0] + '_' + str(j) + chiller1_evap_data[1] + '_' + chiller1_evap_data[3]            
            temp_value2 = temp_value2 + solved_results[code][i]
            
            code = chiller2_evap_data[0] + '_' + str(j) + chiller2_evap_data[1] + '_' + chiller2_evap_data[2]
            temp_value3 = temp_value3 + solved_results[code][i]
            
            code = chiller2_evap_data[0] + '_' + str(j) + chiller2_evap_data[1] + '_' + chiller2_evap_data[3]            
            temp_value4 = temp_value4 + solved_results[code][i]
            
            code = chiller3_evap_data[0] + '_' + str(j) + chiller3_evap_data[1] + '_' + chiller3_evap_data[2]
            temp_value5 = temp_value5 + solved_results[code][i]
            
            code = chiller3_evap_data[0] + '_' + str(j) + chiller3_evap_data[1] + '_' + chiller3_evap_data[3]            
            temp_value6 = temp_value6 + solved_results[code][i] 
            
        return_data.append(temp_value1)
        return_data.append(temp_value2) 
        return_data.append(temp_value3)
        return_data.append(temp_value4) 
        return_data.append(temp_value5)
        return_data.append(temp_value6)     
    
        ##Writing dist_pump values
        for j in range (0, dim_dist_pump_df[0]):
            temp_value1 = 0
            temp_value2 = 0
            for k in range (0, linear_pieces):
                code = dist_pump_df['Unit'][j] + str(k) + '_' + dist_pump_df['v1'][j]
                temp_value1 = temp_value1 + solved_results[code][i]
                code = dist_pump_df['Unit'][j] + str(k) + '_' + dist_pump_df['v2'][j]
                temp_value2 = temp_value2 + solved_results[code][i]
            return_data.append(temp_value1)
            return_data.append(temp_value2)     

        ##Writing not affected values 
        for j in range (0, dim_not_affected_variables[0]):
            code = not_affected_variables['Name'][j] + '_' + not_affected_variables['v1'][j]
            return_data.append(solved_results[code][i])
            if not_affected_variables['v2'][j] != '-':
                code = not_affected_variables['Name'][j] + '_' + not_affected_variables['v2'][j]
                return_data.append(solved_results[code][i])
            
        ##Writing affected values 
        for j in range (0, dim_affected_variables[0]):
            temp_value1 = 0
            temp_value2 = 0
            for k in range (1, linear_pieces+1):
                code = affected_variables['Name'][j] + str(k)+ '_' + affected_variables['v1'][j]
                temp_value1 = temp_value1 + solved_results[code][i]
                if affected_variables['v2'][j] != '-':
                    code = affected_variables['Name'][j] + str(k)+ '_' + affected_variables['v2'][j]
                    temp_value2 = temp_value2 + solved_results[code][i]   
            return_data.append(temp_value1)
            if affected_variables['v2'][j] != '-':
                return_data.append(temp_value2)
            
        ##Making extremely low values 0
        for j in range (0, len(return_data)):
            if return_data[j] < (pow(10,-9)):
                return_data[j] = 0
        
        return_data.append(solved_results['obj'][i])
        temp_df1 = pd.DataFrame(data=[return_data], columns = var_list)
        return_values_df = return_values_df.append(temp_df1, ignore_index = True)
    
    return_values_df.to_csv('C:\\Optimization_zlc\\control_center\\paper_qe_testcase\\optimization_results\\opti_' + dt + '\\' + 'cleansed_' + dt + '.csv')
    
    name_df = pd.DataFrame(columns = ['Name'])
    for i in range (0, len(var_list)):
        temp_df_1 = pd.DataFrame(data = [var_list[i]], columns = ['Name'])
        name_df = name_df.append(temp_df_1, ignore_index = True)
    name_df.to_csv('C:\\Optimization_zlc\\control_center\\paper_qe_testcase\\optimization_results\\opti_' + dt + '\\' + 'cleansed_varlist_only_' + dt + '.csv')
    return return_values_df


############################################################################################################################################################

if __name__ == '__main__':
    dt = 'mid'
    cleansed = reverse_pwl (dt)