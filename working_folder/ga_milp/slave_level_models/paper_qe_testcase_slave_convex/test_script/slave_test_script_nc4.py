##This is a temporary interface for converting the master decision variables into inputs for the slave optimization 

def slave_test_script_nc4(dt, ah, t_evap_ret, t_e_flow, cond_flow, ps, bp):
    
    from datetime import datetime
    startTime = datetime.now()
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level\\auxillary')
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\')
    sys.path.append('C:\\Optimization_zlc\\slave_level_models\paper_qe_testcase_slave_convex\\models\\')
    from nwk_choice4.cvx_prog_run_4nc import cvx_prog_run_4nc
    from input_data_process import extract_demand
    from input_data_process import extract_weather_and_ct_coefficients
    from convert_mdv_to_slave_param import convert_mdv_to_slave_param_v2
    import pandas as pd
    
    ##Preprocess modules 
        ##Here we process the look up tables 
    
    
    ##Location for the demand data 
    demand_type = dt
    allocated_hour = ah
    demand_file_loc = 'C:\\Optimization_zlc\\input_data\\paper_qe_testcase_input_data\\' + demand_type + '_load\\' + demand_type + '_demand_' + str(allocated_hour) + '.csv'
    
    #Location of weather conditions and the cooling tower coefficients 
    weather_and_ct_coeff_loc = 'C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\look_up_tables\\'
    weather_and_ct_coeff = extract_weather_and_ct_coefficients (weather_and_ct_coeff_loc, demand_type, allocated_hour) 
    
    ##Importing them into dataFrames 
    demand = extract_demand(demand_file_loc)
    weather_and_ct_coeff = extract_weather_and_ct_coefficients (weather_and_ct_coeff_loc, demand_type, allocated_hour)
      
    ##Just for this case, the variable values are listed in terms of stepsize, to simulate the action of the master optimizer 
    v0 = t_evap_ret                   ##Chiller evap return temperature  
    v1 = t_e_flow                      ##Total_evaporator_flowrate     
    v3 = cond_flow                         ##0-4 each decides the appropriate condenser flowrate 

    v2 = weather_and_ct_coeff['T_WB'][0] + 273.15 + 5                  ##Chiller condenser entry temperature, since the cooling tower models were not included, this is fixed

    
    v4 = 3                          ##This ranges from 0 to 3. it is fixed in this test case                        

    var = [v0, v1, v2, v3, v4]
    
    ##Solver 
    ##glpk or gurobi
    solver_choice = 'gurobi'
    
    
    ##Solving the linear program for each time-step
    ##No model name ends with a number
    
    parallel_thread_num = 100137
    piecewise_steps = ps
    bilinear_pieces = bp
    
    demand_arr = [demand['ss_gv2_demand'][0], demand['ss_hsb_demand'][0], demand['ss_pfa_demand'][0], demand['ss_ser_demand'][0]]
    print(demand_arr)
    
    ##Invoke a function to print the convert the parameters and the master decision variables for the input parameters for the slave            
    convert_mdv_to_slave_param_v2 (parallel_thread_num, var, demand, weather_and_ct_coeff, piecewise_steps)
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
    
    #results.to_csv('C:\\Optimization_zlc\\slave_level_models\\paper_qe_testcase_slave_convex\\results'+ str(allocated_hour) +'.csv')
    #results_y.to_csv('C:\\Optimization_zlc\\control_center\\3_chiller_1_demand_12ts_3_period\\ga_results_current_store\\high_load\slave_output\\slave_t23_y.csv')    
    #print(datetime.now() - startTime)
    
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

#########################################################################################################################################################################
##Running the test script for base_case  
if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    from datetime import datetime
    startTime = datetime.now()
    
    import_legend = pd.read_csv('C:\\Optimization_zlc\\slave_level_models\\paper_qe_testcase_slave_convex\\legend.csv')
    
    dim_import_legend = import_legend.shape
    
    columns_org = []
    for i in range(0, dim_import_legend[0]):
        columns_org.append(import_legend['Name'][i])
    
    return_df_base = pd.DataFrame(columns = columns_org)
    
    ps = 4
    bp = 20
    dt = 'high'    

#This is for extracting the optimal results from GA    
    for i in range (0, 24):
        
        ah = i
        
        data_loc = 'C:\\Optimization_zlc\\control_center\\paper_qe_testcase\\ga_results_current_store\\' + dt + '_load\\ts_' + str(i) + '\\'
        data_file_loc = data_loc + 'best_agent_movement.csv'       
        optimal_data_ts = np.genfromtxt(data_file_loc, delimiter=',')

        ##First run
        t_evap_ret1 = optimal_data_ts[30,0]
        t_e_flow = optimal_data_ts[30,1]
        cond_flow = optimal_data_ts[30,2]


        obj_value1, difference, results1 = slave_test_script_nc4(dt, ah, t_evap_ret1, t_e_flow, cond_flow, ps, bp)
        

        dim_results1 = results1.shape
        temp_data = []
        for j in range (0, dim_results1[0]):
            temp_data.append(results1['Values'][j])
        temp_data.append(obj_value1)    
        temp_df = pd.DataFrame(data = [temp_data], columns = columns_org)
        return_df_base = return_df_base.append(temp_df, ignore_index = True)
        

        temp_df.to_csv('C:\\Optimization_zlc\\slave_level_models\\paper_qe_testcase_slave_convex\\results_temp' + str(i)  + '.csv')                 
        print(i)
        
    return_df_base.to_csv('C:\\Optimization_zlc\\slave_level_models\\paper_qe_testcase_slave_convex\\results_optimal.csv')

    print(datetime.now() - startTime)    
    
