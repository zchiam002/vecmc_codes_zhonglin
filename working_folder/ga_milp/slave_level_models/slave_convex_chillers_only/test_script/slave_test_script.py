##This is a temporary interface for converting the master decision variables into inputs for the slave optimization 

def slave_test_script():
    
    from datetime import datetime
    startTime = datetime.now()
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level\\auxillary')
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\3_chiller_1_demand_12ts_3_period_master_level_models\\')
    sys.path.append('C:\\Optimization_zlc\\slave_level_models\\slave_convex_chillers_only\\')
    from models.cvx_prog_run import cvx_prog_run
    from input_data_process import extract_temp
    from input_data_process import extract_demand
    from convert_mdv_to_slave_param import convert_mdv_to_slave_param_v2
    import pandas as pd
    
    ##Location for the demand data 
    demand_file_loc = 'C:\\Optimization_zlc\\input_data\\3_chiller_1_demand_12ts_3_period_input_data\\high_load\\high_demand_3.csv'
    
    ##Importing them into dataFrames 
    demand = extract_demand(demand_file_loc)
    dim_demand = demand.shape
    time_steps = dim_demand[0]
    
    ##Just for this case, the variable values are listed in terms of stepsize, to simulate the action of the master optimizer 
    v0 = 280.048709677419     ##Chiller evap return temperature  
    v1 = 186.823546512958     ##Total_evaporator_flowrate     
    v2 = 298.15       ##Chiller condenser entry temperature, since the cooling tower models were not included, this is fixed


    var = [v0, v1, v2]
    
    ##Solver 
    ##glpk or gurobi
    solver_choice = 'gurobi'
    
    
    ##Solving the linear program for each time-step
    ##No model name ends with a number
    
    time_steps_test = 1
    parallel_thread_num = 10013
    piecewise_steps = 1
    bilinear_pieces = 2
    for i in range (0, time_steps_test):
        
        temp_demand_data = [849.1, 0,0,0,0]        
        #temp_demand_data = [demand['ss_gv2_demand'][i], demand['ss_hsb_demand'][i], demand['ss_pfa_demand'][i], demand['ss_ser_demand'][i], demand['ss_fir_demand'][i]]
        temp_demand_rec = pd.DataFrame(data = [temp_demand_data], columns = ['ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'ss_fir_demand'])

        ##Invoke a function to print the convert the parameters and the master decision variables for the input parameters for the slave            
        convert_mdv_to_slave_param_v2 (parallel_thread_num, var, temp_demand_rec,  piecewise_steps)
        
        obj_value, results, results_y = cvx_prog_run(parallel_thread_num, bilinear_pieces, solver_choice)
        
        difference = 0
        if obj_value != 'na':
            calculated_return_temperature = additional_check_function (var, temp_demand_data, results)
            difference = abs(var[0] - calculated_return_temperature)
        print(var)
        print(obj_value)
        print(results)
        print(results_y)
        print('penalty', difference)
        
        #results.to_csv('C:\\Optimization_zlc\\control_center\\3_chiller_1_demand_12ts_3_period\\ga_results_current_store\\high_load\slave_output\\slave_t23.csv')
        #results_y.to_csv('C:\\Optimization_zlc\\control_center\\3_chiller_1_demand_12ts_3_period\\ga_results_current_store\\high_load\slave_output\\slave_t23_y.csv')    
        print(datetime.now() - startTime)
    
    return 

##################################################################################################################################################################
##This function checks the calculated return temperature of the setup 
def additional_check_function (var_input_cts, temp_demand_data, results):
    ##Implementing a check function
        
    ##Calculating the constant value for the exting stream of the combined substation
    if var_input_cts[1] == 0:
        exit_cst_value = 0
    else:
        flow = var_input_cts[1] * 998.2 / 3600
        demand_for_combined = sum(temp_demand_data)
        exit_cst_value = demand_for_combined / (flow * 4.2)
    
    dim_results = results.shape
    check = 4
    for i in range (0, dim_results[0]):
        if results['Name'][i] == 'cb_ss_m_perc':
            cb_ss_m_perc = results['Values'][i]
            check = check - 1
        elif results['Name'][i] == 'cb_ss_t_in':
            cb_ss_t_in = results['Values'][i]
            check = check - 1 
        elif results['Name'][i] == 'cp_nwk_m_perc':
            cp_nwk_m_perc = results['Values'][i]
            check = check - 1 
        elif results['Name'][i] == 'cp_nwk_tinout':
            cp_nwk_tinout = results['Values'][i]
            check = check - 1       
        if check == 0:
            break
        
    ##Calculating outlet temperature for the combined substation
    cb_ss_tinmax = 273.15 + 5
    tout_cb_ss = (274.15 * cb_ss_m_perc) + ((cb_ss_tinmax - 273.15 - 1) * cb_ss_m_perc * cb_ss_t_in) + exit_cst_value
    
    ##Calculating outlet temperature for the common pipe 
    tout_cp = (273.15 * cp_nwk_m_perc) + (30 * cp_nwk_m_perc * cp_nwk_tinout)
    
    calculated_return_temperature = tout_cb_ss + tout_cp

    return calculated_return_temperature
#########################################################################################################################################################################
##Running the test script   
if __name__ == '__main__':
    slave_test_script()