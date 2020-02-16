##This is a temporary interface for converting the master decision variables into inputs for the slave optimization 

def slave_test_script():
    
    from datetime import datetime
    startTime = datetime.now()
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level\\auxillary')
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\2_chillers_3_demand_master_level_models\\')
    sys.path.append('C:\\Optimization_zlc\\slave_convex_handlers\\')
    sys.path.append('C:\\Optimization_zlc\\slave_level_models\\slave_convex_vtest4\\')
    from nwk_choice_4.cvx_prog_run_nwk_4 import cvx_prog_run_nwk_4
    from input_data_process import extract_temp
    from input_data_process import extract_demand
    from prepare_evap_cond_pump_lin_coeff import prepare_evap_cond_pump_lin_coeff
    from prepare_dist_nwk_lin_coeff import prepare_dist_nwk_lin_coeff
    from master_decision_variables import master_decision_variables
    from convert_mdv_to_slave_param import convert_mdv_to_slave_param_v2
    import pandas as pd
    
    ##Pre-run functions which will have to be run before any optimization can take place
    ##A look up table to map the corresponding distribution network and pump combination to one of the 41 choices
    prepare_dist_nwk_lin_coeff()
    ##A look up table for the linearized coefficients of the evaporator and pump system coefficients and the regression coefficients
    prepare_evap_cond_pump_lin_coeff()
    ##A look up table for all the linearized coefficients of all possible combinations of distribution network pump system coefficients 
    
    ##Location for the master decision variables
    mdv_file_loc = 'C:\\Optimization_zlc\\input_data\\2_chiller_3_demand_input_data\\master_decision_variables.csv'
    
    ##Location for the weather conditions data
    weather_file_loc = 'C:\\Optimization_zlc\\input_data\\2_chiller_3_demand_input_data\\weather_data_day_170816.csv'
    
    ##Location for the demand data 
    demand_file_loc = 'C:\\Optimization_zlc\\input_data\\2_chiller_3_demand_input_data\\la_marina_demand_day_170816.csv'
    
    ##Importing them into dataFrames 
    mdv = master_decision_variables(mdv_file_loc)
    weather = extract_temp(weather_file_loc)
    demand = extract_demand(demand_file_loc)
    dim_mdv = mdv.shape 
    dim_demand = demand.shape
    time_steps = dim_demand[0]
    
    ##Sorting the master decision variables into discrete options 
    ##Variable 0: chiller_evap_return_temp, steps = 30 
    ##Variable 1: chiller_cond_entry_temp, steps = 30 
    ##Variable 2: total_evap_nwk_flowrate, steps = 1000
    ##variable 3: total_cond_nwk_flowrate, steps = 1000
    ##Variable 4: dist_nwk_and_pump_option, steps = 41, currently only 34 to 40 are selectable 
    
    ##Just for this case, the variable values are listed in terms of stepsize, to simulate the action of the master optimizer 
    v0 = 2.76E+02
    v1 = 2.92E+02
    v2 = 1.66E+03
    v3 = 7.93E+02
    v4 = 39             ##Currently the choices are limited to 34-40 as the other scripts are not yet prepared 

    var = [v0, v1, v2, v3, v4]
    
    ##Solver 
    ##glpk or gurobi
    solver_choice = 'gurobi'
    
    
    ##Solving the linear program for each time-step
    ##No model name ends with a number
    
    time_steps_test = 1
    parallel_thread_num = 10013
    piecewise_steps = 4
    bilinear_pieces = 20
    for i in range (0, time_steps_test):
        temp_weather_data = [weather['T_DB'][i], weather['T_WB'][i]]
        temp_weather_rec = pd.DataFrame(data = [temp_weather_data], columns = ['T_DB', 'T_WB'])
        
        temp_demand_data = [demand['ss_gv2_demand'][i], demand['ss_hsb_demand'][i], demand['ss_pfa_demand'][i], demand['ss_ser_demand'][i], demand['ss_fir_demand'][i]]
        temp_demand_rec = pd.DataFrame(data = [temp_demand_data], columns = ['ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'ss_fir_demand'])
        
        var_input = []
        for j in range (0, dim_mdv[0]):
            var_input.append(var[j])
        print(temp_demand_rec)
        ##Invoke a function to print the convert the parameters and the master decision variables for the input parameters for the slave
        
        ##Determining the network choice
        if (var[4] >= 0) and (var[4] <= 11):         ##Network choice 1
            nwk_choice = 1
        elif (var[4] >= 12) and (var[4] <= 23):      ##Network choice 2
            nwk_choice = 2
        elif (var[4] >= 24) and (var[4] <= 33):      ##Network choice 3
            nwk_choice = 3
        else:                                        ##Network choice 4
            nwk_choice = 4     
            
        convert_mdv_to_slave_param_v2 (parallel_thread_num, var, temp_weather_rec, temp_demand_rec, nwk_choice,  piecewise_steps)
        
        ##From here onwards, activate the convex solver 
            ##The key issue here is that the different network choices links to different activation scripts
            ##Hence we need to check for the appropriate network choice
        
        ##Checking which script to run 
        if nwk_choice == 1:
            x = 1 #cvx_prog_run_nwk_1(parallel_thread_num)
        elif nwk_choice == 2:
            x = 1 #cvx_prog_run_nwk_2(parallel_thread_num)
        elif nwk_choice == 3:
            x = 1 #cvx_prog_run_nwk_3(parallel_thread_num)
        elif nwk_choice == 4:
            obj_value, results, results_y = cvx_prog_run_nwk_4(parallel_thread_num, bilinear_pieces, solver_choice)
        

        print(var)
        print(obj_value)
        print(results)
        print(results_y)
    
    
        print(datetime.now() - startTime)
    
    return 

##################################################################################################################################################################

#########################################################################################################################################################################
##Running the test script   
if __name__ == '__main__':
    slave_test_script()