##This is the evaluate objective function for the slave formulation 

def ga_scsd_run_ea (variables, iteration):
    
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level\\auxillary')
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\')
    sys.path.append('C:\\Optimization_zlc\\slave_level_models\paper_qe_testcase_slave_convex\\models\\')
    from nwk_choice4.cvx_prog_run_4nc import cvx_prog_run_4nc
    from input_data_process import extract_demand
    from input_data_process import extract_weather_and_ct_coefficients
    from convert_mdv_to_slave_param import convert_mdv_to_slave_param_v2
    import pandas as pd    
    
    ##Location for the demand data 
    demand_type = 'mid'
    allocated_hour = 10
    demand_file_loc = 'C:\\Optimization_zlc\\input_data\\paper_qe_testcase_input_data\\' + demand_type + '_load\\' + demand_type + '_demand_' + str(allocated_hour) + '.csv'
    
    #Location of weather conditions and the cooling tower coefficients 
    weather_and_ct_coeff_loc = 'C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\look_up_tables\\'
    
    ##Importing them into dataFrames 
    demand = extract_demand(demand_file_loc)
    weather_and_ct_coeff = extract_weather_and_ct_coefficients (weather_and_ct_coeff_loc, demand_type, allocated_hour)    
    
    ##Arranging the input variables 
    v0 = variables[0]                                                          ##Chiller evap return temperature  
    v1 = variables[1]                                                          ##Total_evaporator_flowrate     
    v2 = weather_and_ct_coeff['T_WB'][0] + 273.15 + 5                          ##Chiller condenser entry temperature, since the cooling tower models were not included, this is fixed
    v3 = variables[2]                                                          ##0-4 each decides the appropriate condenser flowrate 
    
    v4 = 3
    
    var = [v0, v1, v2, v3, v4]    
    
    ##Solver 
    ##glpk or gurobi
    solver_choice = 'gurobi'    
    
    ##Solving the linear program for each time-step
    ##No model name ends with a number
    
    parallel_thread_num = iteration
    piecewise_steps = 4
    bilinear_pieces = 20    
    
    ##Converting the master decision variables into parameters for the slave solver
    convert_mdv_to_slave_param_v2 (parallel_thread_num, var, demand, weather_and_ct_coeff, piecewise_steps)    
    obj_value, results, results_y = cvx_prog_run_4nc(parallel_thread_num, bilinear_pieces, solver_choice)    
    
    difference = 0
    final_obj_value = 0
    if obj_value != 'na':
        calculated_return_temperature = additional_check_function (var, demand, results)
        difference = abs(var[0] - calculated_return_temperature) 
        final_obj_value = obj_value + (difference * 10000)
    else:
        final_obj_value = 100000
    
    return final_obj_value

###########################################################################################################################################################################
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
        pfa_exit_est_value = demand['ss_pfa_demand'][0] / (flow * 4.2)
        ser_exit_est_value = demand['ss_ser_demand'][0] / (flow * 4.2)
    
    dim_results = results.shape
    check = 10
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
            
        elif results['Name'][i] == 'pfa_ss_4nc_m_perc':
            pfa_ss_4nc_m_perc = results['Values'][i]
            check = check - 1 
        elif results['Name'][i] == 'pfa_ss_4nc_t_in':
            pfa_ss_4nc_t_in = results['Values'][i]
            check = check - 1             
            
        elif results['Name'][i] == 'ser_ss_4nc_m_perc':
            ser_ss_4nc_m_perc = results['Values'][i]
            check = check - 1 
        elif results['Name'][i] == 'ser_ss_4nc_t_in':
            ser_ss_4nc_t_in = results['Values'][i]
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
    tout_pfa_ss = (274.15 * pfa_ss_4nc_m_perc) + ((ss_tinmax - 273.15 - 1) * pfa_ss_4nc_m_perc * pfa_ss_4nc_t_in) + pfa_exit_est_value     
    tout_ser_ss = (274.15 * ser_ss_4nc_m_perc) + ((ss_tinmax - 273.15 - 1) * ser_ss_4nc_m_perc * ser_ss_4nc_t_in) + ser_exit_est_value     
    
    ##Calculating outlet temperature for the common pipe 
    tout_cp = (273.15 * cp_nwk_4nc_m_perc) + (30 * cp_nwk_4nc_m_perc * cp_nwk_4nc_tinout)
    
    calculated_return_temperature = tout_gv2_ss + tout_hsb_ss + tout_pfa_ss + tout_ser_ss + tout_cp

    return calculated_return_temperature

