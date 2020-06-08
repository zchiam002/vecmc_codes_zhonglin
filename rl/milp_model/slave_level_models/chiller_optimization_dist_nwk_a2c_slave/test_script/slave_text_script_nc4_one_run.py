##This is a temporary interface for converting the master decision variables into inputs for the slave optimization 

def slave_test_script_nc4 ():
    
    import os
    current_directory = os.path.dirname(__file__)[:-71] + '//'  
    from datetime import datetime
    startTime = datetime.now()
    import sys     
    sys.path.append(current_directory + 'master_level\\auxillary\\')
    sys.path.append(current_directory + 'master_level_models\\chiller_optimization_dist_nwk_a2c_master_level_models\\')
    sys.path.append(current_directory + 'slave_level_models\\chiller_optimization_dist_nwk_a2c_slave\\models\\')    
    from nwk_choice4.cvx_prog_run_4nc import cvx_prog_run_4nc
    from input_data_process import extract_demand
    from convert_mdv_to_slave_param import convert_mdv_to_slave_param_v2
    from prepare_dist_nwk_lin_coeff import prepare_dist_nwk_lin_coeff
    from prepare_evap_cond_pump_lin_coeff import prepare_evap_cond_pump_lin_coeff
    import pandas as pd
    
    ##Preprocess modules 
        ##Here we process the look up tables 
#    prepare_dist_nwk_lin_coeff()
#    prepare_dist_nwk_lin_coeff()
    
    ##Location for the demand data 
    demand_type = 'high'
    allocated_hour = 0
    demand_file_loc = current_directory + 'input_data\\chiller_optimization_dist_nwk_a2c_input_data\\' + demand_type + '_load\\' + demand_type + '_demand_' + str(allocated_hour) + '.csv'
    
    #Location of weather conditions and the cooling tower coefficients 
    weather_data_dir = current_directory + 'input_data\\chiller_optimization_dist_nwk_a2c_input_data\\' + demand_type + '_load\\' + demand_type + '_demand_weather.csv'

    ##Importing them into DataFrames and making sure that there is no 0 value else it will violate the temperature constraint 
    demand_raw = extract_demand(demand_file_loc)
    headers = list(demand_raw)    
    dim_demand_raw = demand_raw.shape

    demand = pd.DataFrame(columns = headers[1:5])

    for i in range (0, dim_demand_raw[0]):
        curr_demand = []
        for j in range (1, len(headers) - 1):
            if demand_raw[headers[j]][i] < 0.001:
                curr_demand.append(0.01)
            else:
                curr_demand.append(demand_raw[headers[j]][i])
        temp_df = pd.DataFrame(data = [curr_demand], columns = headers[1:5])
        demand = demand.append(temp_df, ignore_index = True)
           
        
    weather_data = pd.read_csv(weather_data_dir)
      
    ##Selecting the master decision variables 
        ##Evaporator return temperature (K) 
    t_evap_ret = 288  
        ##Evaporator flowrate (m3/h)
    t_e_flow = 590
    
    ##Just for this case, the variable values are listed in terms of stepsize, to simulate the action of the master optimizer 
    v0 = t_evap_ret                                                         ##Chiller evap return temperature  
    v1 = t_e_flow                                                           ##Total_evaporator_flowrate     
    v2 = weather_data['T_WB'][allocated_hour] + 273.15 + 5                  ##Chiller condenser entry temperature, since the cooling tower models were not included, this is fixed                   

    var = [v0, v1, v2]
    
    ##Solver 
    ##glpk or gurobi
    solver_choice = 'gurobi'
    
    ##Solving the linear program for each time-step
    ##No model name ends with a number

    parallel_thread_num = 100137
    piecewise_steps = 1
    bilinear_pieces = 2
    
    demand_arr = [demand['ss_gv2_demand'][0], demand['ss_hsb_demand'][0], demand['ss_pfa_demand'][0], demand['ss_ser_demand'][0]]
    for i in range (0, len(demand_arr)):
        if demand_arr[i] < 0.0001:
            demand_arr[i] = 0.01
    
    print(demand_arr)    
    
    ##Invoke a function to print the convert the parameters and the master decision variables for the input parameters for the slave            
    convert_mdv_to_slave_param_v2 (parallel_thread_num, var, demand, weather_data, piecewise_steps)
    obj_value, results, results_y = cvx_prog_run_4nc(parallel_thread_num, bilinear_pieces, solver_choice)
    
    difference = 0
    if obj_value != 'na':
        calculated_return_temperature = additional_check_function (var, demand, results)
        difference = abs(var[0] - calculated_return_temperature)
#    print(var)
    print(obj_value)
#    print(results)
#    print(results_y)
    print('penalty', difference)  
    print(datetime.now() - startTime)
    
    return obj_value, difference, results

##################################################################################################################################################################
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

#############################################################################################################################################################################
##Running the script 
if __name__ == '__main__':
    slave_test_script_nc4 ()

