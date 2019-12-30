##This is the evaluate objective function for the slave formulation 

def ga_scsd_run_ea_nb (variables, iteration):
    
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__))[:-62] + '\\'
    import sys 

    sys.path.append(current_path + 'master_level\\auxillary\\')
    sys.path.append(current_path + 'master_level_models\\manu_revision_chiller_only_with_dist_nwk_master\\')
    sys.path.append(current_path + 'slave_level_models\\manu_revision_chiller_only_with_dist_nwk_slave\\')    
    from models.cvx_prog_run import cvx_prog_run
    from input_data_process import extract_demand
    from input_data_process import extract_weather_and_ct_coefficients
    from convert_mdv_to_slave_param import convert_mdv_to_slave_param_v2
    import pandas as pd 
    
    ##dt            --- demand type 
    ##ah            --- hour of the day 
    ##t_evap_ret    --- evaporator return temperature (K)
    ##t_e_flow      --- total evaporator flowrate (m3/h)
    ##ps            --- the number of piecewise linear steps 
    ##bp            --- the number of bilinear pieces
     
    ##Importing the current time_step 
    import_directory = current_path + 'control_center\\manu_revision_chiller_only_with_dist_nwk_slave\\temp_working_dir\\'
    current_time_file_directory = import_directory + 'curr_ts.csv'
    curr_ts_df = pd.read_csv(current_time_file_directory)
    
    ##Preprocess modules 
        ##Here we process the look up tables 
    dt = 'high'
    ah = curr_ts_df['Current_time_step'][0]
    t_evap_ret = variables[0] 
    t_e_flow = variables[1]
    ps = 4 
    bp = 12
    
    
    ##Location for the demand data 
    demand_type = dt
    allocated_hour = ah
    demand_file_loc = current_path + 'input_data\\manu_revision_chiller_only_with_dist_nwk_input_data\\' + demand_type + '_load\\' + demand_type + '_demand_' + str(allocated_hour) + '.csv'
    
    #Location of weather conditions and the cooling tower coefficients 
    weather_and_ct_coeff_loc = current_path + 'master_level_models\\manu_revision_chiller_only_with_dist_nwk_master\\look_up_tables\\'
    weather_and_ct_coeff = extract_weather_and_ct_coefficients (weather_and_ct_coeff_loc, demand_type, allocated_hour) 
    
    ##Importing them into dataFrames 
    demand = extract_demand(demand_file_loc)
    weather_and_ct_coeff = extract_weather_and_ct_coefficients (weather_and_ct_coeff_loc, demand_type, allocated_hour)
      
    ##Just for this case, the variable values are listed in terms of stepsize, to simulate the action of the master optimizer 
    v0 = t_evap_ret                    ##Chiller evap return temperature  
    v1 = t_e_flow                      ##Total_evaporator_flowrate     

    v2 = weather_and_ct_coeff['T_WB'][0] + 273.15 + 5                  ##Chiller condenser entry temperature, since the cooling tower models were not included, this is fixed    
    
    v3 = 3                      ##Always 3, means network 4
    var = [v0, v1, v2, v3]
    
    ##Solver 
    ##glpk or gurobi
    solver_choice = 'gurobi'
        
    ##Solving the linear program for each time-step
    ##No model name ends with a number
    
    parallel_thread_num = iteration
    piecewise_steps = ps
    bilinear_pieces = bp
    
    ##Invoke a function to print the convert the parameters and the master decision variables for the input parameters for the slave            
    convert_mdv_to_slave_param_v2 (parallel_thread_num, var, demand, weather_and_ct_coeff, piecewise_steps)
    obj_value, results, results_y = cvx_prog_run(parallel_thread_num, bilinear_pieces, solver_choice)
    
    difference = 0
    final_obj_value = 0
    if obj_value != 'na':
        calculated_return_temperature = additional_check_function (var, demand, results)
        difference = abs(var[0] - calculated_return_temperature) 
        final_obj_value = obj_value + (difference * 10000)
    else:
        final_obj_value = 100000
    
    
    return final_obj_value

######################################################################################################################################################################################################
##This function checks the calculated return temperature of the setup 
def additional_check_function (var_input_cts, demand, results):
    ##Implementing a check function
        
    ##Calculating the constant value for the exting stream of the combined substation
    if var_input_cts[1] == 0:
        gv2_exit_est_value = 0
        hsb_exit_est_value = 0
        pfa_exit_est_value = 0
        ser_exit_est_value = 0
    else:
        flow = var_input_cts[1] * 998.2 / 3600
        gv2_exit_est_value = demand['ss_gv2_demand'][0] / (flow * 4.2)
        hsb_exit_est_value = demand['ss_hsb_demand'][0] / (flow * 4.2)
        pfa_exit_est_value = demand['ss_pfa_demand'][0] / (flow * 4.2)
        ser_exit_est_value = demand['ss_ser_demand'][0] / (flow * 4.2)
    
    dim_results = results.shape
    check = 10
    for i in range (0, dim_results[0]):
        if results['Name'][i] == 'gv2_ss_m_perc':
            gv2_ss_4nc_m_perc = results['Values'][i]
            check = check - 1
        elif results['Name'][i] == 'gv2_ss_t_in':
            gv2_ss_4nc_t_in = results['Values'][i]
            check = check - 1 
            
        elif results['Name'][i] == 'hsb_ss_m_perc':
            hsb_ss_4nc_m_perc = results['Values'][i]
            check = check - 1 
        elif results['Name'][i] == 'hsb_ss_t_in':
            hsb_ss_4nc_t_in = results['Values'][i]
            check = check - 1             
            
        elif results['Name'][i] == 'pfa_ss_m_perc':
            pfa_ss_4nc_m_perc = results['Values'][i]
            check = check - 1 
        elif results['Name'][i] == 'pfa_ss_t_in':
            pfa_ss_4nc_t_in = results['Values'][i]
            check = check - 1             
            
        elif results['Name'][i] == 'ser_ss_m_perc':
            ser_ss_4nc_m_perc = results['Values'][i]
            check = check - 1 
        elif results['Name'][i] == 'ser_ss_t_in':
            ser_ss_4nc_t_in = results['Values'][i]
            check = check - 1             
            
        elif results['Name'][i] == 'cp_nwk_m_perc':
            cp_nwk_4nc_m_perc = results['Values'][i]
            check = check - 1 
        elif results['Name'][i] == 'cp_nwk_tinout':
            cp_nwk_4nc_tinout = results['Values'][i]
            check = check - 1       

        if check == 0:
            break
        
    ##Calculating outlet temperature for the substations
    ss_tinmax = 273.15 + 5
    
    tout_gv2_ss = (274.15 * gv2_ss_4nc_m_perc) + ((ss_tinmax - 273.15 - 1) * gv2_ss_4nc_m_perc * gv2_ss_4nc_t_in) + gv2_exit_est_value
    tout_hsb_ss = (274.15 * hsb_ss_4nc_m_perc) + ((ss_tinmax - 273.15 - 1) * hsb_ss_4nc_m_perc * hsb_ss_4nc_t_in) + hsb_exit_est_value    
    tout_pfa_ss = (274.15 * pfa_ss_4nc_m_perc) + ((ss_tinmax - 273.15 - 1) * pfa_ss_4nc_m_perc * pfa_ss_4nc_t_in) + pfa_exit_est_value     
    tout_ser_ss = (274.15 * ser_ss_4nc_m_perc) + ((ss_tinmax - 273.15 - 1) * ser_ss_4nc_m_perc * ser_ss_4nc_t_in) + ser_exit_est_value     
    
    ##Calculating outlet temperature for the common pipe 
    tout_cp = (273.15 * cp_nwk_4nc_m_perc) + (30 * cp_nwk_4nc_m_perc * cp_nwk_4nc_tinout)
    
    calculated_return_temperature = tout_gv2_ss + tout_hsb_ss + tout_pfa_ss + tout_ser_ss + tout_cp

    return calculated_return_temperature