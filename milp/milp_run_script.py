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
    from milp_prog_run import milp_prog_run
    
    ##Parameters 
    pwl_steps = 1                                                                               ##The number of piecewise linear steps used for the model  
    bl_steps = 2                                                                                ##The number of steps used for linearizing bilinear variables in the model 
    parallel_thread_num = 1010                                                                  ##The unique identifier used for the GA to locate the outputs of the MILP
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
    obj_value, results, results_y  = milp_prog_run(parallel_thread_num, bl_steps, solver)
    
    print(obj_value)
    print(results)
    print(results_y)    
        
    ##Now we have to check the difference in temperature!

    return 

####################################################################################################################################################################
####################################################################################################################################################################
##Additional functions 
    
##This function checks the calculated return temperature of the setup 
def additional_check_function (var_input_cts, demand, results):
    ##Implementing a check function
        
    ##Calculating the constant value for the exting stream of the combined substation
    if var_input_cts[1] == 0:
        exit_cst_value = 0
    else:
        flow = var_input_cts[1] * 998.2 / 3600
        gv2_exit_est_value = demand['ss_gv2_demand'][0] / (flow * 4.2)
        hsb_exit_est_value = demand['ss_hsb_demand'][0] / (flow * 4.2)
    
    dim_results = results.shape
    check = 6
    for i in range (0, dim_results[0]):
        if results['Name'][i] == 'gv2_ss_4nc_m_perc':
            gv2_ss_4nc_m_perc = results['Values'][i]
            check = check - 1
        elif results['Name'][i] == 'gv2_ss_4nc_t_in':
            gv2_ss_4nc_t_in = results['Values'][i]
            check = check - 1 
            
        elif results['Name'][i] == 'hsb_ss_4nc_m_perc':
            hsb_ss_4nc_m_perc = results['Values'][i]
            check = check - 1 
        elif results['Name'][i] == 'hsb_ss_4nc_t_in':
            hsb_ss_4nc_t_in = results['Values'][i]
            check = check - 1             
            
        elif results['Name'][i] == 'cp_nwk_4nc_m_perc':
            cp_nwk_4nc_m_perc = results['Values'][i]
            check = check - 1 
        elif results['Name'][i] == 'cp_nwk_4nc_tinout':
            cp_nwk_4nc_tinout = results['Values'][i]
            check = check - 1       

        if check == 0:
            break
        
    ##Calculating outlet temperature for the substations
    ss_tinmax = 273.15 + 5
    
    tout_gv2_ss = (274.15 * gv2_ss_4nc_m_perc) + ((ss_tinmax - 273.15 - 1) * gv2_ss_4nc_m_perc * gv2_ss_4nc_t_in) + gv2_exit_est_value
    tout_hsb_ss = (274.15 * hsb_ss_4nc_m_perc) + ((ss_tinmax - 273.15 - 1) * hsb_ss_4nc_m_perc * hsb_ss_4nc_t_in) + hsb_exit_est_value      
    
    ##Calculating outlet temperature for the common pipe 
    tout_cp = (273.15 * cp_nwk_4nc_m_perc) + (30 * cp_nwk_4nc_m_perc * cp_nwk_4nc_tinout)
    
    calculated_return_temperature = tout_gv2_ss + tout_hsb_ss + tout_cp

    return calculated_return_temperature

####################################################################################################################################################################
####################################################################################################################################################################
#Running the script 
if __name__ == '__main__':
    milp_run_script()