##This function calculates the real values for the variables 

def determine_real_values (dt):
    import numpy as np 
    import pandas as pd 
    
    ##Import the solved data 
    solved_data_loc = 'C:\\Optimization_zlc\\control_center\\paper_qe_testcase\\optimization_results\\opti_' + dt + '\\cleansed_' + dt + '.csv'
    solved_data = pd.read_csv(solved_data_loc)
    
    ##Importing the variable list 
    solved_var_loc = 'C:\\Optimization_zlc\\control_center\\paper_qe_testcase\\optimization_results\\opti_' + dt + '\\cleansed_varlist_only_' + dt + '.csv'
    solved_varlist = pd.read_csv(solved_var_loc)
    
    ##Creating variable list 
    var_list = []
    dim_solved_varlist  = solved_varlist.shape 
    
    for i in range(0, dim_solved_varlist[0]):
        var_list.append(solved_varlist['Name'][i])
        
    ##Creating return dataframe 
    return_dataframe = pd.DataFrame(columns = [var_list])
    
    for i in range (0, 24):
        
        ##Loading Limits 
        limits_loc = 'C:\\Optimization_zlc\\control_center\\paper_qe_testcase\\optimization_results\\opti_' + dt + '\\limits' + str(i) + '.csv'
        limits_data = pd.read_csv(limits_loc)
        
        temp_data = []
        for j in range (0, dim_solved_varlist[0]):
            
            if limits_data['lower_limit'][j] != '-':
                difference = float(limits_data['upper_limit'][j]) - float(limits_data['lower_limit'][j])
                print(var_list[j])
                print(solved_data[var_list[j]][i])
                value = (solved_data[var_list[j]][i] * difference) +  float(limits_data['lower_limit'][j])
                temp_data.append(value)
            else:
                print(var_list[j])
                print(solved_data[var_list[j]][i])
                temp_data.append(solved_data[var_list[j]][i])
        
        temp_df = pd.DataFrame(data = [temp_data], columns = var_list)
        return_dataframe = return_dataframe.append(temp_df, ignore_index = True)
        
    ##Saving the return dataframe 
    save_file_loc = 'C:\\Optimization_zlc\\control_center\\paper_qe_testcase\\optimization_results\\opti_' + dt + '\\final_processed_values.csv'
    return_dataframe.to_csv(save_file_loc)
    return

############################################################################################################################################################

if __name__ == '__main__':
    dt = 'low'
    determine_real_values (dt)