##This is a temporary interface for converting the master decision variables into inputs for the slave optimization 

def slave_test_script_nc4(dt, ps, bp, ah):
    
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level\\auxillary')
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\conference_network_only_master_level_models\\')
    sys.path.append('C:\\Optimization_zlc\\slave_level_models\conference_network_only_slave_convex\\models\\')
    from nwk_choice4.cvx_prog_run_4nc import cvx_prog_run_4nc
    from input_data_process import extract_demand
    from input_data_process import extract_weather_and_ct_coefficients
    from convert_mdv_to_slave_param import convert_mdv_to_slave_param_v2
    import pandas as pd
    
    ##Preprocess modules 
        ##Here we process the look up tables 
    
    ##Setting the evaporator outlet temperature to the network 
    tevap_out = 273.15 + 5
    
    ##Extracting the total evaporator flowrate for the network
    evap_flow_loc = 'C:\\Optimization_zlc\\control_center\\conference_network_only\\seeding_values_hl.csv'
    evap_flow_df = pd.read_csv(evap_flow_loc)
        ##Extracting the relevant flowrate based on time 
    evap_flow_curr = evap_flow_df['evap_flow'][ah]
    
    ##Location for the demand data 
    demand_type = dt
    allocated_hour = ah
    demand_file_loc = 'C:\\Optimization_zlc\\input_data\\conference_network_only_input_data\\' + demand_type + '_load\\' + demand_type + '_demand_' + str(allocated_hour) + '.csv'
    
    ##Importing them into dataFrames 
    demand = extract_demand(demand_file_loc)
      
    ##Just for this case, the variable values are listed in terms of stepsize, to simulate the action of the master optimizer 
    v0 = tevap_out                   ##Chiller evap return temperature  
    v1 = evap_flow_curr                      ##Total_evaporator_flowrate 

    #Network choice 
    v2 = 3    

    var = [v0, v1, v2]
    
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
    convert_mdv_to_slave_param_v2 (parallel_thread_num, var, demand, piecewise_steps)
    obj_value, results, results_y = cvx_prog_run_4nc(parallel_thread_num, bilinear_pieces, solver_choice)
    
    print(obj_value)
    print(results)
    print(results_y)

    
    return obj_value

#########################################################################################################################################################################

#########################################################################################################################################################################
##Running the test script for base_case  
if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    from datetime import datetime
    startTime = datetime.now()
    
    
    ps = 4
    bp = 20
    dt = 'high'    
    ##llocated hour
    ah = 23
    print('allocated hour =', ah)

    obj_value = slave_test_script_nc4(dt, ps, bp, ah)


    print(datetime.now() - startTime)    
    
