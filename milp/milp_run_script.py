##This function runs the MILP solver based on th predefined models 
def milp_run_script ():
    
    import os 
    current_path = os.path.dirname(__file__) + '//'
    current_path_basic = os.path.dirname(__file__)[:-5] + '//' 
    import sys 
    sys.path.append(current_path + 'linearlized_models_coefficients//')                         ##Certain models need coefficients when linearized 
    sys.path.append(current_path + 'milp_models//')                                             ##Location of the milp models
    from mrs_ancillaries import mrs_import_relevant_files
    from mrs_ancillaries import mrs_write_slave_param
    
    ##Parameters 
    pwl_steps = 4                                                                               ##The number of piecewise linear steps used for the model  
    bl_steps = 12                                                                               ##The number of steps used for linearizing bilinear variables in the model 
    parallel_thread_num = 1010                                                                 ##The unique identifier used for the GA to locate the outputs of the MILP
    solver = 'glpk'                                                                             ##CPLEX and Gurobi used to be available, but now only GLPK is used as it 
                                                                                                ##is free, i.e. open sourced.
    
    ##Sepcific directories 
    cooling_load_data_loc = current_path_basic + 'input_data//milp_sample//cooling_demand.csv'  ##Location of the cooling load data 
    weather_condition_loc = current_path_basic + 'input_data//milp_sample//weather.csv'         ##Location of the weather data 
    ga_inputs_loc = current_path + 'ga_inputs\\ga_inputs.csv'                                   ##Location of the GA inputs (Sample)
    
    ##Importing the relevant files 
    cooling_load_data, weather_condition, ga_inputs = mrs_import_relevant_files(cooling_load_data_loc, weather_condition_loc, ga_inputs_loc)
    ##Preparing the parameters for the model 
    mrs_write_slave_param (cooling_load_data, weather_condition, ga_inputs, pwl_steps, parallel_thread_num)
    ##Solving the preparing and solving the MILP problem 
        

    


    return 

####################################################################################################################################################################
####################################################################################################################################################################
#Running the script 
if __name__ == '__main__':
    milp_run_script()