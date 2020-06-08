##This function runs the MILP solver based on th predefined models 
def milp_run_script ():
    
    import os 
    current_path = os.path.dirname(__file__) + '//'
    current_path_basic = os.path.dirname(__file__)[:-5] + '//' 
    import sys 
    sys.path.append(current_path + 'linearlized_models_coefficients//')                         ##Certain models need coefficients when linearized 
    sys.path.append(current_path + 'milp_models//')                                             ##Location of the milp models
    import pandas as pd 
    from mrs_ancillaries import mrs_import_relevant_files
    from mrs_ancillaries import mrs_write_slave_param
    from mrs_ancillaries import mrs_check_temperature_diff
    from milp_prog_run import milp_prog_run
    
    ##Hyperparameters 
    pwl_steps = 4                                                                               ##The number of piecewise linear steps used for the model  
    bl_steps = 10                                                                               ##The number of steps used for linearizing bilinear variables in the model 
    parallel_thread_num = 1010                                                                  ##The unique identifier used for the GA to locate the outputs of the MILP
    solver = 'glpk'                                                                             ##CPLEX and Gurobi used to be available, but now only GLPK is used as it 
                                                                                                ##is free, i.e. open sourced.
    obj_func_penalty = 10000                                                                    ##The default value of the objective function if infeasibility occurs. 
    
    ##Sepcific directories 
    cooling_load_data_loc = current_path_basic + 'input_data//milp_sample//cooling_demand.csv'  ##Location of the cooling load data 
    weather_condition_loc = current_path_basic + 'input_data//milp_sample//weather.csv'         ##Location of the weather data
        ##Parameters
    ga_inputs_loc = current_path + 'ga_inputs\\ga_inputs.csv'                                   ##Location of the GA inputs (Sample)
    
    ##Importing the relevant files 
    cooling_load_data, weather_condition, ga_inputs = mrs_import_relevant_files(cooling_load_data_loc, weather_condition_loc, ga_inputs_loc)
    ##Preparing the parameters for the model 
    mrs_write_slave_param (cooling_load_data, weather_condition, ga_inputs, pwl_steps, parallel_thread_num)
    ##Solving the preparing and solving the MILP problem 
    obj_value, results, results_y, all_dataframes  = milp_prog_run(parallel_thread_num, bl_steps, solver)
    
    ##Augmenting the objective function 
    if obj_value != 'na':
        ##Calculating the difference in the return temperatures
        milp_ret_temp, diff = mrs_check_temperature_diff (obj_value, results, cooling_load_data, ga_inputs, all_dataframes)
        if diff != 'na':
            ret_obj_func = obj_value + (obj_func_penalty * diff)
        else:
            ret_obj_func = obj_func_penalty 
    else:
        ret_obj_func = obj_func_penalty
    
    ##Placing the objective function value into a dataframe 
    obj_func_df = pd.DataFrame(data = [[ret_obj_func]], columns = ['obj_func_value'])
    ##Saving the MILP results 
    results.to_csv(current_path + 'milp_results\\results_continuous' + str(parallel_thread_num) + '.csv')
    results_y.to_csv(current_path + 'milp_results\\results_binary' + str(parallel_thread_num) + '.csv')
    obj_func_df.to_csv(current_path + 'milp_results\\results_obj_value' + str(parallel_thread_num) + '.csv')
        
    return ret_obj_func 

####################################################################################################################################################################
####################################################################################################################################################################
#Running the script 
if __name__ == '__main__':
    obj_func = milp_run_script()
    print(obj_func)