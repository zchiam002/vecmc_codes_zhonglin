##This is the custom environment for the a2c algorithm to interact with 
class a2c_env_custom ():
    
    ##The inbuilt functions 
    def __init__ (self):
        
        self.num_states = 5                             ##4 demand values + 1 weather value
        self.num_actions = 2                            ##Evap ret temp and total evap flow
        self.state_space_norm_low = -1                  ##normalized state space values
        self.state_space_norm_high = 1      
        self.action_space_norm_low = -1                 ##normalized action space values 
        self.action_space_norm_high = 1
        
        self.action_space_lb = [275.16, 450]            ##Evap ret temp and total_evap_flow
        self.action_space_ub = [279.00, 1000]
        
        self.model_output_lb = [0, 0]
        self.model_output_ub = [10000, 10000]
        self.model_output_norm_lb = [-1, -1]
        self.model_output_norm_ub = [1, 1]
        
        self.state_lb, self.state_ub = state_lb_ub ()   ##The upper and lower bounds of the 4 demand values + 1 weather value
        
        return 
    
    ##This function evaluates the reward 
    def evaluate_reward (self, state, action):
        
        ##state         --- the input state values in the form of an array 
        ##action        --- the input action values in the form of an array 

        ##Converting the state back to original values 
        actual_state = []
        for i in range (0, self.num_states):
            curr_value = (state[i] - self.state_space_norm_low) / (self.state_space_norm_high - self.state_space_norm_low)
            curr_value = (curr_value * (self.state_ub[i] - self.state_lb[i])) +  self.state_lb[i]
            actual_state.append(curr_value)
        
        ##Converting the action back to original values 
        actual_action = []
        for i in range (0, self.num_actions):
            curr_value = (action[i] - self.action_space_norm_low) / (self.action_space_norm_high - self.action_space_norm_low)
            curr_value = (curr_value * (self.action_space_ub[i] - self.action_space_lb[i])) +  self.action_space_lb[i]
            actual_action.append(curr_value)
            
        return_obj, temp_error = one_run_slave (actual_action, actual_state, iteration = 10089)
        
        ##Convert the return values to the normalized form 
        return_obj_norm = (return_obj - self.model_output_lb[0]) / (self.model_output_ub[0] - self.model_output_lb[0])
        return_obj_norm = (return_obj_norm * (self.model_output_norm_ub[0] - self.model_output_norm_lb[0])) + self.model_output_norm_lb[0]
        
        temp_error_norm = (temp_error - self.model_output_lb[1]) / (self.model_output_ub[1] - self.model_output_lb[1])
        temp_error_norm = (temp_error_norm * (self.model_output_norm_ub[1] - self.model_output_norm_lb[1])) + self.model_output_norm_lb[1]
        
        return return_obj_norm, temp_error_norm
    
    ##This function evaluates the reward and return the real values 
    def evaluate_reward_real (self, state, action):
        
        ##state         --- the input state values in the form of an array 
        ##action        --- the input action values in the form of an array 
        
        ##Getting the bounds of the states 
        vali_states, state_lb, state_ub = return_validation_states ()
        
        ##Converting the state back to original values 
        actual_state = []
        for i in range (0, self.num_states):
            curr_value = (state[i] - self.state_space_norm_low) / (self.state_space_norm_high - self.state_space_norm_low)
            curr_value = (curr_value * (state_ub[i] - state_lb[i])) +  state_lb[i]
            actual_state.append(curr_value)

        ##Converting the action back to original values 
        actual_action = []
        for i in range (0, self.num_actions):
            curr_value = (action[i] - self.action_space_norm_low) / (self.action_space_norm_high - self.action_space_norm_low)
            curr_value = (curr_value * (self.action_space_ub[i] - self.action_space_lb[i])) +  self.action_space_lb[i]
            actual_action.append(curr_value)
            
        final_obj_value = one_run_slave_ga_outputs (actual_action, actual_state, iteration = 1008900)        
        
        return final_obj_value, actual_action, actual_state

    ##This function prepares a the validation state input for the agent 
    def get_validation_states (self):
        
        import numpy as np 
        
        ##Getting the states from the validation data 
        vali_states, state_lb, state_ub = return_validation_states ()
        
        ##Getting the dimension of the validation data
        dim_vali_states = vali_states.shape
        
        ##An empty array for holding the normalized state values 
        norm_state = np.zeros((dim_vali_states[0], dim_vali_states[1]))
        
        for i in range (0, dim_vali_states[0]):
            for j in range (0, dim_vali_states[1]):
                norm_state[i,j] = (vali_states[i,j] - state_lb[j]) / (state_ub[j] - state_lb[j])
                norm_state[i,j] = norm_state[i,j] * (self.state_space_norm_high - self.state_space_norm_low)
                norm_state[i,j] = norm_state[i,j] + self.state_space_norm_low
        
        return norm_state
    
    ##This function gets a state from the environment within the specifice bounds 
    def get_state_sampled_from_data (self):
        
        import numpy as np
        
        ##Getting a selected state from the data range 
        selected_state, state_lb, state_ub = sample_state_from_data_trace ()
        
        ##Normalizing the selected state
        norm_state = []
        for i in range (0, len(selected_state)):
            curr_norm = (selected_state[i] - state_lb[i]) / (state_ub[i] - state_lb[i])
            curr_norm = curr_norm * (self.state_space_norm_high - self.state_space_norm_low)
            curr_norm = curr_norm + self.state_space_norm_low
            norm_state.append(curr_norm)
        
        norm_state = np.array([norm_state])
        
        return norm_state

    ##This function gets a random state from the environment 
    def get_random_state (self):
        
        import numpy as np
        
        random_state = []
        for i in range (0, self.num_states):
            random_state.append(np.random.uniform(self.state_space_norm_low, self.state_space_norm_high))

        random_state = np.array([random_state])
        return random_state 
    
    ##This function generates a random action from the environment 
    def take_random_action (self):
        
        import numpy as np 
        
        random_action = []
        for i in range (0, self.num_actions):
            random_action.append(np.random.uniform(self.action_space_norm_low, self.action_space_norm_high))    
        
        random_action = np.array([random_action])
        return random_action

################################################################################################################################################################################
################################################################################################################################################################################
##Auxillary functions

##This function runs the slave one time
def one_run_slave (action, state, iteration):
    
    ##action     --- an array of values for the master decision variables 
    ##state      --- an array of state values, i.e. weather, and 4 demand values 
    ##iteration  --- for marking the milp script
    
    import os
    current_directory = os.path.dirname(__file__) + '//'    
    import sys
    sys.path.append(current_directory + 'milp_model//auxillary//')
    sys.path.append(current_directory + 'milp_model//master_level_models//')
    sys.path.append(current_directory + 'milp_model//slave_level_models//')    
    from cvx_prog_run_4nc import cvx_prog_run_4nc
    from input_data_process import extract_demand
    from convert_mdv_to_slave_param import convert_mdv_to_slave_param_v2    
#    from prepare_dist_nwk_lin_coeff import prepare_dist_nwk_lin_coeff
#    from prepare_evap_cond_pump_lin_coeff import prepare_evap_cond_pump_lin_coeff
    import pandas as pd    
    
    ##Preprocess modules 
        ##Here we process the look up tables 
#    prepare_dist_nwk_lin_coeff()
#    prepare_dist_nwk_lin_coeff()
      
    ##Selecting the master decision variables 
        ##Evaporator return temperature (K) 
    t_evap_ret = action[0]  
        ##Evaporator flowrate (m3/h)
    t_e_flow = action[1]
    
    ##Just for this case, the variable values are listed in terms of stepsize, to simulate the action of the master optimizer 
    v0 = t_evap_ret                                                         ##Chiller evap return temperature  
    v1 = t_e_flow                                                           ##Total_evaporator_flowrate     
    v2 = state[4] + 273.15 + 5                  ##Chiller condenser entry temperature, since the cooling tower models were not included, this is fixed                   
    
    ##A check function if the condenser temperature drops too low
    cond_low_limit = 273.15 + 20
    if v2 < cond_low_limit:
        v2 = cond_low_limit
     
    var = [v0, v1, v2]
    
    ##Solver 
    ##glpk or gurobi
    solver_choice = 'glpk'
    
    ##Solving the linear program for each time-step
    ##No model name ends with a number

    parallel_thread_num = iteration
    piecewise_steps = 4
    bilinear_pieces = 12
    
    ##Putting the demand into a dataframe 
    demand = pd.DataFrame(data = [[state[0], state[1], state[2], state[3]]], columns = ['ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand'])
    weather_data = []
    
    ##Invoke a function to print the convert the parameters and the master decision variables for the input parameters for the slave         
    convert_mdv_to_slave_param_v2 (parallel_thread_num, var, demand, weather_data, piecewise_steps)
    obj_value, results, results_y = cvx_prog_run_4nc(parallel_thread_num, bilinear_pieces, solver_choice)
    
    difference = 0
    final_obj_value = 0
    if obj_value != 'na':
        calculated_return_temperature = additional_check_function (var, demand, results)
        difference = abs(var[0] - calculated_return_temperature) 
        final_obj_value = obj_value + (difference * 10000)
        
        return_obj = obj_value
        temp_error = difference * 500
        
    else:
        final_obj_value = 10000
    
        return_obj = 10000
        temp_error = 10000
    
    
    return return_obj, temp_error

##This function runs the slave one time but returns the outputs in the same way it communicates with the GA
def one_run_slave_ga_outputs (action, state, iteration):
    
    ##action     --- an array of values for the master decision variables 
    ##state      --- an array of state values, i.e. weather, and 4 demand values 
    ##iteration  --- for marking the milp script
    
    import os
    current_directory = os.path.dirname(__file__) + '//'    
    import sys 
    sys.path.append(current_directory + 'milp_model//auxillary//')
    sys.path.append(current_directory + 'master_level_models//')
    sys.path.append(current_directory + 'slave_level_models//')    
    from cvx_prog_run_4nc import cvx_prog_run_4nc
    from input_data_process import extract_demand
    from convert_mdv_to_slave_param import convert_mdv_to_slave_param_v2    
#    from prepare_dist_nwk_lin_coeff import prepare_dist_nwk_lin_coeff
#    from prepare_evap_cond_pump_lin_coeff import prepare_evap_cond_pump_lin_coeff
    import pandas as pd    
    
    ##Preprocess modules 
        ##Here we process the look up tables 
#    prepare_dist_nwk_lin_coeff()
#    prepare_dist_nwk_lin_coeff()
      
    ##Selecting the master decision variables 
        ##Evaporator return temperature (K) 
    t_evap_ret = action[0]  
        ##Evaporator flowrate (m3/h)
    t_e_flow = action[1]
    
    ##Just for this case, the variable values are listed in terms of stepsize, to simulate the action of the master optimizer 
    v0 = t_evap_ret                                                         ##Chiller evap return temperature  
    v1 = t_e_flow                                                           ##Total_evaporator_flowrate     
    v2 = state[4] + 273.15 + 5                  ##Chiller condenser entry temperature, since the cooling tower models were not included, this is fixed                   
    
    ##A check function if the condenser temperature drops too low
    cond_low_limit = 273.15 + 20
    if v2 < cond_low_limit:
        v2 = cond_low_limit
     
    var = [v0, v1, v2]
    
    ##Solver 
    ##glpk or gurobi
    solver_choice = 'glpk'
    
    ##Solving the linear program for each time-step
    ##No model name ends with a number

    parallel_thread_num = iteration
    piecewise_steps = 2
    bilinear_pieces = 4
    
    ##Putting the demand into a dataframe 
    demand = pd.DataFrame(data = [[state[0], state[1], state[2], state[3]]], columns = ['ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand'])
    weather_data = []
    
    ##Invoke a function to print the convert the parameters and the master decision variables for the input parameters for the slave         
    convert_mdv_to_slave_param_v2 (parallel_thread_num, var, demand, weather_data, piecewise_steps)
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

##This function determines the upper and lower bound of the all possible state values 
def state_lb_ub ():

    import os
    current_directory = os.path.dirname(__file__) + '//'
    import pandas as pd 
    
    ##Importing the load data 
    high_load_data = pd.read_csv(current_directory + 'input_data//high_load//high_demand.csv')
    mid_load_data = pd.read_csv(current_directory + 'input_data//mid_load//mid_demand.csv')
    low_load_data = pd.read_csv(current_directory + 'input_data//low_load//low_demand.csv')
    
    ##Importing the weather data 
    high_load_weather = pd.read_csv(current_directory + 'input_data//high_load//high_demand_weather.csv')
    mid_load_weather = pd.read_csv(current_directory + 'input_data//mid_load//mid_demand_weather.csv')
    low_load_weather = pd.read_csv(current_directory + 'input_data//low_load//low_demand_weather.csv') 
    
    all_load_data = pd.DataFrame(columns = ['ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'ss_fir_demand'])
    all_load_data = all_load_data.append(high_load_data, ignore_index = True)
    all_load_data = all_load_data.append(mid_load_data, ignore_index = True)  
    all_load_data = all_load_data.append(low_load_data, ignore_index = True)
    
    all_weather_data = pd.DataFrame(columns = ['T_DB', 'T_WB'])
    all_weather_data = all_weather_data.append(high_load_weather, ignore_index = True)
    all_weather_data = all_weather_data.append(mid_load_weather, ignore_index = True)
    all_weather_data = all_weather_data.append(low_load_weather, ignore_index = True)    
    
    ##Appending upper and lower bounds of the state data 
    state_lb = [min(all_load_data['ss_gv2_demand'][:]), min(all_load_data['ss_hsb_demand'][:]), min(all_load_data['ss_pfa_demand'][:]), 
                min(all_load_data['ss_ser_demand'][:]), min(all_weather_data['T_WB'][:])]
    
    state_ub = [max(all_load_data['ss_gv2_demand'][:]), max(all_load_data['ss_hsb_demand'][:]), max(all_load_data['ss_pfa_demand'][:]), 
                max(all_load_data['ss_ser_demand'][:]), max(all_weather_data['T_WB'][:])]   
    
    
    return state_lb, state_ub

##This function samples a state from the data trace 
def sample_state_from_data_trace ():
    
    import os
    current_directory = os.path.dirname(__file__) + '//'       
    import pandas as pd 
    import random
    
    ##Importing the load data 
    high_load_data = pd.read_csv(current_directory + 'input_data//high_load//high_demand.csv')
    high_load_weather = pd.read_csv(current_directory + 'input_data//high_load//high_demand_weather.csv')
    
    dim_high_load_data = high_load_data.shape 
    
    selected_state_index = random.randint(0, dim_high_load_data[0]-1)
    
    selected_state = [high_load_data['ss_gv2_demand'][selected_state_index], high_load_data['ss_hsb_demand'][selected_state_index], 
                      high_load_data['ss_pfa_demand'][selected_state_index], high_load_data['ss_ser_demand'][selected_state_index],
                      high_load_weather['T_WB'][selected_state_index]]

    ##Appending upper and lower bounds of the state data 
    state_lb = [min(high_load_data['ss_gv2_demand'][:]), min(high_load_data['ss_hsb_demand'][:]), min(high_load_data['ss_pfa_demand'][:]), 
                min(high_load_data['ss_ser_demand'][:]), min(high_load_weather['T_WB'][:])]
    
    state_ub = [max(high_load_data['ss_gv2_demand'][:]), max(high_load_data['ss_hsb_demand'][:]), max(high_load_data['ss_pfa_demand'][:]), 
                max(high_load_data['ss_ser_demand'][:]), max(high_load_weather['T_WB'][:])] 
    
    return selected_state, state_lb, state_ub

##This function returns the numpy array of states from the validation data trace 
def return_validation_states ():
    
    import os
    current_directory = os.path.dirname(__file__) + '//'       
    import pandas as pd    
    import numpy as np
    
    ##Importing the load data 
    high_load_data = pd.read_csv(current_directory + 'input_data//high_load//high_demand.csv')
    high_load_weather = pd.read_csv(current_directory + 'input_data//high_load//high_demand_weather.csv')    
    
    dim_high_load_data = high_load_data.shape 

    vali_states = np.zeros((dim_high_load_data[0], 5))

    for i in range (0, dim_high_load_data[0]):
        vali_states[i,0] = high_load_data['ss_gv2_demand'][i]
        vali_states[i,1] = high_load_data['ss_hsb_demand'][i]
        vali_states[i,2] = high_load_data['ss_pfa_demand'][i]
        vali_states[i,3] = high_load_data['ss_ser_demand'][i]
        vali_states[i,4] = high_load_weather['T_WB'][i]
        
    ##Appending upper and lower bounds of the state data 
    state_lb = [min(high_load_data['ss_gv2_demand'][:]), min(high_load_data['ss_hsb_demand'][:]), min(high_load_data['ss_pfa_demand'][:]), 
                min(high_load_data['ss_ser_demand'][:]), min(high_load_weather['T_WB'][:])]
    
    state_ub = [max(high_load_data['ss_gv2_demand'][:]), max(high_load_data['ss_hsb_demand'][:]), max(high_load_data['ss_pfa_demand'][:]), 
                max(high_load_data['ss_ser_demand'][:]), max(high_load_weather['T_WB'][:])] 
    
    return vali_states, state_lb, state_ub














